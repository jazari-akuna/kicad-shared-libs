# kicad-shared-libs

Shared KiCad symbol, footprint and 3D model libraries (`*_KSL`), the English
datasheet for every part, and the agent skills describing how parts here are
built and verified.

## Setup

Add `KSL_ROOT` to KiCad's path variables (Preferences → Configure Paths),
pointing at this folder. NDA-restricted parts live in the separate private
`kicad-nda-libs` repo under `KNL_ROOT`; nothing NDA belongs here, because this
repo may be published.

Then fetch the datasheets, which are stored with **git-lfs**:

    scripts/datasheets.py setup

A clone made without git-lfs installed leaves pointer files where the PDFs
should be, and pressing **D** on a part in Eeschema then opens nothing. `setup`
enables LFS, pulls, and checks that every file really is a PDF, because that
failure is otherwise silent.

## Layout

| Path | What |
|------|------|
| `<Category>_KSL/` | One self-contained library: `.kicad_sym`, `.pretty/`, `.3dshapes/` |
| `datasheets/` | One English PDF per part, git-lfs. See `datasheets/README.md` |
| `scripts/datasheets.py` | Fetch, language-triage, relink and verify datasheets |
| `skills/` | Agent skills for building and checking parts. See `skills/README.md` |
| `repository.json` | Library index |
| `_attic/` | Retired or duplicate leftovers, kept rather than deleted |
| `.kibrary/` | kibrary-automator's own workspace — leave it alone |

## Datasheets

Every part links to a local file, `${KSL_ROOT}/datasheets/<MPN>.pdf`, never a
URL. URLs rot — LCSC re-hashes its CDN paths, TI retires `lit/ds/symlink`
aliases, st.com refuses automated clients — and when the link dies the part
loses its only authoritative document.

If you would rather not carry the LFS objects, `scripts/datasheets.py relink
--mode url` switches every link back upstream, and `--mode local` switches back.

## Checking the libraries

    scripts/datasheets.py verify     # every part resolves to an English PDF
