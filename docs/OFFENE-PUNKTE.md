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
- Optional Mini-DC-USV (5 V, ≥ 2 A, unterbrechungsfrei) nur für Board + Servo; Netzausfall
  über D0 (Spannungsteiler vor der USV); bei Akku knapp → Notstellung.
- **Entscheidung offen:** Stellung bei Störung (Akku leer, Fühler defekt, AS5600 gestört):
  a) letzte Stellung beibehalten, b) feste Notstellung z. B. 500 ‰, c) phasenabhängig
  (Abbrand → 500 ‰, Glut → letzte Stellung). Empfehlung: c), bis zur Regelung a).
  Nie automatisch „ganz zu“, solange Feuer im Ofen sein kann.

## Mechanik / Kalibrierung

- Druck-Riemenräder (3 Varianten) eingetroffen? → passende Variante wählen, M3-Schraube nach
  Einschraubtiefe.
- Axialspiel der Luftbox-Welle: Scheiben M10 (≈ 3,6 mm) + Riemenrad als Anschlag.
- Servo gekoppelt. AIR_US_AT_0 = 2360 µs (ganz zu, 27.10.). AIR_US_AT_1000 (ganz auf) noch antasten.
- Klappen prüfen: Liegt der Übergang Primär/Sekundär wirklich bei 500 ‰?
- Voreinstellungen „Abbrand mittel/leicht“ am echten Feuer festlegen.

## Später

- Messphase mit echten Abbränden (Ereignisse Angeheizt/Nachgelegt nutzen).
- Abbrandregelung (Phasen + PID auf Brennraumtemperatur).
- Umstieg ESP32 + MAX31856, Gehäuse, Kabelführung.
