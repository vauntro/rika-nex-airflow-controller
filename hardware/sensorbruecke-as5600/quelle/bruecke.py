import cadquery as cq
T=2.0          # Blechdicke
HX=73.5        # halber Lochabstand Laschen (147)
BW=8.0         # Breite Steg
EYE=14.0       # Auge um die M5-Bohrung
PL=24.0        # Mittelplatte
HM5=5.5        # Bohrung M5
HM3=3.2        # Bohrung M3
PX,PY=16.1/2,16.3/2   # Platinenlöcher
WX,WY=17.0,11.0       # Fenster
R=2.0          # Radius Außenecken und Übergänge

def make():
    b=cq.Workplane("XY").rect(2*HX,BW).extrude(T)
    b=b.union(cq.Workplane("XY").pushPoints([(-HX,0),(HX,0)]).circle(EYE/2).extrude(T))
    b=b.union(cq.Workplane("XY").rect(PL,PL).extrude(T))
    # Außenecken der Platte und Übergänge Steg/Auge, Steg/Platte runden
    b=b.edges("|Z").fillet(R)
    b=b.faces(">Z").workplane().pushPoints([(-HX,0),(HX,0)]).hole(HM5)
    b=b.faces(">Z").workplane().pushPoints([(sx*PX,sy*PY) for sx in(-1,1) for sy in(-1,1)]).hole(HM3)
    b=b.faces(">Z").workplane().rect(WX,WY).cutThruAll()
    b=b.edges("|Z").edges(cq.selectors.BoxSelector((-WX/2-0.1,-WY/2-0.1,-1),(WX/2+0.1,WY/2+0.1,5))).fillet(1.5)
    return b

if __name__=="__main__":
    b=make()
    cq.exporters.export(b,"sensorbruecke-as5600.step")
    cq.exporters.export(b,"sensorbruecke-as5600.stl",tolerance=0.02,angularTolerance=0.1)
    cq.exporters.export(b.section(T/2),"sensorbruecke-as5600.dxf")
    bb=b.val().BoundingBox(); print(bb.xlen,bb.ylen,bb.zlen, b.val().Volume())
