# TPS22919DCKR HOST_1V8 gate — 2026-10-16

Canonical Power_Management_IC_KSL:TPS22919DCKR, JLC C2149796. Exact TI SLVSEN5B pin table:1 IN,2 GND,3 active-high ON,4 NC,5 QOD,6 VOUT. Local public English datasheet retained. Corrected symbol electrical types and local datasheet/footprint properties.

Reused existing Power_Management_IC_KSL:SOT-363_L2.0-W1.3-P0.65-LS2.1-BR,0.65mm pitch,0.9×0.4mm lands. JLC downloaded alternative had two duplicate STEP entries with conflicting rotations; neither imported. Existing single-model footprint was rendered top/isometric and visually checked: all6leads align and seat, pin1 matches lower-right mark. Exported symbol parses. Model is existing package representation, not claimed exact manufacturer CAD.

Source: https://www.ti.com/lit/ds/symlink/tps22919.pdf
Application: P1V8 input; ON tied to controlled enable with default pulldown; QOD tied directly OUT;47Ω series to external HOST_1V8. The device is not reverse-current blocking; externally powering HOST_1V8 is not permitted. QOD under unpowered/brownout conditions is not guaranteed by this review. Physical fault/rail sequencing remains untested.
