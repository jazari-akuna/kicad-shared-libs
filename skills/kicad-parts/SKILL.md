---
name: kicad-parts
description: >-
  Create, download, and verify KiCad parts (symbols, footprints, 3D models)
  for the shared KSL libraries in ~/Projects/kicad-shared-libs. Use when
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
    never a URL — run `scripts/datasheets.py` rather than editing links by
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

| What | Path |
|------|------|
| Library repo (`${KSL_ROOT}`) | `/Users/raph/Projects/kicad-shared-libs` |
| NDA library repo (`${KNL_ROOT}`) | `/Users/raph/Projects/kicad-nda-libs` (private, never push) |
| Datasheets (git-lfs) | `${KSL_ROOT}/datasheets/<MPN>.pdf`, `${KNL_ROOT}/datasheets/` for NDA |
| Datasheet pipeline | `${KSL_ROOT}/scripts/datasheets.py` |
| This skill's source of truth | `${KSL_ROOT}/skills/kicad-parts/` (`~/.cursor/skills/kicad-parts` symlinks here) |
| kibrary-automator | `/Users/raph/Projects/kibrary-automator/kibrary_automator.py` |
| Its venv (has `JLC2KiCadLib`) | `~/Library/Application Support/kibrary-automator/venv/bin/` |
| kicad-cli | `/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli` |
| KiCad python (has `pcbnew`) | `/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/Current/bin/python3` |
| KiCad settings | `~/Library/Preferences/kicad/<ver>/` (defines `KSL_ROOT` and `KNL_ROOT` in `kicad_common.json`) |

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
  `Datasheet` (direct PDF URL), `Description`, `LCSC` (e.g. `C107671`),
  `ki_keywords` (contains the LCSC code).
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

`kicad-cli` does not inherit these variables from the KiCad GUI prefs, so pass
BOTH to every command that resolves models or symbols and accepts the flag:

```
-D KSL_ROOT=/Users/raph/Projects/kicad-shared-libs \
-D KNL_ROOT=/Users/raph/Projects/kicad-nda-libs
```

Not all commands accept it: `sch export netlist` rejects `-D` outright
("Unknown argument"), and needs nothing — symbols resolve from the schematic's
embedded `lib_symbols` cache.

**Forgetting `-D KNL_ROOT` fails silently.** An unresolved model is a warning,
not an error, so a STEP or render export simply comes out missing the NDA parts
(on the carrier project: the SOM; on hdmi: the BRIDGE-A) while the command
still exits 0. Always confirm the expected bodies are present in the output
rather than trusting the exit code.

## Library hygiene and restricted parts

**Parts that must stay out of the published library set** (no public datasheet,
NDA'd design guide) get their own library in a **separate private repository**,
`~/Projects/kicad-nda-libs`, addressed by the `${KNL_ROOT}` path variable.
Currently `SOM_KSL` and `Video_Interface_NDA_KSL`. They are registered in the
consuming board's project `sym-lib-table`/`fp-lib-table` via `${KNL_ROOT}`, so
the design records exactly which library it needs while the content stays out
of the public repo.

That repo has **no remote configured, by design** — do not add one, and do not
push it.

> **Superseded pattern — do not reintroduce.** These libraries used to sit
> inside `kicad-shared-libs` as *gitignored* directories. That kept them off the
> public remote but left them untracked: no history, no backup, destroyed by a
> fresh clone or a stray `git clean -x`. If you find an NDA library gitignored
> in place, move it to `${KNL_ROOT}` rather than perpetuating this.

Library **nicknames do not encode the repo**. `SOM_KSL:MODULE-A-SOM` stayed
spelled exactly that way through the move; only the lib-table URIs and the
`(model ...)` paths changed. When relocating a library, rewrite the URIs and
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

## Workflow for a new part

### Step 1 — Download from the JLC/LCSC API (always first)

Use kibrary-automator. Two ways, detailed in
[kibrary-automator.md](kibrary-automator.md):

- **Interactive tool** (preferred when the user is present):
  `python3 /Users/raph/Projects/kibrary-automator/kibrary_automator.py add C1525`
- **Its code directly** (preferred for unattended agent runs): call
  `JLC2KiCadLib` from the tool's venv into a temp dir, then merge into the
  target `*_KSL` library replicating what the tool does (rewrite footprint
  ref and `${KSL_ROOT}` model path, fill Description/Datasheet from the LCSC
  API, update `metadata.json`/`repository.json`, run the `install` command).

Find the LCSC part number first if you only have an MPN (search LCSC/JLCPCB).

### Step 2 — Check everything

**Datasheets are local files (must be an English PDF).**

Do not hand-roll this. `${KSL_ROOT}/scripts/datasheets.py` does the whole
pipeline and is the source of truth:

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
because boards place real components on stock generic symbols: all four buck
inductors on this project are `Device:L_Small` and the SOM's ESD diodes are
`Device:D_TVS`, with the MPN in the Value field. Keying only on `lib_id` leaves
exactly those parts opening a browser. Never let it walk into `.history/` or
`design/handoff/` — those are point-in-time snapshots.

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
   and a shared library has no single project. The variable must exist in
   `kicad_common.json` — and note KiCad **rewrites that file on exit**, so a
   hand-added variable can vanish. `KNL_ROOT` was silently lost exactly this
   way; the symptom is NDA libraries failing to resolve while everything else
   works. Re-check it whenever NDA parts go missing, and edit it only with
   KiCad closed.
3. **Language.** The script's heuristic decides `en` only when confident and
   sends everything else to the queue. Thresholds that took real tuning:
   ≥30% CJK is Chinese; <1% CJK is English with an incidental note (a 46-page
   English AMPAK datasheet carries two Chinese sentences in the stencil note);
   a CJK vocabulary under ~25 distinct glyphs is a company name in a page
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
7. **NDA/restricted documents never enter KSL** — it may be published. They
   go in `${KNL_ROOT}/datasheets/`. Test before deciding: render the first
   pages and grep for *Confidential* / *Proprietary* / *NDA*. the vendor's
   SOM datasheet and the vendor's BRIDGE-A design guide are both stamped
   Confidential; AMPAK's AP6276P has no marking and is published openly on
   `ampak.com.tw`, so it is public. When genuinely unsure, treat as NDA.
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
- Datasheet: <final URL> (English: yes/no→fixed, NDA: local path)
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
  -D KSL_ROOT=/Users/raph/Projects/kicad-shared-libs \
  -D KNL_ROOT=/Users/raph/Projects/kicad-nda-libs --side top --zoom 2
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
