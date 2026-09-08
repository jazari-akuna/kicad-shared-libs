#!/usr/bin/env python3
"""Correct C43314439 provider CAD against Infineon v1.0, pp8,10,12–13.

PCB top view: pin 1 lower left; shared map negates Y exactly once for STEP.
The imported MP23ABS1TR-named footprint was not the recommended land pattern.
"""
from pathlib import Path
import json, math, re
from shapely.geometry import Point, LineString
from shapely.ops import unary_union
K=Path(__file__).resolve().parents[2]
M='IM69D129FV01XTMA1'; F='MIC-LGA-5_IM69D129FV01_3.50x2.65mm'
R=K/'docs/part-reports'/M
PADS={'1':{'name':'DATA','type':'output','x':-1.364,'y':.838},
      '2':{'name':'LR_SELECT','type':'input','x':-.542,'y':.838},
      '3':{'name':'GND','type':'power_in','x':.710,'y':0},
      '4':{'name':'CLOCK','type':'input','x':-.542,'y':-.838},
      '5':{'name':'VDD','type':'power_in','x':-1.364,'y':-.838}}
facts={'source':'Infineon IM69D129FV01 datasheet v1.0, 2025-02-21, pp12–13',
 'body_mm':[3.50,2.65,.98],'height_max_mm':1.08,
 'signal_lands_mm':[.54,.75],'ground_land_outer_inner_diameter_mm':[1.725,.985],
 'pcb_acoustic_hole_diameter_mm':.6,'device_acoustic_port_diameter_mm':.325,
 'package_signal_terminal_mm':[.522,.725], 'package_terminal_row_pitch_mm':1.675,
 'pads_pcb_top':PADS,'silk_courtyard_mask':'engineering allowances; not manufacturer dimensions',
 'model':'simplified nominal body, terminals and bottom acoustic port; not internal construction'}
R.mkdir(parents=True,exist_ok=True);(R/'source-geometry.json').write_text(json.dumps(facts,indent=2)+'\n')
def prop(n,v,x=0,y=0,hide=True):
 return f'(property "{n}" "{v}" (at {x} {y} 0) (effects (font (size 1.27 1.27))'+(' (hide yes)' if hide else '')+'))'
symbol=f'(symbol "{M}" (in_bom yes) (on_board yes)\n'
symbol+=prop('Reference','MK?',0,10.16,False)+prop('Value',M,0,7.62,False)
symbol+=prop('Footprint',f'Microphone_KSL:{F}')+prop('Datasheet',f'${{KSL_ROOT}}/datasheets/{M}.pdf')
symbol+=prop('Description','Infineon single bottom-port PDM MEMS microphone; exact five-pad land pattern, nominal simplified STEP; source v1.0 pp8/10/12/13')
symbol+=prop('LCSC','C43314439')+prop('ki_keywords','C43314439 PDM microphone bottom-port')+prop('Manufacturer','Infineon')
symbol+=f'(symbol "{M}_0_1" (rectangle (start -8.89 6.35) (end 8.89 -6.35) (stroke (width 0) (type default)) (fill (type background))))'
symbol+=f'(symbol "{M}_1_1"'
for n,x,y,angle in [('5',-12.7,3.81,0),('4',-12.7,1.27,0),('2',-12.7,-1.27,0),('3',-12.7,-3.81,0),('1',12.7,1.27,180)]:
 p=PADS[n];symbol+=f'(pin {p["type"]} line (at {x} {y} {angle}) (length 3.81) (name "{p["name"]}" (effects (font (size 1.016 1.016)))) (number "{n}" (effects (font (size 1.016 1.016)))))'
symbol+='))\n'
lib=K/'Microphone_KSL/Microphone_KSL.kicad_sym';s=lib.read_text()
# Replace only our own exact definition on repeat; preserve every other symbol.
needle=f'(symbol "{M}"';start=s.find(needle)
if start>=0:
 depth=0;quoted=False;escaped=False;end=start
 for end in range(start,len(s)):
  c=s[end]
  if quoted:
   if escaped:escaped=False
   elif c=='\\':escaped=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:break
 s=s[:start]+symbol+s[end+1:]
else:s=s[:s.rfind(')')]+symbol+s[s.rfind(')'):]
lib.write_text(s)
fp=f'(footprint "{F}" (version 20241229) (generator "kicad-footprint-generator") (layer "F.Cu") (attr smd)\n'
fp+='(descr "Infineon IM69D129FV01 v1.0 p13 recommended PCB top-view lands; 0.6mm unplated acoustic hole; 3-sector paste; nominal simplified model")\n'
fp+='(property "Reference" "REF**" (at 0 -2.0) (layer "F.SilkS") (effects (font (size 0.8 0.8) (thickness .1))))\n'
fp+=f'(property "Value" "{M}" (at 0 2.0) (layer "F.Fab") (effects (font (size .5 .5) (thickness .08))))\n'
fp+='(fp_text user "${REFERENCE}" (at 0 -2.0) (layer "F.Fab") (effects (font (size .8 .8) (thickness .1))))\n'
for layer,w,h,width in [('F.Fab',3.5,2.65,.05),('F.CrtYd',4,3.2,.05),('F.SilkS',3.74,2.89,.1)]:
 fp+=f'(fp_rect (start {-w/2} {-h/2}) (end {w/2} {h/2}) (stroke (width {width}) (type solid)) (fill none) (layer "{layer}"))\n'
fp+='(fp_circle (center -2.1 1.1) (end -2.02 1.1) (stroke (width .1) (type solid)) (fill solid) (layer "F.SilkS"))\n'
fp+='(fp_circle (center -1.56 1.13) (end -1.50 1.13) (stroke (width .04) (type solid)) (fill none) (layer "F.Fab"))\n'
for n,p in PADS.items():
 if n=='3':continue
 fp+=f'(pad "{n}" smd rect (at {p["x"]} {p["y"]}) (size .54 .75) (layers "F.Cu" "F.Mask") (solder_mask_margin .05))\n'
 fp+=f'(pad "" smd roundrect (at {p["x"]} {p["y"]}) (size .47 .63) (layers "F.Paste") (roundrect_rratio .212766))\n'
def arc_sector_pad(number,start,end,ri,ro,layer):
 # Put the tiny required custom-pad anchor inside the ring, never in the sound hole.
 mid=math.radians((start+end)/2);anchor=((ri+ro)/2*math.cos(mid),(ri+ro)/2*math.sin(mid))
 points=[]
 for rad,ts in [(ro,[start+(end-start)*i/32 for i in range(33)]),(ri,[end-(end-start)*i/32 for i in range(33)])]:
  points.extend((rad*math.cos(math.radians(t))-anchor[0],rad*math.sin(math.radians(t))-anchor[1]) for t in ts)
 pts=' '.join(f'(xy {x:.6f} {y:.6f})' for x,y in points)
 return f'(pad "{number}" smd custom (at {.71+anchor[0]:.6f} {anchor[1]:.6f}) (size .01 .01) (layers {layer}) (solder_mask_margin .05) (options (clearance outline) (anchor circle)) (primitives (gr_poly (pts {pts}) (width 0) (fill yes))))\n'
for a in range(0,360,90):fp+=arc_sector_pad('3',a,a+90,.985/2,1.725/2,'"F.Cu" "F.Mask"')
# Figure14: three paste arcs, R0.54/R0.83, constant0.12mm radial gaps,
# and all undimensioned corner radii0.1mm. Directions follow the top-view source.
ring=Point(0,0).buffer(.83,resolution=256).difference(Point(0,0).buffer(.54,resolution=256))
cuts=unary_union([LineString([(0,0),(math.cos(math.radians(a)),math.sin(math.radians(a)))]).buffer(.06,cap_style=2) for a in [60,180,300]])
sectors=ring.difference(cuts)
assert len(sectors.geoms)==3
for sector in sectors.geoms:
 rounded=sector.buffer(-.1,resolution=32).buffer(.1,resolution=32)
 anchor=rounded.representative_point();pts=' '.join(f'(xy {x-anchor.x:.6f} {y-anchor.y:.6f})' for x,y in list(rounded.exterior.coords)[:-1])
 fp+=f'(pad "" smd custom (at {.71+anchor.x:.6f} {anchor.y:.6f}) (size .01 .01) (layers "F.Paste") (options (clearance outline) (anchor circle)) (primitives (gr_poly (pts {pts}) (width 0) (fill yes))))\n'
fp+='(pad "" np_thru_hole circle (at .71 0) (size .6 .6) (drill .6) (layers "*.Cu" "*.Mask"))\n'
fp+=f'(model "${{KSL_ROOT}}/Microphone_KSL/Microphone_KSL.3dshapes/{F}.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))\n)\n'
(K/'Microphone_KSL/Microphone_KSL.pretty'/f'{F}.kicad_mod').write_text(fp)
print('Updated exact microphone symbol, footprint and shared geometry map.')
