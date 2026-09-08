#!/usr/bin/env python3
"""Correct the C132554 import against TI SLLSEQ8D pp3,35–36.

Exact LAIRWBR: 12-pin RWB0012A, no exposed pad. PCB top view.
"""
from pathlib import Path
import json,re
K=Path(__file__).resolve().parents[2];M='TUSB320LAIRWBR';F='X2QFN-12_TUSB320LAI_RWB0012A_1.6x1.6mm'
R=K/'docs/part-reports'/M;R.mkdir(parents=True,exist_ok=True)
pads={str(n):{'x':x,'y':y,'w':w,'h':h} for n,x,y,w,h in [(1,-.65,-.2,.7,.2),(2,-.65,.2,.7,.2),(7,.65,.2,.7,.2),(8,.65,-.2,.7,.2)]+[(n,x,y,.2,.5) for n,x,y in [(12,-.6,-.75),(11,-.2,-.75),(10,.2,-.75),(9,.6,-.75),(3,-.6,.75),(4,-.2,.75),(5,.2,.75),(6,.6,.75)]]}
names=['CC1','CC2','PORT','VBUS_DET','ADDR','INT_N/OUT3','SDA/OUT1','SCL/OUT2','ID','GND','EN_N','VDD']
types=['bidirectional','bidirectional','input','input','input','open_collector','bidirectional','bidirectional','open_collector','power_in','input','power_in']
def prop(n,v,x=0,y=0,hide=True):return f'(property "{n}" "{v}" (at {x} {y} 0) (effects (font (size 1.27 1.27))'+(' (hide yes)' if hide else '')+'))'
s=f'(symbol "{M}" (in_bom yes) (on_board yes)'+prop('Reference','U',0,12.7,False)+prop('Value',M,0,10.16,False)+prop('Footprint',f'Power_Management_IC_KSL:{F}')+prop('Datasheet',f'${{KSL_ROOT}}/datasheets/{M}.pdf')+prop('LCSC','C132554')+prop('Manufacturer','Texas Instruments')+prop('Description','USB-C CC controller, active-low enable, 1.65–3.6V I2C; RWB0012A no EP; TI SLLSEQ8D p3/35/36')
s+=f'(symbol "{M}_0_1" (rectangle (start -11.43 8.89) (end 11.43 -8.89) (stroke (width 0) (type default)) (fill (type background))))(symbol "{M}_1_1"'
for i,(name,t) in enumerate(zip(names,types),1):
 x,y,a=(-13.97,8.89-2.54*i,0) if i<=6 else (13.97,-6.35+2.54*(i-7),180)
 s+=f'(pin {t} line (at {x:.2f} {y:.2f} {a}) (length 2.54) (name "{name}" (effects (font (size 1 1)))) (number "{i}" (effects (font (size 1 1)))))'
s+='))\n';lib=K/'Power_Management_IC_KSL/Power_Management_IC_KSL.kicad_sym';all=lib.read_text();needle=f'(symbol "{M}"';start=all.find(needle)
if start>=0:
 depth=0;quoted=False;escaped=False
 for end in range(start,len(all)):
  c=all[end]
  if quoted:
   if escaped:escaped=False
   elif c=='\\':escaped=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:break
 all=all[:start]+s+all[end+1:]
else:all=all[:all.rfind(')')]+s+all[all.rfind(')'):]
lib.write_text(all)
fp=f'(footprint "{F}" (version 20241229) (generator "source-corrected-import") (layer "F.Cu") (attr smd) (descr "TI SLLSEQ8D p36 recommended RWB0012A land pattern. No EP. Pin 1 top-left side. Mask +0.05mm and courtyard +0.25mm are engineering allowances.")\n'
for name,value,y,layer,size in [('Reference','REF**',-1.7,'F.SilkS',.8),('Value',M,1.7,'F.Fab',.5)]:fp+=f'(property "{name}" "{value}" (at 0 {y}) (layer "{layer}") (effects (font (size {size} {size}) (thickness .1))))\n'
fp+='(fp_text user "${REFERENCE}" (at 0 -1.7) (layer "F.Fab") (effects (font (size .8 .8) (thickness .1))))\n'
for layer,size in [('F.Fab',.8),('F.CrtYd',1.25)]:fp+=f'(fp_rect (start {-size} {-size}) (end {size} {size}) (stroke (width .05) (type solid)) (fill none) (layer "{layer}"))\n'
fp+='(fp_circle (center -1.35 -.2) (end -1.28 -.2) (stroke (width .1) (type solid)) (fill solid) (layer "F.SilkS"))\n'
fp+='(fp_circle (center -.68 -.55) (end -.62 -.55) (stroke (width .04) (type solid)) (fill none) (layer "F.Fab"))\n'
for n,p in pads.items():fp+=f'(pad "{n}" smd roundrect (at {p["x"]} {p["y"]}) (size {p["w"]} {p["h"]}) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio .25) (solder_mask_margin .05))\n'
fp+=f'(model "${{KSL_ROOT}}/Power_Management_IC_KSL/Power_Management_IC_KSL.3dshapes/{F}.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))\n)\n'
(K/'Power_Management_IC_KSL/Power_Management_IC_KSL.pretty'/f'{F}.kicad_mod').write_text(fp)
(R/'source-geometry.json').write_text(json.dumps({'source':'TI SLLSEQ8D pp3,35–36; RWB0012A drawing 4221631/B 03/2015','frame':'PCB top; Y downward; package drawing bottom view must be reflected','body_mm':[1.6,1.6,.4],'body_xy_minmax_mm':[1.55,1.65],'height_max_mm':.4,'pitch_mm':.4,'pads':pads,'pins':{str(i):{'name':n,'type':t} for i,(n,t) in enumerate(zip(names,types),1)},'pad_corner_radius_mm':.05,'import_correction':'Four side lands were 0.505x0.2 at X +/-0.750; TI example is 0.7x0.2 at X +/-0.650. Top/bottom lands normalized from 0.505 to 0.5. Symbol pin types/source corrected.'},indent=2)+'\n')
print('Built source-corrected TUSB320LAIRWBR symbol and recommended lands.')
