# Fertigungszeichnung A4 quer, Maßstab 1:1, 2 Blätter (Stil wie Bauteil H):
# Blatt 1 Ansichten, Blatt 2 Montage und Hinweise. Schriftfeld nach ISO 7200,
# Projektionsmethode 1 (E). Kontur aus bruecke.py.
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.backends.backend_pdf import PdfPages
import bruecke as B

W,H=297,210
MM=1/25.4
plt.rcParams["font.family"]="DejaVu Sans"
THICK,THIN=0.5/0.3528,0.25/0.3528   # Linienbreite mm -> pt
CENTER=dict(ls=(0,(12,3,2,3)))
HIDDEN=dict(ls=(0,(4,2)))
ax=None

def new_sheet():
    global ax
    fig=plt.figure(figsize=(W*MM,H*MM))
    ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis("off")
    return fig
def L(x,y,lw=THIN,**k): ax.plot(x,y,'k',lw=lw,solid_capstyle="butt",**k)
def T(x,y,s,fs=3.5,ha="left",va="baseline",w="normal",rot=0):
    ax.text(x,y,s,fontsize=fs/0.3528,ha=ha,va=va,weight=w,rotation=rot)

def draw_frame():
    x0,y0,x1,y1=20,10,287,200
    ax.add_patch(plt.Rectangle((x0,y0),x1-x0,y1-y0,fill=False,lw=0.7/0.3528))
    nx,ny=6,4
    for i in range(nx+1):
        x=x0+i*(x1-x0)/nx; L([x,x],[y0-5,y0]); L([x,x],[y1,y1+5])
    for i in range(nx):
        xc=x0+(i+0.5)*(x1-x0)/nx
        T(xc,y1+1.5,str(i+1),3.5,"center"); T(xc,y0-4,str(i+1),3.5,"center")
    for j in range(ny+1):
        y=y0+j*(y1-y0)/ny; L([x0-5,x0],[y,y]); L([x1,x1+5],[y,y])
    for j in range(ny):
        yc=y1-(j+0.5)*(y1-y0)/ny
        T(x0-2.5,yc-1.2,"ABCD"[j],3.5,"center"); T(x1+2.5,yc-1.2,"ABCD"[j],3.5,"center")
    for (a,b) in [((x0+x1)/2,y0),((x0+x1)/2,y1)]: L([a,a],[b-5,b+5],lw=THICK)
    for (a,b) in [(x0,(y0+y1)/2),(x1,(y0+y1)/2)]: L([a-5,a+5],[b,b],lw=THICK)

def box(x,y,w,h,label,val,vfs=3.8,bold=False):
    ax.add_patch(plt.Rectangle((x,y),w,h,fill=False,lw=THIN))
    T(x+0.8,y+h-2.2,label,1.9)
    T(x+0.8,y+1.4,val,vfs,w="bold" if bold else "normal")

def title_block(blatt,zusatz):
    tx,ty0,tw=107,10,180
    y=ty0+48
    box(tx,y,108,8,"Werkstoff","EN AW-5754 H22 (AlMg3), Blech t = 2")
    box(tx+108,y,24,8,"Masse","≈ 8 g")
    box(tx+132,y,20,8,"Maßstab","1:1")
    box(tx+152,y,28,8,"Projektion","")
    px,py=tx+163,y+3.5
    L([px-6,px-1.5,px-1.5,px-6,px-6],[py-1,py-2.2,py+2.2,py+1,py-1])
    ax.add_patch(Circle((px+3.5,py),2.2,fill=False,lw=THIN)); ax.add_patch(Circle((px+3.5,py),1.0,fill=False,lw=THIN))
    L([px-7,px+7],[py,py],lw=THIN*0.7,**CENTER)
    y=ty0+40
    box(tx,y,64,8,"Allgemeintoleranzen","ISO 2768-mK")
    box(tx+64,y,68,8,"Werkstückkanten","ISO 13715  −0,3")
    box(tx+132,y,48,8,"Oberfläche","walzblank, entgratet",3.4)
    y=ty0+32
    box(tx,y,56,8,"Rechtlicher Eigentümer","Nico · Projekt RIKA PID Regler",3.0)
    box(tx+56,y,44,8,"Dokumentart","Fertigungszeichnung",3.4)
    box(tx+100,y,32,8,"Dokumentstatus","Entwurf",3.4)
    box(tx+132,y,48,8,"Sachnummer","RNX-S-001",4.6,True)
    y=ty0+24
    box(tx,y,56,8,"Technische Referenz","sensorbruecke-as5600.step",3.0)
    box(tx+56,y,76,8,"Titel, Zusatztitel","Sensorbrücke AS5600",5.0,True)
    box(tx+132,y,24,8,"Änderungsindex","A")
    box(tx+156,y,24,8,"Ausgabedatum","2026-11-06",3.2)
    y=ty0+16
    box(tx,y,56,8,"Erstellt durch","Claude (KI) für Nico",3.4)
    box(tx+56,y,76,8,"",zusatz,3.4)
    box(tx+132,y,24,8,"Sprache","de")
    box(tx+156,y,24,8,"Blatt",blatt)
    y=ty0+8
    box(tx,y,56,8,"Genehmigt von","")
    box(tx+56,y,76,8,"Abteilung","RIKA NEX Luftregelung",3.4)
    box(tx+132,y,48,8,"Format","A4")
    ax.add_patch(plt.Rectangle((tx,ty0+8),tw,48,fill=False,lw=THICK))

AR=dict(arrowstyle="<|-|>,head_length=0.9,head_width=0.25",lw=THIN,color="k",shrinkA=0,shrinkB=0)
AR1=dict(arrowstyle="-|>,head_length=0.9,head_width=0.25",lw=THIN,color="k",shrinkA=0,shrinkB=0)
def dimh(xa,xb,yra,yrb,y,txt):
    s=1 if y>max(yra,yrb) else -1
    L([xa,xa],[yra+s*1,y+s*1.5]); L([xb,xb],[yrb+s*1,y+s*1.5])
    ax.annotate("",(xa,y),(xb,y),arrowprops=AR)
    T((xa+xb)/2,y+0.8,txt,3.5,"center")
def dimv(ya,yb,xra,xrb,x,txt):
    s=1 if x>max(xra,xrb) else -1
    L([xra+s*1,x+s*1.5],[ya,ya]); L([xrb+s*1,x+s*1.5],[yb,yb])
    ax.annotate("",(x,ya),(x,yb),arrowprops=AR)
    T(x-0.9,(ya+yb)/2,txt,3.5,"right","center",rot=90)
def leader(xp,yp,xt,yt,txt,left=False):
    ax.annotate("",(xp,yp),(xt,yt),arrowprops=AR1)
    w=len(txt)*2.0
    xe=xt-w if left else xt+w
    L([xt,xe],[yt,yt]); T(min(xt,xe)+0.5,yt+0.8,txt,3.5)
def cross(x,y,l):
    L([x-l,x+l],[y,y],**CENTER); L([x,x],[y-l,y+l],**CENTER)

HX,PX,PY,WX,WY,PL,BW,EYE=B.HX,B.PX,B.PY,B.WX,B.WY,B.PL,B.BW,B.EYE
pdf=PdfPages("sensorbruecke-as5600-zeichnung-iso.pdf")
pngs=[]

# ===================== Blatt 1: Ansichten =====================
fig=new_sheet(); draw_frame()
fx,fy=120,152
face=B.make().faces("<Z").val()
for wire in face.Wires():
    for e in wire.Edges():
        n=max(2,int(e.Length()/0.25))
        p=[e.positionAt(i/(n-1)) for i in range(n)]
        L([fx+q.x for q in p],[fy+q.y for q in p],lw=THICK)
L([fx-HX-EYE/2-4,fx+HX+EYE/2+4],[fy,fy],**CENTER)
L([fx,fx],[fy-PL/2-4,fy+PL/2+4],**CENTER)
for sx in(-1,1):
    L([fx+sx*HX]*2,[fy-EYE/2-3,fy+EYE/2+3],**CENTER)
    for sy in(-1,1): cross(fx+sx*PX,fy+sy*PY,2.8)
dimh(fx-PL/2,fx+PL/2,fy+PL/2,fy+PL/2,fy+PL/2+15,"24")
dimh(fx-PX,fx+PX,fy+PY,fy+PY,fy+PL/2+7,"16,1")
dimh(fx-WX/2,fx+WX/2,fy-WY/2,fy-WY/2,fy-PL/2-6,"17")
dimh(fx-HX,fx+HX,fy,fy,fy-PL/2-14,"147")
dimh(fx-HX-EYE/2,fx+HX+EYE/2,fy,fy,fy-PL/2-22,"161")
dimv(fy-PY,fy+PY,fx-PX,fx-PX,fx-PL/2-6,"16,3")
dimv(fy-WY/2,fy+WY/2,fx+WX/2,fx+WX/2,fx+PL/2+5,"11")
dimv(fy-PL/2,fy+PL/2,fx+PL/2,fx+PL/2,fx+PL/2+12,"24")
xs=fx-42
ax.annotate("",(xs,fy+BW/2),(xs,fy+BW/2+6),arrowprops=AR1)
ax.annotate("",(xs,fy-BW/2),(xs,fy-BW/2-6),arrowprops=AR1)
L([xs,xs],[fy+BW/2+6,fy+BW/2+8]); T(xs-1,fy+BW/2+3,"8",3.5,"right")
leader(fx+HX+EYE/2*math.cos(math.radians(60)),fy+EYE/2*math.sin(math.radians(60)),fx+HX+2,fy+16,"2× R7")
leader(fx-HX+5.5/2*math.cos(math.radians(120)),fy+5.5/2*math.sin(math.radians(120)),fx-HX+6,fy+16,"2× Ø5,5")
a=math.radians(45)
leader(fx+PX+1.6*math.cos(a),fy+PY+1.6*math.sin(a),fx+26,fy+26,"4× Ø3,2")
leader(fx+WX/2-0.45,fy-WY/2+0.45,fx+30,fy-16,"4× R1,5")
leader(fx+PL/2-0.6,fy-PL/2+0.6,fx+40,fy-24,"R2 (alle Ecken, Übergänge)")
T(fx,fy-PL/2-31,"Vorderansicht",4.5,"center")
# Ansicht von links (rechts daneben, Methode 1)
lx=fx+HX+EYE/2+30
L([lx,lx+2,lx+2,lx,lx],[fy-PL/2,fy-PL/2,fy+PL/2,fy+PL/2,fy-PL/2],lw=THICK)
for yc in(-PY,PY):
    for s in(-1,1): L([lx,lx+2],[fy+yc+s*1.6]*2,**HIDDEN)
    L([lx-3,lx+5],[fy+yc]*2,**CENTER)
for s in(-1,1): L([lx,lx+2],[fy+s*WY/2]*2,**HIDDEN)
L([lx-3,lx+5],[fy,fy],**CENTER)
ax.annotate("",(lx,fy+PL/2+5),(lx-6,fy+PL/2+5),arrowprops=AR1)
ax.annotate("",(lx+2,fy+PL/2+5),(lx+8,fy+PL/2+5),arrowprops=AR1)
L([lx,lx],[fy+PL/2+1,fy+PL/2+6.5]); L([lx+2,lx+2],[fy+PL/2+1,fy+PL/2+6.5])
T(lx+9,fy+PL/2+4,"2",3.5)
T(lx+1,fy-PL/2-31,"Ansicht von links",4.5,"center")
# Draufsicht (unter der Vorderansicht)
ty=82
L([fx-HX-EYE/2,fx+HX+EYE/2,fx+HX+EYE/2,fx-HX-EYE/2,fx-HX-EYE/2],[ty,ty,ty+2,ty+2,ty],lw=THICK)
for xc,d in [(-HX,5.5),(HX,5.5),(-PX,3.2),(PX,3.2)]:
    for s in(-1,1): L([fx+xc+s*d/2]*2,[ty,ty+2],**HIDDEN)
    L([fx+xc]*2,[ty-3,ty+5],**CENTER)
for s in(-1,1): L([fx+s*WX/2]*2,[ty,ty+2],**HIDDEN)
T(fx,ty-10,"Draufsicht",4.5,"center")
# Kontrollmaß und Kurzhinweise
L([25,75],[56,56],lw=THICK); L([25,25],[54.5,57.5]); L([75,75],[54.5,57.5])
T(25,59,"Kontrolle 50 mm (Druck 100 %)",3.0)
T(25,46,"Hinweise",3.8,w="bold")
for i,n in enumerate(["1 Zuschnitt nach DXF oder 1:1-Ausdruck.",
                      "2 Fenster: Ecken Ø3 vorbohren, aussägen,","   auf 17 × 11 feilen, entgraten.",
                      "3 Montage siehe Blatt 2."]):
    T(25,41-i*4.6,n,3.0)
title_block("1/2","Fertigteil, eben – Ansichten")
pdf.savefig(fig); fig.savefig("_b1.png",dpi=150); plt.close(fig)

# ===================== Blatt 2: Montage =====================
fig=new_sheet(); draw_frame()
# Schnitt durch die Wellenmitte (schematisch, Maßstab 2,5:1), Box links
k=2.5; ox,oy=45,138
def R(d,w): return ox+d*k, oy+w*k
def rect(d1,w1,d2,w2,lw=THICK,hatch=False,fill=None,ls="-"):
    (xa,ya),(xb,yb)=R(d1,w1),R(d2,w2)
    ax.add_patch(plt.Rectangle((min(xa,xb),min(ya,yb)),abs(xb-xa),abs(yb-ya),fill=fill is not None,
                 facecolor=fill if fill else "none",edgecolor="k",lw=lw,ls=ls,hatch="////" if hatch else None))
T(25,192,"Schnitt durch die Wellenmitte, schematisch 2,5:1 (Blick von oben)",3.2)
rect(-6,-20,0,20,hatch=True)                       # Luftbox, Stirnseite
rect(-1.5,-3,1,3,lw=THIN,fill="#bbbbbb")           # Magnet, Oberfläche 1 vor Laschenebene
rect(2.9,-2.5,4.4,2.5,lw=THIN,fill="#555555")      # Chip
rect(4.4,-11.6,6.0,11.6)                           # Platine
for w in(-8.05,8.05): rect(6.0,w-2.5,12.0,w+2.5,lw=THIN,ls=(0,(4,2)))   # Abstandshalter (außerhalb Schnitt)
rect(12,8.5,14,20,fill="#dddddd"); rect(12,-20,14,-8.5,fill="#dddddd")  # Brücke, Fenster ±8,5
for w in(-6.6,6.6): L([R(6.0,w)[0],R(20,w)[0]],[R(0,w)[1]]*2,lw=THIN)  # Stiftleisten
L([R(0,0)[0]]*2,[R(0,-24)[1],R(0,23)[1]],**CENTER)
L([R(-8,0)[0],R(22,0)[0]],[oy,oy],**CENTER)
def dd(d1,d2,y,txt,tx=None):
    (xa,_),(xb,_)=R(d1,0),R(d2,0)
    for x in(xa,xb): L([x,x],[R(0,-20)[1]-1,y-1.5])
    ax.annotate("",(xa,y),(xb,y),arrowprops=AR)
    T(tx if tx else (xa+xb)/2,y-4.6,txt,3.0,"center")
y0=R(0,-20)[1]
dd(0,1,y0-6,"1",R(0,0)[0]-3)
dd(1,2.9,y0-6,"≈1,9",R(2,0)[0]+3)
dd(6,12,y0-6,"6")
dd(0,12,y0-16,"12 = Hülsenlänge")
def lab(d,w,yt,txt):
    x,y=R(d,w); xt=110
    ax.annotate("",(x,y),(xt,yt),arrowprops=AR1); L([xt,xt+len(txt)*1.75],[yt,yt]); T(xt+0.5,yt+0.8,txt,3.0)
lab(13,17,184,"Brücke t = 2")
lab(9,10,176,"Abstandshalter M3 × 6")
lab(17,6.6,168,"Stiftleiste durch Fenster")
lab(0.4,2.0,160,"Magnet Ø6 × 2,5, verklebt")
lab(3.6,-1.5,152,"Chip AS5600 zur Welle")
lab(5.2,-10,144,"Platine 1,6")
lab(-3,-17,128,"Luftbox, Laschenebene")
# Hinweise Montage
hx,hy=110,112
T(hx,hy,"Hinweise Montage",3.8,w="bold")
notes=["1 Lochabstand 147 an den mittleren Laschen (Ø6,8) geprüft (Nico, 06.11.2026).",
"2 Je Seite: ISO 4017 M5 × 30 – A2-70 (Lasche 6,2 dick), Distanzhülse Ø10/5,3 × 12 zwischen",
"   Lasche und Brücke, 2× Scheibe ISO 7089 – 5, Ganzmetall-Sicherungsmutter ISO 7042 M5 – A2.",
"3 Platine auf der Box-Seite, Chip zur Welle: 4× Abstandshalter M3 × 6 innen/innen,",
"   8× ISO 7380 M3 × 5 – A2, Abstandshalter Messing. Lochbild 16,1 × 16,3 prüfen.",
"4 Spalt kleiner: Scheibe M3 zwischen Abstandshalter und Brücke (je ≈ 0,5); zulässig 0,5…3.",
"5 Vor dem Anziehen Chip mittig über dem Magneten ausrichten (Spiel ≈ ±0,6).",
"6 Danach Feldstärke (MD/ML/MH) prüfen und Nullpunkt neu setzen."]
for i,n in enumerate(notes): T(hx,hy-5-i*4.2,n,2.8)
title_block("2/2","Montage und Hinweise")
pdf.savefig(fig); fig.savefig("_b2.png",dpi=150); plt.close(fig)
pdf.close()
