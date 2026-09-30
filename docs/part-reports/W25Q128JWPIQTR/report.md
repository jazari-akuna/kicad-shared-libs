# W25Q128JWPIQTR thin-package part report

## Selected package and source

The exact orderable Winbond `W25Q128JWPIQ TR` is the same 1.7–1.95 V,
128-Mbit W25Q128JW flash family as the existing `W25Q128JWSIQTR`; only the
package code changes from **S** (SOIC-8 208 mil) to **P** (WSON-8 6 × 5 mm).
The local English [Winbond W25Q128JW Rev G datasheet](../../../datasheets/W25Q128JWPIQTR.pdf)
shows identical pin functions for the two packages (printed p. 5), package
heights (printed pp. 67–68), and the package/order-code table (printed p. 75).
[Winbond's product listing](https://www.winbond.com.tw/hq/product/code-storage-flash-memory/serial-nor-flash/?__locale=en&partNo=W25Q128JW)
shows WSON8 6 × 5 mm as a production package.
[JLCPCB lists `W25Q128JWPIQ TR` as C6000493](https://jlcpcb.com/partdetail/WinbondElec-W25Q128JWPIQTR/C6000493)
with assembly support. Live stock must be rechecked when buying.

The SOIC package height A is 1.75/1.95/2.16 mm min/nom/max; the WSON
package is 0.70/0.75/0.80 mm. The worst-case package-height reduction is
**1.36 mm**. These are package dimensions, not the final mounted assembly
height; solder, board warp, frame and battery tolerances still apply. The
sampled 0.90 mm frame clearance at U502 leaves at most 0.10 mm beyond the
WSON package maximum before all those contributors, so mechanical release is
not yet demonstrated.

## KiCad artifacts

- Symbol `Memory_KSL:W25Q128JWPIQTR` in `Memory_KSL.kicad_sym` has the same
  numbered-pin positions and electrical types as the SOIC symbol. Its
  footprint property points to the existing
  `Memory_KSL:WSON-8_L6.0-W5.0-P1.27-BL-EP`.
- The existing shared footprint and simplified STEP model are reused; the
  silkscreen pin-1 dot is moved inside the package to local center
  (−2.25, +2.15) mm with 0.10 mm radius. This is the board-validated
  position that clears a neighboring U601 silkscreen collision. No copper
  pad or 3D model geometry changed.
  Pads 1–8 have the same functions as the old part: 1 CS#, 2 DO/IO1, 3
  WP#/IO2, 4 GND, 5 DI/IO0, 6 CLK, 7 HOLD#/IO3, 8 VCC. The exposed center
  land is a second copper pad numbered **4**, so it shares GND. Winbond says
  this metal has no internal electrical connection and may float or connect
  to GND; it also says to avoid exposed vias under it (printed p. 68).
- In its saved footprint orientation, pad 1 is at (−1.905004, +3.0127) mm,
  the bottom-left pad in KiCad coordinates. At a **270°** board rotation it
  lies top-left, with pads 1–4 down the left and 8–5 down the right.
- The existing STEP file identifies itself as nominal **H0.7**. It is a
  placement illustration and must not be used as a maximum-height collision
  envelope; use datasheet **Amax 0.80 mm** plus assembly allowances.

## Checks and visuals

- [Symbol export](symbol.svg) and [footprint export](footprint.svg) were
  generated with KiCad CLI and inspected. The footprint includes a visible
  pin-1 dot inside the body beside pad 1.
- A parsed library comparison found all eight pin numbers, positions, names,
  and electrical types identical to `W25Q128JWSIQTR`; the parsed WSON
  footprint has numbered copper pads 1–8 and the second pad 4.
- `check_models.py --repo ksl --check units --check transform` reported no
  model-placement violations across 184 shared footprints. This does not
  establish exact model height or the mechanical clearance in the assembly.
- No project schematic or PCB was edited here. Board-level connectivity,
  DRC, and clearance remain integration checks.
