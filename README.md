# rika-nex-airflow-controller

Automatische Verbrennungsluftregelung für den Rika NEX Kaminofen ohne Rikatronic. Ein ESP8266 (D1 mini) misst die Brennraumtemperatur, fährt den Luftschieber per Servo und GT2-Riemen und regelt per PID von Anfeuern bis Glut halten. AS5600 zur Positionsrückmeldung, Steuerung und Logging über Home Assistant.

## Aufbau des Repos

| Ordner | Inhalt |
|---|---|
| [`firmware/rika-nex-controller/`](firmware/rika-nex-controller/) | PlatformIO-Projekt für den D1 mini (ESP8266), Firmware 0.3.2, MQTT-Anbindung an Home Assistant |
| [`docs/`](docs/) | Funktionsweise der Luftbox, Projektpläne (v1–v3), Mechanik, Kalibrierung, offene Punkte, Home-Assistant-Werte |
| [`home-assistant/`](home-assistant/) | Dashboard-YAML für Home Assistant |
| [`hardware/`](hardware/) | CAD-Daten (STEP/STL) und Zeichnungen: Servohalter (Bauteil H), GT2-Riemenrad |

## Funktionsprinzip

Der NEX hat einen zentralen Luftschieber (links offen, rechts geschlossen), der über zwei Klappen in der Luftbox Primär- und Sekundärluft steuert (Details in [`docs/rika-nex-manuelle-luftsteuerung.md`](docs/rika-nex-manuelle-luftsteuerung.md)). Ein Servo bewegt die Welle der Luftbox über einen GT2-Riemen, ein AS5600-Magnetsensor meldet die tatsächliche Stellung zurück. Der Brennraumfühler (Thermoelement Typ K) sitzt an der Original-Rikatronic-Position.

## Firmware bauen

1. `firmware/rika-nex-controller/include/secrets.example.h` nach `include/secrets.h` kopieren und WLAN, MQTT und OTA-Passwort eintragen. `secrets.h` wird nicht eingecheckt.
2. `pio run -e d1_mini -t upload`, danach Updates per OTA.

Weitere Hinweise und die Servo-Endpunkte stehen in [`firmware/rika-nex-controller/LIESMICH.md`](firmware/rika-nex-controller/LIESMICH.md).

## Hinweise

- Die Herstelleranleitungen von RIKA sind aus urheberrechtlichen Gründen nicht enthalten; die Dokumente verlinken auf die offiziellen Downloads.
- Eigenbau-Projekt ohne Bezug zum Hersteller. Eingriffe in die Luftsteuerung eines Kaminofens erfolgen auf eigene Verantwortung; die Nullstellung darf im Betrieb nicht angefahren werden (Verpuffungsgefahr).
