# kicad-shared-libs

Shared KiCad symbol, footprint and 3D model libraries (`*_KSL`), with the
English datasheet for every part.

This repository carries parts and their datasheets. Nothing else: no build
tooling, no project documents, no internal notes.

## Setup

Add `KSL_ROOT` to KiCad's path variables (Preferences → Configure Paths),
pointing at this folder.

The datasheets are stored with **git-lfs**, so install it before cloning:

    git lfs install
    git lfs pull

A clone made without git-lfs leaves pointer files where the PDFs should be, and
pressing **D** on a part in Eeschema then opens nothing.

## Layout

| Path | What |
|------|------|
| `<Category>_KSL/` | One self-contained library: `.kicad_sym`, `.pretty/`, `.3dshapes/` |
| `datasheets/` | One English PDF per part, git-lfs. See `datasheets/README.md` |
| `repository.json` | Library index |
| `_attic/` | Retired or duplicate leftovers, kept rather than deleted |
| `.kibrary/` | [kibrary-automator](https://github.com/jazari-akuna/kibrary-automator)'s own workspace — leave it alone |

## Datasheets

Every part links to a local file, `${KSL_ROOT}/datasheets/<MPN>.pdf`, never a
URL. URLs rot — LCSC re-hashes its CDN paths, TI retires `lit/ds/symlink`
aliases, st.com refuses automated clients — and when the link dies the part
loses its only authoritative document.

## Footprints and 3D models

Two things about `(model ...)` placement are worth knowing before you edit a
footprint by hand, because both fail silently:

- **Units.** In the legacy `(module ...)` format KiCad reads
  `(model ... (at (xyz ...)))` in **inches**; the modern `(footprint ...)`
  format spells it `(offset (xyz ...))` and reads **millimetres**. A legacy
  footprint carrying `(at (xyz 0 0 -0.074803))` therefore drops its model
  1.900 mm, not 0.075 mm — straight through a 1.6 mm board. Re-save in the
  modern format and the ambiguity is gone permanently.
- **Stale converter coordinates.** EasyEDA canvas offsets have shipped here as
  `(at (xyz -37.465 32.335 0))`, which is 951 mm off-board.

## Scope

Parts whose vendor documentation is supplied under NDA are not in this
repository, and neither are their datasheets. They live in a separate private
library addressed by the `KNL_ROOT` path variable; a symbol that needs one
links to `${KNL_ROOT}/datasheets/<MPN>.pdf`. Contributors outside that
arrangement will see the link and not the file, which is the intended
behaviour.

Library maintenance tooling (datasheet fetching, 3D-model seating checks, and
the pre-push guard that keeps restricted documents out of this repository) also
lives in that private repository, and is installed from there.
