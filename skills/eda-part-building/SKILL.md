---
name: eda-part-building
description: Build KiCad parts (symbol, footprint, 3D STEP model) from scratch from a datasheet when a part is not available from LCSC/JLC or online CAD libraries. Use when drawing a footprint from a datasheet land pattern, generating a 3D model with FreeCAD or OCC, sizing symbol bodies, pin stubs and pin-number text so they stay legible on a sheet, or verifying footprint/symbol/3D alignment and orientation. Complements the kicad-parts skill (KSL library conventions).
---

# Building KiCad Parts from Scratch

Lessons from building a part (footprint + symbol + STEP model) purely from a
datasheet. All commands verified on this machine (macOS, KiCad 10.0.2,
FreeCAD 1.1.1). The **kicad-parts** skill (`${KSL_ROOT}/skills/kicad-parts/`)
owns the KSL library conventions, file naming, symbol properties, datasheet
handling, and render/verification commands — read it alongside this one;
nothing here repeats it.

Both skills live in the `kicad-shared-libs` repo, so edit them there and commit
the change — see `${KSL_ROOT}/skills/README.md` for how they are wired into an
agent's skills directory.

## Workflow order

1. **Extract the package drawing and pin table from the datasheet PDF:**
   - Pin tables: `pdftotext -layout ds.pdf -` (plain `pdftotext` scrambles
     columns).
   - Mechanical/land-pattern drawings: rarely survive pdftotext. Render the
     pages and read them visually:
     `pdftoppm -png -r 150 -f <page> -l <page> ds.pdf /tmp/ds-p`, then Read
     the PNGs.
2. **Build ONE shared pad-map data structure** — pad name → grid position →
   function/electrical type — and generate the footprint, symbol, and STEP
   model programmatically from it. A single source of truth means the three
   artifacts cannot drift apart (pad counts, positions, missing pads).
3. Generate, then run the verification loop (below) until every render is
   actually correct.

## The orientation trap (the big one)

Three coordinate conventions collide; each mismatch produces a mirrored part
that looks plausible in isolation.

- **`.kicad_mod` coordinates: +Y points DOWN** (screen coordinates). A naive
  generator that places "row 0 at +Y" mirrors the footprint vertically.
- **STEP model coordinates: +Y points UP.** Footprint `(x, y)` corresponds
  to model `(x, -y)`. Negate Y once, in the generator, from the shared
  pad map.
- **Area-array packages (LGA/BGA) are drawn in datasheets as BOTTOM views**
  (looking at the package underside). The PCB footprint is the MIRROR of
  that view — usually a horizontal flip: bottom-view "column 1 on the right"
  becomes footprint "column 1 on the left". If the datasheet has a
  "recommended solder pattern" / "land pattern" page, it is drawn as PCB top
  view and is **authoritative** — use it, and check where pin 1/A1 lands.

After generating, cross-check that pin 1 is in the SAME corner in all of:

- footprint pads (pad "1"/"A1" position in the `.kicad_mod`),
- silkscreen pin-1 dot,
- fab-layer pin-1 dot,
- the STEP model's pin-1 feature (notch/dot/chamfer).

Render and LOOK. Coordinates that "seem right" are not verification.

## Fab/silk text placement (tiny packages especially)

Generated and JLC-downloaded footprints often drop `${REFERENCE}` on F.Fab at
(0,0) with the default 1.27/1.0 mm font — on a small package that lands on
top of the fab body outline, pin-1 marks, and polarity triangles (seen on a
1.0×1.0 mm LED where the 1 mm text covered the whole part). Check every text
after generating:

- **Never overlap text with other text or graphics on the SAME layer.**
  That is the hard rule; DRC does not catch it, only a render does.
- **Fab-vs-silkscreen cross-layer text overlap is acceptable ONLY if the
  texts are identical** (they are never fabbed together, e.g. fab
  `${REFERENCE}` under silk `REF**` is fine). Different texts across those
  layers may also be kept visually aligned — the constraint is within-layer.
- For tiny parts, scale fab texts down (0.5 mm height / 0.1 mm thickness is
  a good KLC-ish minimum) and move reference/value clear of the body —
  e.g. reference above, value below, outside the fab graphics' bounding box.
- Keep the pin-1 marker and any polarity/data-direction glyphs unobstructed.

## STEP generation with FreeCAD (headless)

Run scripts **as files** — inline code crashes:

```bash
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd /tmp/make_step.py
# freecadcmd -c "..." → "Application unexpectedly terminated"
```

Export with `shape.exportStep(path)` on the fused Part shape.
`Part.export([compound], path)` **silently writes a near-empty file**
(~1.6 KB header shell) — if the output STEP is a few KB with no
`CARTESIAN_POINT`s, this is why.

Fuse everything into one solid; don't export loose compounds:

```python
import FreeCAD as App, Part
shape = body                      # main package body
for pad in pads:                  # thin pad plates, Z = 0..0.03
    shape = shape.fuse(pad)
shape = shape.removeSplitter()
shape.exportStep(OUT)             # NOT Part.export([...], OUT)
```

Model spec (what KiCad expects for a seated model with zero offsets):

- Z=0 is the board surface; body seated at Z=0.
- Pads flush/coplanar at Z=0 — never protruding below (renders sunken).
- Bounding box centered on the origin in X/Y.
- Real body height from the datasheet side view.

### Colored STEP (preferred)

KiCad renders STEP colors, but console FreeCAD has no `ViewObject`, so plain
`exportStep` output is **uncolored** (gray). The route that works without
the GUI: OCC XCAF — build shapes with `BRepPrimAPI`/`BRepAlgoAPI`, create a
`TDocStd_Document`, register solids via `XCAFDoc` ShapeTool + ColorTool,
write with `STEPCAFControl_Writer`. The `OCP` package provides these
bindings under `/usr/bin/python3` (pip user site:
`~/Library/Python/3.9/lib/python/site-packages/`); FreeCAD's bundled OCC
also has them.

Known-good reference script — it produced
`${KSL_ROOT}/Sensor_KSL/Sensor_KSL.3dshapes/LGA-47_D11.0-P1.00.step`, a round
LGA package with a protruding pin-1 tab, so it exercises the colouring, the
fillet-then-fuse ordering and the tab geometry all at once:
[scripts/make_step_colored_example.py](scripts/make_step_colored_example.py)
— run with `/usr/bin/python3`.

Gotchas verified the hard way:

- **Construct colors as sRGB**: `Quantity_Color(r, g, b, Quantity_TOC_sRGB)`.
  With the default linear-RGB constructor, OCCT's writer converts to sRGB on
  output and a 0.08 black lands in the file as 0.31 grey.
- Cut package-level features (notches, chamfers) from **every** solid they
  intersect, including the pads, or a pad corner pokes through the void.
- Check whether a pin-1 mark is a cutout or a protruding tab against a
  product photo — datasheet outline drawings are ambiguous. If a feature
  protrudes past the body outline, mirror it on the footprint on all three
  outline layers (F.Fab at true size, F.SilkS at body-silk offset, F.CrtYd at
  feature radius + 0.25 mm). Draw the **union outline**, never two overlapping
  full circles: compute the circle–circle intersection points analytically
  (chord distance `a = (d² + R² − r_t²) / 2d` from the body center, half-chord
  `h = √(R² − a²)`), then emit the body as a major `fp_arc` between the two
  intersection points and the tab as its outer arc between the same points.
  The result is a clean D-bump per layer, the courtyard stays a single closed
  chain (arc endpoints must match exactly — keep 4 decimals), and the silk
  never wanders inside the body where it would cross a corner pad's mask
  opening and trigger silk-clipped DRC warnings. Convert model coordinates to
  footprint coordinates by negating Y (a tab at 135° on radius r sits at
  footprint `(-r·cos45°, -r·sin45°)`).
- `BRepFilletAPI_MakeFillet` fails ("command not done") on edges crossing a
  tangent junction — fillet the plain solid first, then fuse the bump.
- **JLC2KiCadLib legacy `(module ...)` format renders `fp_poly` ALWAYS
  filled** — that format has no fill token at all. The converter draws the
  package body outline plus per-terminal/EP glyphs as polygons on a doc layer
  (`Cmts.User`, sometimes `F.SilkS`), and once that layer parses correctly
  they become opaque blobs that hide the entire footprint. Fix: convert the
  body-outline poly to unfilled `fp_line` segments and **DELETE the interior
  terminal/EP glyph polys outright** — the pads themselves are the
  authoritative documentation of the land pattern; duplicating them as filled
  comment-layer art only obscures the footprint. If any of that art sits on
  `F.SilkS`, it would print on the board — move the outline to `Cmts.User`.
- **Legacy `(model (at (xyz ...)))` offsets are interpreted in INCHES**
  (unlike `(offset (xyz ...))`, which is mm). Converter junk like
  `(at (xyz -0.0079 0.0151 0))` looks negligible but is 0.2/0.38 mm and
  visibly shifts the 3D model off the pads on a 2 mm package. Zero these
  values (JLC/EasyEDA STEP models are already centered).
- **A fill-token grep misses legacy polys** when auditing for filled-blob
  defects: `(fill yes|solid)` only exists in v6+ files. For files starting
  with `(module`, treat EVERY `fp_poly` as filled — scan for `fp_poly` on
  doc/silk layers in those files instead, and flag body-sized ones as blobs.
- JLC2KiCadLib also drops a 1 mm `${REFERENCE}` on F.Fab at (0,0) — dead
  center on the body, violating the tiny-package fab-text rule above. Move
  it clear of the body/pad extent and shrink to 0.5/0.1 mm while fixing the
  blobs.

Sanity check for color: `grep -c COLOUR_RGB file.step` must be > 0.

If the colored route fails, the uncolored `exportStep` fallback is
acceptable: ship it and note "model is uncolored (headless export)" in the
part report.

### Numeric geometry check

Catch offset/mirroring bugs without rendering by parsing the STEP's
coordinates (open with `errors="ignore"` — STEP files may contain
non-UTF-8 bytes):

```python
import re
pts = [tuple(map(float, m.groups()))
       for m in re.finditer(r"CARTESIAN_POINT\s*\(\s*'[^']*'\s*,\s*\(\s*([-\d.eE+]+)\s*,\s*([-\d.eE+]+)\s*,\s*([-\d.eE+]+)", 
                            open(path, errors="ignore").read())]
xs, ys, zs = zip(*pts)
print(min(xs), max(xs), min(ys), max(ys), min(zs), max(zs))
# Expect: X/Y roughly symmetric about 0, Z from ~0 to body height.
```

The parse includes axis-placement and construction-geometry points, so the
bbox is approximate — good enough to catch a mirrored part or a
hundreds-of-mm offset, not for micron checks.

## Verification loop

Use the render commands from the **kicad-parts** skill verbatim: footprint
SVG → PNG, symbol SVG → PNG, one-footprint test board +
`kicad-cli pcb render` top/front/iso with
`-D KSL_ROOT="$KSL_ROOT" -D KNL_ROOT="$KNL_ROOT"`. Pass **both** roots even
when the part is public: a missing root drops the model silently, with a
warning but exit 0.

Two things bite here:

- The test board embeds a **COPY** of the footprint (including the model
  block). Rebuild the board with the pcbnew snippet after **every**
  footprint edit, or you render the stale version and the fix "does
  nothing".
- Actually READ every rendered image (top for X/Y and pin-1 corner, front
  for Z seating, iso for overall shape). Skipping a render is how mirrored
  footprints ship.

## Symbol construction for big modules

- Group pins logically: power on the left, interfaces/GPIO on the right,
  DNC/debug pins on the bottom.
- **Text-overlap layout rules** (with the default 1.27 mm font):
  - Side pins at **2.54 mm pitch** — 1.27 mm pitch makes adjacent pin names
    touch.
  - Body half-width ≥ longest-left-name + longest-right-name in mm (the
    stroke-font advance measures ≈ 0.817 × the text size per character, so
    ≈ 1 mm/char at 1.27 mm) with margin; ~17.8 mm suits names like
    `DBG_UART_RX`.
  - Bottom (vertical) pins: names extend UP into the body ≈ their length in
    mm — drop the body bottom ~12 mm below the lowest side pin or they
    strike through the side-pin names. Space them at 5.08 mm.
  - Put Reference AND Value above the body top edge; a Value under the body
    collides with bottom pin numbers.
  - Render the symbol SVG and look for collisions; don't trust coordinates.
- **Size the pin stub to the widest pin NUMBER, not to a default.** The number
  is drawn along the stub and is routinely wider than it: `AB31` at 1.27 mm
  measures ~4.15 mm on a 3.81 mm stub and overhangs the connection point at
  both ends, where it runs into whatever net label the sheet anchors there
  (labels normally sit exactly on the connection point, on both sides of the
  symbol). For dense symbols use **1.0 mm pin-number text on a 2.54 mm stub**,
  which leaves ~0.45 mm clear at each end.
- Never hide pin numbers on a big connector or SOM to dodge that collision —
  the pin/ball coordinates are the most useful thing on the sheet during
  bring-up.
- **Fixing an EXISTING symbol: lengthen stubs INWARD** and shrink the body to
  match, so every pin's `(at ...)` coordinate stays byte-unchanged and
  connectivity is preserved by construction. Extending outward moves the
  connection points and forces every attached label and wire on every sheet to
  move with them, where a single miss silently orphans a net.
- For LGA/BGA, pin number = pad name (e.g. `"A1"`).
- Electrical types from the pin table: `power_in` for supplies, `passive`
  for DNC/ESD pins (avoids ERC noise from unconnected `unspecified` pins).
- **Symbol pin set must equal footprint pad set exactly.** Diff them
  programmatically:

```python
import re
pads = set(re.findall(r'\(pad "([^"]+)"', open("fp.kicad_mod").read()))
pins = set(re.findall(r'\(number "([^"]+)"', open("lib.kicad_sym").read()))
print("fp-only:", pads - pins, "sym-only:", pins - pads)  # both must be empty
```
