CRCW060368R0FKEAHP (C242566) -> Resistor_KSL

Source: public Vishay CRCW-HP e3 document20043, revision17-Mar-2026, pp1/3/6/9. Local English datasheet ${KSL_ROOT}/datasheets/CRCW060368R0FKEAHP.pdf. Exact68ohm1%100ppm/K EA tape variant verified from ordering table. JLC live API:1992 stock, SMT extended, checked2026-10-16;101 perstrip plus8assembly allowance (not reserved).

Library search found no exact part; JLC2KiCadLib import succeeded. Its downloaded datasheet pointed to unrelated Yageo RT, so replaced with official Vishay PDF. Retained established passive resistor symbol drafting/pins1/2. Corrected canonical footprint to recommended reflow0.75x1.00 pads at+/-0.75mm, gap0.75, outer2.25; body1.60x0.85mm. Removed imported custom-paste pattern in favor of standard pad apertures.

Canonical footprint uses existing simplified0603 model:0.80mm model width versus0.85mm nominal Vishay body, model height0.45mm; not exact vendor CAD. Model transforms unchanged and seating inspected.

This flex has an explicit placed-footprint override retaining0.60x0.80mm pads/gap0.90mm and its currentmodel. Pads/routes/placement were not changed. Dense lands require JLC assembly and assembled-flex thermal qualification; not manufacturer recommended. Worst body1.70x0.95x0.55mm leaves0.85mm minimum rear-array body clearance.

P70=0.33W, ambient linear derating to155C gives0.213529W at100C, compared with0.0976W calculatedworstload. Rating applies only if assembled film stays<=155C. The different0.75W rating assumes105C terminal temperature and is not used here.

Checks: native canonical two-net fixture DRC0violations/0opens; numbered pads match passive pins1/2; native symbol/footprint SVG and top/front3D inspected. Full-library transform gate reports one pre-existing missing STEP in reports/0603WAF820JT5E/downloaded-footprint, not this footprint. Datasheet full-library gate has pre-existing source/language findings; this exact public English PDF was manually checked. NDA all-scope gate passes. Full seating gate passes with0new violations (17pre-existing baselined); exact new footprint/model bounds recorded in model-native-bounds.json.
