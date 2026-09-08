import Part,FreeCAD,json
from FreeCAD import Vector
from pathlib import Path
K=Path('/Users/raph/Projects/kicad-shared-libs');j=json.loads((K/'docs/part-reports/BGS12P2L6E6327XTSA1/geometry.json').read_text());b=Part.makeBox(.7,1.1,.29,Vector(-.35,-.55,.02));b=b.cut(Part.makeCylinder(.04,.01,Vector(.2,-.4,.30)));sol=[b]
for n,(x,y) in j['pads'].items():sol.append(Part.makeBox(.2,.2,.02,Vector(x-.1,-y-.1,0)))
s=Part.makeCompound(sol);s.exportStep(str(K/'RF_Wireless_KSL/RF_Wireless_KSL.3dshapes/BGS12P2L6_TSLP-6-4.step'));print(s.BoundBox)
