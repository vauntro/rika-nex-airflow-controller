#pragma once

// ---------------------------------------------------------------------------
// Sensortyp des Original-Flammtemperatursensors
// Widerstand bei Raumtemperatur messen:
//   wenige Ohm   -> Thermoelement Typ K -> SENSOR_MAX31856
//   ca. 1000 Ohm -> PT1000             -> SENSOR_MAX31865
// Ergebnis 18.10.: ca. 6 Ohm, lief bereits an einem MAX6675 -> Thermoelement Typ K
// ---------------------------------------------------------------------------
#define SENSOR_MAX31856 1
#define SENSOR_MAX31865 2
#define SENSOR_MAX6675  3   // Typ K, vorhandenes Modul; erkennt nur offenen Fühler
#ifndef TEMP_SENSOR_TYPE
#define TEMP_SENSOR_TYPE SENSOR_MAX31856
#endif

// ---------------------------------------------------------------------------
// Pinbelegung je Board
// ---------------------------------------------------------------------------
#if defined(ESP8266)
// Wemos D1 Mini (erste Tests). Gemieden: D3/GPIO0 und D4/GPIO2 (Bootmodus),
// D8/GPIO15 nur als CS (muss beim Booten LOW sein, Modul-CS ist unkritisch).
#define PIN_SPI_SCK   14   // D5
#define PIN_SPI_MISO  12   // D6
#define PIN_SPI_MOSI  13   // D7 (nur MAX31856/MAX31865, MAX6675 braucht es nicht)
#define PIN_SPI_CS    15   // D8
#define PIN_I2C_SDA    4   // D2
#define PIN_I2C_SCL    5   // D1
#if TEMP_SENSOR_TYPE == SENSOR_MAX6675
#define PIN_DOOR      13   // D7, frei solange MAX6675 genutzt wird
#define PIN_MAINS_SENSE 16 // D0, digital über Spannungsteiler
#else
// MAX31856/MAX31865 belegen D7 (MOSI): Tür auf D0 mit externem 10k-Pull-up
// nach 3,3 V (GPIO16 hat keinen internen Pull-up), Netzerkennung entfällt.
#define PIN_DOOR      16   // D0
#define PIN_DOOR_EXTERNAL_PULLUP 1
#define PIN_MAINS_SENSE -1
#endif
#define PIN_BATTERY   A0   // einziger ADC; D1 Mini hat 220k/100k-Teiler an Bord (max. 3,2 V)
// Mit zusätzlichem 100k-Vorwiderstand an A0 sind 4,2 V = Vollausschlag
#define BATTERY_FULLSCALE_V 4.2f
#else
// ESP32 DevKit (Zielhardware)
#define PIN_SPI_CS     5
#define PIN_SPI_SCK   18
#define PIN_SPI_MISO  19
#define PIN_SPI_MOSI  23
#define PIN_I2C_SDA   21
#define PIN_I2C_SCL   22
#define PIN_DOOR      27
#define PIN_MAINS_SENSE 34 // digital über Spannungsteiler
#define PIN_BATTERY   35   // Teiler 100k/100k
#define BATTERY_DIVIDER 2.0f
#endif

// Türkontakt: geschlossene Tür = geschlossener Kontakt nach GND.
// Kabelbruch liest sich dadurch wie "Tür offen" (sichere Seite).
// Netzerkennung: 5 V von der Netzteilseite (vor dem Lademodul) über Teiler
// 10k/20k auf ca. 3,3 V -> HIGH = Netz vorhanden.

// MAX31865: Referenzwiderstand des Moduls (PT1000-Module meist 4300 Ohm)
#define MAX31865_RREF     4300.0f
#define MAX31865_RNOMINAL 1000.0f

// ---------------------------------------------------------------------------
// Luftbox: Servo (PCA9685) + AS5600, siehe luftbox.h und
// rika-nex-servotest/KALIBRIERUNG.md. Stellung in ‰: 0 = ganz zu, 1000 = ganz auf.
// ---------------------------------------------------------------------------
#define PCA9685_ADDR     0x40
#define SERVO_CHANNEL    1          // zweiter Kanal von links
#define SERVO_MOVE_MS    1000UL     // Puls nur zum Anfahren, danach aus (Servo hält nicht)
// Abbildung ‰ -> Servo-Puls. VORLÄUFIG (Geodreieck 21.10.), nach dem Koppeln an der
// Luftbox mit dem AS5600 kalibrieren. Die Werte sind zugleich die harten Grenzen.
#define AIR_US_AT_0      2360       // 0 ‰    = ganz zu (gemessen 27.10.: vollständig geschlossen)
#define AIR_US_AT_1000   860        // 1000 ‰ = ganz auf (bestätigt 28.10.: Endlage stimmt)
// Software-Sperre (wie der Hebel am Original-Schieber): der freie Regler fährt nicht
// unter diesen Wert, ganz zu nur über die Auswahl "Glut halten".
// Zwischenanschlag gemessen bei ca. 152 ‰ (27,6°).
#define AIR_LOCK_PERMILLE 160
// Plausibilitätsprüfung nach jeder Fahrt (Ist vom AS5600 gegen Soll)
#define AIR_CHECK_DELAY_MS     500UL
#define AIR_CHECK_TOL_PERMILLE 20
// Voreinstellungen für Home Assistant: Name, Stellung in ‰ (mittel/leicht vorläufig)
#define AIR_PRESETS \
  {"Anfeuern", 1000}, {"Abbrand stark", 500}, {"Abbrand mittel", 335}, \
  {"Abbrand leicht", 165}, {"Glut halten", 0}

// "Luftbox Zustand" nennt die Voreinstellung, wenn die Ist-Stellung so nah daran liegt
#define AIR_PRESET_NEAR_PERMILLE 15

#define AS5600_ADDR           0x36
#define AS_RAW_CLOSED_DEFAULT 3530   // ganz zu; wird per "Nullpunkt setzen" im EEPROM überschrieben
#define AS_RAW_SPAN           2074   // ganz zu -> ganz auf = 182,3°
#define AS_TOL_RAW            57     // ca. 5° Toleranz an den Anschlägen
#define AS_CHANGE_RAW         6      // ca. 0,5°: sofort senden
#define AS_INTERVAL_MS        100UL
#define AS_PUBLISH_MS         1000UL
#define EEPROM_MAGIC          0xA560 // gleiches Format wie das Servo-Testprogramm

// Takt
#define SAMPLE_INTERVAL_MS   2000UL   // Messung
#define PUBLISH_INTERVAL_MS  5000UL   // MQTT
#define TEMP_FILTER_ALPHA    0.3f     // gleitender Mittelwert gegen Rauschen

// MQTT
#define DEVICE_ID    "rika_nex"
#define TOPIC_PREFIX "rika_nex/"
#define FW_VERSION   "0.3.2-luftbox"
