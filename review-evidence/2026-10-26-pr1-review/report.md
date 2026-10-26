# PR #1 review and fixes: Aarav's Audio Board parts and the Harting connector

2026-10-26. Reviewed against each part's datasheet with the `kicad-parts` and
`eda-part-building` skills, then fixed on the PR branch before merging.

## What was wrong, and what changed

No symbol had a wrong pin number, name or electrical function. The defects were in land
patterns, paste, courtyards, duplicate symbols and library hygiene.

| Part | Problem | Fix |
|------|---------|-----|
| TPS25730DREFR | Thermal pads 39/40 printed 100 % paste; TI's stencil (SLVSGP9 p.66) asks for 78 % / 80 % in split windows. Pins 20–25 25 µm too far out. | TI's windows and HotRod E/U apertures; measured 77.3 % / 80.8 %. Pins at ±0.2/0.65/1.1. Symbol renamed from `_Functional`. `tps25730d-paste.png` |
| SWPA4020S3R3MT | Borrowed another series' footprint: 1.9×3.7 pads at ±1.8 (5.5 mm span). | New `IND-SMD_L4.0-W4.0_SWPA4020S`: 1.1×3.7 at ±1.5 per Sunlord (a 1.9, b 1.1, c 3.7). `swpa4020s-footprint.png` |
| TPS62933FDRLR | SOT-583 pads 0.28×0.68 at ±0.64. | 0.30×0.67 at ±0.74 per TI DRL0008A p.49. `tps62933-top.png` |
| TLV3502AIDCNR | Filed in Interface_KSL; no description; pads narrower than TI; model floated 0.05 mm. | Moved to Amplifier_Comparator_KSL; pads 1.1×0.45 at 2.6 mm span; model seated. **Provisional:** the datasheet has no DCN land pattern, so the pads use TI's DBV length/span. `tlv3502-front.png` |
| USB4120-03-C | `USB4120-03-C_Verified`: no courtyard, a round hole where GCT has a slot, signal pads at ±0.80, wrong voltage (48 V). | `TYPE-C-SMD_USB4120-03-C_GCT` from GCT's drawing: Ø0.52 hole + 0.72×0.52 slot, pads at ±0.865, courtyard, shell pads `0` with one SHELL pin; 20 V. main's `TYPE-C-SMD_USB4120-03-C` belongs to a different 10 mm part and is unchanged. `usb4120-gct-footprint.png` |
| AFC01-S05FCA-00 | Mounting pads rotated (1.6 wide × 2.0 tall); courtyard short of the body. | 2.00 × 1.60 per the drawing; courtyard covers body and lock. `afc01-top.png` |
| XT30PW-M30.G.Y | Courtyard 1.6 mm short on the mating side; pegs Ø1.1 vs drawing Ø1.0. | Courtyard to +8.4; pegs Ø1.0. Polarity left unmarked: Amass's drawing does not say which contact is +. `xt30-footprint.png` |
| ESP32-S3-WROOM-1U-N16R2 | Courtyard missed the module end by 0.08 mm; bottom pad row 0.03 mm off; Chinese properties. | Courtyard and silk enclose 18×19.2 mm; pads at 8.865 per p.46; properties in English. `esp32-s3-wroom-1u-footprint.png` |
| U263-241N-4BQC02 | Courtyard ±4.35 inside a ±4.47 body. | ±4.8. |
| VQFN-HR-10_RPW0010A_2x2mm (main) | Model leads 0.05 mm into the board. | Z +0.05, ported from the PR's duplicate. `tps25947-2x2-front-before.png`, `-after.png` |
| Harting 09231486921 | No pin-1 mark. | A1 triangle on silk and fab. |
| TAS2781RYYR | PVDDL typed passive. | power_in. |
| TPD6S300ARUKR | Pin names were one board's net names ("C_SBU1 / DP"). | Datasheet names (C_SBU1, SBU1, NC…); silk body corners. |
| PM254-2-10-W-8_5, HC-JN254-2-03-W | Pins unspecified (ERC noise). | passive. |
| B3U-1000P | Reference and Value text overlapped. | Moved apart. |
| 3 capacitors | Reference `C`. | `C?`. |

### Removed duplicates

These had the same pins and footprint as a symbol already in the library:
`TAS2781RYYR_Functional`, `TPS62933FDRLR_Functional`, `TLV62569DBVR_Functional`,
`TPS7A2018DQNR_Functional` (also stated the wrong dropout), `TPS259470LRPWR_Functional`
with its footprint and a byte-identical STEP.

### Library hygiene

- 15 footprints stored on a single line were re-saved by KiCad (identical content).
- The converter's filled comment-layer glyphs, which covered the pads, were removed from
  the 27 added footprints (`decluttered-c0603-r0402-tps25730d.png`).
- Two unused STEP files were removed (`C1206.step`, `C2220_PSA.step`).
- Board-specific text was removed from descriptions.
- Datasheet verdicts for 09231486921 and SM02B-ULHK-1TA1-ETB(HF) were added to
  `../2026-10-22-aarav-local-parts/datasheet-verdicts.json`.

## If your project uses the old names

| Old | Use instead |
|-----|-------------|
| `Audio_KSL:TAS2781RYYR_Functional` | `Audio_KSL:TAS2781RYYR` |
| `Power_Management_IC_KSL:TPS25730DREFR_Functional` | `Power_Management_IC_KSL:TPS25730DREFR` |
| `Power_Management_IC_KSL:TPS259470LRPWR_Functional` | `Power_Management_IC_KSL:TPS259470LRPWR` |
| footprint `VQFN-HR-10_RPW0010A_TPS25947` | `Power_Management_IC_KSL:VQFN-HR-10_RPW0010A_2x2mm` |
| `DC-DC_converter_KSL:TPS62933FDRLR_Functional` | `DC-DC_converter_KSL:TPS62933FDRLR` |
| `DC-DC_converter_KSL:TLV62569DBVR_Functional` | `Interface_KSL:TLV62569DBVR` (or the copies in DC-DC_converter_KSL / Video_Interface_KSL) |
| `LDO_KSL:TPS7A2018DQNR_Functional` | `LDO_KSL:TPS7A2018DQNR` |
| `Interface_KSL:TLV3502AIDCNR` | `Amplifier_Comparator_KSL:TLV3502AIDCNR` |
| footprint `Connector_KSL:USB4120-03-C_Verified` | `Connector_KSL:TYPE-C-SMD_USB4120-03-C_GCT` (shell pins are now one pin `0`) |
| footprint `Inductor_KSL:IND-SMD_L4.0-W4.0_SLW4010S` | `Inductor_KSL:IND-SMD_L4.0-W4.0_SWPA4020S` |

The `_Functional` symbols placed pins differently from the base symbols, so
"Change Symbol" moves pin ends: re-check the wires on those sheets afterwards. Footprints
whose pads moved (TPS25730D pins 20–25, SWPA4020, TPS62933, TLV3502, AFC01, USB4120, ESP32
bottom row) need "Update Footprints from Library" and a re-route of the affected pads.

## Checks (on the merged result)

- Every new symbol's pins match its footprint's pads; every library loads in kicad-cli
  (Screen_KSL fails identically on main: its symbol file is named differently).
- `datasheets.py verify`: 55 problems, the same 55 as main; none from this PR.
- `check_models.py`: one finding beyond main, the Harting housing overhanging the board
  edge (by design; the checker does not model board edges). Not baselined.
- `check_nda.py --scope all`: clean; `--self-test` passes.

## Still open

- TLV3502 pads are derived (no DCN land pattern published in the datasheet); its model is
  1.05 mm tall against a 1.45 mm maximum package.
- TAS2781 and REF0038A (TPS25730D) 3D models are generic/nominal; the REF0038A model still
  shows pins 20–25 25 µm outboard of the corrected pads.
- XT30 polarity is not marked; the XT30 STEP has the 2 mm-tail variant's tails.
- Harting land pattern is cross-checked against KiCad's DIN 41612 footprint, not Harting's
  part drawing; dry-fit before ordering boards.
- main's `TYPE-C-SMD_USB4120-03-C` (used by `TYPE-C_16PLT-H10_0`) has its model buried
  under the board and borrows the 6.5 mm USB4120 model for a 10 mm part.
