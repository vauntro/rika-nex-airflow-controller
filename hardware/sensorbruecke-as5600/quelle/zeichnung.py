import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc
from matplotlib.backends.backend_pdf import PdfPages
MM=1/25.4
HX,BW,PL=73.5,16.0,32.0
PX,PY=8.05,8.15; WX,WY=17.0,11.0
def draw(ax,ox,oy,lw=0.35):
    r=BW/2
    # outline: stadium bar + plate (draw as union by path)
    import numpy as np
    pts=[]
    # start top-left of bar at plate
    def arc(cx,cy,rad,a0,a1,n=40):
        return [(cx+rad*math.cos(math.radians(a)),cy+rad*math.sin(math.radians(a))) for a in np.linspace(a0,a1,n)]
    c=2.0;h=PL/2
    pts+= [(-h,r)]
    pts+= [(-h,h-c)]+arc(-h+c,h-c,c,180,90)[1:]
    pts+= [(h-c,h)]+arc(h-c,h-c,c,90,0)[1:]
    pts+= [(h,r),(HX,r)]+arc(HX,0,r,90,-90)[1:]
    pts+= [(h,-r),(h,-h+c)]+arc(h-c,-h+c,c,0,-90)[1:]
    pts+= [(-h+c,-h)]+arc(-h+c,-h+c,c,270,180)[1:]
    pts+= [(-h,-r),(-HX,-r)]+arc(-HX,0,r,-90,-270)[1:]
    pts.append(pts[0])
    xs=[ox+p[0] for p in pts]; ys=[oy+p[1] for p in pts]
    ax.plot(xs,ys,'k',lw=lw*2)
    for sx in(-1,1):
        ax.add_patch(Circle((ox+sx*HX,oy),5.5/2,fill=False,lw=lw*2))
        for sy in(-1,1):
            ax.add_patch(Circle((ox+sx*PX,oy+sy*PY),3.2/2,fill=False,lw=lw*2))
    ax.add_patch(FancyBboxPatch((ox-WX/2+1.5,oy-WY/2+1.5),WX-3,WY-3,boxstyle="round,pad=1.5",fill=False,lw=lw*2))
    # center marks
    def cm(x,y,l=3):
        ax.plot([x-l,x+l],[y,y],'k',lw=0.2); ax.plot([x,x],[y-l,y+l],'k',lw=0.2)
    for sx in(-1,1):
        cm(ox+sx*HX,oy,4.5)
        for sy in(-1,1): cm(ox+sx*PX,oy+sy*PY,2.5)
    ax.plot([ox-HX-12,ox+HX+12],[oy,oy],'k',lw=0.2,ls=(0,(8,2,1,2)))
    ax.plot([ox,ox],[oy-22,oy+22],'k',lw=0.2,ls=(0,(8,2,1,2)))
def dim(ax,x1,y1,x2,y2,txt,off,horiz=True,fs=7):
    if horiz:
        y=y1+off
        ax.plot([x1,x1],[y1,y+ (1 if off>0 else -1)],'k',lw=0.2); ax.plot([x2,x2],[y2,y+(1 if off>0 else -1)],'k',lw=0.2)
        ax.annotate("",(x1,y),(x2,y),arrowprops=dict(arrowstyle="<->",lw=0.35,shrinkA=0,shrinkB=0))
        ax.text((x1+x2)/2,y+0.8,txt,ha="center",va="bottom",fontsize=fs)
    else:
        x=x1+off
        ax.plot([x1,x+(1 if off>0 else -1)],[y1,y1],'k',lw=0.2); ax.plot([x2,x+(1 if off>0 else -1)],[y2,y2],'k',lw=0.2)
        ax.annotate("",(x,y1),(x,y2),arrowprops=dict(arrowstyle="<->",lw=0.35,shrinkA=0,shrinkB=0))
        ax.text(x+(0.8 if off>0 else -0.8),(y1+y2)/2,txt,ha="left" if off>0 else "right",va="center",fontsize=fs,rotation=0)
fig=plt.figure(figsize=(297*MM,210*MM))
ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,297); ax.set_ylim(0,210); ax.axis("off")
ox,oy=148.5,128
draw(ax,ox,oy)
dim(ax,ox-HX-8,oy,ox+HX+8,oy,"163",-27)
dim(ax,ox-HX,oy,ox+HX,oy,"147 (Lochmitte)",-21)
dim(ax,ox-PL/2,oy+PL/2,ox+PL/2,oy+PL/2,"32",14)
dim(ax,ox-PX,oy+PY,ox+PX,oy+PY,"16,1",2.6,fs=6)
dim(ax,ox+PL/2,oy-PL/2,ox+PL/2,oy+PL/2,"32",14,horiz=False)
dim(ax,ox+PX,oy-PY,ox+PX,oy+PY,"16,3",-25,horiz=False)
dim(ax,ox-HX,oy-BW/2,ox-HX,oy+BW/2,"16",-14,horiz=False)
ax.text(ox+HX-6,oy+12,"2× Ø 5,5 (M5)",fontsize=7)
ax.text(ox+18,oy+19,"4× Ø 3,2 (M3, Platine AS5600)",fontsize=7)
ax.text(ox-HX-11,oy+12,"R 8",fontsize=7)
ax.text(ox-34,oy+19,"Ecken R 2",fontsize=7)
ax.annotate("Fenster 17 × 11, Ecken R 1,5\n(Ecken Ø 3 vorbohren, aussägen, feilen)",(ox-4,oy-4),(ox-75,oy+30),fontsize=6.5,arrowprops=dict(arrowstyle="-",lw=0.3))
# title block
ax.text(12,198,"Sensorbrücke AS5600 – Rückseite Luftbox",fontsize=13,weight="bold")
ax.text(12,191,"Werkstoff: Alu-Blech 2 mm · Maßstab 1:1 (A4 quer, ohne Seitenanpassung drucken) · Maße in mm · Stand 06.11.2026",fontsize=7.5)
# scale check
ax.plot([12,62],[86,86],'k',lw=0.8); [ax.plot([x,x],[85,87],'k',lw=0.8) for x in range(12,63,10)]
ax.text(12,88,"Prüfmaß 50 mm (beim Ausdruck nachmessen)",fontsize=6.5)
notes=["Aufbau (von der Box aus): Lasche · Distanzhülse 12 mm · Brücke 2 mm · Scheibe · Mutter, Schraube M5 × 22 bis 25",
"Laschenlöcher Ø 6,8 geben ca. ±0,6 mm Spiel: Brücke beim Anziehen so ausrichten, dass das Fenster mittig über der Welle sitzt.",
"Platine mit Chip zur Welle auf der Box-Seite der Brücke, 4 Abstandshalter M3 × 6 (Innen/Innen), Schrauben M3 × 5.",
"Stack: Magnet 1 vor Laschenebene + Luftspalt ca. 1,9 + Chip 1,5 + Platine 1,6 + Abstandshalter 6 = 12 (Hülsenlänge).",
"Luftspalt einstellen: Scheibe M3 zwischen Abstandshalter und Brücke verkleinert den Spalt (je ca. 0,5 mm); Abstandshalter 5 mm → Spalt ca. 2,9 mm.",
"AS5600 arbeitet mit Spalt ca. 0,5–3 mm; Feldstärke nach Montage per Firmware prüfen (Status MD/ML/MH).",
"Fenster: Dupont-Stecker der Stiftleisten (Stifte zeigen von der Welle weg) gehen nach hinten durch. Platinenlage: Stiftreihen senkrecht."]
for i,n in enumerate(notes): ax.text(12,70-i*6.2,"• "+n,fontsize=6.6)
ax.add_patch(plt.Rectangle((6,6),285,198,fill=False,lw=0.6))
fig.savefig("sensorbruecke-as5600-zeichnung.pdf"); fig.savefig("sensorbruecke-as5600-zeichnung.png",dpi=200)
