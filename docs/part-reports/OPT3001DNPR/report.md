# OPT3001DNPR qualification report

## Library identity

- Symbol: `Sensor_KSL:OPT3001DNPR`
- Footprint: `Sensor_KSL:USON-6_L2.0-W2.0-P0.65-DNP0006A`
- Model: `${KSL_ROOT}/Sensor_KSL/Sensor_KSL.3dshapes/USON-6_L2.0-W2.0-P0.65-DNP0006A.step`
- Datasheet: `${KSL_ROOT}/datasheets/OPT3001DNPR.pdf`
- Qualified part commit: `36348b4`

## Source-backed pin and package definition

TI OPT3001 Rev C defines pin 1 VDD, 2 ADDR, 3 GND, 4 SCL, 5 INT
(open-drain), and 6 SDA. The DNP0006A exposed thermal pad is represented as
`EP`; TI requires it to be soldered and recommends connecting it to electrical
ground.

The footprint follows TI's DNP0006A recommended land pattern: 0.50 mm by
0.25 mm signal pads on 0.65 mm pitch with 1.90 mm row separation, a 0.65 mm by
1.35 mm exposed-pad copper land, and a 0.62 mm by 1.25 mm paste aperture.

- Datasheet: <https://www.ti.com/lit/ds/symlink/opt3001.pdf>
- Official TI DNP0006A STEP: <https://webench.ti.com/cad/dlbxl.cgi/newstep/DNP0006A.stp>

## Availability and verification

On 2026-09-11, the live LCSC record for C90462 showed 2,983 units and a
quantity-one price of USD 1.5673.

KiCad symbol and footprint exports passed. Exact symbol-pin to footprint-pad
identity passed for `1`, `2`, `3`, `4`, `5`, `6`, and `EP`. The symbol and land
pattern were visually reviewed against the TI source. Top, front, and isometric
renders confirmed that the official TI model is centered, seated, and oriented
to pin 1. The shared model-placement check reported no new violations, the NDA
gate passed, and the local datasheet was verified as the English primary source.
