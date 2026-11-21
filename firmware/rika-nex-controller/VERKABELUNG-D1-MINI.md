# Verkabelung Wemos D1 Mini (Firmware 0.3.4-luftbox)

Stand 21.11.2026. Gilt für den aktuellen Aufbau: D1 Mini (`pio run -e d1_mini`), MAX6675 mit Thermoelement Typ K,
AS5600 auf der Sensorbrücke, Servo DS3225MG am PCA9685. Pins wie in `include/config.h`.
Übersicht für D1 Mini und ESP32: [`docs/VERKABELUNG.md`](../../docs/VERKABELUNG.md).

Alle Module laufen mit **3,3 V Logik**. Alle GND-Leitungen (Board, Module, Servo-Netzteil) sind miteinander verbunden.

## Übersicht D1 Mini

| D1 Mini | GPIO | Anschluss |
|---|---|---|
| 3V3 | – | VCC von MAX6675, AS5600, PCA9685 (Logik) |
| G | – | GND aller Module, Türkontakt, Servo-Netzteil (−) |
| 5V | – | Versorgung des Boards (USB oder 5 V) |
| D1 | 5 | I²C SCL → AS5600 SCL, PCA9685 SCL |
| D2 | 4 | I²C SDA → AS5600 SDA, PCA9685 SDA |
| D5 | 14 | MAX6675 SCK |
| D6 | 12 | MAX6675 SO |
| D8 | 15 | MAX6675 CS (nur CS, nichts mit Pull-up) |
| D7 | 13 | Türkontakt (interner Pull-up) |
| D0 | 16 | Netzerkennung über Teiler 10k/20k |
| A0 | ADC | Akkuspannung über 100 kΩ Vorwiderstand |
| D3, D4 | 0, 2 | **frei lassen** (Bootmodus) |

I²C-Adressen: PCA9685 0x40, AS5600 0x36.

## Servo DS3225MG über PCA9685

| PCA9685 | Anschluss |
|---|---|
| VCC | 3V3 vom D1 Mini (nur Logik) |
| GND | G vom D1 Mini |
| SDA / SCL | D2 / D1 |
| OE | offen lassen (auf dem Modul nach GND gezogen) |
| V+ (Schraubklemme) | **externes 5-V-Netzteil (+), mindestens 3 A**, nicht vom D1 Mini |
| GND (Schraubklemme) | externes Netzteil (−), mit G des D1 Mini verbunden |
| **Kanal 1** (zweite Stiftreihe von links) | Servostecker: Signal (orange/gelb) an PWM, rot an V+, braun/schwarz an GND |

- Die Firmware gibt pro Fahrt 1 s Puls (plus bis zu 2 Nachstellfahrten), danach ist der Servo stromlos.
- Endwerte: 2360 µs = ganz zu, 860 µs = ganz auf (`AIR_US_AT_0`, `AIR_US_AT_1000`).

## AS5600 (Sensorbrücke, 5-adriges Kabel)

| AS5600 | D1 Mini | Ader |
|---|---|---|
| VCC | 3V3 | rot |
| GND | G | schwarz |
| SDA | D2 | gelb |
| SCL | D1 | weiß |
| DIR | **G** (nicht offen lassen) | grün |

Kabel bis ca. 1,5 m, mit Abstand zu heißem Blech. Prüfen in HA: „AS5600 Magnet“ = ok, AGC ca. 29,
Feldstärke ca. 2066 (gemessen 21.11.2026).

## Thermoelement Typ K am MAX6675

| MAX6675 | D1 Mini |
|---|---|
| VCC | 3V3 |
| GND | G |
| SCK | D5 |
| SO | D6 |
| CS | D8 |

Fühler an die Schraubklemmen: gelbe bzw. grüne Ader (+) an `+`, rote bzw. weiße Ader (−) an `−`. Fällt die Anzeige
beim Erwärmen, sind die Adern vertauscht. Verlängern nur mit Typ-K-Ausgleichsleitung.

## Türkontakt

Anschluss 1 an **D7**, Anschluss 2 an **G**. Tür zu = Kontakt geschlossen = LOW. Kabelbruch liest sich wie
„Tür offen“ (sichere Seite).

## Netzerkennung und Akku

- **Netzerkennung:** 5 V vom Netzteil (vor dem Lademodul) → 10 kΩ → **D0** → 20 kΩ → G. Netz da ≈ 3,3 V = HIGH.
  Ohne Beschaltung meldet die Firmware „akku“; dann D0 mit 10 kΩ an 3V3 legen.
- **Akkuspannung:** Akku + → 100 kΩ → **A0**. Mit dem Teiler auf dem Board sind 4,2 V Vollausschlag. Ohne Akku
  ist der Wert bedeutungslos (z. B. 0,04 V).

## Später: MAX31856 oder ESP32

Der MAX31856 braucht zusätzlich MOSI an D7. Der Türkontakt wandert dann auf D0 (externer 10-kΩ-Pull-up nach 3V3),
die Netzerkennung entfällt am D1 Mini. Für die Zielhardware ist der ESP32 vorgesehen (`docs/SCHALTPLAN.md`).
