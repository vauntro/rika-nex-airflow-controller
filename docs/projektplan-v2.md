# Projektplan v2: Abbrandregelung für RIKA NEX 8 kW (Scheitholz, ohne Rikatronic)

Stand: 18.10.2026 · Ersetzt v1 (`projektplan-v1.md` bleibt als Verlauf)

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
- Akku-Kapazität: muss mindestens für eine Fahrt in Mittelstellung plus Meldung reichen. Wenn der Abbrand auf Akku weitergeregelt werden soll, für ca. 4–6 h Ofenbetrieb auslegen (Servo die meiste Zeit stromlos bzw. im Halten).

## 3. Diskussion Servo am Flansch der Luftbox

Vorschlag ist gut, weil der Antrieb unsichtbar sitzt und direkt auf die Schieberwelle wirkt. Diese Punkte müssen geklärt bzw. gelöst werden:

| Thema | Problem | Vorschlag |
|---|---|---|
| **Fail-safe ohne Feder** | Rikatronic hat eine Rückzugsfeder; ein Servo bleibt bei Defekt (Elektronik, Kabelbruch, Getriebe) einfach stehen, auch in einer gedrosselten Stellung oder in Null. Der Akku deckt nur Netzausfall ab, nicht einen Defekt der Steuerung. | Hardware-Watchdog: unabhängige Schaltung oder zweiter kleiner µC, der bei fehlendem Lebenszeichen den Servo auf Mittelstellung schickt. Alternativ eine Feder Richtung Mittelstellung mit einem Servo, der stark genug ist, dagegen zu arbeiten. |
| **Kein Handbetrieb** | Bei Defekt, Wartung oder Firmware-Update kann man den Ofen nicht mehr bedienen. | Lösbare Kupplung zwischen Servo und Welle (Klauen- oder Stiftkupplung), Originalgriff bleibt montiert. Zusätzlich Handbetrieb über Home Assistant und Taster an der Steuerung. |
| **Positionsrückmeldung** | Hobby-Servos melden die Ist-Position nicht. Blockiert der Schieber (Ruß, Verzug), merkt die Steuerung das nicht. | Servo mit Feedback (z. B. Feetech/Dynamixel-Bus-Servos mit Positions-, Last- und Temperaturrückmeldung) oder magnetischer Winkelsensor AS5600 auf der Welle. |
| **Temperatur am Flansch** | Die Luftbox führt kalte Zuluft, aber das Gehäuse ist nah am Feuerraum. | Temperatur am Flansch bei Volllast messen (Phase 1). Servo-Typ mit min. 70–85 °C Betriebstemperatur wählen. |
| **Kraft und Winkel** | Drehmoment, Drehwinkel und Lage der Anschläge (Anheiz, Mittel, Null) am Flansch sind unbekannt. | In Phase 1 mit Drehmomentschlüssel/Federwaage messen, Servo mit min. Faktor 2 Reserve wählen. |
| **Nullstellung mechanisch** | Laut Anleitung ist Null nur mit gedrücktem Sperrschieber erreichbar. Wirkt der Servo hinter dieser Sperre, gibt es keine mechanische Sicherung mehr. | Nullstellung in Firmware nur in den Zuständen „Aus“ zulassen, Endlagen über Encoder überwachen. |
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
| **Netzausfall** | Netzspannung weg | Mittelstellung, Meldung an HA (solange WLAN/Router läuft) | Netz zurück |

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

Ein Türkontakt ist deshalb für E5 nicht mehr optional, sondern Voraussetzung.

## 6. Home-Assistant-Integration
- ESPHome als Firmware-Basis bietet sich an (native HA-API, OTA-Updates, PID-Komponente vorhanden). Für den Zustandsautomaten und die Sicherheitslogik ist eigener C++-Code (Custom Component) sinnvoll, damit die Sicherheitsfunktionen nicht von HA abhängen.
- Entitäten: Brennraumtemperatur, Schieberposition, Zustand, Akkuspannung, Netzstatus, Türkontakt, Sollwert (einstellbar), Handbetrieb-Schalter, Buttons „Anheizen“ und „Nachgelegt“.
- Benachrichtigungen per HA-Automation: Nachlegen, Feuer aus/geschlossen, Störung, Netzausfall.
- **Die Regelung läuft vollständig lokal auf dem ESP32.** HA ist nur Anzeige und Bedienung.

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
- Reed-Kontakt + Magnet für die Feuerraumtür
- Taster/LED für lokale Bedienung, Gehäuse

## 9. Risiken
- Gewährleistung/Zulassung durch Umbau an Brennraum und Luftführung, mit dem Schornsteinfeger abstimmen.
- Verpuffung bei Nullstellung mit Restglut oder Anheizen bei geschlossener Luft (Abschnitt 5).
- Servo-Defekt ohne mechanischen Fail-safe (Abschnitt 3).
- Akku in warmer Umgebung.

## 10. Offene Fragen

| Nr. | Frage |
|---|---|
| F11 | Ist ein Türkontakt (Reed-Kontakt an der Feuerraumtür) für dich machbar? Nach Abschnitt 5 halte ich ihn für Pflicht, wenn automatisch auf Null geschlossen wird. |
| F12 | Lösbare Kupplung am Servo, damit der Griff im Notfall wieder von Hand bedient werden kann: einverstanden? |
| F13 | Soll auf Akku nur in Mittelstellung gefahren und gemeldet werden, oder soll der Abbrand auf Akku weitergeregelt werden? Das bestimmt die Akkugröße. |
| F14 | Kannst du den Flansch der Luftbox fotografieren bzw. ausmessen (Welle, Drehwinkel zwischen Anheiz/Mittel/Null)? |
| F15 | Firmware mit ESPHome (plus eigener Sicherheitslogik) oder komplett eigene Arduino/ESP-IDF-Firmware? |
