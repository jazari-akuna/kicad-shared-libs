import Part,FreeCAD,json
from FreeCAD import Vector
from pathlib import Path
K=Path('/Users/raph/Projects/kicad-shared-libs');j=json.loads((K/'docs/part-reports/TCA9800DGKR/geometry.json').read_text())
b=Part.makeBox(3,3,.9,Vector(-1.5,-1.5,.1));b=b.cut(Part.makeCylinder(.16,.025,Vector(-1,1, .98)));sol=[b]
for n,(x,y) in j['pads'].items():
 side=1 if x>0 else -1;y=-y
 sol.append(Part.makeBox(.55,.32,.12,Vector(1.9 if side>0 else -2.45,y-.16,0)))
 sol.append(Part.makeBox(.15,.32,.42,Vector(1.8 if side>0 else -1.95,y-.16,.05)))
 sol.append(Part.makeBox(.45,.32,.12,Vector(1.4 if side>0 else -1.85,y-.16,.35)))
s=Part.makeCompound(sol);s.exportStep(str(K/'Interface_KSL/Interface_KSL.3dshapes/TCA9800_DGK0008A.step'));print(s.BoundBox)
