CRCW060356R0FKEAHP (C2078109) -> Resistor_KSL

56 ohm,1%,0603,Vishay CRCW-HP e3.P70=0.33 W;155C film limit and ambient derating remain applicable. Official public English Vishay document20043 revision17-Mar-2026 is local. JLC/LCSC1730 units on2026-10-17; not reserved.

JLC2KiCadLib download succeeded. Reused the verified68-ohm member's identical passive1/2 symbol geometry, canonical recommended footprint and simplified0603 model. No pad, courtyard, model or pin-number change. Canonical default uses0.75x1mm lands; the consuming flex retains its reviewed DenseFlex0.60x0.80mm assembly override, which needs assembler acceptance. Images of the unchanged geometry are copied from the68-ohm report; the symbol render is new.

Selection: at5.25V, two assumed1.2V LEDs and1% low ballast, no bus drop, peak51.41mA;1.2V is a sensitivity, not a guaranteed Vf minimum. The47-ohm candidate exceeds60mA in that same sensitivity. No heat-budget limit is imposed.

Verification2026-10-17: native symbol SVG parsed and visually inspected; unchanged footprint/model top+front images inspected. Complete consuming schematic ERC0 after101 ballasts changed, with unchanged physical geometry/pins/nets asserted by apply_56ohm_ballast.py. NDA all-scope PASS. Global datasheet check still has unrelated pre-existing findings; no56-ohm finding. Global model gate has4 unrelated downloaded-fixture findings (logs attached); no new56-ohm geometry exists because the canonical same-family footprint/model is reused. Simplified model dimensions remain documented above.
