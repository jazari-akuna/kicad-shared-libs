#!/usr/bin/env python3
"""Render CAD-kernel tessellation produced by build_model.py."""
import json,sys
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
items=json.loads((Path(__file__).parent/'model-mesh.json').read_text());fig=plt.figure(figsize=(9,5));ax=fig.add_subplot(projection='3d')
for i,item in enumerate(items):
 v=np.array(item['v']);polys=v[np.array(item['t'])];ax.add_collection3d(Poly3DCollection(polys,facecolors='#303238'if i==0 else'#b9b2a0',edgecolors='#555555',linewidths=.10))
ax.set_xlim(-3,3);ax.set_ylim(-3,.7);ax.set_zlim(0,2);ax.set_box_aspect((6,3.7,2));ax.view_init(elev=25,azim=-65);ax.set_xlabel('X (mm)');ax.set_ylabel('Y (mm)');ax.set_zlabel('Z (mm)');ax.set_title('ACES 50208-0040N-001\nDrawing-derived; mating/contact details simplified')
fig.tight_layout();fig.savefig(Path(__file__).parent/'model.png',dpi=180)
