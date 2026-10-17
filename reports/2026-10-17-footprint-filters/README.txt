Footprint-filter metadata correction — 2026-10-17

14 existing resistor/capacitor symbols had vendor-name filters that rejected their own renamed canonical footprints. Existing patterns were retained and the exact default footprint name appended. No pin, graphic, footprint assignment, datasheet, model or electrical field changed. Each part folder contains a report and identical before/after native-render PNGs.

Project aliases Device:C → Strip:C0201 and Connector:TestPoint → Strip:FeedPad_1p2x0p8, plus placed DenseFlex overrides, are handled by project-local synchronized symbol masters; installed generic libraries are unchanged.

Native project ERC and schematic-to-PCB parity pass after the project transform. NDA all-scope gate passes. Repository-wide datasheet gate reports57 unrelated unresolved coverage findings; model gate reports4 unrelated imported-report findings, with0newseating failures. These broader library findings were not suppressed or changed.
