# SW-DOME_ROUND_D4.0_CENTER-RING_PROVISIONAL

## Status and scope

This is a **provisional, source-matched mechanical dome contact**, not a qualified purchasing MPN. The user-selected target is a 4 mm round dome with a center feature, 160–250 gf operating force, and 0.16–0.20 mm travel. The source selection image also shows three-leg and cross PCB diagrams; those were not used because they are not confirmed as the selected round contact geometry.

The PCB contact follows the published Snaptron 4 mm double-sided contact-pad dimensions: 1.70 mm center diameter, 2.71 mm ring inside diameter, and 4.76 mm ring outside diameter. Snaptron describes this as one possible pad pattern and assigns final circuit suitability to the customer, so supplier qualification and switching-life validation remain required.

Sources:

- [Snaptron double-sided PCB contact pad](https://www.snaptron.com/products/pcb-pads/double-sided-contact-pad/)
- [Snaptron P-series round-dome reference](https://www.snaptron.com/products/standard-domes/p-series/) (shape/family reference only; P15150's 150 gf force is outside the selected 160–250 gf range and is not claimed as the selected part)

## Source model identity

- Preserved authority: `remote-hardware/Remote Assembly/Remote Assembly - Dome D=4mm.step`
- SHA-256: `8455ad77bffaba4f29854352ac8e29a3eaeda769c6d18261a13f37397d3ad82c`
- Library copy: `Switch_KSL/Switch_KSL.3dshapes/SW-DOME_ROUND_D4.0_CENTER-RING_PROVISIONAL.step`
- Copy policy: byte-for-byte; no tessellation, scaling, healing, fusing, or color rewriting
- CAD-kernel result: one solid, seven faces, 0.6320494 mm³; tight shape bounds X/Y ±2.0528567 mm, Z 0.0000–0.2000 mm
- KiCad transform: offset `(0, 0, 0)`, scale `(1, 1, 1)`, rotation `(0, 0, 0)`

## Numbered contact mapping

- Pad 1: exposed outer annulus, 2.71 mm inside / 4.76 mm outside diameter. The project connects this pad to GND so the dome shell is grounded while open.
- Pad 2: 1.70 mm center disk, the switched signal.
- Both pads are copper plus solder-mask opening. There is no paste layer; the dome is retained mechanically rather than soldered by stencil paste.
- A filled 4.76 mm mask opening clears the entire contact region, matching Snaptron's instruction to keep the circuit area beneath the dome free of solder mask.
- The footprint is excluded from pick-and-place output because the dome/tape assembly process must be qualified separately.

## Known boundary

The exact purchasing MPN, plating compatibility, adhesive/tape array, rated life, force tolerance, bounce, and environmental qualification are pending. Do not substitute a nominally similar P15150 or infer an exact MPN from this footprint name. The model and assembly positions are authoritative for enclosure fit; the copper pattern is documented provisional engineering guidance.
