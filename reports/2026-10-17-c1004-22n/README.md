# C1004: change 1µF to22nF

FH0402B223K500NT (C1532),22nF50V X7R±10%, verified against the exact manufacturer product page and public FH family catalog. JLC snapshot:704,709 units on2026-10-17; stock is not reserved. Original downloaded symbol/footprint are retained as `.txt` records. Canonical symbol reuses the checked nonpolar two-pin geometry; the existing0402 footprint/model are unchanged.

The local PDF starts with a clearly labelled English engineering reference, followed by the original bilingual catalog; it is not represented as a manufacturer-issued English translation. Model is a nominal0402 MLCC envelope. Top/front/isometric views inspected: left capacitor seated over both pads, right resistor provided for scale. No source geometry was altered.

Receiver model:38kHz transimpedance3.170MΩ at100pF total sense capacitance (+13.5% versus1µF reference capacitor), phase−39.96°. At22nF±10% plus±15% temperature sensitivity:3.081..3.311MΩ at38kHz. Reference-divider output noise20–60kHz≈5.14µVrms nominal; this excludes opamp/photodiode noise. Shutdown simplified clamp model requires≥0.301µF effective AVCC capacitance under5.25V supply, capacitor/resistor tolerances,0.3V assumed clamp and10mA discharge reserve. Actual capacitor bias behavior and power waveform need prototype verification; no guaranteed DC-bias minimum was invented.

No added footprint/model waiver. See integration proof in the consuming LED project for unchanged physical records and all2562 pin/net pairs.
