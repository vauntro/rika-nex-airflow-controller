# Changelog

Alle Änderungen am Projekt (Firmware, Kalibrierung, Hardware, Planung) werden hier festgehalten, neueste oben.

## 2026-11-06

### Schaltplan
- **Neu: KiCad-Schaltplan der ESP32-Steuerung** (`hardware/schaltplan/`, Doku `docs/SCHALTPLAN.md`), Rev. A Entwurf:
  Versorgung mit USV-/Power-Path-Modul und 18650, Netz- und Akkuüberwachung, ESP32 D1 Mini, MAX31856, AS5600 über
  JST-XH, PCA9685, schaltbare Servoversorgung über P-MOSFET (E21), Dioden-ODER für den Servopuls, Hardware-Watchdog
  mit ATtiny85, Türkontakt, Taster und LED. PDF/PNG-Export und Generator-Skript dabei.
- Annahmen (Akku statt Mini-USV, ATtiny als Watchdog) in `docs/SCHALTPLAN.md` und `docs/OFFENE-PUNKTE.md`.
- `config.h`: GPIO 25/26/32/33 für Lebenszeichen, Servoversorgung, Taster und LED reserviert (noch ohne Funktion).
- `docs/VERKABELUNG.md`: neue GPIOs und Verweis auf den Schaltplan.

### Planung
- **E21: Servo im Stand stromlos** (Nico, 06.11.). Nach Erreichen der Stellung wird der Servo abgeschaltet.
  Akku-Abschätzung für 6 h: ESP32 + WLAN ≈ 3,3 Wh, mit Wandlerverlusten ≈ 4 Wh, Servo-Stellbewegungen ≈ 0,5 Wh;
  eine 18650-Zelle (9–13 Wh) reicht. Wandler ≥ 3 A wegen der Servo-Spitzen. `docs/projektplan-v3.md` (E21,
  Abschnitt 2.3) und `docs/OFFENE-PUNKTE.md` ergänzt. Offen: Hält der Riemenantrieb stromlos? Akku oder Mini-DC-USV?

### Hardware
- **Sensorbrücke Anschluss:** Belegung der 5 Adern (VCC, GND, SDA, SCL, DIR auf GND) im README des Bauteils,
  Kabel 5-adrig 24 AWG mit Dupont- oder JST-XH-Stecker statt 4-poligem Dupont-Kabel.
- **Sensorbrücke Mutter:** Sicherungsmutter DIN 985 M5 A2 mit Nylonring statt Ganzmetall ISO 7042. An der
  Stelle wird es nicht heiß (Nico). Höhe gleich (5 mm), M5 × 30 bleibt. README, Zeichnungen und Montage aktualisiert.
- **3D-Baugruppe Sensorbrücke** als STEP, STL und GLB, montiert und als Explosion, mit Vorschaubild.
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
- **Neu: `docs/VERKABELUNG.md`**: Verkabelungsplan aus dem Testaufbau ins Repo übernommen und für den ESP32 ergänzt
  (AS5600 mit DIR auf GND, PCA9685, Thermoelement, Türkontakt, Netz/Akku).
- `docs/MECHANIK.md`: Abschnitt Sensorbrücke mit den von Nico gemessenen Maßen.
- `docs/OFFENE-PUNKTE.md`: Bau und Inbetriebnahme der Sensorbrücke.

## 2026-10-28

### Hardware / Test
- Dauer- und Stresstest des Antriebs ohne AS5600: 16 Fahrten im 10-s-Takt, danach 120 Fahrten im 1,5-s-Takt (60 volle Hübe). Alle Befehle quittiert, kein Neustart. Servo kalt, Riemenrad-Markierungen an beiden Endlagen exakt, keine Geräusche. **Antrieb freigegeben.** Details in `docs/MECHANIK.md`.
- Servo mit Unterlegscheiben ausgerichtet (Riemen lief am inneren Bord an), Nachtest mit 56 Fahrten (10 s und 3 s) ohne Fehler, Endlage „Anfeuern“ passt.
- 10-Minuten-Stresstest (200 Fahrten, 3 s): alle quittiert, danach fehlte bei „Glut halten“ ca. 1 mm, vermutlich Riemensprung um einen Zahn. Riemen neu auflegen und strammer spannen, Pulswerte bleiben. Details in `docs/MECHANIK.md`.

### Kalibrierung
- Endwert „ganz auf“ (1000 ‰, „Anfeuern“) = **860 µs** bestätigt: stimmt mit der von Hand erprobten Endlage überein. Firmware unverändert. Zwischenstellungen und nächste Schritte (AS5600-Nullpunkt, Linearitätsprüfung) in `docs/KALIBRIERUNG.md`.

## 2026-10-27

### Planung
- **E20: Umstieg auf ESP32 für den Produktivbetrieb** (Nico, 27.10.). Empfohlenes Board: ESP32 D1 Mini (WROOM-32). Servo-PWM bleibt auf dem PCA9685, die Pulswerte gelten weiter. Pinbelegung, Verkabelung und Portierungsschritte in `docs/projektplan-v3.md`, Abschnitt 6.1. Stückliste angepasst.

### Firmware 0.3.2
- Endwert „ganz zu“ (0 ‰) neu gemessen: **2360 µs** statt 2200 µs. „Glut halten“ schließt damit vollständig. Endwert „ganz auf“ (1000 ‰, vorläufig 860 µs) wird noch nachgemessen.
