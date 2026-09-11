# TPS22916BYFPT qualification report

## Library identity

- Symbol: `Power_Management_IC_KSL:TPS22916BYFPT`
- Footprint: `Power_Management_IC_KSL:DSBGA-4_L0.78-W0.78-R2-C2-P0.40-YFP`
- Model: `${KSL_ROOT}/Power_Management_IC_KSL/Power_Management_IC_KSL.3dshapes/DSBGA-4_L0.78-W0.78-R2-C2-P0.40-YFP.step`
- Datasheet: `${KSL_ROOT}/datasheets/TPS22916BYFPT.pdf`
- Qualified part commit: `36348b4`

## Source-backed pin and package definition

TI TPS22916 Rev F defines A1 VOUT, A2 VIN, B1 GND, and B2 ON. The footprint
follows TI's YFP0004 land pattern with 0.23 mm diameter pads on 0.40 mm pitch.

TI publishes the YFP0004 BXL package data but no STEP model. The linked model
is the exact LCSC/JLC/EasyEDA C2680360 model. Its Z offset and Z rotation were
corrected against the authoritative TI footprint and verified in top, front,
and isometric renders.

- Datasheet: <https://www.ti.com/lit/ds/symlink/tps22916.pdf>

## Electrical reuse and availability

TI specifies VIH at 1.0 V minimum and VIL at 0.35 V maximum across VIN from
1 V to 5.5 V, so a direct 1.8 V nRF high level is valid. The B variant is
active-high with fast turn-on. Its smart ON pulldown is 750 kohm typical while
ON is low and disconnects when ON is high, where ON current is at most 10 nA.
A permanent 100 kohm external pulldown would draw 18 uA while driven high at
1.8 V.

The 2 A-rated switch is suitable for both the small 1V8_SENS branch and the
3V3_FP+LED branch at no more than 400 mA. At VIN 3.6 V, RON is 70 mohm typical
and 120 mohm maximum across -40 C to 85 C, corresponding to about 28/48 mV
drop and 11.2/19.2 mW loss at 400 mA. The part has no current limit, so output
capacitance and inrush require system-level review.

On 2026-09-11, the live LCSC record for C2680360 showed 3 units and a
quantity-one price of USD 1.5159. Recent distributor results also showed 11,990
at DigiKey and 347 at Mouser, both at USD 1.21 each.

## Verification

KiCad symbol and footprint exports passed. Exact symbol-pin to footprint-pad
identity passed for `A1`, `A2`, `B1`, and `B2`. The symbol and land pattern were
visually reviewed against the TI source, and the adjusted exact-SKU model was
verified in three views. The shared model-placement check reported no new
violations, the NDA gate passed, and the local datasheet was verified as the
English primary source.
