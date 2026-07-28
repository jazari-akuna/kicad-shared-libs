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
- **Public only.** NDA or Confidential documents never go in this repo, which may
  be published. They live in `${KNL_ROOT}/datasheets/` in the private
  `kicad-nda-libs` repo. If you are unsure, treat the document as NDA.
- **Right part, not just right language.** A datasheet for a different part is a
  worse defect than one in the wrong language, and it happens: this library had
  `2N7002` pointing at a generic SOT23 package drawing with no electrical specs.
- One file may serve a family covered by one document.

## Getting them after a clone

The PDFs are stored with **git-lfs**, so a plain clone without git-lfs installed
leaves 100-byte pointer files here. That failure is silent — the paths still
resolve and the files still exist, they just are not PDFs — so check for it:

    scripts/datasheets.py setup      # enables LFS, pulls the PDFs, verifies each one

If you would rather not carry ~160 MB of LFS objects, switch every link back to
its upstream URL instead:

    scripts/datasheets.py relink --mode url
    scripts/datasheets.py sync-project --project <board-repo> --mode url

`--mode local` switches back. The round trip is lossless. Four parts can never
go back to a URL: `CH221K`, `CH224D`, `NB7VPQ904M` (only ever local copies of
documents with no stable direct link) and `YZ90415045R-01` (a translation that
exists nowhere else). Those stay local in either mode, and the script says so.

## Maintaining it

Do not curate by hand. `../scripts/datasheets.py` runs the pipeline:

    datasheets.py fetch      # download, rejecting HTML pages saved as .pdf
    datasheets.py triage     # language + wrong-document detection
    datasheets.py queue      # what needs a human or agent judgement
    datasheets.py apply --results verdicts.json
    datasheets.py relink     # rewrite the symbol properties
    datasheets.py verify     # gate: every part resolves to an English PDF

Add `--repo knl` for the NDA repo (which stays plain git — it is small, and its
pre-push guard must not be replaced by the LFS hook).

Two steps concern a consuming board repo rather than this one:

    datasheets.py sync-project --project <board-repo>
    datasheets.py harvest     --project <board-repo>

`sync-project` is not optional. A `.kicad_sch` carries its own copy of every
symbol — in the `lib_symbols` cache and again on each placed instance — and
**D** reads those copies, not the library. Relinking here alone leaves the
boards opening URLs. It also matches on the part *value*, because boards place
real components on stock generic symbols: all four buck inductors are
`Device:L_Small` and the SOM's ESD diodes are `Device:D_TVS`, with the MPN in
the Value field.

`harvest` collects datasheets for parts a board uses that no library defines,
taking the URL straight off the schematic.

`.state.json` records, per part, where the file came from, its language
statistics and why any non-obvious call was made. It is how a future reader
knows a bilingual document was reviewed and accepted rather than missed.
