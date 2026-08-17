# Skills

Agent skills for building and maintaining the parts in this repository. They
live here rather than only in an agent's personal skills directory so that the
conventions ship with the libraries they describe: a rule about symbol pin
numbering or datasheet storage is worthless if it drifts away from the parts it
governs, and reviewing a part change alongside the rule it follows only works if
both are in the same history.

| Skill | Covers |
|-------|--------|
| `kicad-parts/` | Library conventions: downloading from LCSC/JLC, naming, symbol properties, footprint and 3D verification, datasheet policy, restricted-part handling, and the three gates that check all of it |
| `eda-part-building/` | Building a part from scratch off a datasheet when it is not available anywhere: land patterns, FreeCAD/OCC STEP generation, symbol and fab-text legibility, the orientation trap |

Read `kicad-parts/` first. It owns the conventions; `eda-part-building/`
deliberately does not repeat them and assumes you have read it.

## Before you use them

Two things a fresh clone does not give you.

**1. Path variables.** Nothing in these skills names a checkout location,
because the libraries are shared and no two machines agree on where they sit.
Every path is written against one of two variables:

| Variable | Repository |
|----------|------------|
| `${KSL_ROOT}` | this repository, `kicad-shared-libs` — public remote |
| `${KNL_ROOT}` | `kicad-nda-libs` — private, holds documents and parts that may not be published |

Declare both to KiCad in Preferences → Configure Paths, and export them in your
shell so the commands in the skills can be pasted as written:

    export KSL_ROOT="$PWD"
    export KNL_ROOT=<path to the kicad-nda-libs checkout>

`${KNL_ROOT}` is optional if you only work on public parts, but `kicad-cli`
resolves an unset variable to a *silently missing 3D model*, with a warning and
exit 0 — so set it, or check your renders rather than your exit codes.

Note that KiCad **rewrites `kicad_common.json` on exit**, so a hand-added
variable can vanish. Edit it with KiCad closed, and re-check it whenever
restricted parts stop resolving.

**2. The pre-push hook.** `git clone` does not carry hooks. This repository has
a public remote and a guard that refuses to push restricted material, and that
guard is inert until you install it:

    install -m 755 ${KNL_ROOT}/hooks/ksl-pre-push ${KSL_ROOT}/.git/hooks/pre-push

It replaces the stock git-lfs pre-push hook and calls `git lfs pre-push` itself,
because git allows only one. Without it you get no NDA gate; without its
git-lfs line you get no datasheet uploads.

Then fetch the datasheets, which are stored with git-lfs:

    git lfs install && git lfs pull

## Using them as agent skills

Each subdirectory is a skill in the usual `SKILL.md` layout — YAML frontmatter
with `name` and `description`, markdown body, supporting files alongside — so
pointing an agent at this directory as a skills source works with no
conversion.

To wire them into a personal skills directory instead, symlink rather than
copy, so there is one source of truth and edits land in git:

    ln -s "$PWD/skills/kicad-parts"       ~/.cursor/skills/kicad-parts
    ln -s "$PWD/skills/eda-part-building" ~/.cursor/skills/eda-part-building

Edit the files **here** and commit. Editing through the symlink reaches the same
files, but the change is then an uncommitted edit sitting in a git repo, which
is easy to lose.

## Scope

These two skills are about *parts*. Skills about a *board* — placement,
schematic design — deliberately stay out of this repository. They belong with
the project that uses them, not with the component library.
