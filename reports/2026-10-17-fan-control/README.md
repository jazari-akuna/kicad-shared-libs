# Fan control logic — 2026-10-17

Imported exact TI SN74LVC1G14DRLR (C2877550) and TXU0101DCKR (C5217868) with JLC2KiCadLib. The source files are retained in `imported/`; `import_parts.py` repeats the corrections against a library revision without these two symbols. No new library/global table was introduced.

Manufacturer sources: TI SN74LVC1G14 Rev AB (`https://www.ti.com/lit/ds/symlink/sn74lvc1g14.pdf`, local family PDF retained under exact MPN) and TXU0101 SCES940A (`https://www.ti.com/lit/ds/symlink/txu0101.pdf`). DRL0005A land example: pads0.67×0.30mm at x±0.74mm, y−0.5/0/+0.5mm. DCK0006A land example, rotated90°counterclockwise: pads0.40×0.90mm, x−0.65/0/+0.65mm, y±1.10mm. Pin-one numbering follows top-view land patterns. Pins were corrected from unspecified to NC/input/output/power_in; TXU's unrelated downloaded datasheet URL was replaced with the correct local TI PDF. Added courtyards and legible fab text. Legacy User.Comments changed to canonical Cmts.User to prevent Rescue-layer load failure.

The downloaded STEP models are preserved. Native model offsets use millimetres: TXU0101(0,0,+0.5) seats its source z−0.5mm terminals at the PCB; inverter(0,0,0). Do not use legacy `(at (xyz ...))`, which interprets inches. OCP verified both STEP files are nonempty; `model-check.json` records raw bounds before footprint transforms. Inverter model height0.611mm is a conservative supplier approximation to the0.6mm maximum package; no precision mechanical model claim.

LCSC catalog observations2026-10-17: TI inverter C2877550 listed565pieces, referenceprice$0.0867; TXU0101DCKR C5217868 productpage listed8650pieces,$0.6372@1/$0.3482@1000 (imagepage7815pieces). Indexed figures differ and are sourcing evidence, not reserved stock. Exact TI parts were selected; similarly named TECH PUBLIC substitutes were not accepted.

Circuit integration and independent critique are in carrier-pcb `design/reviews/fan-control-20261017/`. These parts implement an explicit PWM hardware inverter and a separate Schmitt tach translator. No hardware or assembly qualification is implied.
