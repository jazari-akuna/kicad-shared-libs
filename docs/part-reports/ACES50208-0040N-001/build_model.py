#!/usr/bin/env python3
"""Drawing-derived simplified ACES50208 four-way connector, not vendor CAD."""
from pathlib import Path
import json,hashlib
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCP.gp import gp_Pnt
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color,Quantity_TOC_sRGB
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs,STEPControl_Reader
from OCP.IFSelect import IFSelect_RetDone
from OCP.Bnd import Bnd_Box
from OCP.BRepBndLib import BRepBndLib
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TDataStd import TDataStd_Name
R=Path(__file__).resolve().parents[3];D=Path(__file__).parent
P=R/'Connector_KSL/Connector_KSL.3dshapes/ACES_50208-0040N-001_DrawingDerived.step'
def box(x,y,z,dx,dy,dz):return BRepPrimAPI_MakeBox(gp_Pnt(x,y,z),dx,dy,dz).Shape()
# Nominal body5.38x2.70x1.70 per revAA drawing. Seat the terminal plane atZ0.
body=box(-2.69,-2.70,.05,5.38,2.70,1.65)
# Cavity B=3.50 clear span is illustrative: B is the source mating-width datum,
# not a guaranteed cavity dimension. Walls/floor/roof and contact geometry simplified.
body=BRepAlgoAPI_Cut(body,box(-1.75,-2.71,.25,3.50,2.10,1.25)).Shape()
parts=[('Housing_drawing_derived',body,(.12,.12,.12))]
for i,x in enumerate([-1.2,-.4,.4,1.2],1):
 # Source terminal stock0.15mm; width0.25mm and straight spring shape are estimates.
 parts.append((f'Contact_{i}_simplified',box(x-.125,-2.3,0,.25,2.75,.15),(0.72,.70,.64)))
for x in [-2.32,2.32]:
 # Source nail stock0.20mm and D=4.64; widths/longitudinal shape illustrative.
 parts.append(('Fitting_nail_simplified',box(x-.25,-2.65,0,.50,1.30,.20),(.70,.72,.74)))
doc=TDocStd_Document(TCollection_ExtendedString('ACES50208 drawing-derived'))
st=XCAFDoc_DocumentTool.ShapeTool_s(doc.Main());ct=XCAFDoc_DocumentTool.ColorTool_s(doc.Main())
for name,shape,color in parts:
 assert BRepCheck_Analyzer(shape).IsValid()
 label=st.AddShape(shape,False);TDataStd_Name.Set_s(label,TCollection_ExtendedString(name));ct.SetColor(label,Quantity_Color(*color,Quantity_TOC_sRGB),XCAFDoc_ColorType.XCAFDoc_ColorGen)
w=STEPCAFControl_Writer();w.SetColorMode(True);w.SetNameMode(True);assert w.Transfer(doc,STEPControl_AsIs);assert w.Write(str(P))==IFSelect_RetDone
reader=STEPControl_Reader();assert reader.ReadFile(str(P))==IFSelect_RetDone;reader.TransferRoots();shape=reader.OneShape();assert BRepCheck_Analyzer(shape).IsValid();b=Bnd_Box();BRepBndLib.Add_s(shape,b);lo,hi=b.CornerMin(),b.CornerMax();bounds=[lo.X(),lo.Y(),lo.Z(),hi.X(),hi.Y(),hi.Z()];print(bounds)
out={'status':'valid drawing-derived simplified STEP; not manufacturer CAD','source':'datasheets/50208-0040N-001.pdf','source_sha256':hashlib.sha256((R/'datasheets/50208-0040N-001.pdf').read_bytes()).hexdigest(),'source_revision':'AA, page1, four-circuit table','source_dimensions_mm':{'A_contact_span':2.4,'B_mating_width_datum':3.5,'C_body_width':5.38,'D_nail_center_span':4.64,'body_depth':2.7,'overall_height':1.7,'pitch':.8,'terminal_stock':.15,'nail_stock':.2},'model_bounds_mm':bounds,'footprint_model_transform':{'offset':[0,0,0],'rotate':[0,0,0],'scale':[1,1,1]},'frame':'footprintX=modelX; footprintY=-modelY; pin1x=-1.2; opening toward footprint+y;terminalplaneZ=0','solid_count_expected':7,'step_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'assumptions':['Simplified cavity uses B datum but internal width/walls/roof are not independently dimensioned.','Contact width0.25mm, straight spring form, nail width0.50mm and length1.30mm are visual approximations.','No mating plug, wire, latch travel or insertion-envelope qualification.','Manufacturerdownloadterms were not accepted and its ZIP was not downloaded.']}
(D/'validation.json').write_text(json.dumps(out,indent=2)+'\n')

# Reproducible preview mesh from the same CAD-kernel shapes.
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.TopExp import TopExp_Explorer
from OCP.TopAbs import TopAbs_FACE
from OCP.TopoDS import TopoDS
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
meshes=[]
for name,shape,color in parts:
 BRepMesh_IncrementalMesh(shape,.02)
 vertices=[];triangles=[];faces=TopExp_Explorer(shape,TopAbs_FACE)
 while faces.More():
  loc=TopLoc_Location();tri=BRep_Tool.Triangulation_s(TopoDS.Face(faces.Current()),loc)
  base=len(vertices)
  for j in range(1,tri.NbNodes()+1):
   pt=tri.Node(j).Transformed(loc.Transformation());vertices.append([pt.X(),pt.Y(),pt.Z()])
  for j in range(1,tri.NbTriangles()+1):triangles.append([base+n-1 for n in tri.Triangle(j).Get()])
  faces.Next()
 meshes.append({'v':vertices,'t':triangles})
(D/'model-mesh.json').write_text(json.dumps(meshes))
