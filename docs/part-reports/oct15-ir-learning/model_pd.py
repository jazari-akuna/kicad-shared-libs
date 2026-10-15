from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCP.gp import gp_Pnt
from OCP.TDocStd import TDocStd_Document
from OCP.TCollection import TCollection_ExtendedString
from OCP.XCAFDoc import XCAFDoc_DocumentTool,XCAFDoc_ColorType
from OCP.Quantity import Quantity_Color,Quantity_TOC_sRGB
from OCP.STEPCAFControl import STEPCAFControl_Writer
from OCP.STEPControl import STEPControl_AsIs
from pathlib import Path
p=Path(__file__).resolve().parents[3]/'Sensor_KSL/Sensor_KSL.3dshapes/PHOTODIODE-0805_TEMD7100X01.step'
d=TDocStd_Document(TCollection_ExtendedString('MDTV-XCAF'));s=XCAFDoc_DocumentTool.ShapeTool_s(d.Main());c=XCAFDoc_DocumentTool.ColorTool_s(d.Main())
def box(x,y,z,dx,dy,dz,rgb):
 sh=BRepPrimAPI_MakeBox(gp_Pnt(x,y,z),dx,dy,dz).Shape();l=s.AddShape(sh,False);c.SetColor(l,Quantity_Color(*rgb,Quantity_TOC_sRGB),XCAFDoc_ColorType.XCAFDoc_ColorSurf)
box(-1,-.625,.04,2,1.25,.81,(.035,.035,.04))
box(-1,-.625,0,.6,1.25,.04,(.65,.65,.62));box(.4,-.625,0,.6,1.25,.04,(.65,.65,.62))
# Nominal optical window/marker are illustrative, body/terminal envelope from datasheet.
box(-.91,-.525,.85,.1,1.05,.002,(.45,.45,.45))
w=STEPCAFControl_Writer();w.SetColorMode(True);w.Transfer(d,STEPControl_AsIs);w.Write(str(p));print(p)
