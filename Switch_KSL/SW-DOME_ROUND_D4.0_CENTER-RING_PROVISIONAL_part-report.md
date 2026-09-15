# SW-DOME_ROUND_D4.0_CENTER-RING_PROVISIONAL

## Status and scope

This is a **provisional, source-matched mechanical dome contact**, not a qualified purchasing MPN. The user-selected target is a 4 mm round dome with a center feature, a force marking of 160–250 whose unit is not visible in the source image, and 0.16–0.20 mm travel. The source selection image also shows three-leg and cross PCB diagrams; those were not used because they are not confirmed as the selected round contact geometry.

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

- Pad 1: exposed outer annulus, 2.71 mm inside / 4.76 mm outside diameter. The custom-pad anchor is at X=+1.8675 mm on the copper annulus, while its circular primitive remains centered on the footprint origin. This keeps the required center clearance without creating a disconnected copper anchor island. The project connects this pad to GND so the dome shell is grounded while open.
- Pad 2: 1.70 mm center disk, the switched signal.
- Both pads are copper plus solder-mask opening. There is no paste layer; the dome is retained mechanically rather than soldered by stencil paste.
- A filled 4.76 mm mask opening clears the entire contact region, matching Snaptron's instruction to keep the circuit area beneath the dome free of solder mask.
- The shared mask opening intentionally bridges the mask definitions of pads 1 and 2; the copper remains separated by a 0.505 mm radial gap. A two-net KiCad DRC fixture is required because a render alone does not prove custom-pad anchor connectivity or absence of shorts.
- The footprint is excluded from pick-and-place output because the dome/tape assembly process must be qualified separately.

## Known boundary

The exact purchasing MPN, plating compatibility, adhesive/tape array, rated life, force tolerance, bounce, and environmental qualification are pending. Do not substitute a nominally similar P15150 or infer an exact MPN from this footprint name. The model and assembly positions are authoritative for enclosure fit; the copper pattern is documented provisional engineering guidance.

## Electrical geometry verification

KiCad 10.0.2 loaded the corrected footprint with two pads. A minimal board assigned pad 1 to `GND` and pad 2 to `KEY` and ran `kicad-cli pcb drc --format json`. It reported zero `shorting_items`, zero `padstack_invalid`, and zero unconnected items. The raw run reports one `solder_mask_bridge` because the manufacturer-guided contact intentionally removes mask across the whole dome region; this is an intentional mask construction, not a copper bridge. The fixture and JSON report are preserved under `remote-hardware/review-evidence/grouped-placement-2026-09-15/domes/`.
