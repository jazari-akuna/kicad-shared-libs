# R134: change49.9Ω to220Ω

Uniroyal0402WGF2200TCE (C25091),220Ω±1%,0402,62.5mW at70°C,50V. Exact JLC identity/stock and downloaded CAD checked; reused verified English Uniroyal thick-film series datasheet (Feb12,2019V3). JLC snapshot1,280,042 units on2026-10-17; stock is not reserved. Existing0402 footprint and generic nominal resistor model unchanged. Visual fixture in ../2026-10-17-c1004-22n shows resistor at right, capacitor at left; top/front/isometric alignment and seating inspected.

With5.25V and−1%R, ideal initial capacitive step≤24.105mA; at5.5V≤25.253mA. Driver output resistance only lowers this bound. SN74LXC1T45 has±50mA continuous absolute output current and32mA recommended at4.5V; lower local supplies are checked against the conservative supply-table category by the final power model. No undocumented pulse-current allowance is used.

Nominal10k pulldown gives DC gate factor10000/10220=0.97847. MOSFET typicalQg8.9nC/Qgd4.4nC are measured at4.5Vgate/10Vdrain/6.3A, not guaranteed switching charge at this board's load. A1.5V assumed Miller plateau and ideal4.8V drive give approximately0.293µs rise plus0.645µs fall of the Miller interval through220Ω. Illustrative switching loss at5V,2A,20kHz≈0.094W; gate-drive energy≈0.85mW. This is separate from DC conduction, not a PWM-frequency qualification. Measure actual edges/temperature for the chosen PWM frequency.

Peak resistor voltage5.5V is below the family's short-time overload level2.5sqrt(P×R)≈9.27V (5s test); gate pulses have much lower energy. Repetitive operation still needs actual duty/frequency verification. No footprint/model waiver added.
