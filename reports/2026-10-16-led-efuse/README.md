# TPS259470LRPWR — 2026-10-16

Imported symbol/model from JLC C3662793; verified exact variant against TI SLVSFC9C Rev C, Table5-1 and RPW0010A land pattern (PDFpage73). Manufacturer public PDF retained in datasheets/TPS259470LRPWR.pdf.

Canonical symbol Power_Management_IC_KSL:TPS259470LRPWR; footprint VQFN-HR-10_RPW0010A_2x2mm. Pin1 EN/UVLO input;2 OVLO input;3 AUXOFF open drain;4 active-low FLT open drain;5 IN;6 OUT;7 dVdt;8 GND;9 ILM;10 ITIMER. Variant is active current limiting with latch-off thermal response, not circuit-breaker variant.

Corrected imported generic pin names/types. Downloaded footprint's corner-pad dimensions differed from TI: rebuilt exact TI compound lands using overlapping same-number rectangles. Center power lands0.3×2.4mm at x±0.25; side lands0.6×0.25 at x±0.9,y±0.225; corner horizontal0.6×0.3 plus vertical0.25×0.65, with actual touching copper. Distinct nets for every numbered pad in fixture; CLI DRC reports0violations and0unconnected items. This includes no padstack-invalid or shorting findings. Top/iso rendered and inspected: pin1/lead alignment correct. STEP retained from JLC, no manufacturer-model fidelity claim.

845Ω gives3334/845=3.947A nominal, with IC±10% and1% resistor approximately3.52–4.39A; do not label4A as a hard maximum. EN1.8V exceeds1.223V maximum rising threshold. Thermal latch recovery requires power cycle or disable/re-enable. Thermal copper and fault/OVLO timing require board qualification; this import does not certify4A layout dissipation.

Source: https://www.ti.com/lit/ds/symlink/tps25947.pdf
