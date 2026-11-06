# Sensorbrücke AS5600 (Rückseite Luftbox)

Flache, schmale Brücke aus 2-mm-Alublech, die den AS5600 auf der Rückseite der Luftbox über dem Magneten am
Wellenende hält. Die Gegenseite (Servo, Riemen) ist davon nicht betroffen. Stand 06.11.2026.

## Dateien

| Datei | Inhalt |
|---|---|
| `sensorbruecke-as5600-zeichnung-iso.pdf` | **Fertigungszeichnung nach ISO** (A4 quer, 1:1, Sachnummer RNX-S-001), Stil wie Bauteil H: Blatt 1 Ansichten mit Bemaßung, Blatt 2 Montage (Schnitt durch die Wellenmitte) und Hinweise |
| `sensorbruecke-as5600-baugruppe-montiert.step` / `-explosion.step` | **3D-Baugruppe** für CAD (Luftbox-Rückseite vereinfacht, Magnet, Platine, Abstandshalter, Brücke, Hülsen, Normteile), montiert und als Explosion |
| `sensorbruecke-as5600-baugruppe-montiert.stl` / `-explosion.stl` | Dieselbe Baugruppe als STL (alle Teile in einem Netz) |
| `sensorbruecke-as5600-baugruppe-montiert.glb` / `-explosion.glb` | Dieselbe Baugruppe farbig zum direkten Anschauen (macOS Vorschau/Quick Look, Windows 3D-Viewer, Browser) |
| `sensorbruecke-as5600-baugruppe.png` | Vorschaubild der montierten Baugruppe |
| `sensorbruecke-as5600-montage.pdf` / `.png` | **Montageanleitung**: Explosionsdarstellung mit Positionsnummern, Teileliste und Montageschritten |
| `sensorbruecke-as5600-zeichnung.pdf` | Zeichnung **1:1 auf A4 quer** mit Maßen und Montagehinweisen, als Bohr- und Anreißschablone ausdrucken (ohne Seitenanpassung, Prüfmaß 50 mm nachmessen) |
| `sensorbruecke-as5600-zeichnung.png` | Dieselbe Zeichnung als Bild |
| `sensorbruecke-as5600.step` / `.stl` | 3D-Modell |
| `sensorbruecke-as5600.dxf` | Kontur für Laser/Wasserstrahl |
| `quelle/bruecke.py`, `quelle/zeichnung.py`, `quelle/zeichnung_iso.py`, `quelle/montage.py`, `quelle/vorschau.py` | CadQuery-/Matplotlib-Skripte, aus denen die Dateien erzeugt werden |
| `entwurf/` | Skizzen aus der Abstimmung (überholt: Schraube M5 statt M6, Blech 2 mm statt 3 mm, Variante B gewählt) |

## Maße

- Länge 161, Steg **8** breit, Augen Ø 14 um die M5-Bohrungen, Mittelplatte **24 × 24**, Ecken und
  Übergänge R 2, Dicke 2. Schmal gehalten, damit die Brücke möglichst wenig Luft verdeckt (06.11.: vorher
  Steg 16 und Platte 32 × 32). Steg nicht unter 6 mm, sonst biegt sich das Blech beim Anziehen.
- 2 × Ø 5,5 für M5 im Abstand **147** (Laschenlöcher der Luftbox Ø 6,8, auf Höhe der Wellenmitte).
- 4 × Ø 3,2 für die AS5600-Platine, Lochmitten **16,1 × 16,3** (Platine 23,2 × 22,7, Löcher Ø 3,6).
- Fenster 17 × 11 mittig (Ecken R 1,5) für die Dupont-Stecker der Stiftleisten.

## Aufbau (von der Box aus)

1. Scheibe · Lasche (6,2 dick) · Distanzhülse **12 mm** (Ø10/5,3) · Brücke · Scheibe · Sicherungsmutter
   DIN 985 M5 (Nylonring), Schraube **ISO 4017 M5 × 30** (Klemmlänge 6,2 + 12 + 2 + 2 × 1 + Mutter 5 + Überstand ≈ 28,7).
   Nylon-Stoppmutter ist in Ordnung: an der Stelle wird es nicht heiß (Nico, 06.11.), Nylon hält bis ca. 120 °C.
2. Platine auf der Box-Seite der Brücke, Chip zur Welle, auf vier Abstandshaltern **M3 × 6** (Innen/Innen),
   Schrauben ISO 7380 M3 × 5. Abstandshalter aus Messing, nicht Kunststoff. Stiftreihen senkrecht, die Stifte zeigen durch das Fenster nach hinten.
3. Höhenkette: Magnet 1 vor Laschenebene + Luftspalt ca. 1,9 + Chip 1,5 + Platine 1,6 + Abstandshalter 6
   = 12. Eine M3-Scheibe zwischen Abstandshalter und Brücke verkleinert den Spalt um ca. 0,5 mm,
   Abstandshalter 5 mm vergrößern ihn auf ca. 2,9 mm. Der AS5600 arbeitet mit ca. 0,5–3 mm.
4. Die Laschenlöcher Ø 6,8 geben mit M5 ca. ±0,6 mm Spiel: Brücke so ausrichten, dass der Chip mittig
   über dem Magneten sitzt, dann anziehen. Danach Feldstärke per Firmware prüfen (Status MD/ML/MH).

## Einkaufsliste Montage

| Anzahl | Teil |
|---|---|
| 2 | Sechskantschraube ISO 4017 M5 × 30, A2 |
| 2 | Distanzhülse 12 mm, Ø 10 / 5,3, ohne Gewinde (Alu oder Edelstahl) |
| 4 | Scheibe ISO 7089 – 5, A2 |
| 2 | Sicherungsmutter DIN 985 M5 (Nylonring), A2 |
| 4 | Abstandshalter M3 × 6, Innen-/Innengewinde, Messing |
| 8 | Linsenkopfschraube ISO 7380 M3 × 5, A2 |
| optional | Scheiben ISO 7089 – 3 zum Einstellen des Luftspalts |
| 1 | Anschlusskabel 5-adrig 24 AWG (z. B. UL2464 5 × 0,2 mm²), Stecker Dupont oder JST XH 5-polig, selbst gecrimpt |

## Anschluss

Fünf Adern, siehe auch [`docs/VERKABELUNG.md`](../../docs/VERKABELUNG.md):

| AS5600 | Board | Ader (Vorschlag) |
|---|---|---|
| VCC | 3V3 | rot |
| GND | GND | schwarz |
| SDA | SDA (D1 Mini D2, ESP32 GPIO 21) | gelb |
| SCL | SCL (D1 Mini D1, ESP32 GPIO 22) | weiß |
| DIR | GND (darf nicht offen bleiben) | grün |

I²C-Leitung kurz halten (bis ca. 1,5 m), Kabel mit Abstand zu heißem Blech führen (PVC bis 80 °C).
Alternative mit 4 Polen: DIR auf der Platine mit einer Drahtbrücke auf GND legen.

## Neu erzeugen

```bash
pip install cadquery matplotlib
cd quelle && python3 bruecke.py && python3 zeichnung.py && python3 zeichnung_iso.py && python3 montage.py && python3 vorschau.py   # Ausgabe in quelle/, danach eine Ebene höher verschieben
```
