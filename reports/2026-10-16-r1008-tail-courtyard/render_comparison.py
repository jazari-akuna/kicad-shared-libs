from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,FancyBboxPatch
import sexpdata as sx
root=Path(__file__).resolve().parents[2];lib=root/'Resistor_KSL/Resistor_KSL.pretty'
fig,axs=plt.subplots(1,2,figsize=(8,3.4))
for ax,name,title in zip(axs,['R_0402_Yageo_RT','R_0402_Yageo_RT_DenseFlexTail'],['Previous courtyard: 0.99 mm','Tail courtyard: 0.78 mm']):
 t=sx.loads((lib/(name+'.kicad_mod')).read_text())
 def kids(q,n):return [v for v in q if isinstance(v,list) and v and str(v[0])==n]
 def one(q,n):return kids(q,n)[0]
 c=next(v for v in kids(t,'fp_rect') if one(v,'layer')[1]=='F.CrtYd');x,y=one(c,'start')[1:];xx,yy=one(c,'end')[1:];ax.add_patch(Rectangle((x,y),xx-x,yy-y,fill=False,edgecolor='#a01a88',linewidth=2))
 for p in kids(t,'pad'):
  x,y=one(p,'at')[1:3];w,h=one(p,'size')[1:];radius=min(w,h)*one(p,'roundrect_rratio')[1]
  ax.add_patch(FancyBboxPatch((x-w/2,y-h/2),w,h,boxstyle=f'round,pad=0,rounding_size={radius}',facecolor='#c76940'))
  ax.text(x,y,p[1],ha='center',va='center',color='white',weight='bold')
 ax.add_patch(Rectangle((-.525,-.275),1.05,.55,fill=False,edgecolor='#142e3a',linestyle='--',linewidth=1))
 ax.set(xlim=(-1.05,1.05),ylim=(-.67,.67),aspect='equal',title=title);ax.tick_params(labelsize=8)
fig.suptitle('R1008: tighten the courtyard; keep the copper lands',fontsize=13,y=.96)
fig.text(.5,.065,'Purple: courtyard centerline. Dashed: maximum resistor body. Dimensions in mm.',ha='center',fontsize=9)
fig.subplots_adjust(top=.78,bottom=.20,left=.07,right=.98,wspace=.18)
fig.savefig(Path(__file__).with_name('courtyard-comparison.png'),dpi=170)
