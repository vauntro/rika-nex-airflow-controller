# Explosionsdarstellung der Montage (A4 quer), gerendert aus vereinfachten CadQuery-Körpern.
# Achsen im Modell: X quer, Y senkrecht, Z = weg von der Luftbox (Laschenebene Z = 0).
import math
import numpy as np
import cadquery as cq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import proj3d
import bruecke as B

HX,PX,PY=B.HX,B.PX,B.PY
WP=lambda z=0: cq.Workplane("XY",origin=(0,0,z))
def cyl(r,h,x=0,y=0,z=0,ri=0):
    w=WP(z).center(x,y).circle(r)
    if ri: w=w.circle(ri)
    return w.extrude(h)
def hexnut(s,h,x,y,z,ri):
    return WP(z).center(x,y).polygon(6,s/math.cos(math.pi/6)).circle(ri).extrude(h)
def hexbolt(x,y,z_head_top,L,direction):
    # Kopf SW8 h3,5, Schaft Ø5 Länge L; direction +1: Schaft zeigt nach +Z
    if direction>0:
        head=WP(z_head_top-3.5).center(x,y).polygon(6,8/math.cos(math.pi/6)).extrude(3.5)
        shaft=cyl(2.5,L,x,y,z_head_top)
    return head.union(shaft)
def m3screw(x,y,z,direction):
    # ISO 7380 M3 × 5: Linsenkopf Ø5,7 h1,65; direction +1: Schaft nach +Z
    if direction>0:
        return cyl(2.85,1.65,x,y,z-1.65).union(cyl(1.5,5,x,y,z))
    return cyl(2.85,1.65,x,y,z).union(cyl(1.5,5,x,y,z-5))

GREY,ALU,BRASS,STEEL,PCB,MAG,DARK="#b9b9b9","#a9c4e0","#d4b25a","#c8c8c8","#2f6fbf","#8a8a8a","#333333"
# Lage der Teile in Z: Explosion für die Zeichnung, MONTIERT = Einbaulage
EXPLODE=dict(m3a=10,pcb=22,sp=34,sl=34,br=56,m3b=70,w=72,nut=82,bolt=-40,wr=-20)
MONTIERT=dict(m3a=4.4,pcb=4.4,sp=6,sl=0,br=12,m3b=14,w=14,nut=15,bolt=-7.2,wr=-7.2)
def build(E):
    parts=[]   # (Nummer, Name, Körper, Farbe)
    def add(n,solid,color,name=""): parts.append((n,name,solid,color))

    # 1 Luftbox-Rückseite (vereinfacht): Rahmen mit den beiden mittleren Laschen, Dicke 6,2
    box=WP(-6.2).rect(130,68).extrude(6.2).faces(">Z").workplane().rect(120,58).cutThruAll()
    box=box.union(WP(-6.2).rect(120,3).extrude(6.2)).union(WP(-6.2).rect(3,58).extrude(6.2))
    box=box.union(cyl(6,6.2,0,0,-6.2))
    for sx in(-1,1):
        box=box.union(WP(-6.2).center(sx*(HX+65)/2,0).rect(HX-65+2,13.2).extrude(6.2)).union(cyl(6.6,6.2,sx*HX,0,-6.2))
        box=box.cut(cyl(3.4,8,sx*HX,0,-7))
    add(1,box,GREY)
    add(2,cyl(3,2.5,0,0,-1.5),MAG)                     # Magnet auf dem Wellenende
    for sx in(-1,1):
        for sy in(-1,1):
            add(7,m3screw(sx*PX,sy*PY,E["m3a"],+1),STEEL)        # Platinenseite
            add(4,cyl(2.75,6,sx*PX,sy*PY,E["sp"],1.5),BRASS)     # Abstandshalter
            add(7,m3screw(sx*PX,sy*PY,E["m3b"],-1),STEEL)        # Brückenseite
    pcb=WP(E["pcb"]).rect(23.2,22.7).extrude(1.6)
    for sx in(-1,1):
        for sy in(-1,1): pcb=pcb.cut(cyl(1.8,3,sx*PX,sy*PY,E["pcb"]-0.5))
    add(3,pcb,PCB)
    add(3,WP(E["pcb"]-1.5).rect(5,4).extrude(1.5),DARK)                       # Chip
    for x0 in(-6.6,6.6):
        add(3,WP(E["pcb"]+1.6).center(x0,0).rect(2.5,10.2).extrude(2.5),DARK) # Stiftleisten
    add(5,B.make().translate((0,0,E["br"])),ALU)
    for sx in(-1,1):
        x=sx*HX
        add(6,cyl(5,12,x,0,E["sl"],2.65),STEEL)                 # Distanzhülse
        add(9,cyl(5,1,x,0,E["w"],2.65),STEEL)                  # Scheibe außen
        add(10,hexnut(8,5,x,0,E["nut"],2.5),STEEL)              # Ganzmetall-Sicherungsmutter
        add(9,cyl(5,1,x,0,E["wr"],2.65),STEEL)                 # Scheibe hinten
        add(8,hexbolt(x,0,E["bolt"],30,+1),STEEL)               # M5 × 30, Kopf hinter der Lasche

    return parts

parts=build(EXPLODE)
E=EXPLODE

# ---- Rendern ----
light=np.array([0.4,-0.6,0.7]); light/=np.linalg.norm(light)
def mapv(v): return (v[0],v[2],v[1])          # Modell (x,y,z) -> Plot (x, Tiefe, hoch)
polys,cols=[],[]
for n,_,s,c in parts:
    verts,tris=s.val().tessellate(0.15,0.3)
    V=np.array([mapv((p.x,p.y,p.z)) for p in verts])
    rgb=np.array(matplotlib.colors.to_rgb(c))
    for t in tris:
        tri=V[list(t)]
        nrm=np.cross(tri[1]-tri[0],tri[2]-tri[0]); ln=np.linalg.norm(nrm)
        if ln==0: continue
        k=0.45+0.55*abs(np.dot(nrm/ln,light))
        polys.append(tri); cols.append(np.clip(rgb*k,0,1))
MM=1/25.4
fig=plt.figure(figsize=(297*MM,210*MM))
ax=fig.add_axes([-0.04,0.10,0.78,0.86],projection="3d")
pc=Poly3DCollection(polys,facecolors=cols,edgecolors="none",linewidths=0)
ax.add_collection3d(pc)
xr,yr,zr=(-85,85),(-45,88),(-36,36)
ax.set_xlim(*xr); ax.set_ylim(*yr); ax.set_zlim(*zr)
ax.set_box_aspect((xr[1]-xr[0],yr[1]-yr[0],zr[1]-zr[0]))
ax.view_init(elev=24,azim=122); ax.set_proj_type("ortho"); ax.axis("off")
# Montageachsen
for x in(-HX,HX):
    ax.plot([x,x],[E["bolt"]-4,E["nut"]+8],[0,0],color="k",lw=0.5,ls=(0,(6,2,1,2)))
for sx in(-1,1):
    for sy in(-1,1):
        ax.plot([sx*PX]*2,[E["m3a"]-4,E["m3b"]+4],[sy*PY]*2,color="k",lw=0.4,ls=(0,(6,2,1,2)))
ax.plot([0,0],[-6,E["m3b"]+6],[0,0],color="k",lw=0.4,ls=(0,(6,2,1,2)))
# Positionsnummern
def balloon(n,p,ang,dist=48):
    x2,y2,_=proj3d.proj_transform(p[0],p[1],p[2],ax.get_proj())
    off=(dist*math.cos(math.radians(ang)),dist*math.sin(math.radians(ang)))
    ax.annotate(str(n),xy=(x2,y2),xytext=off,textcoords="offset points",fontsize=9,weight="bold",ha="center",va="center",
                bbox=dict(boxstyle="circle,pad=0.3",fc="white",ec="k",lw=0.6),arrowprops=dict(arrowstyle="-",lw=0.5))
# Punkte in Plot-Koordinaten (x, Tiefe, hoch); Winkel = Richtung der Nummer
balloon(1,(-55,-3,-29),-60)
balloon(2,(0,1,-3),-110,70)
balloon(3,(-11.6,E["pcb"],11),95,60)
balloon(4,(PX,E["sp"]+3,-PY-2.75),-95,70)
balloon(5,(-40,E["br"]+2,-4),-75)
balloon(6,(-HX,E["sl"]+6,5),100)
balloon(7,(-PX,E["m3b"],-PY-2.8),-150,75)
balloon(8,(HX,E["bolt"]-1.5,4),60)
balloon(9,(-HX,E["wr"]+0.5,5),75)
balloon(9,(-HX,E["w"]+0.5,5),120)
balloon(10,(-HX,E["nut"]+2.5,-4.6),-120)
# Texte
fig.text(0.03,0.955,"Sensorbrücke AS5600 – Montage (Explosionsdarstellung)",fontsize=14,weight="bold")
fig.text(0.03,0.925,"Blick schräg auf die Rückseite der Luftbox · Teile entlang der Montageachsen auseinandergezogen",fontsize=8.5,color="#444")
legend=[("1","Luftbox-Rückseite, mittlere Laschen (6,2 dick, Ø6,8)","vorhanden"),
("2","Magnet Ø6 × 2,5, mittig auf dem Wellenende","vorhanden"),
("3","AS5600-Platine, Chip zur Welle","1"),
("4","Abstandshalter M3 × 6, innen/innen, Messing","4"),
("5","Sensorbrücke, Alu 2 mm (RNX-S-001)","1"),
("6","Distanzhülse 12, Ø10/5,3","2"),
("7","ISO 7380 M3 × 5 – A2","8"),
("8","ISO 4017 M5 × 30 – A2","2"),
("9","Scheibe ISO 7089 – 5 – A2","4"),
("10","Ganzmetall-Sicherungsmutter ISO 7042 M5 – A2","2")]
x0,y0=0.70,0.86
fig.text(x0,y0+0.03,"Teileliste",fontsize=10,weight="bold")
fig.text(x0,y0,"Pos.   Benennung",fontsize=7.5,weight="bold"); fig.text(0.985,y0,"Stk.",fontsize=7.5,weight="bold",ha="right")
for i,(p,b,s) in enumerate(legend):
    y=y0-0.033*(i+1)
    fig.text(x0+0.008,y,p,fontsize=7.5,ha="center"); fig.text(x0+0.03,y,b,fontsize=7.2); fig.text(0.985,y,s,fontsize=7.5,ha="right")
steps=["1  Platine (3) mit 4× M3 × 5 (7) an die vier Abstandshalter (4) schrauben,",
"    Chip-Seite zu den Schraubenköpfen (zeigt später zur Welle).",
"2  Abstandshalter mit 4× M3 × 5 (7) von außen an der Brücke (5) befestigen,",
"    Stiftleisten durch das Fenster, Stiftreihen senkrecht.",
"3  Dupont-Kabel durch das Fenster auf die Stiftleisten stecken.",
"4  Je Seite: Schraube M5 × 30 (8) mit Scheibe (9) von hinten durch die Lasche (1),",
"    Distanzhülse (6) aufschieben, Brücke aufsetzen, Scheibe (9), Mutter (10) handfest.",
"5  Brücke ausrichten: Chip mittig über dem Magneten (2), dann Muttern anziehen.",
"6  Feldstärke prüfen (MD/ML/MH), ggf. Spalt mit M3-Scheiben unter den",
"    Abstandshaltern verkleinern, Nullpunkt neu setzen."]
fig.text(0.03,0.135,"Montageschritte",fontsize=10,weight="bold")
for i,s in enumerate(steps[:5]): fig.text(0.03,0.11-i*0.022,s,fontsize=7.6)
for i,s in enumerate(steps[5:]): fig.text(0.5,0.11-i*0.022,s,fontsize=7.6)
fig.savefig("sensorbruecke-as5600-montage.png",dpi=200)
fig.savefig("sensorbruecke-as5600-montage.pdf")

# ---- 3D-Modelle: STEP (CAD) und GLB (Betrachter), montiert und als Explosion ----
NAMEN={1:"Luftbox_Rueckseite",2:"Magnet",3:"AS5600_Platine",4:"Abstandshalter_M3x6",5:"Sensorbruecke",
       6:"Distanzhuelse_12",7:"ISO7380_M3x5",8:"ISO4017_M5x30",9:"Scheibe_ISO7089_5",10:"Mutter_ISO7042_M5"}
for tag,E_ in (("montiert",MONTIERT),("explosion",EXPLODE)):
    assy=cq.Assembly(name="sensorbruecke_as5600_"+tag)
    cnt={}
    for n,_,solid,c in build(E_):
        cnt[n]=cnt.get(n,0)+1
        assy.add(solid,name=f"{n:02d}_{NAMEN[n]}_{cnt[n]}",color=cq.Color(*matplotlib.colors.to_rgb(c)))
    assy.save(f"sensorbruecke-as5600-baugruppe-{tag}.step")
    assy.save(f"sensorbruecke-as5600-baugruppe-{tag}.glb")
    # STL: alle Teile als ein Netz
    comp=cq.Compound.makeCompound([solid.val() for _,_,solid,_ in build(E_)])
    cq.exporters.export(cq.Workplane().add(comp),f"sensorbruecke-as5600-baugruppe-{tag}.stl",tolerance=0.05,angularTolerance=0.2)
