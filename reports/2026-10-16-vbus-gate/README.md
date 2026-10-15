# VBUS sense gate parts — 2026-10-16

Imported JLC C46506 TPS2552DBVR (normal current limiting, not the -1 variant) and C81464 MMBT3904LT1G using JLC2KiCadLib. Manufacturer English datasheets are retained under datasheets/. Symbols use local KSL_ROOT references.

TPS2552 pin table verified: 1 IN,2 GND,3 active-low EN,4 open-drain FAULT,5 ILIM,6 OUT. Reused existing TI DBV SOT23-6 footprint. MMBT3904:1 base,2 emitter,3 collector; imported SOT23-3 footprint/model.

Corrected electrical pin types and local paths. Corrected imported legacy User.Comments layer to Cmts.User: the former normalized to invalid Rescue and made the CLI reject the fixture. This was a real footprint-import defect, not a waived render failure. After correction both symbol exports and fixture render pass. parts.png visually checked: pads/leads aligned, pin1 indicators and seating correct. No mechanical mating qualification applies to these ICs.

TI TPS2552 family datasheet: https://www.ti.com/lit/ds/symlink/tps2553.pdf
ON MMBT3904: https://www.onsemi.com/pdf/datasheet/mmbt3904lt1-d.pdf

Application boundary:210kΩ ILIM corresponds110/130/150mA(min/typ/max), not100mA ceiling. This switch does not provide20V protection. Hardware startup/detach performance remains untested.
