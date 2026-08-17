# kibrary-automator reference

Single self-contained script, `kibrary_automator.py`, living in its own
checkout (referred to below as `$KIBRARY`) — it is a separate tool, not part of
this repository. It wraps
[JLC2KiCadLib](https://github.com/TousstNicolas/JLC2KiCad_lib) to download a
part from the JLC/EasyEDA API, previews it in the terminal, fills
Description + Datasheet from the LCSC API, files it into a `*_KSL` library,
and registers the library in KiCad's `sym-lib-table` / `fp-lib-table`.

On first launch it bootstraps a private venv (Rich + JLC2KiCadLib) at
`~/Library/Application Support/kibrary-automator/venv/`. Config lives at
`~/Library/Application Support/kibrary-automator/config.yaml`:

```yaml
library_root: <path to the kicad-shared-libs checkout>
lib_suffix: _KSL
github_user: <github account owning the remote>
model_var: ${KSL_ROOT}
```

New parts land in `kicad-shared-libs`, so `${KSL_ROOT}` is the right
`model_var`. A **restricted** part belongs in the separate `kicad-nda-libs`
repo instead — move it there after import and rewrite its model path to
`${KNL_ROOT}/<Lib>/<Lib>.3dshapes/<Model>.step`. If only the *document* is
restricted and the part is not, leave the part here and move just the PDF; see
the two tiers in [SKILL.md](SKILL.md).

## Commands

```
kibrary_automator.py [--library-root PATH] [command]
  add [PART ...]   download JLCPCB/LCSC parts and add to a library (default)
  install          register the repository's libraries in KiCad (idempotent,
                   backs up the library tables; safe to run unattended when
                   only one KiCad version is installed)
  config           show the stored configuration (--reset to change path)
```

Companion scripts in the same folder:

- `fill_datasheets.py [--dry-run]` — sweep all libraries and fix symbols
  whose Datasheet field isn't a real PDF (resolved via LCSC API, validated).
  Caveat: it accepts any existing PDF link as "ok" — it does NOT detect
  Chinese-language or wrong-document PDFs, and it can't fix parts the LCSC
  API no longer lists (`not-found`). Language audits must be done manually
  (see SKILL.md Step 2).
- `uninstall.py [--yes]` — removes venv/config/KiCad table entries only.

## Route A: drive the interactive tool

`add` is interactive. When stdin is not a TTY every prompt falls back to a
line-based prompt, so answers can be piped. Prompt sequence per part:

1. `Component description` — Enter accepts the API-resolved default.
2. `Default reference` — e.g. `U` (a `?` is appended automatically).
3. Duplicate warning `y/n` — only if the symbol name already exists.
4. Library menu: `1` = create new library; existing libraries are listed
   from `2` in **alphabetical order** (folders in the repo root containing
   `<name>.kicad_sym`). List them yourself first to compute the number.
5. If creating new: `Library name` (suffix `_KSL` auto-appended), then
   `Library description`.
6. `Add another component?` — `n`.

After the loop it always runs the install step. Example (merge C1525 into
the 2nd library alphabetically, accepting defaults):

```bash
printf '\nC\n3\nn\n' | python3 "$KIBRARY/kibrary_automator.py" add C1525
```

Caution: if the run is aborted, loose files stay in the library root and the
next launch starts with a leftover add/cleanup prompt — answer it first.

## Route B: reuse its code directly (unattended)

Download with the venv's JLC2KiCadLib into a **temp dir** (same flags the
tool uses):

```bash
mkdir -p /tmp/jlc-dl && cd /tmp/jlc-dl
"$HOME/Library/Application Support/kibrary-automator/venv/bin/JLC2KiCadLib" C1525 \
  -dir . -symbol_lib_dir . -footprint_lib . -model_dir .
```

Produces loose files: `<MPN>.kicad_sym`, `<Footprint>.kicad_mod`,
`<Footprint>.step`. Then replicate the tool's merge (see
`merge_into()` / `create_library()` in the script for the exact behavior):

1. **Merge symbol**: append the inner `(symbol "...")` block (everything
   from the first `(symbol ` line, minus the file's closing paren, indented
   by two spaces) before the final `)` of `<Lib>.kicad_sym`. Check for a
   duplicate symbol name first.
2. **Copy assets**: `.kicad_mod` → `<Lib>.pretty/`, `.step` →
   `<Lib>.3dshapes/`.
3. **Rewrite symbol footprint ref**: raw download has
   `(property "Footprint" ".:C0402")` — replace the `.` library prefix with
   the real name: `"<Lib>:C0402"`.
4. **Rewrite model path**: raw `.kicad_mod` has `(model ./C0402.step` —
   change to `(model ${KSL_ROOT}/<Lib>/<Lib>.3dshapes/C0402.step` (no
   quotes needed; keep offset/scale/rotate lines).
5. **Fix Reference/Description/Datasheet** in the symbol:
   Reference like `U?` (must end in `?`); Description and Datasheet from the
   LCSC API below (raw downloads often have an empty Description and a
   non-PDF Datasheet like `https://item.szlcsc.com/15869.html`).
6. **New library only**: create `<Lib>/metadata.json` by copying an existing
   one (e.g. `Audio_KSL/metadata.json`) and adjusting name, description and
   `identifier` — keep the identifier prefix the other libraries use and only
   swap the trailing `<Lib>`, since KiCad's PCM keys off it. Then append
   `{"path": "<Lib>/metadata.json"}` to the repo-root `repository.json`.
7. **Register in KiCad**: `python3 kibrary_automator.py install`.

## LCSC / EasyEDA / JLC API endpoints (as used by the tool)

```bash
# Product detail: description keys productIntroEn/productDescEn/productNameEn,
# datasheet at .pdfUrl. NOTE: returns "result": null (with code 200) for
# delisted/marketplace parts — fall through to the endpoints below.
curl -s -A "Mozilla/5.0" \
  "https://wmsc.lcsc.com/ftps/wm/product/detail?productCode=C1525"

# EasyEDA fallback for description: .result.description
curl -s -A "Mozilla/5.0" \
  "https://easyeda.com/api/products/C1525/components?version=6.4.19.5"

# JLC component detail: .data.dataManualFileAccessId holds a datasheet
# file id even when LCSC has none
curl -s -A "Mozilla/5.0" \
  "https://cart.jlcpcb.com/shoppingCart/smtGood/getComponentDetail?componentCode=C1525"
# ...download that file id as a PDF:
#   https://jlcpcb.com/api/file/downloadByFileSystemAccessId/<dataManualFileAccessId>
```

Validate datasheet URLs before writing them: LCSC redirects unknown
resources to its homepage instead of 404ing, so a fetch that lands on a
bare domain root counts as broken.
