#!/usr/bin/env python3
"""Run with KiCad Python; create a reproducible inspection coupon."""
from pathlib import Path
import json,pcbnew
K=Path(__file__).resolve().parents[2];R=K/'docs/part-reports/IM69D129FV01XTMA1'
F='MIC-LGA-5_IM69D129FV01_3.50x2.65mm'
b=pcbnew.CreateEmptyBoard();f=pcbnew.FootprintLoad(str(K/'Microphone_KSL/Microphone_KSL.pretty'),F);assert f
b.Add(f);f.SetReference('MK1')
for a,c in [((-3,-2.6),(3,-2.6)),((3,-2.6),(3,2.6)),((3,2.6),(-3,2.6)),((-3,2.6),(-3,-2.6))]:
 s=pcbnew.PCB_SHAPE();s.SetShape(pcbnew.SHAPE_T_SEGMENT);s.SetStart(pcbnew.VECTOR2I(int(a[0]*1e6),int(a[1]*1e6)));s.SetEnd(pcbnew.VECTOR2I(int(c[0]*1e6),int(c[1]*1e6)));s.SetLayer(pcbnew.Edge_Cuts);s.SetWidth(50000);b.Add(s)
b.GetDesignSettings().SetBoardThickness(800000)
pcbnew.SaveBoard(str(R/'coupon.kicad_pcb'),b)
pads=[{'number':p.GetNumber(),'xy_mm':[v/1e6 for v in [p.GetPosition().x,p.GetPosition().y]],'size_mm':[v/1e6 for v in [p.GetSize().x,p.GetSize().y]],'drill_mm':p.GetDrillSize().x/1e6,'copper':p.IsOnCopperLayer()} for p in f.Pads()]
numbers={p['number'] for p in pads if p['copper'] and p['number']}
assert numbers=={'1','2','3','4','5'},numbers
assert len([p for p in pads if p['number']=='3'])==4
assert len([p for p in pads if p['drill_mm']==.6])==1
(R/'footprint-audit.json').write_text(json.dumps({'numbered_copper_ids':sorted(numbers),'pads':pads,'repeated_ground_pad':'four touching annular sectors, all pad3; a single electrical terminal','npth_acoustic_hole_mm':.6},indent=2)+'\n')
print('Copper parity, acoustic drill and coupon generated.')
