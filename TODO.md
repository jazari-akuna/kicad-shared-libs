# KSL cleanup notes

## Protection_KSL TPD4E02B04DQAR — unconnected-pin naming artifacts (benign, fix at leisure)

Filed 2026-07-21 by the carrier rev-A check loop (a consuming board `design/review/final-check-3`).

The carrier board's 9 embedded TPD4E02B04 (USON-10) footprints were netted from an
older revision of the symbol whose I/O pins were named `I/O2`–`I/O4` and mapped to
different pad numbers (e.g. `I/O4` on pad 6) than the current
`Protection_KSL.kicad_sym` symbol (`IO2` = pad 2, `IO3` = pad 4, `IO4` = pad 5,
`NC` = 6/7/9/10). Result: 47 netlist↔PCB parity deltas on the carrier, ALL of the
class `unconnected-(Uxxx-IO…-PadN)` name mismatches or NC pads that the current
symbol nets but the board leaves bare.

Verified 2026-07-21 (post-placement-pass-4 check loop): every one of the 47 deltas
is on a no-copper net — zero segments/vias/zones reference these nets on the board,
each net name attaches to exactly one pad, and all *connected* pads (real signals +
GND) match the schematic exactly. No electrical content; do NOT chase these into
the boards.

Cleanup wanted here (KSL master):
1. Decide one canonical pin-name set for TPD4E02B04DQAR (suggest datasheet `IO1`…`IO4`,
   no slashes — slashes escape as `{slash}` in net names and cause churn).
2. Confirm the NC pin/pad set matches the DQA package drawing (pads 6/7/9/10 = NC),
   and give every pad a pin so symbol/footprint pin counts agree.
3. After the KSL fix, re-sync the 9 carrier instances (U406, U612/U613, U907–U911,
   U1003) in one commit so the parity checker goes to true 0.
