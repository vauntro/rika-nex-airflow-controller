#!/usr/bin/env python3
"""Erzeugt den KiCad-Schaltplan der RIKA-NEX-Steuerung.

Aufruf (aus dem Repo-Wurzelverzeichnis):
    python3 hardware/schaltplan/quelle/schaltplan.py

Schreibt nach hardware/schaltplan/:
    rika-nex-steuerung.kicad_sch   Schaltplan (KiCad 7, öffnet auch in KiCad 8/9)
    rika-nex-steuerung.kicad_sym   Projektbibliothek "rika_nex" (Module + Standardbauteile)
    rika-nex-steuerung.kicad_pro   Projektdatei
    sym-lib-table                  Verweis auf die Projektbibliothek

Standardbauteile (R, C, MOSFET, ATtiny, ...) werden aus der installierten
KiCad-Standardbibliothek kopiert (/usr/share/kicad/symbols), die Module (ESP32,
MAX31856, PCA9685, AS5600, USV) sind eigene Symbole.

Verbindungen laufen über Netzlabels und Versorgungssymbole an kurzen
Leitungsstücken an jedem Pin. Pinbelegung wie in
firmware/rika-nex-controller/include/config.h (Zweig esp32dev).
"""
import json
import os
import uuid as uuidlib

from sexpr import Str, dump, find, parse

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
NAME = "rika-nex-steuerung"
LIB = "rika_nex"
KICAD_SYMS = "/usr/share/kicad/symbols"
NS = uuidlib.UUID("6b1c3a52-6f0e-4c35-9d1a-3e7b9a2f4c10")
ROOT_UUID = str(uuidlib.uuid5(NS, "root"))
STUB = 5.08
FONT = [["font", ["size", "1.27", "1.27"]]]


def uid(*key):
    return str(uuidlib.uuid5(NS, "/".join(str(k) for k in key)))


def num(v):
    s = ("%.4f" % v).rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ---------------------------------------------------------------------------
# Symbole aus der KiCad-Standardbibliothek (abgeleitete Symbole aufgelöst)
# ---------------------------------------------------------------------------
_libcache = {}


def stdlib(file):
    if file not in _libcache:
        tree = parse(open(os.path.join(KICAD_SYMS, file + ".kicad_sym")).read())[0]
        _libcache[file] = {x[1]: x for x in find(tree, "symbol")}
    return _libcache[file]


def rename_units(node, old, new):
    for x in node:
        if isinstance(x, list) and x and x[0] == "symbol" and isinstance(x[1], str):
            if x[1].startswith(old + "_"):
                x[1] = Str(new + x[1][len(old):])


def std_symbol(file, name, newname=None):
    syms = stdlib(file)
    node = parse(dump(syms[name]))[0]  # tiefe Kopie
    ext = find(node, "extends")
    if ext:
        parent = std_symbol(file, ext[0][1])
        props = find(node, "property")
        merged = [x for x in parent if not (isinstance(x, list) and x[0] == "property")]
        merged[1] = Str(name)
        # Eigenschaften des abgeleiteten Symbols vor die Untereinheiten setzen
        idx = next(i for i, x in enumerate(merged) if isinstance(x, list) and x[0] == "symbol")
        merged[idx:idx] = props
        rename_units(merged, ext[0][1], name)
        node = merged
    if newname:
        rename_units(node, node[1], newname)
        node[1] = Str(newname)
    return node


# ---------------------------------------------------------------------------
# Eigene Modulsymbole
# ---------------------------------------------------------------------------
def module_symbol(name, ref, value, left, right, width=20.32, desc="", footprint=""):
    """left/right: Listen von (Nummer, Name, Typ) oder None für Leerzeile."""
    rows = max(len(left), len(right))
    h = rows * 2.54 + 2.54
    top = h / 2
    w2 = width / 2
    pins = []
    for side, lst in (("L", left), ("R", right)):
        for i, p in enumerate(lst):
            if p is None:
                continue
            pnum, pname, ptype = p
            y = top - 2.54 - i * 2.54
            x = -w2 - 2.54 if side == "L" else w2 + 2.54
            ang = 0 if side == "L" else 180
            hide = ["hide"] if ptype == "nc" else []
            pins.append(["pin", "no_connect" if ptype == "nc" else ptype, "line",
                         ["at", num(x), num(y), str(ang)], ["length", "2.54"], *hide,
                         ["name", Str(pname), ["effects", *FONT]],
                         ["number", Str(pnum), ["effects", *FONT]]])
    # Raster: Ober-/Unterkante auf 1,27
    def prop(k, v, y, hidden=False):
        eff = ["effects", *FONT] + (["hide"] if hidden else [])
        return ["property", Str(k), Str(v), ["at", "0", num(y), "0"], eff]

    return ["symbol", Str(name), ["pin_names", ["offset", "1.016"]], ["in_bom", "yes"], ["on_board", "yes"],
            prop("Reference", ref, top + 1.27),
            prop("Value", value, -top - 1.27),
            prop("Footprint", footprint, -top - 3.81, True),
            prop("Datasheet", "", -top - 6.35, True),
            prop("ki_description", desc, -top - 8.89, True),
            ["symbol", Str(name + "_0_1"),
             ["rectangle", ["start", num(-w2), num(top)], ["end", num(w2), num(-top)],
              ["stroke", ["width", "0.254"], ["type", "default"]], ["fill", ["type", "background"]]]],
            ["symbol", Str(name + "_1_1"), *pins]]


SYMBOLS = {}


def add_std(file, name, newname=None):
    sym = std_symbol(file, name, newname)
    SYMBOLS[sym[1]] = sym
    return sym[1]


def add_module(*a, **k):
    sym = module_symbol(*a, **k)
    SYMBOLS[sym[1]] = sym
    return sym[1]


def sym_pins(name):
    """Liefert {nummer: (x, y, winkel, name)} in Bibliothekskoordinaten."""
    pins = {}
    for unit in find(SYMBOLS[name], "symbol"):
        for p in find(unit, "pin"):
            at = find(p, "at")[0]
            pnum = find(p, "number")[0][1]
            pname = find(p, "name")[0][1]
            pins[str(pnum)] = (float(at[1]), float(at[2]), int(float(at[3])), str(pname))
    return pins


# ---------------------------------------------------------------------------
# Schaltplan-Elemente
# ---------------------------------------------------------------------------
ITEMS = []
POWER_NETS = {"GND": "GND", "+5V": "+5V", "+3V3": "+3V3"}
power_count = [0]


def place_power(net, x, y, outward):
    power_count[0] += 1
    ref = "#PWR%02d" % power_count[0]
    if net == "GND":
        rot = {"down": 0, "up": 180, "right": 90, "left": 270}[outward]
    else:
        rot = {"up": 0, "down": 180, "left": 90, "right": 270}[outward]
    ITEMS.append(instance(LIB + ":" + net, ref, net, x, y, rot, {}, power=True, power_dir=outward))


def wire(x1, y1, x2, y2):
    ITEMS.append(["wire", ["pts", ["xy", num(x1), num(y1)], ["xy", num(x2), num(y2)]],
                  ["stroke", ["width", "0"], ["type", "default"]], ["uuid", uid("w", x1, y1, x2, y2)]])


def label(net, x, y, left=False):
    just = ["justify", "right", "bottom"] if left else ["justify", "left", "bottom"]
    ITEMS.append(["label", Str(net), ["at", num(x), num(y), "180" if left else "0"], ["fields_autoplaced"],
                  ["effects", *FONT, just], ["uuid", uid("l", net, x, y)]])


def noconnect(x, y):
    ITEMS.append(["no_connect", ["at", num(x), num(y)], ["uuid", uid("nc", x, y)]])


def text(s, x, y, size=1.5, bold=False):
    font = ["font", ["size", num(size), num(size)]] + (["bold"] if bold else [])
    ITEMS.append(["text", Str(s), ["at", num(x), num(y), "0"],
                  ["effects", font, ["justify", "left", "top"]], ["uuid", uid("t", s[:40], x, y)]])


def frame(title, x1, y1, x2, y2):
    ITEMS.append(["rectangle", ["start", num(x1), num(y1)], ["end", num(x2), num(y2)],
                  ["stroke", ["width", "0.3"], ["type", "dash"], ["color", "0", "0", "132", "1"]],
                  ["fill", ["type", "none"]], ["uuid", uid("r", title)]])
    text(title, x1 + 1.5, y1 + 1.5, 2.0, True)


INSTANCES = []


def instance(lib_id, ref, value, x, y, rot, fields, power=False, dnp=False, power_dir=None):
    name = lib_id.split(":")[1]
    sym = SYMBOLS[name]
    props = {str(p[1]): str(p[2]) for p in find(sym, "property")}
    pins = sym_pins(name)
    node = ["symbol", ["lib_id", Str(lib_id)], ["at", num(x), num(y), str(rot)], ["unit", "1"],
            ["in_bom", "no" if power else "yes"], ["on_board", "yes"], ["dnp", "yes" if dnp else "no"],
            ["uuid", uid("s", ref)]]
    fp = fields.pop("Footprint", props.get("Footprint", ""))
    ds = fields.pop("Datasheet", props.get("Datasheet", ""))
    allf = [("Reference", ref), ("Value", value), ("Footprint", fp), ("Datasheet", ds)] + list(fields.items())
    libprops = {str(pp[1]): pp for pp in find(sym, "property")}
    vertical2 = rot in (0, 180) and len(pins) == 2 and all(p[0] == 0 for p in pins.values())
    for k, v in allf:
        hidden = (power and k == "Reference") or k not in ("Reference", "Value")
        if power and name == "PWR_FLAG" and k == "Value":
            hidden = False
        just = []
        if power and k == "Value" and power_dir:
            off, j = {"up": ((0, -3.81), None), "down": ((0, 3.81), None),
                      "left": ((-7.62, 0), None), "right": ((7.62, 0), None)}[power_dir]
            at = (x + off[0], y + off[1])
            just = [["justify", j]] if j else []
        elif vertical2 and k in ("Reference", "Value"):
            at = (x + 2.54, y - 1.27) if k == "Reference" else (x + 2.54, y + 1.27)
            just = [["justify", "left"]]
        elif k in libprops:
            lat = find(libprops[k], "at")[0]
            at = transform(float(lat[1]), float(lat[2]), rot, x, y)
            if rot == 0 and float(lat[3]) == 0:
                eff0 = find(libprops[k], "effects")
                jj = find(eff0[0], "justify") if eff0 else []
                just = [list(jj[0])] if jj else []
        else:
            at = (x, y)
        eff = ["effects", *FONT] + just + (["hide"] if hidden else [])
        fang = "90" if rot in (90, 270) else "0"  # KiCad dreht Feldtext mit dem Symbol
        node.append(["property", Str(k), Str(v), ["at", num(at[0]), num(at[1]), fang], eff])
    for pnum in pins:
        node.append(["pin", Str(pnum), ["uuid", uid("p", ref, pnum)]])
    node.append(["instances", ["project", Str(NAME), ["path", Str("/" + ROOT_UUID),
                                                      ["reference", Str(ref)], ["unit", "1"]]]])
    INSTANCES.append((ref, value, fields))
    return node


def transform(px, py, rot, x, y):
    sx, sy = px, -py
    if rot == 90:
        sx, sy = sy, -sx
    elif rot == 180:
        sx, sy = -sx, -sy
    elif rot == 270:
        sx, sy = -sy, sx
    return x + sx, y + sy


def outward_dir(ang, rot):
    # Pin zeigt in Richtung ang zum Körper -> nach außen ist die Gegenrichtung
    d = {0: (-1, 0), 90: (0, 1), 180: (1, 0), 270: (0, -1)}[ang]
    dx, dy = d
    for _ in range(rot // 90):
        dx, dy = dy, -dx
    return dx, dy


def part(lib_name, ref, value, x, y, conns, rot=0, stub=STUB, dnp=False, **fields):
    """Bauteil setzen. conns: {Pinnummer oder -name: Netz | 'NC'}."""
    pins = sym_pins(lib_name)
    byname = {}
    for n, p in pins.items():
        byname.setdefault(p[3], n)
    ITEMS.append(instance(LIB + ":" + lib_name, ref, value, x, y, rot, dict(fields), dnp=dnp))
    for key, net in conns.items():
        pnum = str(key) if str(key) in pins else byname[key]
        px, py, ang, _ = pins[pnum]
        cx, cy = transform(px, py, rot, x, y)
        if net == "NC":
            noconnect(cx, cy)
            continue
        dx, dy = outward_dir(ang, rot)
        ex, ey = cx + dx * stub, cy + dy * stub
        wire(cx, cy, ex, ey)
        out = {(-1, 0): "left", (1, 0): "right", (0, -1): "up", (0, 1): "down"}[(dx, dy)]
        if net in POWER_NETS:
            place_power(net, ex, ey, out)
        else:
            label(net, ex, ey, left=(out == "left"))


# ---------------------------------------------------------------------------
# Bibliothek
# ---------------------------------------------------------------------------
add_std("power", "GND")
add_std("power", "+5V")
add_std("power", "+3V3")
add_std("power", "PWR_FLAG")
R = add_std("Device", "R")
C = add_std("Device", "C")
CP = add_std("Device", "C_Polarized")
FUSE = add_std("Device", "Fuse")
LED = add_std("Device", "LED")
BAT = add_std("Device", "Battery_Cell")
TC = add_std("Device", "Thermocouple")
SCHOTTKY = add_std("Diode", "BAT85")
PFET = add_std("Transistor_FET", "AO3401A")
NFET = add_std("Transistor_FET", "BS170")
ATTINY = add_std("MCU_Microchip_ATtiny", "ATtiny85-20P")
LDO = add_std("Regulator_Linear", "MCP1700x-330xxTO")
SERVO = add_std("Motor", "Motor_Servo")
TASTER = add_std("Switch", "SW_Push")
SCREW2 = add_std("Connector", "Screw_Terminal_01x02")
CONN5 = add_std("Connector_Generic", "Conn_01x05")

ESP = add_module(
    "ESP32_D1_Mini", "U", "ESP32 D1 Mini (WROOM-32)",
    left=[("5V", "5V", "power_in"), None, ("3V3", "3V3", "power_out"), None, ("GND", "GND", "power_in"), None,
          None, ("EN", "EN", "input")],
    right=[("IO21", "IO21 SDA", "bidirectional"), ("IO22", "IO22 SCL", "output"), None,
           ("IO18", "IO18 SCK", "output"), ("IO19", "IO19 MISO", "input"), ("IO23", "IO23 MOSI", "output"),
           ("IO5", "IO5 CS", "output"), None,
           ("IO27", "IO27 Tür", "input"), ("IO34", "IO34 Netz", "input"), ("IO35", "IO35 Akku", "input"),
           None, ("IO25", "IO25 Lebenszeichen", "output"), ("IO26", "IO26 Servo EIN", "output"),
           ("IO32", "IO32 Taster", "input"), ("IO33", "IO33 LED", "output")],
    width=33.02,
    desc="ESP32-WROOM-32 im D1-mini-Format, Pinnummern = GPIO bzw. Pinbeschriftung am Board")
MAX = add_module(
    "MAX31856_Modul", "U", "MAX31856-Modul",
    left=[("VIN", "VIN", "power_in"), None, ("GND", "GND", "power_in"), ("3Vo", "3Vo", "power_out"), None,
          ("T+", "T+", "passive"), ("T-", "T-", "passive")],
    right=[("SCK", "SCK", "input"), ("SDO", "SDO", "output"), ("SDI", "SDI", "input"), ("CS", "CS", "input"),
           None, ("FLT", "~{FLT}", "output"), ("DRDY", "~{DRDY}", "output")],
    desc="Thermoelement-Messverstärker MAX31856 auf Breakout-Platine, Typ K, SPI")
PCA = add_module(
    "PCA9685_Modul", "U", "PCA9685-Modul",
    left=[("VCC", "VCC", "power_in"), None, ("GND", "GND", "power_in"), ("V+", "V+", "passive"), None,
          ("SDA", "SDA", "bidirectional"), ("SCL", "SCL", "input"), ("OE", "~{OE}", "input")],
    right=[("PWM1", "Kanal 1 PWM", "output")],
    width=22.86,
    desc="16-Kanal-PWM-Treiber PCA9685 (I2C 0x40), Kanal 1 = Servo")
AS = add_module(
    "AS5600_Modul", "U", "AS5600-Modul",
    left=[("VCC", "VCC", "power_in"), None, ("GND", "GND", "power_in"), None, ("SDA", "SDA", "bidirectional"),
          ("SCL", "SCL", "input"), ("DIR", "DIR", "input")],
    right=[("OUT", "OUT", "output"), ("GPO", "GPO", "passive")],
    desc="Magnetischer Winkelsensor AS5600 (I2C 0x36) auf der Sensorbrücke")
USV = add_module(
    "USV_Modul_1S", "PWR", "USV/Power-Path 1S, 5 V ≥ 3 A",
    left=[("VIN+", "VIN+", "power_in"), None, ("VIN-", "VIN−", "power_in"), None,
          ("BAT+", "BAT+", "passive"), ("BAT-", "BAT−", "passive")],
    right=[("VOUT+", "VOUT+", "power_out"), None, ("VOUT-", "VOUT−", "passive")],
    width=27.94,
    desc="Lade-/Power-Path-Modul 1S Li-Ion mit Schutzschaltung: 5 V Eingang, 5 V Ausgang ≥ 3 A unterbrechungsfrei")

# ---------------------------------------------------------------------------
# Schaltung
# ---------------------------------------------------------------------------
# --- Block 1: Versorgung ---------------------------------------------------
frame("1  Versorgung, Netz- und Akkuüberwachung", 12.7, 25.4, 165.1, 121.92)
part(SCREW2, "J1", "Netzteil 5 V / 4 A", 22.86, 50.8, {"1": "5V_NETZ_ROH", "2": "GND"}, rot=180,
     Footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
part(FUSE, "F1", "4 A träge", 45.72, 50.8, {"1": "5V_NETZ_ROH", "2": "5V_NETZ"},
     Footprint="Fuse:Fuseholder_Cylinder-5x20mm_Schurter_0031_8201_Horizontal_Open")
part(USV, "PWR1", "USV/Power-Path 1S, 5 V ≥ 3 A", 88.9, 50.8,
     {"VIN+": "5V_NETZ", "VIN-": "GND", "BAT+": "VBAT", "BAT-": "VBAT_N", "VOUT+": "+5V", "VOUT-": "GND"})
part(BAT, "BT1", "18650 Li-Ion 2,5–3,5 Ah", 66.04, 76.2, {"1": "VBAT", "2": "VBAT_N"})
part(CP, "C1", "470 µF / 10 V", 132.08, 45.72, {"1": "+5V", "2": "GND"},
     Footprint="Capacitor_THT:CP_Radial_D8.0mm_P3.50mm")
part(C, "C2", "100 nF", 154.94, 45.72, {"1": "+5V", "2": "GND"},
     Footprint="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm")
# Netzerkennung: Teiler 10k/20k vom Netzteil-5-V (vor der USV) auf IO34
part(R, "R1", "10 kΩ", 101.6, 86.36, {"1": "5V_NETZ", "2": "NETZ_MESS"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(R, "R2", "20 kΩ", 101.6, 104.14, {"1": "NETZ_MESS", "2": "GND"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(C, "C3", "100 nF", 116.84, 104.14, {"1": "NETZ_MESS", "2": "GND"},
     Footprint="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm")
# Akkuspannung: Teiler 100k/100k auf IO35
part(R, "R3", "100 kΩ", 134.62, 86.36, {"1": "VBAT", "2": "AKKU_MESS"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(R, "R4", "100 kΩ", 134.62, 104.14, {"1": "AKKU_MESS", "2": "GND"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(C, "C4", "100 nF", 149.86, 104.14, {"1": "AKKU_MESS", "2": "GND"},
     Footprint="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm")
# PWR_FLAGs: Netze, die nur von passiven Pins (Klemme, Sicherung, Akku) getrieben werden
for i, net in enumerate(["5V_NETZ", "GND"]):
    fx = 20.32 + i * 12.7
    ITEMS.append(instance(LIB + ":PWR_FLAG", "#FLG%02d" % (i + 1), "PWR_FLAG", fx, 111.76, 0, {}, power=True))
    wire(fx, 111.76, fx, 116.84)
    if net in POWER_NETS:
        place_power(net, fx, 116.84, "down")
    else:
        label(net, fx, 116.84)
text("Netz da: IO34 ≈ 3,3 V = HIGH\nAkku: IO35 = VBAT / 2", 22.86, 88.9, 1.27)

# --- Block 2: ESP32 ---------------------------------------------------------
frame("2  Mikrocontroller", 170.18, 25.4, 279.4, 121.92)
part(ESP, "U1", "ESP32 D1 Mini (WROOM-32)", 220.98, 63.5,
     {"5V": "+5V", "3V3": "+3V3", "GND": "GND", "EN": "ESP_EN",
      "IO21": "SDA", "IO22": "SCL", "IO18": "SCK", "IO19": "MISO", "IO23": "MOSI", "IO5": "TC_CS",
      "IO27": "TUER", "IO34": "NETZ_MESS", "IO35": "AKKU_MESS",
      "IO25": "LEBENSZEICHEN", "IO26": "SERVO_EIN", "IO32": "TASTER", "IO33": "LED"})
part(C, "C5", "10 µF", 177.8, 106.68, {"1": "+3V3", "2": "GND"},
     Footprint="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm")
part(R, "R5", "4,7 kΩ", 193.04, 106.68, {"1": "+3V3", "2": "SDA"}, dnp=True,
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(R, "R6", "4,7 kΩ", 205.74, 106.68, {"1": "+3V3", "2": "SCL"}, dnp=True,
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
text("R5/R6 nur bestücken, wenn die Module\nkeine I²C-Pull-ups haben", 215.9, 106.68, 1.27)

# --- Block 3: Brennraumtemperatur ------------------------------------------
frame("3  Brennraumtemperatur (Thermoelement Typ K)", 284.48, 25.4, 406.4, 83.82)
part(MAX, "U2", "MAX31856-Modul", 340.36, 55.88,
     {"VIN": "+3V3", "GND": "GND", "3Vo": "NC", "T+": "TC_P", "T-": "TC_N",
      "SCK": "SCK", "SDO": "MISO", "SDI": "MOSI", "CS": "TC_CS", "FLT": "NC", "DRDY": "NC"})
part(TC, "TC1", "Typ K (B17692)", 294.64, 68.58, {"1": "TC_P", "2": "TC_N"})
text("+ gelb/grün, − rot/weiß;\nverlängern nur mit Typ-K-Ausgleichsleitung", 358.14, 71.12, 1.27)

# --- Block 4: Luftbox-Stellung (AS5600) ------------------------------------
frame("4  Stellungsrückmeldung AS5600 (Sensorbrücke)", 284.48, 88.9, 406.4, 142.24)
part(CONN5, "J3", "Sensorbrücke 5-polig (JST-XH)", 304.8, 116.84,
     {"1": "+3V3", "2": "GND", "3": "SDA", "4": "SCL", "5": "GND"}, rot=180,
     Footprint="Connector_JST:JST_XH_B5B-XH-A_1x05_P2.50mm_Vertical")
part(AS, "U4", "AS5600-Modul", 368.3, 116.84,
     {"VCC": "+3V3", "GND": "GND", "SDA": "SDA", "SCL": "SCL", "DIR": "GND", "OUT": "NC", "GPO": "NC"})
text("Kabel 5 × 24 AWG, ≤ 1,5 m: 1 rot, 2 schwarz, 3 gelb, 4 weiß, 5 grün (DIR → GND)",
     289.56, 133.35, 1.27)

# --- Block 5: Servo-Leistungsteil ------------------------------------------
frame("5  Servoansteuerung (Servo im Stand stromlos, E21)", 170.18, 127.0, 279.4, 279.4)
part(PCA, "U3", "PCA9685-Modul", 203.2, 152.4,
     {"VCC": "+3V3", "GND": "GND", "V+": "NC", "SDA": "SDA", "SCL": "SCL", "OE": "PCA_OE", "PWM1": "PWM_PCA"})
part(R, "R7", "100 kΩ", 177.8, 180.34, {"1": "PCA_OE", "2": "GND"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(SCHOTTKY, "D1", "BAT85", 241.3, 175.26, {"A": "PWM_PCA", "K": "SERVO_SIG"}, rot=180)
part(SCHOTTKY, "D2", "BAT85", 241.3, 187.96, {"A": "PWM_WD", "K": "SERVO_SIG"}, rot=180)
part(R, "R8", "10 kΩ", 264.16, 182.88, {"1": "SERVO_SIG", "2": "GND"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
# Schalter für die Servoversorgung
part(PFET, "Q1", "AO3401A", 195.58, 210.82, {"G": "SERVO_GATE", "S": "+5V", "D": "5V_SERVO"}, rot=180,
     Footprint="Package_TO_SOT_SMD:SOT-23")
part(R, "R9", "10 kΩ", 218.44, 198.12, {"1": "+5V", "2": "SERVO_GATE"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(NFET, "Q2", "BS170", 200.66, 248.92, {"G": "SERVO_EIN", "D": "SERVO_GATE", "S": "GND"},
     Footprint="Package_TO_SOT_THT:TO-92_Inline")
part(NFET, "Q3", "BS170", 254.0, 248.92, {"G": "SERVO_EIN_WD", "D": "SERVO_GATE", "S": "GND"},
     Footprint="Package_TO_SOT_THT:TO-92_Inline")
part(R, "R10", "100 kΩ", 185.42, 264.16, {"1": "SERVO_EIN", "2": "GND"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(R, "R11", "100 kΩ", 238.76, 264.16, {"1": "SERVO_EIN_WD", "2": "GND"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(CP, "C6", "1000 µF / 10 V", 231.14, 213.36, {"1": "5V_SERVO", "2": "GND"},
     Footprint="Capacitor_THT:CP_Radial_D10.0mm_P5.00mm")
part(SERVO, "M1", "DS3225MG", 271.78, 210.82, {"PWM": "SERVO_SIG", "+": "5V_SERVO", "-": "GND"},
     Footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical")
text("Servo direkt an M1, nicht am PCA9685-Ausgang:\nPuls über D1/D2 (ODER), Versorgung über Q1.",
     175.26, 231.14, 1.27)

# --- Block 6: Hardware-Watchdog --------------------------------------------
frame("6  Hardware-Watchdog (Annahme, Bestückung optional)", 12.7, 175.26, 165.1, 279.4)
part(LDO, "U6", "MCP1700-3302E/TO", 38.1, 195.58, {"VI": "+5V", "VO": "3V3_WD", "GND": "GND"},
     Footprint="Package_TO_SOT_THT:TO-92_Inline")
part(C, "C7", "1 µF", 22.86, 218.44, {"1": "+5V", "2": "GND"},
     Footprint="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm")
part(C, "C8", "1 µF", 38.1, 218.44, {"1": "3V3_WD", "2": "GND"},
     Footprint="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm")
part(C, "C9", "100 nF", 53.34, 218.44, {"1": "3V3_WD", "2": "GND"},
     Footprint="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm")
part(ATTINY, "U5", "ATtiny85-20P", 101.6, 213.36,
     {"8": "3V3_WD", "4": "GND", "5": "PWM_WD", "6": "PCA_OE", "7": "LEBENSZEICHEN",
      "2": "WD_RESET", "3": "SERVO_EIN_WD", "1": "WD_NRST"},
     Footprint="Package_DIP:DIP-8_W7.62mm_Socket")
part(R, "R12", "10 kΩ", 142.24, 246.38, {"1": "3V3_WD", "2": "WD_NRST"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(R, "R13", "470 Ω", 81.28, 248.92, {"1": "WD_RESET", "2": "ESP_EN"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
text("PB0 Mittelstellungs-Puls (1610 µs = 500 ‰)\nPB1 ~{OE} PCA9685 sperren\nPB2 Lebenszeichen vom ESP32\n"
     "PB3 Reset ESP32 (nur Open-Drain!)\nPB4 Servo-Versorgung EIN\n"
     "Sockel leer = kein Watchdog,\nR7/R11 halten den Normalbetrieb.", 17.78, 236.22, 1.27)

# --- Block 7: Tür, Bedienung ------------------------------------------------
frame("7  Türkontakt und Bedienung", 12.7, 127.0, 165.1, 170.18)
part(SCREW2, "J2", "Türkontakt N111825", 22.86, 147.32, {"1": "TUER_EXT", "2": "GND"}, rot=180,
     Footprint="TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1,5-2-5.08_1x02_P5.08mm_Horizontal")
part(R, "R14", "1 kΩ", 45.72, 147.32, {"1": "TUER_EXT", "2": "TUER"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(R, "R15", "10 kΩ", 60.96, 147.32, {"1": "+3V3", "2": "TUER"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(C, "C10", "100 nF", 76.2, 147.32, {"1": "TUER", "2": "GND"},
     Footprint="Capacitor_THT:C_Disc_D5.0mm_W2.5mm_P5.00mm")
part(TASTER, "SW1", "Taster", 106.68, 139.7, {"1": "TASTER", "2": "GND"},
     Footprint="Button_Switch_THT:SW_PUSH_6mm")
part(R, "R16", "10 kΩ", 106.68, 160.02, {"1": "+3V3", "2": "TASTER"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(R, "R17", "330 Ω", 134.62, 142.24, {"1": "LED", "2": "LED_A"},
     Footprint="Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal")
part(LED, "D3", "LED grün", 147.32, 157.48, {"A": "LED_A", "K": "GND"}, rot=90,
     Footprint="LED_THT:LED_D3.0mm")
text("Tür zu = Kontakt zu = LOW;\nKabelbruch = „Tür offen“", 17.78, 160.02, 1.27)

text("Alle Logikpegel 3,3 V. Verbindungen über gleichnamige Netzlabels. Pinbelegung = config.h (esp32dev). "
     "Doku: docs/SCHALTPLAN.md", 12.7, 283.21, 1.5)


# ---------------------------------------------------------------------------
# Dateien schreiben
# ---------------------------------------------------------------------------
def write_all():
    libsyms = list(SYMBOLS.values())
    sch = ["kicad_sch", ["version", "20230121"], ["generator", "eeschema"], ["uuid", ROOT_UUID],
           ["paper", Str("A3")],
           ["title_block", ["title", Str("RIKA NEX Abbrandregelung – Steuerung")],
            ["date", Str("2026-11-06")], ["rev", Str("A")],
            ["company", Str("vauntro/rika-nex-airflow-controller")],
            ["comment", "1", Str("Entwurf, erzeugt mit hardware/schaltplan/quelle/schaltplan.py")],
            ["comment", "2", Str("Annahmen: USV-Modul 1S + 18650, Watchdog ATtiny85 (siehe docs/SCHALTPLAN.md)")]],
           ["lib_symbols", *[parse(dump(s).replace('(symbol "', '(symbol "' + LIB + ':', 1))[0]
                             for s in libsyms]],
           *ITEMS,
           ["sheet_instances", ["path", Str("/"), ["page", Str("1")]]]]
    with open(os.path.join(OUT, NAME + ".kicad_sch"), "w") as f:
        f.write(dump(sch) + "\n")
    lib = ["kicad_symbol_lib", ["version", "20220914"], ["generator", "kicad_symbol_editor"], *libsyms]
    with open(os.path.join(OUT, NAME + ".kicad_sym"), "w") as f:
        f.write(dump(lib) + "\n")
    with open(os.path.join(OUT, "sym-lib-table"), "w") as f:
        f.write('(sym_lib_table\n  (lib (name "%s")(type "KiCad")(uri "${KIPRJMOD}/%s.kicad_sym")'
                '(options "")(descr "RIKA NEX Steuerung"))\n)\n' % (LIB, NAME))
    pro = {
        "meta": {"filename": NAME + ".kicad_pro", "version": 1},
        "schematic": {"legacy_lib_dir": "", "legacy_lib_list": []},
        "sheets": [[ROOT_UUID, ""]],
        "text_variables": {},
        "boards": [],
        "libraries": {"pinned_footprint_libs": [], "pinned_symbol_libs": []},
    }
    with open(os.path.join(OUT, NAME + ".kicad_pro"), "w") as f:
        json.dump(pro, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    write_all()
    print("geschrieben:", OUT)
