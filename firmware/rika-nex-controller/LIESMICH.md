# RIKA NEX – Firmware (Logger + Luftbox)

Stand 0.3.2-luftbox (27.10.2026). Läuft auf dem Produktiv-D1-Mini (rika_nex.local).
Misst Brennraumtemperatur, Tür, Netz/Akku und stellt die Luftbox über den Servo;
der AS5600 kontrolliert die Ist-Stellung. Noch **keine automatische Regelung** –
die Stellung kommt aus Home Assistant.

## Flashen

```bash
./flash_ota.sh logger            # aus dem Projektordner, per WLAN
```

## Home Assistant (MQTT-Discovery, Gerät „RIKA NEX“)

| Entität | Bedeutung |
|---|---|
| sensor Brennraumtemperatur, Vergleichsstelle, Sensorfehler | Temperatur (MAX6675/Typ K) |
| binary_sensor Feuerraumtür, Netzversorgung; sensor Akkuspannung | Ofen / Versorgung |
| button Angeheizt, Nachgelegt | Ereignisse fürs Log |
| **select Luftbox Stellung** | Voreinstellungen: Anfeuern 1000 ‰, Abbrand stark 500 ‰, Abbrand mittel 335 ‰, Abbrand leicht 165 ‰, Glut halten 0 ‰; „Manuell“ bei freiem Regler |
| **number Luftklappe** | Soll in ‰ (Regler, Schritt 5) – fährt nicht unter die Sperre 160 ‰ |
| **sensor Luftbox Zustand** | Stellung in Worten aus dem Ist-Wert, z. B. „Abbrand mittel · Sekundärluft 67 %, Primärluft zu“ (Voreinstellung wird genannt, wenn ±15 ‰ nah) |
| sensor Primärluft / Sekundärluft | Öffnung in %: 0–500 ‰ öffnet die Sekundärluft, 500–1000 ‰ zusätzlich die Primärluft |
| sensor Luftklappe Stellung | zuletzt gefahren, „‰ / µs“ |
| sensor Luftbox Stellung Ist / Luftbox Winkel | AS5600: Ist in ‰ und ° ab „ganz zu“ |
| sensor Luftklappe Abweichung | Ist − Soll in ‰ (0,5 s nach jeder Fahrt) |
| sensor Luftklappe Status | ok / fährt / Abweichung ±x ‰ / Sensor: … / Kalibrierung … |
| sensor AS5600 Magnet (Diagnose) | ok / zu schwach / zu stark / fehlt / außerhalb Bereich |
| button Nullpunkt setzen (Konfiguration) | aktuelle Stellung als „ganz zu“ speichern (EEPROM) |
| number Servo-Puls (Kalibrierung) (Konfiguration) | roher Puls 500–2500 µs, **ohne** Luftbox-Grenzen |

Dashboard zum Einfügen: `../../home-assistant/rika-nex-dashboard.yaml`.

## Verhalten

- Nach dem Start bewegt sich nichts, bis ein Soll kommt.
- Jede Fahrt: 1000 ms Puls, danach Puls aus (Servo hält nicht aktiv).
- Software-Sperre: Regler und spätere Regelung nicht unter 160 ‰ (alter Zwischenanschlag
  bei ca. 152 ‰); ganz zu nur über „Glut halten“.
- Plausibilität: Abweichung > 20 ‰ → Status „Abweichung“ und Ereignis `luft:abweichung:…`.
  Vor dem Koppeln und Kalibrieren ist das normal (Servo und Box sind noch nicht verbunden).
- Ereignisse auf `rika_nex/event`: `luft:<‰>/<µs>us`, `luft:sperre`, `luft:abweichung:<‰>`,
  `luft:nullpunkt:<raw>`, `luft:kalibrierung:<µs>us`, `tuer_auf`, `tuer_zu`, `nachgelegt`, …

## Kalibrierung der Endpunkte

`AIR_US_AT_0` / `AIR_US_AT_1000` in `include/config.h`:

| Stellung | Puls | Stand |
|---|---|---|
| 0 ‰ = ganz zu („Glut halten“) | 2360 µs | angetastet 27.10.2026, vollständig geschlossen |
| 1000 ‰ = ganz auf („Anfeuern“) | 860 µs | noch vorläufig – mit „Servo-Puls (Kalibrierung)“ antasten |

Vorgehen: mit „Servo-Puls (Kalibrierung)“ den Anschlag antasten, mit dem AS5600 prüfen
(ca. 20 µs vor dem Anschlag), Wert eintragen, neu flashen. Details: `docs/KALIBRIERUNG.md`.
