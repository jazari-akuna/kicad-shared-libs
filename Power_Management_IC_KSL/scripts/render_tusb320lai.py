#!/usr/bin/env python3
"""Run with KiCad Python; create a reproducible inspection coupon."""
from pathlib import Path
import json,pcbnew
K=Path(__file__).resolve().parents[2];R=K/'docs/part-reports/TUSB320LAIRWBR'
F='X2QFN-12_TUSB320LAI_RWB0012A_1.6x1.6mm'
b=pcbnew.CreateEmptyBoard();f=pcbnew.FootprintLoad(str(K/'Power_Management_IC_KSL/Power_Management_IC_KSL.pretty'),F);assert f
b.Add(f);f.SetReference('U1')
for a,c in [((-3,-2.6),(3,-2.6)),((3,-2.6),(3,2.6)),((3,2.6),(-3,2.6)),((-3,2.6),(-3,-2.6))]:
 s=pcbnew.PCB_SHAPE();s.SetShape(pcbnew.SHAPE_T_SEGMENT);s.SetStart(pcbnew.VECTOR2I(int(a[0]*1e6),int(a[1]*1e6)));s.SetEnd(pcbnew.VECTOR2I(int(c[0]*1e6),int(c[1]*1e6)));s.SetLayer(pcbnew.Edge_Cuts);s.SetWidth(50000);b.Add(s)
b.GetDesignSettings().SetBoardThickness(800000)
pcbnew.SaveBoard(str(R/'coupon.kicad_pcb'),b)
pads=[{'number':p.GetNumber(),'xy_mm':[v/1e6 for v in [p.GetPosition().x,p.GetPosition().y]],'size_mm':[v/1e6 for v in [p.GetSize().x,p.GetSize().y]],'drill_mm':p.GetDrillSize().x/1e6,'copper':p.IsOnCopperLayer()} for p in f.Pads()]
numbers={p['number'] for p in pads if p['copper'] and p['number']}
assert numbers=={str(n) for n in range(1,13)},numbers
(R/'footprint-audit.json').write_text(json.dumps({'numbered_copper_ids':sorted(numbers),'pads':pads,'exposed_pad':False},indent=2)+'\n')
