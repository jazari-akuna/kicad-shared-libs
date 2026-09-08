#!/usr/bin/env python3
"""Simplified colored nominal mechanical envelope from the shared pad map.

Infineon v1.0 p12. Metal/base split and colors are illustrative, not internals.
"""
from pathlib import Path
import json
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool, XCAFDoc_ColorType
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from OCP.Quantity import Quantity_Color, Quantity_TOC_sRGB
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
K=Path(__file__).resolve().parents[2];R=K/'docs/part-reports/IM69D129FV01XTMA1'
j=json.loads((R/'source-geometry.json').read_text());pads=j['pads_pcb_top']
def box(x,y,z,w,d,h):return BRepPrimAPI_MakeBox(gp_Pnt(x,y,z),w,d,h).Shape()
def cyl(x,y,z,r,h):return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z),gp_Dir(0,0,1)),r,h).Shape()
port=cyl(.71,0,-.01,.325/2,.30)
base=BRepAlgoAPI_Cut(box(-1.75,-1.325,.01,3.50,2.65,.14),port).Shape()
case=box(-1.75,-1.325,.15,3.50,2.65,.83)
# Coplanar bottom terminals, including the ground annulus surrounding the port.
terminals=BRepAlgoAPI_Cut(cyl(.71,0,0,1.625/2,.02),cyl(.71,0,-.01,1.025/2,.04)).Shape()
for n,p in pads.items():
 if n=='3':continue
 # Package nominal row pitch is 1.675 mm, PCB land pitch rounds to 1.676 mm.
 y=-p['y']/abs(p['y'])*(1.675/2)
 pad=box(p['x']-.522/2,y-.725/2,0,.522,.725,.02)
 terminals=BRepAlgoAPI_Fuse(terminals,pad).Shape()
# Fused geometry is used for the complete nonempty model; per-face colors retain contrast.
shape=BRepAlgoAPI_Fuse(BRepAlgoAPI_Fuse(base,case).Shape(),terminals).Shape()
doc=TDocStd_Document(TCollection_ExtendedString('IM69D129FV01'))
st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());ct=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
label=st.AddShape(shape,False)
ct.SetColor(label,Quantity_Color(.68,.70,.71,Quantity_TOC_sRGB),XCAFDoc_ColorType.XCAFDoc_ColorSurf)
# Colored sub-shapes are illustration only; actual seating comes from geometry.
for s,col in [(base,(.16,.10,.045)),(terminals,(.80,.65,.23))]:
 sub=st.AddSubShape(label,s)
 if not sub.IsNull():ct.SetColor(sub,Quantity_Color(*col,Quantity_TOC_sRGB),XCAFDoc_ColorType.XCAFDoc_ColorSurf)
writer=STEPCAFControl_Writer();writer.SetColorMode(True);assert writer.Transfer(doc,STEPControl_AsIs)
out=K/'Microphone_KSL/Microphone_KSL.3dshapes/MIC-LGA-5_IM69D129FV01_3.50x2.65mm.step'
assert int(writer.Write(str(out)))==1
b=Bnd_Box();BRepBndLib.Add_s(shape,b);bounds=b.Get()
(R/'model-audit.json').write_text(json.dumps({'nominal_bbox_mm':list(bounds),'STEP_bytes':out.stat().st_size,'footprint_offset_xyz_mm':[0,0,0],'model_y_is_negative_footprint_y':True,'height_max_clearance_mm':1.08},indent=2)+'\n')
print(bounds)
