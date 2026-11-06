# Vorschaubild der montierten Baugruppe (nutzt build() aus montage.py)
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import montage as M
light=np.array([0.4,-0.6,0.7]); light/=np.linalg.norm(light)
polys,cols=[],[]
for n,_,s,c in M.build(M.MONTIERT):
    verts,tris=s.val().tessellate(0.15,0.3)
    V=np.array([(p.x,p.z,p.y) for p in verts]); rgb=np.array(matplotlib.colors.to_rgb(c))
    for t in tris:
        tri=V[list(t)]; nrm=np.cross(tri[1]-tri[0],tri[2]-tri[0]); ln=np.linalg.norm(nrm)
        if ln: polys.append(tri); cols.append(np.clip(rgb*(0.45+0.55*abs(np.dot(nrm/ln,light))),0,1))
fig=plt.figure(figsize=(10,6)); ax=fig.add_axes([0,0,1,0.93],projection="3d")
ax.add_collection3d(Poly3DCollection(polys,facecolors=cols,edgecolors="none"))
xr,yr,zr=(-85,85),(-12,25),(-36,36)
ax.set_xlim(*xr); ax.set_ylim(*yr); ax.set_zlim(*zr); ax.set_box_aspect((170,37,72))
ax.view_init(elev=24,azim=122); ax.set_proj_type("ortho"); ax.axis("off")
fig.text(0.02,0.95,"Sensorbrücke AS5600 – montiert (Blick schräg auf die Rückseite der Luftbox)",fontsize=12,weight="bold")
fig.savefig("sensorbruecke-as5600-baugruppe.png",dpi=160)
