# Projektplan v3: Abbrandregelung für RIKA NEX 8 kW (Scheitholz, ohne Rikatronic)

Stand: 18.10.2026 · Ersetzt v2 (`projektplan-v1.md` und `projektplan-v2.md` bleiben als Verlauf)

## 0. Entscheidungen (Nico, 18.10.2026)

| Nr. | Thema | Entscheidung |
|---|---|---|
| E1 | Sensor | Original-Brennraumtemperaturfühler (Flammtemperatursensor B17692, Flammsensorrohr B15248) an der Original-Rikatronic-Position nachrüsten |
| E2 | Aktor | Servomotor am Flansch der Luftbox, manuelle Bedienung entfällt (Detaildiskussion offen, siehe Abschnitt 3) |
| E3 | Fail-safe | Mittelstellung; Steuerung mit kleinem Li-Ion-Akku als Fallback |
| E4 | Ziel | sauberer Abbrand und lange Brenndauer |
| E5 | Ende | nach dem Ausbrand Meldung zum Nachlegen über Home Assistant, dann Nullstellung |
| E6 | Plattform | ESP32, Home Assistant vorhanden |
| E7 | Ofen | 8-kW-Ausführung (Auflage ~2,2 kg, Teillast ~1,1 kg, Abgas ~206 °C, Kaminzug 12 Pa) |
| E8 | Türkontakt | Original-Türkontakt von RIKA (Rikatronic-Ersatzteil, Kontaktschalter Nr. 96 / Schaltstange Nr. 93) |
| E9 | Kupplung | Lösbare Kupplung Servo ↔ Welle, sofern einfach umsetzbar |
| E10 | Netzausfall | Laufenden Abbrand auf Akku bis zum Ausbrand fertig regeln, danach Schutzabschaltung bis Netzstrom wieder anliegt |
| E11 | Firmware | Eigener Arduino-Code (ESP32), Steuerprotokoll MQTT |

| E12 | Schutzabschaltung | Mittelstellung bestätigt |
| E13 | MQTT | Broker läuft bereits als dedizierte VM |
| E15 | Servo | Vorhandener TD-8125MG 360° ist ein Dauerdreher → nur für Tests am Tisch. Für den Endausbau wird ein **Positionsservo** gekauft (Vorschlag DS3225MG 270°, 25 kg·cm), angesteuert über den vorhandenen PCA9685 (Kanal 1, externe 5 V). AS5600 zusätzlich zur Kontrolle der Wellenstellung. Tischtest 18.10.: Kette D1 Mini → I2C → PCA9685 (0x40) → Servo funktioniert; TD-8125MG steht bei 1440–1540 µs, dreht unter 1430 µs rechts, über 1560 µs links (Werte gelten für dieses PCA9685-Modul) |
| E14 | Sensor-Einbau | Original-Sensor ist vorhanden; die vorhandene Umlenkplatte wird von einem Ofenbauer angepasst und für den Sensor vorbereitet (keine Teilebestellung nötig) |
| E16 | Antrieb (Planungsstand 20.10.) | Zahnriemen GT2 1:1: zwei Räder mit 20 Zähnen, Riemen 158 mm × 6 mm, Achsabstand ca. 59 mm. Rad auf der Luftboxwelle mit 8-mm-Bohrung (Welle gemessen: genau 8 mm, 22.10.; nur aufreiben, falls das Rad nicht ohne Gewalt aufgeht), Querstift greift in einen 4,1 mm breiten Schlitz der Nabe (zur Montage Stift aus- und wieder einbauen). Servorad: gedrucktes GT2-20T-Rad mit integrierter 25T-Aufnahme (PA12 bzw. Harz, 3 Spiel-Varianten 0,05/0,10/0,20 mm bei JLC3DP bestellt 22.10., je 2 Stück; Mittelschraube M3 kurz; Dateien `riemenrad_gt2_20t_servo25t_spiel*.stl`); Bastellösungen (Kupplung, Disc, Hülsen) verworfen. Servo (DS3225MG 270°) unter der Luftbox, Achse parallel zur Welle, Halter aus 2-mm-Alublech, Z-förmig (Leiste an den unteren Laschen von 69 mit senkrechten Langlöchern, ca. ±2 mm zum Spannen; Schenkel ca. 33 mm unter der Box; hinten Platte mit Ausschnitt für den Servo). POM-Kappe auf der Nabe hält den Querstift, mit Madenschraube M3 gegen Verdrehen gesichert, vorne Magnet Ø 6 × 2,5 mm (diametral magnetisiert), AS5600 1–2 mm davor auf einem Winkel aus Flachprofil 30 × 2 mm an einer vorhandenen Gehäuseschraube. Ein 6-mm-Riemen auf 20 Zähnen überträgt nur ca. 3 kg·cm; Drehmoment der Welle muss gemessen werden, sonst breiterer Riemen oder größere Räder |
| E17 | Luftbox-Winkel (AS5600, 22.10.) | Magnet + AS5600 sitzen am Einlass der Luftbox (verklebt). Ab „ganz zu“: Zwischenanschlag +27,6° (≈152 ‰), ganz auf +182,3° (1000 ‰); Wiederholgenauigkeit ca. 0,1°, Anschlag-Streuung ca. ±1° (Toleranz ±5° in der Firmware). AS5600 am selben I²C-Bus wie PCA9685 (0x36/0x40). Nullpunkt per HA-Button, dauerhaft gespeichert. Bekannte Einschränkung: axiales Wellenspiel (herstellungsbedingt, nicht behebbar) verschiebt den Messwert um bis zu 2,8° (≈15 ‰); akzeptiert, Störungsschwelle ≥5°. Details: `KALIBRIERUNG.md`, Test Handschieber: `TEST-Handschieber.md` (auf Nicos Mac). |
| E18 | Ziel (22.10.) | Ofen vorerst vollständig elektrisch über den Servo steuern. Ob der Handschieber mit angekoppeltem Servo weiter nutzbar ist (Kraft, Riemen-Überspringen), bleibt vorerst offen. |
| E19 | Stromausfall ohne WLAN (23.10.) | Bei Netzausfall ist auch das WLAN weg (mehrere Access Points, nicht puffbar). Die Firmware muss den Ausfall allein behandeln: Regelung läuft lokal auf dem Board weiter, ohne HA/MQTT; Messwerte und Ereignisse werden lokal zwischengespeichert und nach Rückkehr des WLAN nachgemeldet. Puffer für das Board selbst (eigener Akku oder Mini-DC-USV 5 V, unterbrechungsfrei, ≥ 3 A) noch offen. Notstellung bei Störung (Akku leer, Fühler/AS5600 defekt), entschieden 23.10.: nach Phase, im Abbrand 500 ‰, im Glutbett letzte Stellung; nie automatisch ganz zu; bis die Regelung fertig ist, gilt letzte Stellung. Umsetzung (Offline-Betrieb, Ist-Stellung nach Neustart übernehmen, Neustart-Ereignis, Ausfallzähler) erst mit der Prod-Firmware (Nico, 23.10.). |

Fotos und Maße des Flansches reicht Nico nach (Voraussetzung für die Servo-Auswahl).

**Messwerte Flansch/Welle**
| Maß | Wert | Quelle |
|---|---|---|
| Länge Querstift | 15,05 mm (Nicos Ablesung; Foto passt grob dazu) | Messschieber 18.10. |
| Einbausituation (Fotos 18.10.) | Luftbox (69) hängt unter dem Feuerraumboden über dem offenen Sockelraum. Zwischenwelle verbindet die Welle der Luftbox mit einer zweiten Welle, die in den Schieberegler-Kasten (67) führt; 67 ist mit 4 Sechskantschrauben auf einer Platte montiert. Die große Zugfeder neben dem Schieberegler ist die Türschließfeder (Ersatzteil Nr. 21), sie wirkt nicht auf den Luftschieber. Servo und Kabel müssen ihr Freiraum lassen. Darunter viel freier Platz im Sockel. | Fotos 18.10. |
| Original-Sensor | 6 Ω zwischen den Adern, beim Anfassen der Spitze ca. 6,8 Ω. Passt zu einem Thermoelement (Thermospannung verfälscht die Ohm-Messung). Lief laut Nico bereits an einem MAX6675 (nur Typ K) → **Typ K bestätigt**. Messphase mit vorhandenem MAX6675 möglich, Dauerbetrieb mit MAX31856 empfohlen | Multimeter 18.10. |
| Querstift-Ø | 4,0 mm (Nico). Stift steht beidseitig ca. 3,4 mm über die Welle über. Schlitzbreite Hülse ca. 4,1 mm → ca. 1° Winkelspiel | Messschieber 18.10. |
| Stellbereich Welle | 180° Drehbereich. Original-Rikatronic regelt in ‰: 1000→500 ‰ Unterluft (Primär), 500→0 ‰ Oberluft (Sekundär). Linear angenommen: 0 ‰ = Null ≈ 0°, 500 ‰ = Mittel ≈ 90°, 1000 ‰ = Anheiz ≈ 180° (am kalten Ofen prüfen) | Nico, 19.10. |
| Wellen-Ø direkt an der Luftbox | 8,2 mm (Nico: 0,82 cm; Foto bestätigt: Nonius-Null 0,2 mm hinter dem 8-mm-Strich, Noniusstrich 2 fluchtet). Evtl. Nennmaß 8 mm plus Belag; Hülsenbohrung ca. 8,3–8,4 mm | Messschieber 18.10. |

## 1. Ziel

Der Luftschieber wird über einen Servo automatisch verstellt. Führungsgröße ist die Brennraumtemperatur am Originalfühler. Regelziel: jede Auflage so sauber wie möglich und so lange wie möglich abbrennen lassen, also **so wenig Luft wie möglich, aber nie so wenig, dass die Verbrennung kalt und rußig wird.**

## 2. Systemarchitektur

```
 Original-Flammtemperatursensor ──► Messverstärker (abhängig vom Sensortyp) ──┐
 Türkontakt (dringend empfohlen, s. 5) ────────────────────────────────────────┤
 optional: Abgasfühler Rauchrohr ──────────────────────────────────────────────┤
                                                                              ▼
       230 V ─► Netzteil 5 V ─► Lade-/Power-Path-Modul ─► ESP32 (Zustandsautomat, PID, Sicherheit)
                                     │                         │
                              Li-Ion-Akku + BMS          Servo + Positionsrückmeldung (Encoder)
                                                               │
                                                     Flansch Luftbox → Schieber
                                                               │
                                          WLAN / MQTT bzw. ESPHome-API → Home Assistant
```

### 2.1 Sensor (E1)
- Der Original-Sensor hat sehr wahrscheinlich ein Thermoelement (Typ K) als Messprinzip, das ist aber **nicht belegt**. Vor dem Elektronikentwurf messen: Widerstand bei Raumtemperatur (Thermoelement: wenige Ohm, PT1000: ca. 1000 Ω) und Spannung bei Erwärmung (Typ K: ca. 41 µV/K).
- Bei Typ K: MAX31856 (mit Fehlererkennung offener Fühler/Kurzschluss), Thermo-Ausgleichsleitung Typ K bis zur Elektronik, kein normales Kupferkabel dazwischen.
- Einbau nach Ersatzteilliste: Flammsensorrohr B15248, Andrückwinkel L02783, ggf. Umlenkplatte unten Rikatronic Z32596. Beim Händler klären, ob die Nicht-Rikatronic-Umlenkplatte (Z33588) die Aussparung bereits hat oder getauscht werden muss.

### 2.2 Aktor (E2)
Siehe Abschnitt 3.

### 2.3 Stromversorgung und Akku (E3)
- Power-Path-Lademodul (Last läuft bei Netz weiter, Akku wird geladen), 1S Li-Ion oder LiFePO4 mit BMS, Step-up/Step-down auf Servospannung.
- Netzausfall-Erkennung am ESP32 (Spannung vor dem Lademodul messen).
- **Akku nicht in die warme Zone:** Li-Ion verträgt dauerhaft max. ca. 45–60 °C. Elektronik und Akku außerhalb des Steinmantels oder im kühlsten Bereich (Zuluft) und Temperatur dort im Probebetrieb messen. LiFePO4 ist thermisch unkritischer.
- **Akku-Kapazität (E10):** Ein Zyklus vom Anheizen bis „Feuer aus“ dauert bei einer Auflage grob 4–6 h (Abbrand 0,75–1,5 h, Glut bis 4 h, dazu Abkühlzeit bis T_aus). Grobe Schätzung: ESP32 mit WLAN ca. 100–150 mA im Mittel, Servo nur bei Stellbewegungen. 6 h × 150 mA ≈ 0,9 Ah, mit Reserve und Alterung **eine 18650-Zelle mit 2,5–3,5 Ah (bzw. LiFePO4 entsprechend)**. Das ist eine Schätzung, der echte Verbrauch wird in Phase 3 gemessen.
- Servo im Halten möglichst stromlos (selbsthemmendes Getriebe oder Servo abschalten, wenn die Position steht), das spart Akku und Wärme.

## 3. Diskussion Servo am Flansch der Luftbox

Vorschlag ist gut, weil der Antrieb unsichtbar sitzt und direkt auf die Schieberwelle wirkt. Diese Punkte müssen geklärt bzw. gelöst werden:

| Thema | Problem | Vorschlag |
|---|---|---|
| **Fail-safe ohne Feder** | Rikatronic hat eine Rückzugsfeder; ein Servo bleibt bei Defekt (Elektronik, Kabelbruch, Getriebe) einfach stehen, auch in einer gedrosselten Stellung oder in Null. Der Akku deckt nur Netzausfall ab, nicht einen Defekt der Steuerung. | Hardware-Watchdog: unabhängige Schaltung oder zweiter kleiner µC, der bei fehlendem Lebenszeichen den Servo auf Mittelstellung schickt. Alternativ eine Feder Richtung Mittelstellung mit einem Servo, der stark genug ist, dagegen zu arbeiten. |
| **Kein Handbetrieb** | Bei Defekt, Wartung oder Firmware-Update kann man den Ofen nicht mehr bedienen. | **Entschieden (E9):** einfachste Variante ist eine Steckkupplung mit Querstift (Federstecker/Splint ziehen, Servo ist frei, Griff wieder von Hand bedienbar). Originalgriff bleibt montiert. Zusätzlich Handbetrieb per MQTT und Taster an der Steuerung. Ob das am Flansch passt, zeigen die Maße. |
| **Positionsrückmeldung** | Hobby-Servos melden die Ist-Position nicht. Blockiert der Schieber (Ruß, Verzug), merkt die Steuerung das nicht. | Servo mit Feedback (z. B. Feetech/Dynamixel-Bus-Servos mit Positions-, Last- und Temperaturrückmeldung) oder magnetischer Winkelsensor AS5600 auf der Welle. |
| **Temperatur am Flansch** | Die Luftbox führt kalte Zuluft, aber das Gehäuse ist nah am Feuerraum. | Temperatur am Flansch bei Volllast messen (Phase 1). Servo-Typ mit min. 70–85 °C Betriebstemperatur wählen. |
| **Kraft und Winkel** | Drehmoment, Drehwinkel und Lage der Anschläge (Anheiz, Mittel, Null) am Flansch sind unbekannt. | In Phase 1 mit Drehmomentschlüssel/Federwaage messen, Servo mit min. Faktor 2 Reserve wählen. |
| **Nullstellung mechanisch** | Laut Anleitung ist Null nur mit gedrücktem Sperrschieber erreichbar. Wirkt der Servo hinter dieser Sperre, gibt es keine mechanische Sicherung mehr. | Nullstellung in Firmware nur in den Zuständen „Aus“ zulassen, Endlagen über Encoder überwachen. |
| **Schnittstelle (Explosionszeichnung, 18.10.)** | Der Schieberegler (67, B17378) ist eine Linearmechanik. Er treibt über die geschlitzte Zwischenwelle (68, Z35798) eine kurze Welle mit Querstift an der Seite des Zuluftreglers (69, B17377), die die beiden Klappen verdreht. Antrieb am Flansch heißt also Drehantrieb auf diese Welle. | Servo-Abtrieb mit eigener geschlitzter Hülse nach Vorbild der Zwischenwelle: Hülse über Welle und Querstift schieben = Steckkupplung (E9) ohne Zusatzteile. Benötigt: Wellen-Ø, Querstift-Ø/-Länge, Drehwinkel Null/Mittel/Anheiz, Drehmoment, Platz nach links (wo 67 sitzt), Befestigungsmöglichkeit am Gehäuse von 69. |
| **Rikatronic-Getriebe** | Die Rikatronic sitzt vermutlich genau dort (Luftreglermotor N111817, Getriebe B16464, Getriebehalterung Z36380). | Prüfen, ob Getriebehalterung/Getriebe als mechanische Schnittstelle zum Flansch passen; eigenen Servo dann daran anflanschen. |

## 4. Regelstrategie

Zustandsautomat, PID nur im Hauptabbrand. Stellbereich des PID: von der Mittelstellung (Sekundär 100 %, Primär zu) bis zu einer **Mindestöffnung**, die nie die Nullstellung erreicht.

| Zustand | Eintritt | Schieber | Austritt |
|---|---|---|---|
| **Aus** | Ofen kalt bzw. nach Ausbrand | Nullstellung | Tür geöffnet, Taster/HA „Anheizen“ oder Temperaturanstieg (s. 5) |
| **Anheizen** | Start | Anheizstellung | T > T_anbrand (Startwert 400 °C, aus Messung) und Mindestzeit |
| **Übergang** | Ende Anheizen | Rampe auf Mittelstellung | Temperatur stabil |
| **Hauptabbrand (PID)** | Ende Übergang | PID zwischen Mittelstellung und Mindestöffnung | Stellgröße am oberen Anschlag und T fällt (Ausgasung vorbei) |
| **Glut** | Ende Hauptabbrand | kleine feste Öffnung | Glut zu schwach (s. 5) oder Nachlegen |
| **Nachlegen** | Tür auf, Taster/HA oder Temperatursprung | Anheizstellung bis das Holz angebrannt ist | wie Anheizen |
| **Störung** | Sensor-/Positionsfehler, Akku leer | Mittelstellung, Alarm an HA | Quittierung |
| **Netzausfall (Akkubetrieb)** | Netzspannung weg während eines Zyklus | Regelung läuft normal weiter (E10), Meldung per MQTT soweit Router erreichbar | Netz zurück → normaler Betrieb; „Feuer aus“ → Schutzabschaltung; Akku kritisch → Notstellung |
| **Schutzabschaltung** | Ausbrand während Netzausfall, oder Netzausfall bei kaltem Ofen | Mittelstellung anfahren, Servo stromlos, ESP32 in Deep-Sleep | Netzstrom wieder da → Neustart in „Aus“ |
| **Akku kritisch** | Akkuspannung unter Schwelle während Akkubetrieb | sofort Mittelstellung, dann Schutzabschaltung | Netz zurück |

### Umsetzung von E4 (sauber + lange)
- Sollwert im Hauptabbrand ist die **untere Grenze der sauberen Verbrennung**, nicht ein Maximalwert. Startwert ca. 550–600 °C am Fühler, endgültig aus Messphase (Scheibe klar, kein sichtbarer Rauch am Schornstein, Flammenbild).
- Der PID schließt so weit, wie die Temperatur über dem Sollwert bleibt, und öffnet, sobald sie darunter fällt. Das ergibt automatisch minimale Luft bei sauberer Verbrennung.
- Zusätzlich eine obere Grenze (z. B. 750–800 °C, aus Messung) gegen Überheizen.
- Anti-Windup, D-Anteil auf Messwert mit Filter, Regeltakt 5–30 s.

## 5. Ausbrand, Meldung und Nullstellung (E5)

Hier steckt das größte Sicherheitsrisiko, deshalb ein eigener Abschnitt.

**Zwei getrennte Ereignisse statt einem:**
1. **„Nachlegen jetzt sinnvoll“** (Meldung an HA): wenn das Glutbett noch heiß genug zum Entzünden neuer Scheite ist. Nach der Anleitung braucht Nachlegen ein ausreichendes Glutbett, sonst drohen Rauch und Verpuffung. Kriterium: Brennraumtemperatur fällt unter Schwelle T_nachlegen (Startwert ca. 250–300 °C, aus Messung).
2. **„Feuer aus“ → Nullstellung:** erst wenn das Feuer sicher erloschen ist, z. B. T < T_aus (Startwert ca. 80–100 °C) für mindestens 20–30 min. Optional zweite Meldung „Ofen geschlossen“.

**Warum nicht direkt nach der Glutphase schließen:** Bei geschlossener Luft und Restglut entsteht CO im Brennraum. Öffnet dann jemand die Tür zum Nachlegen, kann das Gas-Luft-Gemisch zünden (die Anleitung warnt genau vor dieser Verpuffung).

**Wiederanheizen aus der Nullstellung:** Die Steuerung muss erkennen, dass jemand den Ofen wieder anfeuert, sonst brennt das Feuer bei geschlossener Luft an. Optionen:
- **Türkontakt (empfohlen):** Tür öffnet → sofort Anheizstellung, bevor Holz drin ist. Die Rikatronic macht das genauso (Kontaktschalter Nr. 96, Schaltstange Nr. 93).
- Taster am Ofen oder Button in HA „Anheizen“ (vergisst man leicht).
- Temperaturanstieg (zu spät als alleiniges Kriterium, nur als Rückfallebene).

Ein Türkontakt ist deshalb für E5 nicht mehr optional, sondern Voraussetzung. **Entschieden (E8): Original-Türkontakt von RIKA.** Vor dem Anschluss klären: Öffner oder Schließer, Schaltspannung, und ob es ein Reed-Kontakt oder ein Mikroschalter mit Schaltstange ist (die Ersatzteilliste nennt „Kontaktschalter“ Nr. 96 mit Schaltstange Nr. 93). Firmware entprellt und behandelt einen Kabelbruch wie „Tür offen“, damit der Fehler auf der sicheren Seite liegt (Kontakt so verdrahten, dass geschlossene Tür = geschlossener Stromkreis).

**Netzausfall und Schutzabschaltung (E10):** Bei Netzausfall regelt der ESP32 den laufenden Abbrand auf Akku normal bis „Feuer aus“ zu Ende. Danach fährt er in die Schutzabschaltung: **Mittelstellung statt Nullstellung**, Servo stromlos, Deep-Sleep bis Netzstrom wieder da ist. Mittelstellung habe ich gewählt, weil ein Ofen, der während eines Stromausfalls trotzdem von Hand angeheizt wird, dann Sekundärluft hat, statt bei Null anzubrennen. Nach Rückkehr des Netzes startet die Steuerung in „Aus“ und fährt auf Null, sofern der Ofen kalt ist.

## 6. Firmware und MQTT-Schnittstelle (E11)

**Firmware:** Arduino-Framework auf ESP32 (PlatformIO empfohlen, Arduino IDE geht auch).
- Bibliotheken (Vorschlag): `PubSubClient` oder `AsyncMqttClient` für MQTT, `Adafruit_MAX31856` (falls Sensor Typ K), `ArduinoOTA` für Updates, `ArduinoJson` für Discovery-Payloads, Servo-Bibliothek passend zum gewählten Servo.
- Struktur: Messung → Zustandsautomat → PID → Sicherheitsprüfung → Servo. Die Sicherheitsprüfung sitzt **nach** dem Regler und hat das letzte Wort.
- Parameter (Sollwerte, Schwellen, PID) im NVS/Preferences des ESP32 speichern, per MQTT änderbar, mit festen Grenzen in der Firmware.
- **Die Regelung läuft vollständig lokal.** MQTT/HA ist nur Anzeige, Meldung und Bedienung. Fällt WLAN, Broker oder HA aus, regelt der Ofen weiter.

**MQTT-Topics (Entwurf):** Präfix `rika_nex/`

| Topic | Richtung | Inhalt |
|---|---|---|
| `rika_nex/status` | ESP → | `online`/`offline` (Last Will) |
| `rika_nex/state` | ESP → | Zustand: `aus`, `anheizen`, `uebergang`, `abbrand`, `glut`, `nachlegen`, `akkubetrieb`, `schutzabschaltung`, `stoerung` |
| `rika_nex/temp/brennraum` | ESP → | °C, z. B. alle 5 s |
| `rika_nex/servo/position` | ESP → | Ist-Position 0–100 % (0 = Null, Mittel und Anheiz als feste Werte nach Kalibrierung) |
| `rika_nex/tuer` | ESP → | `offen`/`zu` |
| `rika_nex/power` | ESP → | `netz`/`akku`, dazu `rika_nex/akku/spannung` |
| `rika_nex/event` | ESP → | einmalige Ereignisse: `nachlegen_empfohlen`, `feuer_aus`, `netzausfall`, `stoerung:<code>` |
| `rika_nex/cmd/mode` | → ESP | `auto`, `hand`, `anheizen` |
| `rika_nex/cmd/position` | → ESP | Sollposition im Handbetrieb (Firmware erzwingt Sicherheitsregeln weiter) |
| `rika_nex/cfg/<param>` | ↔ | Sollwert, Schwellwerte, PID-Parameter (retained) |

- **Home Assistant per MQTT-Discovery** (`homeassistant/...`), dann erscheinen Sensoren, Schalter und Buttons automatisch. Die Nachlege-Meldung ist eine HA-Automation auf `rika_nex/event = nachlegen_empfohlen`.
- Befehle von außen können die Sicherheitsregeln nicht aushebeln (z. B. kein `cmd/position = 0` bei heißem Ofen).

## 7. Projektphasen

| Phase | Inhalt | Ergebnis |
|---|---|---|
| **1 Bestandsaufnahme** | Sensor-Teile beim Händler klären (B15248, B17692, L02783, ggf. Z32596), Flansch der Luftbox ausmessen: Wellendurchmesser, Drehwinkel der drei Stellungen, Drehmoment, Platz, Temperatur am Flansch | Maße, Teileliste, Servo-Anforderungen |
| **2 Sensor + Logging** | Sensor einbauen, Typ bestimmen, ESP32 mit Messverstärker; mehrere Abbrände manuell fahren und loggen (Stellung von Hand in HA eintragen) | Temperaturverläufe, Schwellwerte, Sollwertbereich |
| **3 Aktor** | Servo, Kupplung, Encoder, Watchdog, Akku; Tests kalt: Endlagen, Netzausfall, Absturz der Firmware | funktionierender, ausfallsicherer Antrieb |
| **4 Firmware** | Zustandsautomat, PID, Sicherheitslogik, HA-Entitäten; Test gegen die Logdaten aus Phase 2 | Firmware v1 |
| **5 Inbetriebnahme** | erst Assistenzmodus (nur Empfehlung), dann Regelung unter Aufsicht, Tuning | getunte Parameter |
| **6 Ausbau** | Statistik, Abbrandauswertung, ggf. Abgasfühler | Komfort |

## 8. Stückliste (vorläufig)

- Original: Flammtemperatursensor B17692, Flammsensorrohr B15248, Andrückwinkel L02783 (ggf. Umlenkplatte Z32596)
- ESP32-Board, Messverstärker passend zum Sensor (bei Typ K: MAX31856), Ausgleichsleitung
- Servo mit Positionsrückmeldung oder Servo + AS5600, lösbare Kupplung, Adapterflansch
- Power-Path-Lademodul, Li-Ion- oder LiFePO4-Zelle mit BMS, DC/DC-Wandler, Netzteil 5 V
- Hardware-Watchdog (z. B. ATtiny oder Watchdog-IC)
- Original-RIKA-Türkontakt (Kontaktschalter N111825, ggf. Schaltstange Z36379 und Schalterkonsole Z36378)
- 18650-Zelle 2,5–3,5 Ah (oder LiFePO4) mit BMS
- Taster/LED für lokale Bedienung, Gehäuse

## 9. Risiken
- Gewährleistung/Zulassung durch Umbau an Brennraum und Luftführung, mit dem Schornsteinfeger abstimmen.
- Verpuffung bei Nullstellung mit Restglut oder Anheizen bei geschlossener Luft (Abschnitt 5).
- Servo-Defekt ohne mechanischen Fail-safe (Abschnitt 3).
- Akku in warmer Umgebung.

## 10. Offene Fragen

| Nr. | Frage |
|---|---|
| F14 | Fotos und Maße des Flansches der Luftbox (Welle, Drehwinkel zwischen Anheiz/Mittel/Null, Platz), reicht Nico nach. |
| F19 | Sensortyp des vorhandenen Original-Sensors: Widerstand bei Raumtemperatur messen (wenige Ω = Thermoelement, ca. 1000 Ω = PT1000) und ggf. Aufdruck/Kabelfarben notieren. |

Erledigt: F11 → E8, F12 → E9, F13 → E10, F15 → E11, F16 → E14, F17 → E12, F18 → E13.
