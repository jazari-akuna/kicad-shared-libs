#!/usr/bin/env python3
"""Verify/correct JLC downloads to TI DRL0005A and DCK0006A land patterns."""
from pathlib import Path
import sexpdata as sx,copy,shutil,json
ROOT=Path(__file__).resolve().parents[2]; OUT=Path(__file__).resolve().parent
LIB='Interface_KSL'; dest=ROOT/LIB
S=sx.Symbol
def g(x,k):return next((v for v in x if isinstance(v,list) and str(v[0])==k),None)
parts=[('SN74LVC1G14DRLR','SOT-553-5_L1.6-W1.2-P0.50-LS1.6-TL',{'1':'no_connect','2':'input','3':'power_in','4':'output','5':'power_in'}),('TXU0101DCKR','SC-70-6_L2.0-W1.3-P0.65-LS2.1-BL',{'1':'power_in','2':'power_in','3':'input','4':'output','5':'input','6':'power_in'})]
for name,fp,types in parts:
 raw=sx.load((OUT/'imported'/f'{name}.kicad_sym').open()); sym=next(z for z in raw if isinstance(z,list) and str(z[0])=='symbol')
 for p in sym:
  if isinstance(p,list) and str(p[0])=='property':
   if p[1]=='Reference':p[2]='U?'
   if p[1]=='Datasheet':p[2]='${KSL_ROOT}/datasheets/'+name+'.pdf'
   if p[1]=='Footprint':p[2]=LIB+':'+fp
 for sub in sym:
  if isinstance(sub,list) and str(sub[0])=='symbol':
   for p in sub:
    if isinstance(p,list) and str(p[0])=='pin':p[1]=S(types[g(p,'number')[1]])
 sym.append(sx.loads('(property "Description" '+json.dumps('Single Schmitt-trigger inverter, 1.65-5.5V' if name.startswith('SN') else 'Single fixed-direction dual-supply Schmitt-trigger translator, 1.1-5.5V, Ioff and rail isolation')+' (at 0 0 0) (effects (font (size 1.27 1.27)) hide))'))
 path=dest/(LIB+'.kicad_sym');txt=path.read_text();assert '(symbol "'+name+'"' not in txt
 path.write_text(txt.rstrip()[:-1]+'\n'+sx.dumps(sym)+'\n)\n')
 f=sx.load((OUT/'imported'/(fp+'.kicad_mod')).open())
 # Keep imported body/terminal 3D data, correct pads to manufacturer land example.
 for p in f:
  if not isinstance(p,list):continue
  if str(p[0])=='pad':
   num=str(p[1])
   if name.startswith('SN'):
    x=-.74 if num in ['1','2','3'] else .74;y={'1':-.5,'2':0,'3':.5,'4':.5,'5':-.5}[num];size=[.67,.3]
   else:x,y=g(p,'at')[1:3];x=round(x,2);y=round(y,1);size=[.4,.9]
   g(p,'at')[1:3]=[x,y];g(p,'size')[1:]=size;p[3]=S('roundrect');p.append([S('roundrect_rratio'),.125])
  if str(p[0])=='model':
   a=g(p,'at');a[0]=S('offset');g(a,'xyz')[1:]=[0,0,.5 if name=='TXU0101DCKR' else 0]
  if str(p[0])=='model':p[1]='${KSL_ROOT}/'+LIB+'/'+LIB+'.3dshapes/'+fp+'.step'
  if str(p[0])=='fp_text':
   if str(p[1])=='user':g(p,'at')[1:3]=[0,-2.0]
   if str(p[1])=='value':p[2]=name;g(p,'at')[1:3]=[0,2.1]
   e=g(p,'effects');g(g(e,'font'),'size')[1:]=[.5,.5];g(g(e,'font'),'thickness')[1]=.08
 # Imported silk/pin1 circles include clutter; replace with simple body-end strokes and pin1 dot outside masks.
 f[:]=[v for v in f if not(isinstance(v,list) and str(v[0]) in ['fp_circle','fp_line'] and g(v,'layer') and g(v,'layer')[1]==S('F.SilkS'))]
 inv=name.startswith('SN');cx,cy=(1.35,1.05) if inv else (1.25,1.8)
 for lay,w in [('F.CrtYd',.05)]:
  for a,b in [((-cx,-cy),(cx,-cy)),((cx,-cy),(cx,cy)),((cx,cy),(-cx,cy)),((-cx,cy),(-cx,-cy))]:f.append(sx.loads(f'(fp_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (layer {lay}) (width {w}))'))
 # Fab body and pin-one marker remain separate from moved text.
 bx,by=(.6,.8) if inv else (1,.65)
 for a,b in [((-bx,-by),(bx,-by)),((bx,-by),(bx,by)),((bx,by),(-bx,by)),((-bx,by),(-bx,-by))]:f.append(sx.loads(f'(fp_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (layer F.Fab) (width .05))'))
 (dest/(LIB+'.pretty')/(fp+'.kicad_mod')).write_text(sx.dumps(f).replace('User.Comments','Cmts.User')+'\n')
 shutil.copy2(OUT/'imported'/(fp+'.step'),dest/(LIB+'.3dshapes')/(fp+'.step'))
print('Imported 2 corrected parts; no new library or global table changes')
