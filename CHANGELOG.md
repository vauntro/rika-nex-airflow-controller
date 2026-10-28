# Changelog

Alle Änderungen am Projekt (Firmware, Kalibrierung, Hardware, Planung) werden hier festgehalten, neueste oben.

## 2026-10-28

### Hardware / Test
- Dauer- und Stresstest des Antriebs ohne AS5600: 16 Fahrten im 10-s-Takt, danach 120 Fahrten im 1,5-s-Takt (60 volle Hübe). Alle Befehle quittiert, kein Neustart. Servo kalt, Riemenrad-Markierungen an beiden Endlagen exakt, keine Geräusche. **Antrieb freigegeben.** Details in `docs/MECHANIK.md`.

### Kalibrierung
- Endwert „ganz auf“ (1000 ‰, „Anfeuern“) = **860 µs** bestätigt: stimmt mit der von Hand erprobten Endlage überein. Firmware unverändert. Zwischenstellungen und nächste Schritte (AS5600-Nullpunkt, Linearitätsprüfung) in `docs/KALIBRIERUNG.md`.

## 2026-10-27

### Planung
- **E20: Umstieg auf ESP32 für den Produktivbetrieb** (Nico, 27.10.). Empfohlenes Board: ESP32 D1 Mini (WROOM-32). Servo-PWM bleibt auf dem PCA9685, die Pulswerte gelten weiter. Pinbelegung, Verkabelung und Portierungsschritte in `docs/projektplan-v3.md`, Abschnitt 6.1. Stückliste angepasst.

### Firmware 0.3.2
- Endwert „ganz zu“ (0 ‰) neu gemessen: **2360 µs** statt 2200 µs. „Glut halten“ schließt damit vollständig. Endwert „ganz auf“ (1000 ‰, vorläufig 860 µs) wird noch nachgemessen.
