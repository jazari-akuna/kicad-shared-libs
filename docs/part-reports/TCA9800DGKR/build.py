from pathlib import Path
import re,json,sys,shutil
K=Path('/Users/raph/Projects/kicad-shared-libs');D=K/'docs/part-reports/TCA9800DGKR';L=K/'Interface_KSL';sys.path.insert(0,'/Users/raph/Projects/remote-hardware/remote-motherboard/tools');from sch_lib import block_at
raw=Path('/tmp/remote-tca9800-jlc/TCA9800DGKR.kicad_sym').read_text();s=block_at(raw,raw.index('(symbol "TCA9800DGKR"'));assert '(symbol "TCA9800DGKR"' not in (L/'Interface_KSL.kicad_sym').read_text()
s=s.replace('"U" (id 0) (at 0 1.27 0)','"U?" (id 0) (at 0 9.525 0)').replace('(at 0 -2.54 0)','(at 0 7.62 0)').replace('".:VSSOP-8_L3.0-W3.0-P0.65-LS4.9-BL"','"Interface_KSL:VSSOP-8_TCA9800_DGK0008A"').replace('https://www.ti.com/lit/ds/symlink/ref5020.pdf?ts=1620828249805','${KSL_ROOT}/datasheets/TCA9800DGKR.pdf')
for m in reversed(list(re.finditer(r'\(pin unspecified line',s))):
 b=block_at(s,m.start());n=re.search(r'\(number "([^"]+)"',b)[1];typ='power_in' if n in ['1','4','8'] else 'input' if n=='5' else 'bidirectional';s=s[:m.start()]+b.replace('pin unspecified','pin '+typ,1)+s[m.start()+len(b):]
s=s[:-1]+'\n(property "Manufacturer" "Texas Instruments" (at 0 0 0)(effects(font(size 1.27 1.27))(hide yes)))\n(property "Description" "TCA9800DGKR; two-channel I2C level-translating buffer; VCCA0.8-3.6V, VCCB1.65-3.6V; B-side internal current source requires no external pull-ups; source TI SCPS264B; DGK0008A lands. Generated simplified nominal STEP." (at 0 0 0)(effects(font(size 1.27 1.27))(hide yes)))\n)'
p=L/'Interface_KSL.kicad_sym';t=p.read_text();p.write_text(t[:t.rfind(')')]+s+'\n)\n')
# Shared pad map follows the exact TI top-view drawing; KiCad y is down.
xy={str(i+1):[-2.2,-.975+i*.65] for i in range(4)};xy.update({str(8-i):[2.2,-.975+i*.65] for i in range(4)})
(D/'geometry.json').write_text(json.dumps({'source':'TI TCA9800DGKR SCPS264B, DGK0008A drawing4214862/A04/2023 pp35-36','pads':xy,'land_size':[1.4,.45],'pitch':.65,'row_centers':4.4,'nominal_body':[3,3],'body_range':[2.9,3.1],'height_max':1.1,'model_height_nominal':1.0,'body_standoff_nominal':.1},indent=2)+'\n')
f='''(footprint "VSSOP-8_TCA9800_DGK0008A" (version 20241229)(generator "pcbnew")(layer "F.Cu")
(descr "TCA9800 DGK0008A; exact TI land pattern 1.4x0.45mm pads,4.4mm rows,0.65mm pitch; body3x3mm,1.1mm max height")
(attr smd)
(property "Reference" "REF**" (at 0 -2.5 0)(layer "F.SilkS")(effects(font(size 1 1)(thickness .15))))
(property "Value" "TCA9800DGKR" (at 0 2.5 0)(layer "F.Fab")(effects(font(size 1 1)(thickness .15))))
(fp_text user "${REFERENCE}" (at 0 -2.5 0)(layer "F.Fab")(effects(font(size 1 1)(thickness .15))))
(fp_rect(start -1.5 -1.5)(end 1.5 1.5)(stroke(width .1)(type default))(fill none)(layer "F.Fab"))
(fp_line(start -1.5 -1)(end -1 -1.5)(stroke(width .1)(type default))(layer "F.Fab"))
(fp_rect(start -3.15 -1.85)(end 3.15 1.85)(stroke(width .05)(type default))(fill none)(layer "F.CrtYd"))
(fp_line(start -1.6 -1.65)(end 1.6 -1.65)(stroke(width .12)(type default))(layer "F.SilkS"))
(fp_line(start -1.6 1.65)(end 1.6 1.65)(stroke(width .12)(type default))(layer "F.SilkS"))
(fp_line(start -2.85 -1.55)(end -2.1 -1.55)(stroke(width .12)(type default))(layer "F.SilkS"))
'''
for n,(x,y) in xy.items():f+=f'(pad "{n}" smd roundrect(at {x} {y:.3f})(size 1.4 .45)(layers "F.Cu" "F.Paste" "F.Mask")(roundrect_rratio .111111))\n'
f+='(model "${KSL_ROOT}/Interface_KSL/Interface_KSL.3dshapes/TCA9800_DGK0008A.step"(offset(xyz 0 0 0))(scale(xyz 1 1 1))(rotate(xyz 0 0 0))))\n';(L/'Interface_KSL.pretty/VSSOP-8_TCA9800_DGK0008A.kicad_mod').write_text(f)
shutil.copy2('/tmp/tca-source-35.png',D/'package-source.png');shutil.copy2('/tmp/tca-source-36.png',D/'land-source.png')
(D/'datasheet-verdicts.json').write_text(json.dumps([{'slug':'TCA9800DGKR','action':'keep','note':'Public English TI SCPS264B exact orderable MPN in addendum; pin table p3 and DGK0008A package/land pp35-36 visually inspected. Provider wrongly linked REF5020; corrected to actual manufacturer TCA9800 datasheet.'}],indent=2)+'\n')
