# Skills

Agent skills for building and maintaining the parts in this repository. They
live here rather than only in `~/.cursor/skills/` so that the conventions ship
with the libraries they describe: a rule about symbol pin numbering or datasheet
storage is worthless if it drifts away from the parts it governs, and reviewing
a part change alongside the rule it follows only works if both are in the same
history.

| Skill | Covers |
|-------|--------|
| `kicad-parts/` | KSL/KNL library conventions: downloading from LCSC/JLC, naming, symbol properties, footprint and 3D verification, datasheet policy, NDA handling |
| `eda-part-building/` | Building a part from scratch off a datasheet when it is not available anywhere: land patterns, FreeCAD STEP generation, symbol legibility |

## How they are wired up

The copies in this repo are the source of truth. `~/.cursor/skills/` holds
symlinks to them:

    ~/.cursor/skills/kicad-parts        -> <this repo>/skills/kicad-parts
    ~/.cursor/skills/eda-part-building  -> <this repo>/skills/eda-part-building

So edit the files **here** and commit. Editing through the `~/.cursor` path
reaches the same files, but the change is then an uncommitted edit sitting in a
git repo, which is easy to lose.

To reproduce the wiring on another machine:

    ln -s "$PWD/skills/kicad-parts"       ~/.cursor/skills/kicad-parts
    ln -s "$PWD/skills/eda-part-building" ~/.cursor/skills/eda-part-building

Skills that are about a *board* rather than about parts — `pcb-placement`,
`schematic-design` — deliberately stay out of this repo. They belong with the
project that uses them, not with the component library.
