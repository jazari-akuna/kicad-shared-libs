# KSL cleanup notes

## Protection_KSL TPD4E02B04DQAR — unconnected-pin naming artifacts (benign, fix at leisure)

An older revision of this symbol (TPD4E02B04DQAR, four-channel ESD protection
array, USON-10) named its I/O pins `I/O2`–`I/O4` and mapped them to different
pad numbers — `I/O4` on pad 6, for instance — than the current
`Protection_KSL.kicad_sym` does (`IO2` = pad 2, `IO3` = pad 4, `IO4` = pad 5,
`NC` = 6/7/9/10).

A board netted against the old revision therefore shows netlist-to-PCB parity
deltas of the class `unconnected-(Uxxx-IO…-PadN)`: name mismatches, or NC pads
that the current symbol nets and the board leaves bare. These carry no
electrical content — the nets have no copper on them, each name attaches to
exactly one pad, and every *connected* pad still matches the schematic. Do not
chase them into the boards; fix the symbol here and re-sync.

Cleanup wanted:

1. Decide one canonical pin-name set (suggest the datasheet's `IO1`…`IO4`, with
   no slashes — a slash escapes as `{slash}` in net names and causes churn).
2. Confirm the NC pin/pad set matches the DQA package drawing (pads 6/7/9/10 =
   NC), and give every pad a pin so the symbol and footprint pin counts agree.
3. Re-sync consuming boards in one commit each, so their parity checkers go to
   a true zero.
