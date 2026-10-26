#!/usr/bin/env python3
"""Generate JAE WP26DK land patterns (0.35 mm pitch, 0.6 mm stacking, 2 power hold-downs).

Receptacle (WP26DK-S***VA3): JAE drawing SJ121277 rev 6, "Applicable P.C.B dimension (ref.)".
Plug (WP26DK-P***VA3): JAE drawing SJ121275 rev 6, "Applicable P.C.B dimension (ref.)".

Pad numbering is not defined by JAE. It follows the BM28 footprints in this library so a BM28 can be swapped
for a WP26DK without touching the schematic: row +y holds 1..n/2 left to right, row -y holds n/2+1..n right to
left, the left (x<0, pin-1) hold-down is n+1 (+y corner, also the end pad) and n+2 (-y corner), the right
hold-down is n+3 (+y corner, also the end pad) and n+4 (-y corner).
"""
import sys, os

PITCH = 0.35
# Body outline from MB-0356 / SJ121277 / SJ121275: length grows 0.35 mm per contact pair.
SIZES = (10, 16, 24, 30, 34, 40, 48, 50, 60)

RECEPTACLE = dict(
    kind="S", body_w=1.90, height=0.6, body_len=lambda n: 4.30 + (n - 10) / 2 * PITCH,
    sig=(0.17, 0.44), row_y=0.88,                      # 1.32 inner / 2.20 outer contact SMT area
    corner=(0.70, 0.375), corner_dx=0.93, corner_y=(2.20 - 0.375) / 2,
    end=(0.28, 0.60), end_dx=1.47,                      # overall pattern length A + 3.22
    source="JAE SJ121277 rev 6 (2024-03-12), applicable PCB dimension",
)
PLUG = dict(
    kind="P", body_w=1.81, height=0.49, body_len=lambda n: 3.55 + (n - 10) / 2 * PITCH,
    sig=(0.17, 0.54), row_y=0.83,                      # inner edges 1.12 apart, outer 2.20
    corner=(0.28, 0.65), corner_dx=0.42, corner_y=0.575,   # 4 hold-down pads, inner edges 0.5 apart, outer 1.8
    end=None,
    source="JAE SJ121275 rev 6 (2024-03-12), applicable PCB dimension (same pattern as G-Switch GT-B0351MSV05)",
)


def pads(p, n, mirror=False):
    a = (n // 2 - 1) * PITCH
    out = []
    for k in range(n // 2):
        out.append((k + 1, -a / 2 + k * PITCH, p["row_y"], p["sig"]))
        out.append((n // 2 + k + 1, a / 2 - k * PITCH, -p["row_y"], p["sig"]))
    for side, first in ((-1, n + 1), (1, n + 3)):
        cx = side * (a / 2 + p["corner_dx"])
        out.append((first, cx, p["corner_y"], p["corner"]))
        out.append((first + 1, cx, -p["corner_y"], p["corner"]))
        if p.get("end"):
            out.append((first, side * (a / 2 + p["end_dx"]), 0.0, p["end"]))
    if mirror:   # same copper, numbers mirrored left-right (the LINK flex convention)
        out = [(num, -x, y, s) for num, x, y, s in out]
    return out


def footprint(p, n, mirror=False):
    name = f"CONN-SMD_WP26DK-{p['kind']}{n:03d}VA3-R15000" + ("_MIRROR-NUM" if mirror else "")
    part = f"WP26DK-{p['kind']}{n:03d}VA3-R15000"
    side = "Receptacle" if p["kind"] == "S" else "Plug"
    ps = pads(p, n, mirror)
    L = p["body_len"](n); W = p["body_w"]
    xs = [x + s[0] / 2 * sgn for _, x, _, s in ps for sgn in (-1, 1)]
    ys = [y + s[1] / 2 * sgn for _, _, y, s in ps for sgn in (-1, 1)]
    cx = max(L / 2, max(abs(v) for v in xs)) + 0.25
    cy = max(W / 2, max(abs(v) for v in ys)) + 0.25
    f = lambda v: f"{v:.4f}".rstrip("0").rstrip(".")
    o = [f'(footprint "{name}"', '  (version 20240108)', '  (generator "gen_wp26dk")', '  (layer "F.Cu")',
         f'  (descr "JAE {part}, {side}, {n} contacts + 2 power hold-downs, 0.35 mm pitch, 0.6 mm stacking. '
         f'Land pattern: {p["source"]}. Pad numbering follows the BM28 footprints in this library'
         + (', mirrored left-right as on the LINK flexes' if mirror else '') + '.")',
         f'  (tags "WP26DK {part} board-to-board 0.35mm")', '  (attr smd)',
         f'  (property "Reference" "REF**" (at 0 {f(-cy - 0.8)} 0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness 0.12))))',
         f'  (property "Value" "{part}" (at 0 {f(cy + 0.8)} 0) (layer "F.Fab") (effects (font (size 0.8 0.8) (thickness 0.12))))']
    o.append(f'  (fp_rect (start {f(-L/2)} {f(-W/2)}) (end {f(L/2)} {f(W/2)}) (stroke (width 0.1) (type solid)) (fill none) (layer "F.Fab"))')
    o.append(f'  (fp_rect (start {f(-cx)} {f(-cy)}) (end {f(cx)} {f(cy)}) (stroke (width 0.05) (type solid)) (fill none) (layer "F.CrtYd"))')
    # pin-1 marker: silk dot beyond the pin-1 end of row +y
    a = (n // 2 - 1) * PITCH
    m = -1 if mirror else 1
    o.append(f'  (fp_circle (center {f(-m*a/2)} {f(cy + 0.15)}) (end {f(-m*a/2 + 0.08)} {f(cy + 0.15)}) (stroke (width 0.16) (type solid)) (fill solid) (layer "F.SilkS"))')
    o.append(f'  (fp_text user "${{REFERENCE}}" (at 0 0 0) (layer "F.Fab") (effects (font (size 0.5 0.5) (thickness 0.08))))')
    for num, x, y, (w, h) in ps:
        o.append(f'  (pad "{num}" smd rect (at {f(x)} {f(y)}) (size {f(w)} {f(h)}) (layers "F.Cu" "F.Paste" "F.Mask"))')
    if os.path.exists(os.path.join(os.path.dirname(__file__), "..", "Connector_KSL.3dshapes", name + ".step")):
        model = f"${{KSL_ROOT}}/Connector_KSL/Connector_KSL.3dshapes/{name}.step"
        o.append(f'  (model "{model}" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
    o.append(')')
    return name, "\n".join(o) + "\n"


if __name__ == "__main__":
    outdir = sys.argv[1]
    which = sys.argv[2:] or ["S10", "S24", "S30", "S60"]
    for w in which:
        p = RECEPTACLE if w[0] == "S" else PLUG
        if p is None:
            sys.exit("plug parameters not set")
        name, text = footprint(p, int(w[1:].rstrip("M")), w.endswith("M"))
        open(os.path.join(outdir, name + ".kicad_mod"), "w").write(text)
        print(name)
