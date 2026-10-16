from pathlib import Path
import json,copy,hashlib
import sexpdata as sx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyBboxPatch
root=Path(__file__).resolve().parents[2];lib=root/'Capacitor_KSL/Capacitor_KSL.pretty';out=root/'reports/2026-10-16-tail-passive-courtyards';names=['C_0402_1005Metric_Receiver','C_0402_1005Metric_Receiver_DenseFlexTail'];trees=[sx.loads((lib/(n+'.kicad_mod')).read_text())for n in names]
def kids(t,n):return[q for q in t if isinstance(q,list) and q and str(q[0])==n]
def one(t,n):return kids(t,n)[0]
a,b=copy.deepcopy(trees);a[1]=b[1]='NAME'
for t in [a,b]:
 t[:]=[q for q in t if not(isinstance(q,list)and q and (str(q[0])=='descr' or (str(q[0])=='fp_rect' and one(q,'layer')[1]=='F.CrtYd')))]
 for q in kids(t,'property'):
  if q[1]=='Value':q[2]='VALUE'
assert a==b
proof={'status':'PASS','only_identity_description_value_and_courtyard_changed':True,'numbered_copper_paste_mask_body_and_model_exact':True,'previous_courtyard_centerline_y_mm':[-.46,.46],'new_courtyard_centerline_y_mm':[-.365,.365],'maximum_package_mm':[1.05,.55,.55],'source':'Samsung MLCC November2015 physicalpage6 CL05/thickness5; local English CL05C102JB5NNNC.pdf and CL05C100JB5NNNC.pdf','courtyard_inner_stroke_to_max_body_y_mm':.065,'courtyard_outer_width_mm':.78,'manufacturing_acceptance':'Application-specific courtyard; supplier fixture/assembly acceptance remains open'}
(out/'parity.json').write_text(json.dumps(proof,indent=2)+'\n')
fig,axs=plt.subplots(1,2,figsize=(8,3.4))
for ax,t,title in zip(axs,trees,['Previous courtyard: 0.97 mm','Tail courtyard: 0.78 mm']):
 c=next(v for v in kids(t,'fp_rect')if one(v,'layer')[1]=='F.CrtYd');x,y=one(c,'start')[1:];xx,yy=one(c,'end')[1:];ax.add_patch(Rectangle((x,y),xx-x,yy-y,fill=False,edgecolor='#a01a88',linewidth=2))
 for p in kids(t,'pad'):
  x,y=one(p,'at')[1:3];w,h=one(p,'size')[1:];r=min(w,h)*one(p,'roundrect_rratio')[1];ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f'round,pad=0,rounding_size={r}',facecolor='#c76940'));ax.text(x,y,p[1],ha='center',va='center',color='white',weight='bold')
 ax.add_patch(Rectangle((-.525,-.275),1.05,.55,fill=False,edgecolor='#142e3a',linestyle='--'));ax.set(xlim=(-1.05,1.05),ylim=(-.67,.67),aspect='equal',title=title);ax.tick_params(labelsize=8)
fig.suptitle('C1006 / C1007: reduce courtyard; preserve lands and model',fontsize=13,y=.96);fig.text(.5,.065,'Purple: courtyard centerline. Dashed: maximum Samsung CL05 body. Dimensions in mm.',ha='center',fontsize=9);fig.subplots_adjust(top=.78,bottom=.20,left=.07,right=.98,wspace=.18);fig.savefig(out/'courtyard-comparison.png',dpi=170)
print(proof)
