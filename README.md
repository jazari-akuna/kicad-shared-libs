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
    scripts/check_models.py          # every 3D model is placed where it belongs
    scripts/check_nda.py             # no NDA-restricted document is in this repo

`check_models.py` grades three things a 2D review, DRC, ERC and a netlist
comparison all pass clean:

- **units** — in the legacy `(module ...)` format KiCad reads
  `(model ... (at (xyz ...)))` in **inches**; the modern `(footprint ...)`
  format spells it `(offset (xyz ...))` and reads it in **millimetres**. A
  legacy footprint carrying `(at (xyz 0 0 -0.074803))` therefore drops its model
  1.900 mm, not 0.075 mm — straight through a 1.6 mm board. The JLC/EasyEDA
  converter means inches and mostly gets them right, but the file cannot say so,
  and the next hand-edit types millimetres. Re-save the footprint in the modern
  format and the ambiguity is gone permanently.
- **transform** — missing or unresolvable model, hidden model, scale ≠ 1, or an
  absurd offset. Stale EasyEDA canvas coordinates have shipped here as
  `(at (xyz -37.465 32.335 0))`, which is 951 mm off-board.
- **seating** — geometry. The STEP is placed exactly as KiCad places it, sliced
  at board depth, and every remaining cross-section must fit inside a drilled
  hole. Anything else is a body sunk into the substrate, a leg fatter or longer
  than its hole, or a model rotated with respect to its own land pattern — all
  of which mean the part cannot be assembled. Needs FreeCAD; the script says so
  and grades the rest rather than reporting a false green if it is absent.

`check_nda.py` gates the one mistake this repo cannot take back. It has a public
remote, so a restricted document committed here is disclosed by the next push,
and that has happened once: the vendor' SENSOR-FAMILY product specification was
committed as `datasheets/SENSOR-A.pdf` and had to be purged from history. The
check looks three ways, because a document arrives by more than one route:

- **hash** — sha256 against `scripts/nda_denylist.json`. Immune to renaming, and
  it reads a **git-lfs pointer** without needing the object, since the pointer
  states the sha256 of the real file. That is what makes `--scope history` work
  on a fresh clone.
- **content** — text of any PDF, matched against the vendors and part families
  known to be restricted. The FPC document carries no "Confidential" stamp, only
  a legal notice, so grepping for the stamp would have passed it.
- **reference** — a `Datasheet` property pointing a restricted document at
  `${KSL_ROOT}`. The file can be correctly absent while the link still claims it
  lives here. Restricted parts link to `${KNL_ROOT}/datasheets/<MPN>.pdf`.

`--scope history` is the one that matters before a push: deleting a file in a new
commit does not unpublish the blob. `--self-test` is a negative control — it
plants material each layer must reject and a clean control each must accept, and
fails if any layer stays quiet, because a check nobody has watched fail is not
evidence. Refresh the digests from the private repo with `--sync`.

`hooks/pre-push` runs it at the only moment that counts. Git does not carry hooks
through a clone, so install it by hand:

    install -m 755 hooks/pre-push .git/hooks/pre-push

It **replaces** the stock git-lfs pre-push hook and calls `git lfs pre-push`
itself, because git allows only one. Keep that line or datasheet LFS objects
stop being uploaded.

Pre-existing seating defects are listed in
`scripts/model_seating_backlog.txt` (and `${KNL_ROOT}/model_seating_backlog.txt`,
kept out of this repo because it names an NDA part) so a new regression fails
immediately instead of hiding in the backlog. Delete a line as you fix one.
Add `--repo knl` for the NDA libraries, `-v` to see the clean footprints too.
Exit 0 clean, 1 violations, 2 the check could not run.
