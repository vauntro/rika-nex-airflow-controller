import math, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Arc
from matplotlib.backends.backend_pdf import PdfPages
MM=1/25.4
HX,BW,PL,EYE=73.5,8.0,24.0,14.0
PX,PY=8.05,8.15; WX,WY=17.0,11.0
def draw(ax,ox,oy,lw=0.35):
    # Kontur direkt aus dem CAD-Modell (bruecke.py), damit Zeichnung und Modell übereinstimmen
    import bruecke
    face=bruecke.make().faces("<Z").val()
    for wire in face.Wires():
        for e in wire.Edges():
            n=max(2,int(e.Length()/0.3))
            pts=[e.positionAt(i/(n-1)) for i in range(n)]
            ax.plot([ox+p.x for p in pts],[oy+p.y for p in pts],'k',lw=lw*2)
    def cm(x,y,l=3):
        ax.plot([x-l,x+l],[y,y],'k',lw=0.2); ax.plot([x,x],[y-l,y+l],'k',lw=0.2)
    for sx in(-1,1):
        cm(ox+sx*HX,oy,4.5)
        for sy in(-1,1): cm(ox+sx*PX,oy+sy*PY,2.5)
    ax.plot([ox-HX-12,ox+HX+12],[oy,oy],'k',lw=0.2,ls=(0,(8,2,1,2)))
    ax.plot([ox,ox],[oy-18,oy+18],'k',lw=0.2,ls=(0,(8,2,1,2)))
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
dim(ax,ox-HX-EYE/2,oy,ox+HX+EYE/2,oy,"161",-27)
dim(ax,ox-HX,oy,ox+HX,oy,"147 (Lochmitte)",-21)
dim(ax,ox-PL/2,oy+PL/2,ox+PL/2,oy+PL/2,"24",14)
dim(ax,ox-PX,oy+PY,ox+PX,oy+PY,"16,1",7,fs=6.5)
dim(ax,ox+PL/2,oy-PL/2,ox+PL/2,oy+PL/2,"24",10,horiz=False)
dim(ax,ox-PX,oy-PY,ox-PX,oy+PY,"16,3",-9,horiz=False)
dim(ax,ox-40,oy-BW/2,ox-40,oy+BW/2,"8",-4,horiz=False)
ax.text(ox+HX-6,oy+12,"2× Ø 5,5 (M5)",fontsize=7)
ax.text(ox+14,oy+19,"4× Ø 3,2 (M3, Platine AS5600)",fontsize=7)
ax.text(ox-HX-12,oy+10,"Auge Ø 14",fontsize=7)
ax.text(ox-38,oy+16,"Ecken und Übergänge R 2",fontsize=7,ha="right")
ax.annotate("Fenster 17 × 11, Ecken R 1,5\n(Ecken Ø 3 vorbohren, aussägen, feilen)",(ox-4,oy-4),(ox-75,oy+30),fontsize=6.5,arrowprops=dict(arrowstyle="-",lw=0.3))
# title block
ax.text(12,198,"Sensorbrücke AS5600 – Rückseite Luftbox",fontsize=13,weight="bold")
ax.text(12,191,"Werkstoff: Alu-Blech 2 mm · Maßstab 1:1 (A4 quer, ohne Seitenanpassung drucken) · Maße in mm · Stand 06.11.2026",fontsize=7.5)
# scale check
ax.plot([12,62],[86,86],'k',lw=0.8); [ax.plot([x,x],[85,87],'k',lw=0.8) for x in range(12,63,10)]
ax.text(12,88,"Prüfmaß 50 mm (beim Ausdruck nachmessen)",fontsize=6.5)
notes=["Aufbau (von der Box aus): Lasche · Distanzhülse 12 mm · Brücke 2 mm · Scheibe · Mutter, Schraube ISO 4017 M5 × 30, Mutter DIN 985",
"Laschenlöcher Ø 6,8 geben ca. ±0,6 mm Spiel: Brücke beim Anziehen so ausrichten, dass das Fenster mittig über der Welle sitzt.",
"Platine mit Chip zur Welle auf der Box-Seite der Brücke, 4 Abstandshalter M3 × 6 (Innen/Innen), Schrauben M3 × 5.",
"Stack: Magnet 1 vor Laschenebene + Luftspalt ca. 1,9 + Chip 1,5 + Platine 1,6 + Abstandshalter 6 = 12 (Hülsenlänge).",
"Luftspalt einstellen: Scheibe M3 zwischen Abstandshalter und Brücke verkleinert den Spalt (je ca. 0,5 mm); Abstandshalter 5 mm → Spalt ca. 2,9 mm.",
"AS5600 arbeitet mit Spalt ca. 0,5–3 mm; Feldstärke nach Montage per Firmware prüfen (Status MD/ML/MH).",
"Fenster: Dupont-Stecker der Stiftleisten (Stifte zeigen von der Welle weg) gehen nach hinten durch. Platinenlage: Stiftreihen senkrecht."]
for i,n in enumerate(notes): ax.text(12,70-i*6.2,"• "+n,fontsize=6.6)
ax.add_patch(plt.Rectangle((6,6),285,198,fill=False,lw=0.6))
fig.savefig("sensorbruecke-as5600-zeichnung.pdf"); fig.savefig("sensorbruecke-as5600-zeichnung.png",dpi=200)
