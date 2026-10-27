# Changelog

Alle Änderungen am Projekt (Firmware, Kalibrierung, Hardware, Planung) werden hier festgehalten, neueste oben.

## 2026-10-27

### Planung
- **E20: Umstieg auf ESP32 für den Produktivbetrieb** (Nico, 27.10.). Empfohlenes Board: ESP32 D1 Mini (WROOM-32). Servo-PWM bleibt auf dem PCA9685, die Pulswerte gelten weiter. Pinbelegung, Verkabelung und Portierungsschritte in `docs/projektplan-v3.md`, Abschnitt 6.1. Stückliste angepasst.

### Firmware 0.3.2
- Endwert „ganz zu“ (0 ‰) neu gemessen: **2360 µs** statt 2200 µs. „Glut halten“ schließt damit vollständig. Endwert „ganz auf“ (1000 ‰, vorläufig 860 µs) wird noch nachgemessen.
