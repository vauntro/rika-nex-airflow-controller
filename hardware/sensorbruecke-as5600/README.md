# Sensorbrücke AS5600 (Rückseite Luftbox)

Flache, schmale Brücke aus 2-mm-Alublech, die den AS5600 auf der Rückseite der Luftbox über dem Magneten am
Wellenende hält. Die Gegenseite (Servo, Riemen) ist davon nicht betroffen. Stand 06.11.2026.

## Dateien

| Datei | Inhalt |
|---|---|
| `sensorbruecke-as5600-zeichnung-iso.pdf` | **Fertigungszeichnung nach ISO** (A4 quer, 1:1, Sachnummer RNX-S-001), Stil wie Bauteil H: Blatt 1 Ansichten mit Bemaßung, Blatt 2 Montage (Schnitt durch die Wellenmitte) und Hinweise |
| `sensorbruecke-as5600-zeichnung.pdf` | Zeichnung **1:1 auf A4 quer** mit Maßen und Montagehinweisen, als Bohr- und Anreißschablone ausdrucken (ohne Seitenanpassung, Prüfmaß 50 mm nachmessen) |
| `sensorbruecke-as5600-zeichnung.png` | Dieselbe Zeichnung als Bild |
| `sensorbruecke-as5600.step` / `.stl` | 3D-Modell |
| `sensorbruecke-as5600.dxf` | Kontur für Laser/Wasserstrahl |
| `quelle/bruecke.py`, `quelle/zeichnung.py`, `quelle/zeichnung_iso.py` | CadQuery-/Matplotlib-Skripte, aus denen die Dateien erzeugt werden |
| `entwurf/` | Skizzen aus der Abstimmung (überholt: Schraube M5 statt M6, Blech 2 mm statt 3 mm, Variante B gewählt) |

## Maße

- Länge 161, Steg **8** breit, Augen Ø 14 um die M5-Bohrungen, Mittelplatte **24 × 24**, Ecken und
  Übergänge R 2, Dicke 2. Schmal gehalten, damit die Brücke möglichst wenig Luft verdeckt (06.11.: vorher
  Steg 16 und Platte 32 × 32). Steg nicht unter 6 mm, sonst biegt sich das Blech beim Anziehen.
- 2 × Ø 5,5 für M5 im Abstand **147** (Laschenlöcher der Luftbox Ø 6,8, auf Höhe der Wellenmitte).
- 4 × Ø 3,2 für die AS5600-Platine, Lochmitten **16,1 × 16,3** (Platine 23,2 × 22,7, Löcher Ø 3,6).
- Fenster 17 × 11 mittig (Ecken R 1,5) für die Dupont-Stecker der Stiftleisten.

## Aufbau (von der Box aus)

1. Lasche · Distanzhülse **12 mm** (M5) · Brücke · Scheibe · Mutter, Schraube **M5 × 22** (vorhanden; wird
   knapp, sonst M5 × 25).
2. Platine auf der Box-Seite der Brücke, Chip zur Welle, auf vier Abstandshaltern **M3 × 6** (Innen/Innen),
   Schrauben M3 × 5. Stiftreihen senkrecht, die Stifte zeigen durch das Fenster nach hinten.
3. Höhenkette: Magnet 1 vor Laschenebene + Luftspalt ca. 1,9 + Chip 1,5 + Platine 1,6 + Abstandshalter 6
   = 12. Eine M3-Scheibe zwischen Abstandshalter und Brücke verkleinert den Spalt um ca. 0,5 mm,
   Abstandshalter 5 mm vergrößern ihn auf ca. 2,9 mm. Der AS5600 arbeitet mit ca. 0,5–3 mm.
4. Die Laschenlöcher Ø 6,8 geben mit M5 ca. ±0,6 mm Spiel: Brücke so ausrichten, dass der Chip mittig
   über dem Magneten sitzt, dann anziehen. Danach Feldstärke per Firmware prüfen (Status MD/ML/MH).

## Neu erzeugen

```bash
pip install cadquery matplotlib
cd quelle && python3 bruecke.py && python3 zeichnung.py && python3 zeichnung_iso.py   # Ausgabe in quelle/, danach eine Ebene höher verschieben
```
