# Cube Audio Board parts into KSL — 2026-11-13

Follows `skills/kicad-parts/SKILL.md`. The Audio Board (Blackstar-Cube `Audio_Board/`) was checked part by part
against KSL (every placed symbol and footprint). Step 0 (search KSL, KNL, `_attic`, git history by stem) split
the parts as follows:

- **Already in KSL, nothing added:** everything else on the board.
  - The `_Functional` redraws (TAS2781RYYR, TLV62569DBVR, TPS7A2018DQNR) stay project-local, per the
    2026-10-31 decision.
  - TLV3502AIDCNR is in `Amplifier_Comparator_KSL`. The board still points at `Interface_KSL`; the board needs a
    repoint, not a library change.
- **Added here:** the eight parts in the table below.
- **TPS7A2033PDBVR:** the board places it on stock `Package_TO_SOT_SMD:SOT-23-5`. KSL's default is already the
  KSL SOT-23-5 DBV, so the board should repoint.

## Added

| Part | Library | Footprint | LCSC | Datasheet | Basis / notes |
|---|---|---|---|---|---|
| TPS552872RYQR (TI 36 V 4 A buck-boost, VQFN-HR-21) | DC-DC_converter_KSL | **VQFN-HR-21_L5.0-W3.0-P0.50_RYQ0021A** (new) | C22427496 | local, English (TI SLVSHG1) | Lands per TI example board layout 4226658/A (SLVSHG1 p.38), with pin 9 widened to 0.33 and the 2× 0.54 bar offset around it. Paste per the example stencil (p.39): bar pins 7–11 as 3 × 1.0 mm unnamed paste-only windows. 21 symbol pins checked name-for-name against Table 5-1 |
| PA35V1000M10X15 (JIERR 1000 µF 35 V polymer, radial D10 × L15) | Capacitor_KSL | **CP_Radial_D10.0mm_P5.00mm_SMD-FormedLead** (new) | C46550434 | local, **bilingual** (see open items) | p.7 table: 16 mΩ, 4100 mA ripple, 10X15. The cap is mounted upright with its leads formed into SMD feet on 2.5 × 1.3 pads, with no holes. The model is the nominal part, D10.0 × L15.0 (code 10X15, p.2 table), on a 1.0 mm assumed forming standoff; the courtyard keeps the max D10.5 × L16.0. LCSC's own model was not used: it is a generic D10 can about 12 mm tall with straight through-hole leads |
| AFC01-S10FCA-00 (JUSHUO 10P 0.5 mm FPC, flip-lock, bottom contact) | Connector_KSL | **FPC-SMD_AFC01-S10FCA-00** (new) | C262659 | local, English (family spec, sha256 = the accepted S05 copy) | Signal 0.30 × 1.30 at 0.50; nails 2.00 × 1.60 at ±3.95. This follows the family rule A/2 + 1.70 that also gives the verified S05 (±2.70). 10P row: A 4.50 / B 5.60 / C 9.40 |
| **FPC-05F-14PH20** (XUNPU 14P 0.5 mm FPC, flip-lock, bottom contact, H2.0) | Connector_KSL | **FPC-SMD_14P-P0.50_FPC-05F-14PH20** (new) | C2856800 | local, **bilingual** (see open items) | Built from the verified 12P footprint: outline +0.5 per side, 14 signal pads at exact 0.50 pitch, shells 15/16 at ±4.94. Cross-checked against the LCSC/EasyEDA 14P CAD (pads agree to 0.3 µm) and the maker drawing p.1 (0.30 × 1.25 at 0.50, nails 2.00 × 2.50, 2.69 nail edge → pin 1, 0.70 gap). STEP is the LCSC model, with the same origin convention as the 12P (offset y +1.2) |
| 0402WGF3162TCE (UNI-ROYAL 31.6 kΩ 1 % 0402) | Resistor_KSL | R0402 | C11463 | local, English (family) | |
| 0402WGF4992TCE (UNI-ROYAL 49.9 kΩ 1 % 0402) | Resistor_KSL | R0402 | C25897 | local, English (family) | |
| BW0041BG-L2.5W1.0H1.5 (BAT Wireless spring contact) | Connector_KSL | **ANT-SMD_L2.5-W1.0_BW0041BG-L2.5W1.0H1.5** (new) | C2826541 | local; unofficial English companion page + original (skill item 6) | Land 2.10 × 1.00 per drawing 681-0041B-2 rev A; the body overhangs 0.40 at the curl end |

![](sym_FPC-05F-14PH20.png) ![](fp_FPC-SMD_14P-P0.50_FPC-05F-14PH20.png) ![](3d_top_FPC-SMD_14P-P0.50_FPC-05F-14PH20.png) ![](3d_iso_FPC-SMD_14P-P0.50_FPC-05F-14PH20.png)
![](datasheet_FPC-05F-14PH20_p1.png)

![](sym_TPS552872RYQR.png) ![](fp_VQFN-HR-21_L5.0-W3.0-P0.50_RYQ0021A.png) ![](3d_iso_VQFN-HR-21_L5.0-W3.0-P0.50_RYQ0021A.png) ![](3d_front_VQFN-HR-21_L5.0-W3.0-P0.50_RYQ0021A.png)

![](sym_PA35V1000M10X15.png) ![](fp_CP_Radial_D10.0mm_P5.00mm_SMD-FormedLead.png) ![](3d_iso_CP_Radial_D10.0mm_P5.00mm_SMD-FormedLead.png) ![](3d_front_CP_Radial_D10.0mm_P5.00mm_SMD-FormedLead.png)

![](sym_AFC01-S10FCA-00.png) ![](fp_FPC-SMD_AFC01-S10FCA-00.png) ![](3d_iso_FPC-SMD_AFC01-S10FCA-00.png)

![](sym_BW0041BG-L2.5W1.0H1.5.png) ![](fp_ANT-SMD_L2.5-W1.0_BW0041BG-L2.5W1.0H1.5.png) ![](3d_front_ANT-SMD_L2.5-W1.0_BW0041BG-L2.5W1.0H1.5.png)

## Modifications (flagged)

- **FPC-SMD_14P-P0.50_FPC-05F-14PH20:** the courtyard was taken from the LCSC CAD, which stopped at y +3.14. That is
  short of the body and actuator, so it now runs to y +4.45.
- **CP_Radial_D10.0mm_P5.00mm_SMD-FormedLead model:** regenerated at the nominal D10.0 × L15.0. It was previously
  drawn at the max envelope, D10.5 × L16.0.
- **FPC-SMD_8P-P0.50-FH34SRJ:** removed a second pin-1 triangle that sat on silkscreen under the connector body. The
  pin-1 circle outside the body remains. Before/after: the triangle is the only change (3 `fp_line`s).

## Checks

| Check | Result |
|---|---|
| Symbols parse (`kicad-cli sym export svg`) | pass, all 7 symbols |
| Pin ↔ pad parity | pass: 14P 1–16 / 16 pads; TPS552872 1–21; AFC01 1–12; caps and resistors 1–2; spring 1 |
| Pad-net DRC fixture (each numbered pad on its own net) | pass, 0 `padstack_invalid` and 0 `shorting_items` for all new footprints. TPS552872's minimum pad gap is 0.177 mm, at the corners per TI's land pattern ([drc_*.json](.)) |
| `check_models.py` | 224/243 seat cleanly. The 3 new models (TPS552872, PA cap, AFC01-S10) and the 14P are clean. The 8 violations are all pre-existing (Harting 09231486921, Quectel EG800Q, `reports/` imports) and identical with and without this change ([models.txt](models.txt)) |
| `check_nda.py --scope all` | pass: no restricted documents ([nda.txt](nda.txt)) |
| `datasheets.py verify` | The new parts all resolve to local PDFs. **PA35V1000M10X15 and FPC-05F-14PH20 are recorded as reviewed `bilingual`, which the gate does not count as `en`**, the same state as the existing FPC-05F-12PH20 ([ds_verify.txt](ds_verify.txt)) |

## Open items

1. **Bilingual datasheets.** For PA35V1000M10X15 and FPC-05F-14PH20, the ratings tables and dimensions are in English
   alongside Chinese. Under skill item 4 an English-only engineer can use them, but I did not upgrade the recorded
   verdict to `en` just to pass the gate. Reviewer: please confirm `en` (as was done for CA55-H035M686TE070) or ask
   for translations.
2. **PA cap forming:** the 1.0 mm standoff and the 1.5 mm feet are Blackstar's assembly choice, not the maker's.
   Confirm them with the assembler.
3. **Audio Board repoint (done in the Cube repo):** TLV3502AIDCNR now uses `Amplifier_Comparator_KSL`.

## Added later on 2026-11-13: XGL7030-472MEC (Coilcraft 4.7 µH) → Inductor_KSL

- **Why:** replaces FXL0630-4R7-M as the TPS552872 inductor. It has more saturation margin over the chip's 6.5 A (typ) peak
  current limit: 10.6 A vs 7.5 A, both at a 30 % inductance drop. DCR roughly halves, 17.8 vs 33 mΩ max.
- **Source:** Coilcraft Doc 1736-1/-3 (rev 02/19/26), stored as `datasheets/XGL7030-472MEC.pdf`, English. The STEP is
  Coilcraft's own `XGL7030.STEP`, unmodified.
- **Footprint `IND-SMD_L7.5-W7.5_Coilcraft_XGL7030`:**
  - Pads per Coilcraft's recommended land pattern: 1.78 × 6.50 mm at 4.72 mm centre-to-centre.
  - Cross-checked against the STEP: terminals are 1.60 × 6.0 mm centred at ±2.36 mm, with a 3.12 mm gap.
  - Pad 1 is the start (marked) lead. Coilcraft says to put it on the high-dV/dt node; on the Audio Board that is SW1.
- **Model placement:** the STEP is Y-up at the 8.0 × 8.0 mm body maximum, with terminals 0.1 mm below the body. It is
  placed with rotate x = −90 (KiCad sign) and offset z = +0.1. The renders show it seated, with the start-lead bar over pad 1.
- **Checks:**
  - Symbol parses.
  - Pin/pad parity 1–2.
  - Pad-net DRC fixture passes.
  - `check_models` seats it cleanly (225/244; the 8 violations are pre-existing and unchanged).
  - `check_nda` is clean.
  - `datasheets.py verify` is OK for this part.
- **Sourcing:** not stocked at LCSC, so JLC assembly needs global sourcing or consigned parts. The `LCSC` field is left empty.

![](fp_IND-SMD_L7.5-W7.5_Coilcraft_XGL7030.png) ![](3d_iso_IND-SMD_L7.5-W7.5_Coilcraft_XGL7030.png) ![](3d_front_IND-SMD_L7.5-W7.5_Coilcraft_XGL7030.png)
