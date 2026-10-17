from pathlib import Path
from OCP.STEPControl import STEPControl_Reader
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
import json
root=Path(__file__).resolve().parents[2];p=root/'Interface_KSL/Interface_KSL.3dshapes';out=[]
for n in ['SOT-553-5_L1.6-W1.2-P0.50-LS1.6-TL','SC-70-6_L2.0-W1.3-P0.65-LS2.1-BL']:
 r=STEPControl_Reader();status=r.ReadFile(str(p/(n+'.step')));r.TransferRoots();shape=r.OneShape();assert not shape.IsNull();b=Bnd_Box();BRepBndLib.Add_s(shape,b);a=b.Get();out.append({'model':n,'bbox':a,'dimensions':[a[i+3]-a[i]for i in range(3)],'valid_nonempty_STEP':True})
Path(__file__).with_name('model-check.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
