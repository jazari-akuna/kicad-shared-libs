---
name: kicad-parts
description: >-
  Create, download, and verify KiCad parts (symbols, footprints, 3D models)
  for the shared KSL libraries in the kicad-shared-libs repository. Use when
  creating KiCad parts, symbols, footprints, or 3D models; downloading parts
  from JLC/JLCPCB/LCSC/EasyEDA (LCSC part numbers like C1525); managing or
  fixing KSL libraries, KSL_ROOT paths, datasheet links, or 3D model offsets;
  auditing lib_id/Footprint references against the libraries that hold them;
  keeping NDA-restricted parts in the separate kicad-nda-libs repo addressed by
  KNL_ROOT; or when the user mentions kibrary-automator, kicad-shared-libs,
  kicad-nda-libs, KSL, or KNL.
---

# KiCad Parts (KSL Libraries)

Make new parts for the user's shared KiCad libraries and verify them. These
requirements are non-negotiable:

- When you need a new part, start by downloading it from the JLC API using
  the kibrary-automator project or its code.
- Then check everything, especially:
  - The datasheet. Every part links to a **local English PDF** in the repo,
    never a URL — run `${KNL_ROOT}/scripts/datasheets.py` rather than editing links by
    hand, and check the document is for the right part, not just the right
    language. See "Datasheets are local files" below.
  - If the 3D model has the correct offsets to sit on top of the footprint
    in X, Y, and Z.
  - If the footprint and symbol are correct. Be very careful with this and
    flag it with visuals if you make modifications.
- If the part is not available via the LCSC/JLC API or online, create it
  from the datasheet.
- Make a small report of what was done, with visuals, for each new part.

## Key paths

Two path variables address the two repositories, and **everything in this skill
is written in terms of them** — never a literal checkout path, because the
libraries are shared and no two machines agree on where they sit.

| Variable | Repository | Notes |
|----------|------------|-------|
| `${KSL_ROOT}` | `kicad-shared-libs` (this repo) | Public remote. Everything here may be published. |
| `${KNL_ROOT}` | `kicad-nda-libs` | Private, **no remote by design** — never push it. |

### Set up the roots (once per machine — canonical instructions)

Nothing resolves until both the installed KiCad and your shell know the two
roots. On a fresh machine, do all three of these before any other step in
this skill:

**1. Export them in your shell**, so the commands below can be pasted as-is
and `kicad-cli` picks them up from the environment:

```bash
export KSL_ROOT=<path to this checkout>
export KNL_ROOT=<path to the kicad-nda-libs checkout>
```

**2. Register them in the installed KiCad** as path-substitution variables,
so the GUI resolves `${KSL_ROOT}` in lib-table URIs, footprint `(model ...)`
paths and `Datasheet` links. Either route writes the same setting:

- GUI: **Preferences → Configure Paths**, add `KSL_ROOT` and `KNL_ROOT` with
  the absolute checkout paths.
- Headless/scripted: write them into `kicad_common.json` in the KiCad
  settings directory (`~/Library/Preferences/kicad/<ver>/kicad_common.json`
  on macOS — layout verified against the installed 10.0), under the JSON key
  `environment.vars`:

  ```json
  { "environment": { "vars": {
      "KSL_ROOT": "/abs/path/to/kicad-shared-libs",
      "KNL_ROOT": "/abs/path/to/kicad-nda-libs" } } }
  ```

  Edit it **only with KiCad closed**: KiCad rewrites the file on exit, so a
  variable added while it runs can vanish. `KNL_ROOT` was silently lost
  exactly this way; the symptom is NDA libraries failing to resolve while
  everything else works. Re-check the file whenever NDA parts go missing.

**3. Pass them to `kicad-cli` runs explicitly.** `kicad-cli` resolves the
variables from any of three sources — `-D` flags, the process environment,
or `kicad_common.json` (verified on v10.0.2: a render with only the prefs
set is byte-identical to the `-D` render, and a virgin-config render loses
the model). Scripted runs must NOT lean on the prefs, which are absent on a
fresh machine or CI and can be rewritten away as above — pass BOTH roots per
command, in the form that command needs:

- `pcb render`, `pcb export step`, and anything else that resolves 3D
  models or libraries and accepts the flag:
  `-D KSL_ROOT="$KSL_ROOT" -D KNL_ROOT="$KNL_ROOT"`.
- `sch export pdf`: put the roots in the **environment, not `-D`**. `-D`
  also substitutes the variable in the sheet's displayed text, rewriting
  every datasheet popup to an absolute machine-local path and planting a
  spurious diff in committed PDFs; the environment resolves the embedded
  `file://` link targets while the visible text keeps `${KSL_ROOT}`
  (measured on the carrier boards, all four combinations).
- `sch export netlist`: rejects `-D` outright ("Unknown argument") and needs
  nothing — symbols resolve from the schematic's embedded `lib_symbols`
  cache.

**Forgetting `-D KNL_ROOT` fails silently.** An unresolved model is a
warning, not an error, so a STEP or render export simply comes out missing
every part whose model lives in the restricted repo, while the command still
exits 0. Always confirm the expected bodies are present in the output rather
than trusting the exit code.

This section is the canonical reference for the variables;
`${KSL_ROOT}/skills/README.md` points here and adds the rest of the
fresh-clone setup (pre-push hook, git-lfs).

### Where things live

| What | Path |
|------|------|
| Datasheets (git-lfs) | `${KSL_ROOT}/datasheets/<MPN>.pdf`, `${KNL_ROOT}/datasheets/` for restricted ones |
| Datasheet pipeline | `${KNL_ROOT}/scripts/datasheets.py` |
| 3D model gate | `${KNL_ROOT}/scripts/check_models.py` |
| Publication gate | `${KNL_ROOT}/scripts/check_nda.py`, run by `${KNL_ROOT}/hooks/ksl-pre-push` |
| This skill's source of truth | `${KSL_ROOT}/skills/kicad-parts/` (see `${KSL_ROOT}/skills/README.md` for the symlink wiring) |
| kibrary-automator | `kibrary_automator.py` in its own checkout — a separate tool, not part of this repo |
| Its venv (has `JLC2KiCadLib`) | `~/Library/Application Support/kibrary-automator/venv/bin/` |
| kicad-cli | `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` (macOS default install) |
| KiCad python (has `pcbnew`) | `/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3` |

## Library conventions

Each library is a self-contained folder named `<Category>_KSL` (e.g.
`Audio_KSL`, `Connector_KSL`), registered in the repo-root `repository.json`:

```
Audio_KSL/
├── Audio_KSL.kicad_sym    # one file, all symbols of the library
├── Audio_KSL.pretty/      # footprints, one .kicad_mod per footprint
├── Audio_KSL.3dshapes/    # 3D models (.step), same basename as footprint
└── metadata.json          # KiCad PCM metadata (lists the three above)
```

- Symbols are named after the full MPN (`PCM5102APWR`) and carry properties:
  `Reference` (`U?` — always ends in `?`), `Value` (= MPN), `Footprint`,
  `Datasheet` (a path under `${KSL_ROOT}/datasheets/`, **not** a URL — see
  below), `Description`, `LCSC` (e.g. `C107671`), `ki_keywords` (contains the
  LCSC code).
- Symbol → footprint reference is `LibraryName:FootprintName`, e.g.
  `"Footprint" "Audio_KSL:TSSOP-20_L6.5-W4.4-P0.65-LS6.4-BL"`.
- Footprint → 3D model reference always uses the path variable of the repo that
  holds the library:
  `(model "${KSL_ROOT}/Audio_KSL/Audio_KSL.3dshapes/TSSOP-20_....step")`, or
  `${KNL_ROOT}` for the NDA libraries (see "restricted parts" below).
- Footprint names follow the JLC/EasyEDA package style:
  `TSSOP-20_L6.5-W4.4-P0.65-LS6.4-BL`, `TYPE-C-SMD_TYPE-C-31-D-05`.
- **Symbol pin numbers must match footprint pad names** for every pin that
  carries a net. KiCad parity, `check_pcb_sync`, and the Allegro exporter
  all key off pin number ↔ pad name; a mismatch drops the connection silently
  unless the exporter aborts. Two recurring cases:
  - SOM corner grounds: pad names are `GND1`–`GND4` per the vendor land
    pattern; do not number those pins by fictitious LGA grid coordinates.
  - Hirose U.FL: two shield lands, one electrical pin — symbol gets **one**
    GND pin (pad `2`), not a duplicate pin 3.
  Stacked-pad duplicates like `14`/`14_1` on a mux are a separate class;
  document them rather than pretending parity is clean.
- Keep the library root clean: loose `.kicad_sym`/`.pretty`/`.3dshapes`
  entries at the repo root are treated as aborted-download leftovers by
  kibrary-automator. Quarantine such leftovers into `${KSL_ROOT}/_attic/`
  (never delete) after confirming the part was properly merged into a
  library. `${KSL_ROOT}/.kibrary/` is the tool's own workspace — leave it.
- **Every datasheet is a local file.** PUBLIC ones live in
  `${KSL_ROOT}/datasheets/<MPN>.pdf`, NDA ones in `${KNL_ROOT}/datasheets/`.
  A `Datasheet` property holding a URL is now a defect, not a normal state —
  see "Datasheets are local files" below.

`kicad-cli` needs the roots passed explicitly — the flag/environment rules
per command are in "Set up the roots" above.

## Library hygiene and restricted parts

This repo has a **public remote**. The private `kicad-nda-libs` repo,
addressed by `${KNL_ROOT}`, has **no remote configured, by design** — do not
add one, and do not push it. Sort restricted material into one of two tiers,
because they are not the same problem:

**Tier 1 — the document is restricted, the part is not.** The maker sells the
component openly but will not publish its specification. Symbol, footprint and
3D model stay in the normal public `<Category>_KSL` library; only the PDF moves
to `${KNL_ROOT}/datasheets/`, the symbol's `Datasheet` property points there,
and the filename is added to this repo's `.gitignore` so the datasheet pipeline
cannot re-fetch it from the URL still recorded in `datasheets/.state.json`. This
is the common case, and the `reference` layer of `check_nda.py` exists precisely
because the file can be correctly absent while a stale link still claims it
lives under `${KSL_ROOT}`.

**Tier 2 — the part itself is restricted.** Pinout and land pattern come from a
document that may not be redistributed, so the symbol and footprint are derived
works. The whole library moves to `${KNL_ROOT}` and is registered in the
consuming board's project `sym-lib-table`/`fp-lib-table` via `${KNL_ROOT}`, so
the design records exactly which library it needs while the content stays out
of the public repo.

When you cannot tell which tier applies, treat the part as Tier 2 and ask.

> **Superseded pattern — do not reintroduce.** These libraries used to sit
> inside `kicad-shared-libs` as *gitignored* directories. That kept them off the
> public remote but left them untracked: no history, no backup, destroyed by a
> fresh clone or a stray `git clean -x`. If you find an NDA library gitignored
> in place, move it to `${KNL_ROOT}` rather than perpetuating this.

Library **nicknames do not encode the repo**. A reference such as
`<Lib>_KSL:<PartName>` stays spelled exactly that way when the library moves
between repos — the `_KSL` suffix is part of the nickname, not a claim about
which checkout holds it. Only the lib-table URIs and the `(model ...)` paths
change. When relocating a library, rewrite the URIs and
model paths and leave every nickname alone — a blanket find-and-replace on the
library name will corrupt symbol and footprint links across every sheet.

**Audit every `lib_id` against the library that actually contains it**, and
resolve through the PROJECT tables only: the machine-global table masks
portability gaps that break on anyone else's checkout. Moving a symbol
between libraries without updating the schematics that reference it is
invisible — the design keeps rendering, ERCing and exporting netlists
correctly, because the symbol is cached inline in each sheet's `lib_symbols`
block. The only symptoms are "not found" in the symbol editor and an "Update
Symbols from Library" that breaks the design. The same bug exists one level
down on footprints via the `Footprint` property, and is easier to miss and
costlier to fix, because the correction touches both the netlist and the PCB.

**A cached symbol is not the master.** Editing the copy in a sheet's
`lib_symbols` block changes the design but not the library, so a future
library update silently reverts it. Mirror every such edit into the
`<Lib>.kicad_sym` master (or edit the master and re-sync the sheet), and say
which one you did in the report.

## The three gates

The repo checks itself. Run all three before you claim a part is done; each
exits 0 clean, 1 on violations, 2 when it could not run at all.

```bash
${KNL_ROOT}/scripts/datasheets.py verify   # every non-generic symbol resolves to an English PDF on disk
${KNL_ROOT}/scripts/check_models.py        # every 3D model is placed where its footprint says
${KNL_ROOT}/scripts/check_nda.py --scope all
```

`check_models.py` grades **units**, **transform** and **seating** — the last by
slicing the STEP where KiCad places it and requiring every cross-section below
the board surface to fit inside a drilled hole. Seating needs FreeCAD and says
so rather than reporting a false green without it. Defects that predate the
checker are baselined in `${KNL_ROOT}/scripts/ksl_model_seating_backlog.txt` so a *new*
regression fails today; delete a line as you fix one, and never add one to
silence your own work.

`check_nda.py` is the gate that cannot be undone if it is skipped, because this
repo has a public remote. It looks three ways — **hash** (sha256 against
`${KNL_ROOT}/scripts/nda_denylist.json`, which also reads a git-lfs *pointer* without
needing the object, since the pointer states the digest), **content** (PDF text
against known-restricted vendors and part families) and **reference** (a
`Datasheet` property pointing a restricted document at `${KSL_ROOT}`).

- `--scope history` is the one that matters before a push: deleting a file in a
  new commit does not unpublish the blob.
- `--self-test` is a negative control. It plants material each layer must
  reject plus a clean control each must accept, and fails if any layer stays
  quiet — a check nobody has watched fail is not evidence.
- `--sync` refreshes the digests from the private repo.

`${KNL_ROOT}/hooks/ksl-pre-push` runs `check_nda.py --scope all` at the only moment that
counts. **Git does not carry hooks through a clone**, so install it by hand on
every checkout:

```bash
install -m 755 ${KNL_ROOT}/hooks/ksl-pre-push ${KSL_ROOT}/.git/hooks/pre-push
```

It deliberately **replaces** the stock git-lfs pre-push hook and calls
`git lfs pre-push` itself, because git allows only one. Keep that line or
datasheet LFS objects silently stop being uploaded and the remote ends up
holding pointers to blobs nobody can fetch. There is no environment-variable
override and `--no-verify` is not an answer: if the check is wrong, fix the
check or the denylist in a commit.

## Workflow for a new part

### Step 1 — Download from the JLC/LCSC API (always first)

Use kibrary-automator. Two ways, detailed in
[kibrary-automator.md](kibrary-automator.md):

- **Interactive tool** (preferred when the user is present):
  `python3 <kibrary-automator checkout>/kibrary_automator.py add C1525`
- **Its code directly** (preferred for unattended agent runs): call
  `JLC2KiCadLib` from the tool's venv into a temp dir, then merge into the
  target `*_KSL` library replicating what the tool does (rewrite footprint
  ref and `${KSL_ROOT}` model path, fill Description/Datasheet from the LCSC
  API, update `metadata.json`/`repository.json`, run the `install` command).

Find the LCSC part number first if you only have an MPN (search LCSC/JLCPCB).

Either route leaves the `Datasheet` property as a URL at best. That is not
the finished state — Step 2 turns it into a local PDF under
`${KSL_ROOT}/datasheets/` and a `${KSL_ROOT}` link, always.

### Step 2 — Check everything

**Datasheets are local files (must be an English PDF).**

After Step 1 the new symbol's `Datasheet` property holds whatever the LCSC
API returned — usually a bare URL, sometimes nothing. Both are defects to fix
now, not ship. For EVERY part you add, do this, in order:

1. **Download the datasheet PDF into `${KSL_ROOT}/datasheets/`**
   (`${KNL_ROOT}/datasheets/` if the document is restricted — Tier 1 above,
   decision criteria in item 7 below). `datasheets.py fetch` does this from
   the URL in the property; fetch manually only when there is no usable URL,
   and put the file in the same folder.
2. **Name the file after the MPN**: `<MPN>.pdf`, with every run of
   characters outside `A-Za-z0-9._+-` collapsed to a single `_` — the
   `slug()` rule in `datasheets.py`, e.g. `ESD5311N-2/TR` →
   `ESD5311N-2_TR.pdf`. The MPN is the symbol's `Value`. `fetch` names files
   this way itself; match it exactly when placing a file by hand, or
   `verify` will not find the document.
3. **Check it is English and the right document** (`datasheets.py triage`,
   then `queue`/`apply` for anything it cannot decide — judgement criteria
   are items 3–6 below).
4. **Set the symbol's `Datasheet` property to the literal string
   `${KSL_ROOT}/datasheets/<file>.pdf`** (`${KNL_ROOT}/...` for a restricted
   document) — the path-variable spelling, verbatim. Never an absolute
   machine-local path, never a bare URL, never a project-relative path.
   `datasheets.py relink` writes this form; prefer it over hand-editing.
5. **Run `${KNL_ROOT}/scripts/datasheets.py verify` and get exit 0** before
   calling the part done — it is one of the three gates.

Beyond the single-part flow, `datasheets.py` is the source of truth for the
whole pipeline — do not hand-roll any of it:

```
datasheets.py setup        # fresh clone: enable git-lfs, pull PDFs, check them
datasheets.py inventory    # every symbol and its datasheet state
datasheets.py fetch        # download into datasheets/<MPN>.pdf, reject non-PDFs
datasheets.py triage       # language + "is this even the right part" check
datasheets.py queue        # emit only what needs a judgement
datasheets.py apply --results verdicts.json
datasheets.py relink       # rewrite properties to ${KSL_ROOT}/datasheets/...
datasheets.py sync-project --project <board-repo>   # push into the schematics
datasheets.py harvest      --project <board-repo>   # parts no library defines
datasheets.py verify       # gate: every part resolves to an English PDF
```

Add `--repo knl` for the NDA repo. `--kiprjmod <dir>` resolves legacy
`${KIPRJMOD}` links. `--mode url` flips every link back to its upstream URL for
a checkout without the LFS objects; `--mode local` flips back, losslessly.

**`sync-project` is not optional, and this is the trap.** Relinking the
libraries does *not* make **D** open a local file. A `.kicad_sch` carries its
own copy of every symbol — in the `lib_symbols` cache and again on each placed
instance — and D reads those copies. Sync also matches on the part *value*,
because boards routinely place real components on stock generic symbols: a
whole set of buck inductors drawn as `Device:L_Small`, ESD diodes as
`Device:D_TVS`, each with the real MPN in the Value field. Keying only on
`lib_id` leaves exactly those parts opening a browser. Never let it walk into a
project's `.history/` or handoff-snapshot directories — those are point-in-time
copies and rewriting them falsifies the record.

Storage is **git-lfs** (`datasheets/*.pdf`), roughly 160 MB. The NDA repo stays
plain git: it is small, and `git lfs install` wants to overwrite the pre-push
hook that refuses publication, which must not happen.

1. **Why local, not a URL.** URLs rot: LCSC re-hashes CDN paths, TI retires
   `lit/ds/symlink` aliases, Hirose serves `document?clcode=` only to a
   browser UA. When the link dies, pressing **D** in Eeschema opens a 404 and
   the part's only authoritative document is gone. A file in the repo works
   offline and is versioned alongside the symbol.
2. **Link form is `${KSL_ROOT}/datasheets/<MPN>.pdf`** (`${KNL_ROOT}/...` for
   NDA). Not a bare relative path: KiCad resolves those against the *project*,
   and a shared library has no single project. The variable must be
   registered with the installed KiCad or the link opens nothing — see "Set
   up the roots" above, including the trap where KiCad rewrites
   `kicad_common.json` on exit and silently drops a hand-added variable.
3. **Language.** The script's heuristic decides `en` only when confident and
   sends everything else to the queue. Thresholds that took real tuning:
   ≥30% CJK is Chinese; <1% CJK is English with an incidental note (a 46-page
   English datasheet in this repo carries exactly two Chinese sentences, in the
   stencil note); a CJK vocabulary under ~25 distinct glyphs is a company name in a page
   footer, however many pages it appears on. Between those, a human or agent
   looks. **Ratio alone is not enough** — TI's *Chinese* edition of a part
   (`ti.com.cn`, doc `ZHCS...`) sits near 10% CJK because part numbers, units
   and tables stay Latin. Check the document ID and domain, not just the mix.
4. **Bilingual is acceptable** when a competent English-only engineer can use
   the document: dimensions, pin assignments and ratings all legible in
   English. Many LCSC connector/switch drawings are like this. Chinese
   *alongside* complete English is fine; Chinese-only substance is not.
5. **Check it is the right document, not just the right language.** The
   script flags PDFs whose MPN never appears in the text, and that catches
   real defects that language checks never would: `2N7002` linked to a generic
   *SOT23 package drawing* with no electrical specs, and `YZ90415045R-01`
   linked to a different maker's part entirely. Expect false positives on
   family datasheets (`PZ254V-11-XX` covering the `-04P`), which is why a
   human confirms rather than the script auto-replacing.
6. **No English edition anywhere?** Translate as a last resort, and keep the
   original: append the source pages after the translation so the dimensioned
   drawings survive and can be cross-checked, and mark the file plainly as an
   unofficial machine translation with its source and date.
7. **Restricted documents never enter KSL** — it may be published. They go in
   `${KNL_ROOT}/datasheets/`, and the filename goes in this repo's
   `.gitignore`. Test before deciding: render the first pages and grep for
   *Confidential* / *Proprietary* / *NDA*. Two traps, both seen here:
   - A **stamp is sufficient but not necessary**. At least one restricted
     document in the set carries no marking at all, only a legal notice in the
     front matter forbidding reproduction and disclosure. Read the notice, do
     not just grep for the word.
   - **Absence of a stamp does not make it public** — but publication does. If
     the maker serves the PDF from its own public website with no login, it is
     public whatever it looks like. Check the source, not the styling.

   When genuinely unsure, treat it as restricted. Adding a document to the
   private repo is reversible; a push is not.
8. **Coverage: every part with a public datasheet must have one** —
   connectors, switches and passives included, not just ICs. The only exempt
   symbols are generic drafting ones with no maker at all (`R`, `C`,
   `TestPoint`, `Fiducial`, `MountingHole`); `verify` counts these separately
   so an empty field on a real part cannot hide among them.

**3D model offsets (X, Y, Z):**

1. Read the `(model ...)` block at the end of the `.kicad_mod`. Offsets are
   in mm and should be small (|value| ≲ a few mm). Huge values (hundreds of
   mm) are a known EasyEDA-conversion failure — the model renders hundreds
   of mm off-board. Example of a broken one in the wild:
   `(offset (xyz -911.47 683.72 0))`.
2. To compute the correct offset without guessing, get the STEP model's own
   bounding box: parse `CARTESIAN_POINT` coordinates from the `.step` file
   (open with `errors="ignore"` — STEP files may contain non-UTF-8 bytes).
   JLC/EasyEDA models are usually already centered at X=Y=0, so the fix is
   typically `(offset (xyz 0 0 0))` with the existing rotate kept.
3. Verify visually with a 3D render (see "Visuals" below): top view for X/Y
   centering over the pads, front/side views for Z seating (body must rest
   on the board, pins meeting the pads — not floating or sunken).
4. Fix by editing the offset/rotate values in the `(model ...)` block and
   re-rendering until it seats correctly.

**Footprint and symbol correctness (be very careful):**

- Compare pad numbering/geometry and the symbol pin list against the
  datasheet: pad count, pitch, pad sizes, pin-1 marker location, exposed
  pad, pin names/numbers/electrical types on the symbol.
- Render SVGs (below) and *look* at them; compare against the datasheet
  land pattern drawing.
- If you modify a footprint or symbol, render **before and after** images
  and flag the change prominently in the report.

### Step 3 — Part not available from LCSC/JLC or online

Create it from the datasheet:

- Footprint: write the `.kicad_mod` from the datasheet's recommended land
  pattern (use an existing KSL footprint as a format template; KiCad's
  standard libraries under `/Applications/KiCad/KiCad.app/Contents/SharedSupport/`
  may have a matching package to copy and adapt).
- Symbol: write the symbol into the target `<Lib>.kicad_sym` from the pin
  table, with all the standard properties listed above.
- 3D model: reuse a generic package STEP from another KSL library or KiCad's
  3dmodels when the package matches; otherwise ship without a model and say
  so in the report.
- Verify with the same Step 2 checks and renders.

### Step 4 — Report (always, one per part)

Write a short markdown report (in the chat, plus save renders under
`/tmp/kicad-part-reports/<LCSC-or-MPN>/`) containing:

```markdown
## <MPN> (<LCSC#>) → <Library>_KSL
- Source: JLC API via kibrary-automator | drawn from datasheet
- Datasheet: <final `Datasheet` property value — `${KSL_ROOT}/datasheets/<file>.pdf`, or `${KNL_ROOT}/...` if restricted> (English: yes/no→fixed)
- Checks: footprint ✓/✗, symbol ✓/✗, 3D offsets ✓/✗ (what was wrong, what was changed)
- Modifications: none | list each edit — with before/after images
![symbol](sym.png) ![footprint](fp.png) ![3D iso](render_iso.png) ![3D front](render_front.png)
```

Embed the images in your chat response with `![...](/absolute/path.png)`.

## Visuals: rendering commands (verified on this machine)

`CLI=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` (v10.0.2).
Always `mkdir -p` the output dir first — `fp export svg` fails otherwise.

**Footprint → SVG:**

```bash
"$CLI" fp export svg <Lib>.pretty --fp "<FootprintName>" \
  -o /tmp/out -l F.Cu,F.SilkS,F.Fab,F.Mask,F.CrtYd
```

**Symbol → SVG** (output is `<name>_unit1.svg`):

```bash
"$CLI" sym export svg <Lib>.kicad_sym -s "<SymbolName>" -o /tmp/out
```

SVGs can't be viewed directly — convert to PNG to inspect/embed:
`rsvg-convert -w 1000 in.svg -o out.png` (installed at /opt/homebrew/bin).

**3D render** — `kicad-cli` can't render a bare footprint, so first build a
one-footprint board with KiCad's bundled python (a wxApp assert warning on
stderr is harmless):

```bash
/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3 - <<'EOF'
import pcbnew
board = pcbnew.CreateEmptyBoard()
fp = pcbnew.FootprintLoad("/path/to/Lib.pretty", "FootprintName")
assert fp, "footprint not found"
board.Add(fp)
pcbnew.SaveBoard("/tmp/fp_test.kicad_pcb", board)
EOF
```

Then render top (X/Y check), front (Z check), and isometric views:

```bash
"$CLI" pcb render /tmp/fp_test.kicad_pcb -o /tmp/out/top.png \
  -D KSL_ROOT="$KSL_ROOT" -D KNL_ROOT="$KNL_ROOT" --side top --zoom 2
"$CLI" pcb render ... -o /tmp/out/front.png --side front --zoom 2
"$CLI" pcb render ... -o /tmp/out/iso.png --rotate '-45,0,45' --zoom 3
```

WARNING: the `.kicad_pcb` embeds its own copy of the footprint, including
the `(model ...)` block. After editing the `.kicad_mod`, you MUST re-run
the board-building python snippet above before re-rendering — otherwise
you render the stale offset and the fix appears to have no effect.

Read the PNGs to actually verify — if the model doesn't appear in the top
view, it is probably offset far away (render with `--zoom 0.05` to find it,
then fix the offset; a model hundreds of mm away can be outside even that
frame, so an empty wide view plus a huge offset value is confirmation
enough). Note: raw JLC downloads reference the model by a relative path
(`(model ./X.step`), which the one-footprint board won't resolve — do the
`${KSL_ROOT}` rewrite before rendering.

After editing a `.kicad_sym`, sanity-check it still parses:
`"$CLI" sym export svg <Lib>.kicad_sym -o /tmp/symcheck` (exit 0 = OK).

## Manual 3D checklist (when a render is inconclusive)

Open the board in KiCad's 3D viewer (`open /tmp/fp_test.kicad_pcb`, View →
3D Viewer) and confirm: body centered on the courtyard (X/Y), pins touching
the pads, body resting on the board surface (Z), correct rotation.

## Additional resources

- [kibrary-automator.md](kibrary-automator.md) — invocation details, prompt
  sequence, raw-output rewrites, LCSC API endpoints, install/registration.
