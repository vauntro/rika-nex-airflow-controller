# Verkabelung

Stand 06.11.2026. Pinbelegung wie in `firmware/rika-nex-controller/include/config.h`. Übernommen aus dem
Verkabelungsplan des Testaufbaus (`VERKABELUNG-D1-MINI.md` der Logger-Firmware) und für den ESP32 ergänzt.

Alle Module laufen mit **3,3 V Logik**. Die Elektronik sitzt im Sockelraum unter der Luftbox, nicht im Steinmantel.

## Übersicht

| Funktion | Modul-Pin | ESP32 (Ziel, `esp32dev`) | D1 Mini (aktuell, `d1_mini`) |
|---|---|---|---|
| I²C SDA (PCA9685 0x40, AS5600 0x36) | SDA | GPIO 21 | D2 (GPIO 4) |
| I²C SCL | SCL | GPIO 22 | D1 (GPIO 5) |
| SPI SCK (Thermoelement) | SCK | GPIO 18 | D5 (GPIO 14) |
| SPI MISO | SO / SDO | GPIO 19 | D6 (GPIO 12) |
| SPI MOSI (nur MAX31856/MAX31865) | SDI | GPIO 23 | D7 (GPIO 13) |
| SPI CS | CS | GPIO 5 | D8 (GPIO 15) |
| Türkontakt (nach GND) | – | GPIO 27 | D7 mit MAX6675, D0 + 10 kΩ nach 3V3 mit MAX31856 |
| Netzerkennung (Teiler 10k/20k) | – | GPIO 34 | D0 (nur mit MAX6675) |
| Akkuspannung | – | GPIO 35 (Teiler 100k/100k) | A0 (+100 kΩ Vorwiderstand) |
| Lebenszeichen an Watchdog | – | GPIO 25 | – |
| Servoversorgung EIN | – | GPIO 26 | – |
| Taster / Status-LED | – | GPIO 32 / GPIO 33 | – |

Vollständiger Schaltplan der ESP32-Steuerung (KiCad): [`SCHALTPLAN.md`](SCHALTPLAN.md). Dort hängt der Servo
nicht mehr am PCA9685-Kanal 1, sondern bekommt Puls und schaltbare 5 V über die Trägerplatine.

Nicht verwenden am D1 Mini: **D3, D4** (Bootmodus), **D8** nur als CS.

## AS5600 Winkelsensor (Sensorbrücke)

| AS5600 | Board | Ader (5-adrig, 24 AWG) |
|---|---|---|
| VCC | 3V3 | rot |
| GND | GND | schwarz |
| SDA | SDA | gelb |
| SCL | SCL | weiß |
| DIR | **GND** (darf nicht offen bleiben) | grün |

- I²C-Leitung kurz halten, bis ca. 1,5 m.
- Kabel mit Abstand zu heißem Blech führen (PVC-Mantel bis 80 °C).
- Alternative mit 4 Polen: DIR auf der Platine mit einer Drahtbrücke auf GND legen.
- Mechanik und Stecker: `hardware/sensorbruecke-as5600/README.md`.

## PCA9685 Servotreiber

| PCA9685 | Anschluss |
|---|---|
| VCC | 3V3 vom Board (Logik) |
| GND | GND (gemeinsam mit Board und Servo-Netzteil) |
| SDA / SCL | I²C-Bus wie oben |
| V+ (Schraubklemme) | **externe 5 V** für den Servo, nicht vom Board |
| Kanal 1 | Servo (zweiter Kanal von links) |

## Thermoelement Typ K

| MAX6675 / MAX31856 | Board |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SCK | SPI SCK |
| SO / SDO | SPI MISO |
| SDI (nur MAX31856) | SPI MOSI |
| CS | SPI CS |

Fühler an die Schraubklemmen: **gelbe bzw. grüne Ader (+)** an `+`, **rote bzw. weiße Ader (−)** an `−`.
Fällt die Anzeige beim Erwärmen, sind die Adern vertauscht. Verlängern nur mit Typ-K-Ausgleichsleitung.

## Türkontakt

Anschluss 1 an den Tür-Pin, Anschluss 2 an GND. Tür zu = Kontakt geschlossen = LOW; ein Kabelbruch liest sich
wie „Tür offen“ (sichere Seite). ESP32 und D1 Mini D7: interner Pull-up. D1 Mini D0: externer 10-kΩ-Pull-up nach 3V3.

## Netzerkennung und Akku

- **Netzerkennung:** 5 V vom Netzteil (vor dem Lademodul) → 10 kΩ → Pin → 20 kΩ → GND. Netz da ≈ 3,3 V = HIGH.
  Ohne Beschaltung meldet die Firmware dauerhaft „akku“.
- **Akkuspannung:** ESP32 Teiler 100k/100k auf GPIO 35. D1 Mini: Akku + → 100 kΩ → A0 (zusammen mit dem
  Teiler auf dem Board 4,2 V Vollausschlag).
