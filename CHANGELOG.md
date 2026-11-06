# Changelog

Alle Änderungen am Projekt (Firmware, Kalibrierung, Hardware, Planung) werden hier festgehalten, neueste oben.

## 2026-11-06

### Hardware
- **3D-Baugruppe Sensorbrücke** als STEP und GLB, montiert und als Explosion, mit Vorschaubild.
- **Montageanleitung Sensorbrücke** (`sensorbruecke-as5600-montage.pdf`): Explosionsdarstellung aus dem CAD-Modell
  mit Positionsnummern, Teileliste und Montageschritten.
- **Sensorbrücke Befestigung korrigiert:** Laschen sind 6,2 mm dick (gemessen Nico), daher ISO 4017 **M5 × 30** statt
  M5 × 22, Ganzmetall-Sicherungsmutter ISO 7042 (keine Nylon-Stoppmutter wegen Wärme), Abstandshalter aus Messing.
  Einkaufsliste im README des Bauteils, beide Zeichnungen neu erzeugt.
- **ISO-Fertigungszeichnung der Sensorbrücke** (`sensorbruecke-as5600-zeichnung-iso.pdf`, RNX-S-001): A4 quer,
  1:1, Schriftfeld nach ISO 7200 wie beim Servohalter. Blatt 1 Ansichten, Blatt 2 Montage und Hinweise.
- **Sensorbrücke schmaler** (Wunsch Nico, weniger Luftwiderstand): Steg 8 statt 16 mm, Augen Ø 14 um die
  M5-Löcher, Mittelplatte 24 × 24 statt 32 × 32, Länge 161. STEP, STL, DXF und Zeichnung neu erzeugt; die
  Zeichnung übernimmt die Kontur jetzt direkt aus dem CAD-Modell.
- **Neu: AS5600-Sensorbrücke** für die Rückseite der Luftbox (`hardware/sensorbruecke-as5600/`): flaches
  2-mm-Alublech 163 × 16 mit Mittelplatte 32 × 32, befestigt an den mittleren Laschen (Lochabstand 147) mit
  M5 × 22 und Distanzhülsen 12 mm, Platine auf Abstandshaltern M3 × 6, Fenster 17 × 11 für die Stecker.
  STEP, STL, DXF, Zeichnung 1:1 (PDF) und Entwurfsskizzen. Ersetzt den Sensorwinkel aus E16.

### Doku
- `docs/MECHANIK.md`: Abschnitt Sensorbrücke mit den von Nico gemessenen Maßen.
- `docs/OFFENE-PUNKTE.md`: Bau und Inbetriebnahme der Sensorbrücke.

## 2026-10-27

### Planung
- **E20: Umstieg auf ESP32 für den Produktivbetrieb** (Nico, 27.10.). Empfohlenes Board: ESP32 D1 Mini (WROOM-32). Servo-PWM bleibt auf dem PCA9685, die Pulswerte gelten weiter. Pinbelegung, Verkabelung und Portierungsschritte in `docs/projektplan-v3.md`, Abschnitt 6.1. Stückliste angepasst.

### Firmware 0.3.2
- Endwert „ganz zu“ (0 ‰) neu gemessen: **2360 µs** statt 2200 µs. „Glut halten“ schließt damit vollständig. Endwert „ganz auf“ (1000 ‰, vorläufig 860 µs) wird noch nachgemessen.
