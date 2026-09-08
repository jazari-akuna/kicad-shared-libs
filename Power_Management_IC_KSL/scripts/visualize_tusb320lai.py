#!/usr/bin/env python3
"""Equal-scale PCB-top comparison of downloaded and TI recommended lands."""
from pathlib import Path
import json
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
k=Path(__file__).resolve().parents[2];r=k/'docs/part-reports/TUSB320LAIRWBR';j=json.loads((r/'source-geometry.json').read_text());fig,axs=plt.subplots(1,2,figsize=(10,5.2))
for idx,a in enumerate(axs):
 a.set_aspect('equal');a.set_xlim(-1.5,1.5);a.set_ylim(1.4,-1.4);a.grid(alpha=.15);a.set_xlabel('mm; PCB top view');a.set_title(['Downloaded C132554 lands','TI RWB0012A recommended lands'][idx]);a.add_patch(Rectangle((-.8,-.8),1.6,1.6,fc='#e7eff5',ec='#446677'))
 for n,p in j['pads'].items():
  x,y,w,h=[p[t] for t in ['x','y','w','h']]
  if idx==0:
   if n in ['1','2','7','8']:x=(.75 if x>0 else -.75);w=.505
   else:h=.505
  a.add_patch(Rectangle((x-w/2,y-h/2),w,h,fc='#e7b342',ec='#996416'));a.text(x,y,n,ha='center',va='center',fontsize=9)
 a.annotate('',xy=(-.8,-1.22),xytext=(.8,-1.22),arrowprops={'arrowstyle':'<->'});a.text(0,-1.25,'1.60 mm body',ha='center',va='bottom',fontsize=9)
fig.text(.07,.04,'Same orthographic scale. Four side lands: 0.505 × 0.20 → 0.70 × 0.20 mm; center X ±0.75 → ±0.65 mm.\nTI SLLSEQ8D p36, drawing 4221631/B. Corner radius 0.05 mm; no exposed pad.',fontsize=9)
fig.subplots_adjust(left=.07,right=.98,bottom=.22,top=.92,wspace=.23)
for ext in ['png','svg']:fig.savefig(r/('geometry-comparison.'+ext),dpi=180,bbox_inches='tight')
