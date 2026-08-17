# Datasheets

One English PDF per part, named after the MPN. Symbols point here with

    ${KSL_ROOT}/datasheets/<MPN>.pdf

so pressing **D** on a part in Eeschema opens the local file in the system PDF
reader, with no network involved.

## Why the files are in the repo

Datasheet URLs rot. LCSC re-hashes its CDN paths, TI retires `lit/ds/symlink`
aliases, Hirose serves `document?clcode=` only to a browser user-agent, and
st.com refuses automated clients outright. When a link dies the part loses its
only authoritative document. A file committed next to the symbol survives that,
works offline, and is versioned with the part it describes.

`${KSL_ROOT}/...` rather than a plain relative path because KiCad resolves
relative datasheet paths against the *project*, and a shared library has no one
project. The variable is set in KiCad under Preferences → Configure Paths.

## Rules

- **English.** Bilingual is fine when the English is complete — many LCSC
  connector and switch drawings are Chinese and English side by side. Chinese-only
  substance is not acceptable.
- **Public only.** A document supplied under NDA, or marked Confidential, never
  goes in this repo. Those live under `${KNL_ROOT}/datasheets/` in the private
  library. If you are unsure, treat the document as restricted.
- **Right part, not just right language.** A datasheet for a different part is a
  worse defect than one in the wrong language, and it happens: this library had
  `2N7002` (small-signal N-channel MOSFET) pointing at a generic SOT-23 package
  drawing with no electrical specs.
- One file may serve a family covered by one document.

## Getting them after a clone

The PDFs are stored with **git-lfs**, so a plain clone without git-lfs installed
leaves 100-byte pointer files here. That failure is silent — the paths still
resolve and the files still exist, they just are not PDFs:

    git lfs install && git lfs pull

Four parts have no stable upstream link and exist here only as local copies:
`CH221K` (USB Type-C configuration channel controller), `CH224D` (USB PD sink
controller), `NB7VPQ904M` (USB 3.1 / DisplayPort redriver-mux) and
`YZ90415045R-01` (a translated connector drawing that exists nowhere else).

## Maintaining it

Do not curate by hand. The datasheet pipeline lives with the rest of the
library tooling in the private repository, `${KNL_ROOT}/scripts/datasheets.py`,
and is run from there against this one. It fetches, detects wrong-language and
wrong-part documents, rewrites the symbol `Datasheet` properties, and gates on
every part resolving to an English PDF.

One thing to know if you consume this library from a board repo: a `.kicad_sch`
carries its **own copy** of every symbol — in the `lib_symbols` cache and again
on each placed instance — and **D** reads those copies, not the library.
Relinking here alone leaves the boards opening URLs, so the pipeline has a
`sync-project` step for them. It matches on the part *value* as well as the
symbol name, because boards routinely place real components on stock generic
symbols such as `Device:L_Small` and `Device:D_TVS`, with the MPN in the Value
field.

Per-part bookkeeping (where each file came from, its language statistics, and
why any non-obvious call was made) is kept in `.state.json`, which is
deliberately **not tracked** here: it is fetch bookkeeping, not a part.
