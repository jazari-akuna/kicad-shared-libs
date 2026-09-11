# VCNL36828P qualification report

## Library identity

- Symbol: `Sensor_KSL:VCNL36828P`
- Footprint: `Sensor_KSL:SENSOR-SMD_VCNL36828P_L2.0-W1.0-P0.725`
- Model: `${KSL_ROOT}/Sensor_KSL/Sensor_KSL.3dshapes/SENSOR-SMD_VCNL36828P_L2.0-W1.0-P0.725.step`
- Datasheet: `${KSL_ROOT}/datasheets/VCNL36828P.pdf`
- Qualified part commit: `36348b4`

## Source-backed pin and package definition

Vishay VCNL36828P Rev 1.6 defines pin 1 INT (open-drain), 2 VDD, 3 GND,
4 VCSELA, 5 SCL, and 6 SDA. Vishay permits SCL and SDA to be swapped to select
the alternate I2C slave address; the symbol uses the normal mapping. VCSELA is
the emitter supply and remains distinct from VDD.

The footprint follows Vishay's recommended pattern: 0.35 mm by 0.50 mm pads,
0.600 mm column span, and 0.725 mm row pitch for the 2.0 mm by 1.0 mm body.

- Datasheet: <https://www.vishay.com/docs/80306/vcnl36828p.pdf>
- Official Vishay model archive: <https://www.vishay.com/docs/80424/vcnl36828p_3d_models.zip>

## Availability and verification

On 2026-09-11, the live LCSC record for C19183990 showed 89 units and a
quantity-one price of USD 2.2796.

KiCad symbol and footprint exports passed. Exact symbol-pin to footprint-pad
identity passed for pins `1` through `6`. The symbol and land pattern were
visually reviewed against the Vishay source. Top, front, and isometric renders
confirmed that the official Vishay model is centered, seated, and oriented to
pin 1. The shared model-placement check reported no new violations, the NDA
gate passed, and the local datasheet was verified as the English primary source.
