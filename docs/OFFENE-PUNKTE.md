# Offene Punkte – RIKA NEX Abbrandregelung

## Für die Produktiv-Firmware (Entscheidung Nico 23.10.2026: erst beim Ausrollen umsetzen)

Strom- und WLAN-Ausfall werden **firmwareseitig** behandelt (Access Points können nicht
gepuffert werden).

- Regelung läuft vollständig autark auf dem Board; WLAN/MQTT/HA nur Anzeige und Bedienung.
- Selbstständiger Wiederaufbau von WLAN/MQTT, danach Discovery + Zustände neu senden.
- Messwerte während Ausfall puffern (z. B. 1–2 h im Minutenraster) und nachsenden.
- AS5600 auch ohne MQTT-Verbindung lesen (bisher nur bei Verbindung).
- Nach Neustart: Ist-Stellung (AS5600) als Soll übernehmen, keine Bewegung; Ereignis
  „neustart“ mit Grund (Stromausfall/Reset).
- Betriebsart/Regelphase im Flash speichern und nach Neustart fortsetzen.
- Diagnose-Sensor: Zähler für WLAN-/MQTT-Ausfälle.
- Servo im Stand abschalten (E21, Nico 06.11.): nach Erreichen der Stellung stromlos, kein aktives Halten.
- **Entscheidung offen:** Puffer eigener Akku (eine 18650-Zelle reicht laut Abschätzung, ≈ 4,5 Wh von
  9–13 Wh für 6 h) oder Mini-DC-USV (5 V, unterbrechungsfrei) nur für Board + Servo. Wandler bzw. USV
  **≥ 3 A** wegen der Servo-Spitzen. Netzausfall über D0 (Spannungsteiler vor der USV); bei Akku knapp → Notstellung.
- **Entscheidung offen:** Stellung bei Störung (Akku leer, Fühler defekt, AS5600 gestört):
  a) letzte Stellung beibehalten, b) feste Notstellung z. B. 500 ‰, c) phasenabhängig
  (Abbrand → 500 ‰, Glut → letzte Stellung). Empfehlung: c), bis zur Regelung a).
  Nie automatisch „ganz zu“, solange Feuer im Ofen sein kann.

## Mechanik / Kalibrierung

- AS5600-Sensorbrücke bauen (`hardware/sensorbruecke-as5600/`): Zeichnung 1:1 drucken, aus 2-mm-Alublech
  aussägen, Teile laut Einkaufsliste im README des Bauteils besorgen (u. a. M5 × 30, Hülsen 12 mm,
  Abstandshalter M3 × 6). Nach Montage Luftspalt und Feldstärke (MD/ML/MH) prüfen und den Nullpunkt neu setzen.
- Druck-Riemenräder (3 Varianten) eingetroffen? → passende Variante wählen, M3-Schraube nach
  Einschraubtiefe.
- Axialspiel der Luftbox-Welle: Scheiben M10 (≈ 3,6 mm) + Riemenrad als Anschlag.
- Servo gekoppelt. AIR_US_AT_0 = 2360 µs (ganz zu, 27.10.). AIR_US_AT_1000 = 860 µs (ganz auf, bestätigt 28.10.). Offen: AS5600-Nullpunkt neu setzen und Linearität prüfen (KALIBRIERUNG.md).
- Klappen prüfen: Liegt der Übergang Primär/Sekundär wirklich bei 500 ‰?
- **Test (E21):** Hält der Riemenantrieb die Stellung mit stromlosem Servo, oder drücken die Klappen ihn zurück?
  Mehrere Stellungen anfahren, Servo abschalten, AS5600-Wert über einige Minuten beobachten (auch mit
  warmem Ofen). Falls er wegdriftet: Nachstellen bei Abweichung oder Servo doch halten lassen (dann Akku neu rechnen).
- Echten Verbrauch messen (Board + Servo, Phase 3) und die Akku-Abschätzung prüfen.
- Voreinstellungen „Abbrand mittel/leicht“ am echten Feuer festlegen.

## Schaltplan (Entwurf Rev. A, `docs/SCHALTPLAN.md`)

- Annahmen bestätigen: USV-/Power-Path-Modul 1S + 18650 als PWR1, Watchdog mit ATtiny85.
- Konkretes USV-Modul auswählen (5 V Ausgang ≥ 3 A dauerhaft, Laden und Entladen gleichzeitig).
- ERC in KiCad 8/9 laufen lassen.
- Firmware: IO26 (Servoversorgung) um jede Fahrt schalten, Lebenszeichen auf IO25, Taster/LED.
- Watchdog-Firmware für den ATtiny85 schreiben.
- Prüfen, ob die Module (PCA9685, AS5600) eigene I²C-Pull-ups haben (sonst R5/R6 bestücken).

## Später

- Messphase mit echten Abbränden (Ereignisse Angeheizt/Nachgelegt nutzen).
- Abbrandregelung (Phasen + PID auf Brennraumtemperatur).
- Umstieg ESP32 + MAX31856, Gehäuse, Kabelführung.

- Optional: sanfte Fahrrampe im Servo-Antrieb (ca. 1,5 s voller Weg, langsamer vor den Anschlägen), nur falls im Betrieb hartes Anschlagen auffällt. Stand 28.10.: nicht nötig, Fahrweg passt.
