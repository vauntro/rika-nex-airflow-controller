# Projektplan v1: Abbrandregelung für RIKA NEX (Scheitholz, ohne Rikatronic)

Stand: 18.10.2026 · Status: Entwurf, offene Fragen am Ende

## 1. Ziel

Der zentrale Luftschieber des NEX soll automatisch so verstellt werden, dass jeder Abbrand sauber, effizient und möglichst gleichmäßig verläuft. Messgröße ist die Brennraumtemperatur oben im Feuerraum, Stellgröße die Schieberposition. Die Regelung ersetzt das, was man heute von Hand macht: Anheizstellung, nach dem Anbrennen Mittelstellung, dann weiter Richtung Null drosseln, beim Nachlegen wieder auf.

## 2. Ausgangslage aus den Unterlagen

| Thema | Fakt | Quelle |
|---|---|---|
| Luftschieber | Ein Regler für Primär- und Sekundärluft: Anheizstellung = beide 100 % offen, Mittelstellung = Primär zu / Sekundär 100 %, Nullstellung = beide zu. Zwischen Mittel und Null wird nur die Sekundärluft gedrosselt. | Anleitung S. 12, `rika-nex-manuelle-luftsteuerung.md` |
| Kennlinie | Keine quantitative Kennlinie Schieberweg → Luftmenge dokumentiert. | dito |
| Sicherheit | Nullstellung dichtet 100 % ab und ist im Betrieb verboten (Verpuffungsgefahr). Bei starker Rauchentwicklung nach dem Nachlegen: Tür zu, Anheizstellung. | Anleitung S. 12 |
| Rikatronic-Vorbild | Die RIKATRONIC4-Variante hat Flammtemperatursensor (B17692) im Flammsensorrohr (B15248), Luftreglermotor (N111817) mit Getriebe (B16464), Elektrohubmagnet, Türkontaktschalter. Bei Stromausfall öffnet eine Rückzugsfeder die Luftklappe. | Ersatzteilliste (Datei 03), FAQ |
| Fühlerposition | Ganz oben im Brennraum, Spitze ragt seitlich in eine Aussparung der oberen Umlenkplatte, links der Mitte. Diese Position ist der Rikatronic-Sensor. | Anleitung S. 19 |
| Leistungsdaten (8 kW) | Nennleistung 8 kW, Teillast 4 kW, Auflage ~2,2 kg (Teillast ~1,1 kg), Abgastemperatur ~206 °C, Kaminzug 12 Pa (max. 15 Pa), Flachfeuerung: nur eine Lage auf Grundglut. | Technische Daten |
| Abbrandphasen | Abbrandphase ca. 45–90 min, Glutphase bis 4 h. Pyrolyse 150–550 °C, Gasoxidation ab ca. 400 °C. | FAQ |

**Wichtige Folgerung:** Laut Ersatzteilliste sind Sensor, Sensorrohr und Motor nur bei der RIKATRONIC4-Variante verbaut. Ein NEX ohne Rikatronic hat sehr wahrscheinlich keinen Brennraumfühler. Das ist abgeleitet und muss am Ofen geprüft werden (Frage F1).

## 3. Systemarchitektur (Vorschlag)

```
 Thermoelement Typ K ──► MAX31856 ──┐
 (Brennraum oben)                    │
 optional: Abgasfühler, Türkontakt ──┤
                                     ▼
                              Mikrocontroller (ESP32)
                         Zustandsautomat + PID + Sicherheit
                                     │
                     Schrittmotor-/Servotreiber + Endschalter
                                     ▼
                Aktor am Reglerhebel/Schieber (mit Rückstellfeder → offen)
                                     │
                    WLAN/MQTT → Home Assistant / Web-UI / Logging
```

### 3.1 Sensorik
- **Brennraumtemperatur:** Mantelthermoelement Typ K (Inconel, 3–6 mm), Messbereich bis ca. 1000 °C, Auswertung mit MAX31856 (Fehlererkennung für offenen Fühler/Kurzschluss). Alternative: Original-Rikatronic-Sensor B17692 samt Rohr B15248, falls bezahlbar und der Signaltyp klar ist.
- **Einbau:** an der dokumentierten Rikatronic-Position, ideal über das Original-Flammsensorrohr. Ob der Brennraum dort eine vorbereitete Öffnung hat, muss geprüft werden.
- **Optional, empfohlen:** Türkontakt (Reed-Kontakt) zur sicheren Nachlege-Erkennung (Rikatronic macht das auch), Abgastemperatur im Rauchrohr als Plausibilitätskanal.
- **Optional, später:** Lambdasonde für echte Verbrennungsgüte. Teuer und aufwendig, für v1 nicht nötig.

### 3.2 Aktorik
Drei Varianten, Entscheidung offen (F2):

| Variante | Beschreibung | Vorteile | Nachteile |
|---|---|---|---|
| A: Außen am Reglergriff | Linearantrieb oder Schrittmotor mit Spindel greift am Griff/Hebel an, kein Eingriff in den Ofen | reversibel, kein Öffnen der Luftbox | Optik, Montagepunkt am Steinmantel, Kraft/Weg unbekannt |
| B: Rikatronic-Teile nachrüsten | Reglereinheit B17682 bzw. Motor N111817 + Getriebe B16464 + Hubmagnet | mechanisch passend, Fail-safe-Konzept vorhanden | Teileverfügbarkeit/Preis, Ansteuerung der Originalteile unbekannt, Eingriff in Ofen |
| C: Eigener Aktor in der Luftbox | Servo/Schrittmotor direkt an der Zwischenwelle (Z35798) oder am Reglerhebel (L02747) | unsichtbar, kurze Wege | Hitze, Platz, Umbau |

**Anforderungen unabhängig von der Variante:**
- Position muss bekannt sein: Referenzfahrt auf Endschalter oder Potentiometer/Encoder als Rückmeldung.
- **Fail-safe:** Bei Stromausfall, Absturz oder Sensorfehler geht der Schieber selbsttätig in eine sichere offene Stellung (Feder wie bei Rikatronic, oder Supercap/Akku-Puffer).
- Die Nullstellung ist mechanisch nur mit gedrücktem Sperrschieber erreichbar (Anleitung). Diese Sperre im Regelbetrieb beibehalten, damit der Aktor die Nullstellung physisch nicht anfahren kann, oder die Nullstellung per Software und Endschalter sperren.
- Kraft und Weg am Griff vorher messen (Federwaage, Messschieber).

### 3.3 Steuerung
- ESP32 (z. B. mit ESPHome oder eigener Firmware in C++/Arduino), Temperatur alle 1–2 s, Regeltakt 5–30 s (der Ofen ist träge, Speichermasse ~130 kg).
- Lokale Bedienung (Taster „Nachlegen“, Status-LED) plus Web-UI/MQTT. Die Regelung läuft autark, auch ohne WLAN.
- Datenlogging von Anfang an (Temperatur, Position, Zustand), weil die Reglerparameter aus Messdaten bestimmt werden.

## 4. Regelstrategie

Ein reiner PID über den ganzen Abbrand funktioniert nicht gut: Der Prozess ändert sich über die Phasen stark, die Stellgröße ist nichtlinear (Primärluft nur im Anheizbereich) und in der Glutphase würde ein PID die Luft öffnen, um die Solltemperatur zu halten, was nur die Glut schneller verbrennt. Vorschlag: **Zustandsautomat mit PID nur in der Hauptabbrandphase.**

| Zustand | Eintritt | Schieber | Austritt |
|---|---|---|---|
| **Aus / Bereit** | Ofen kalt (T < ~60 °C) | Mittelstellung oder offen (nie automatisch Null, siehe F5) | Temperaturanstieg oder Taster |
| **Anheizen** | Start erkannt (dT/dt > Schwelle) oder Taster | Anheizstellung, fest | T > T_anbrand (z. B. 350–450 °C, aus Messung) und Mindestzeit erfüllt |
| **Übergang** | Ende Anheizen | Rampe auf Mittelstellung (Primär zu) | Temperatur stabil steigend |
| **Hauptabbrand (PID)** | Ende Übergang | PID regelt nur den Sekundärbereich: zwischen Mittelstellung und einer **Mindestöffnung > Null** | Temperatur fällt trotz offener Luft (Ausgasung beendet) |
| **Ausbrand / Glut** | Peak überschritten, dT/dt dauerhaft negativ, Stellgröße am oberen Anschlag | Fest auf kleine Öffnung (Glut erhalten, Scheibenspülung) | T < T_glut_ende oder Nachlegen |
| **Nachlegen** | Türkontakt öffnet, Taster, oder Temperatursprung | Anheizstellung bis neues Holz angebrannt, dann wie oben | T > T_anbrand |
| **Störung** | Sensorfehler, unplausibler Wert, Positionsfehler | sichere offene Stellung, Alarm | Quittierung |

### PID-Details
- Regelgröße Brennraumtemperatur, Sollwert zunächst z. B. 550–650 °C. Der richtige Wert wird in der Messphase ermittelt (sauberer Abbrand ohne Überhitzung, Scheibe bleibt klar).
- Anti-Windup (Clamping) und Ausgangsbegrenzung auf den erlaubten Bereich.
- D-Anteil auf den Messwert, nicht auf den Fehler, mit Filter. Thermoelemente im Feuer rauschen.
- Mögliche Linearisierung der Stellgröße über eine in der Messphase aufgenommene Kennlinie.
- Ggf. Gain-Scheduling: andere Parameter zu Beginn und am Ende des Abbrands.
- Optional als Komfortstufe: Sollwert aus gewünschter Leistung bzw. Raumtemperatur ableiten (Kaskade). Für v1 nicht nötig.

### Sicherheitsregeln (fest in Firmware, nicht parametrierbar)
1. Während Betrieb (T > Schwelle) nie Nullstellung.
2. Sensorfehler, Watchdog-Reset, Stromausfall → sichere offene Stellung.
3. Starker Temperatureinbruch direkt nach Nachlegen (Schwelbrand-Risiko) → Anheizstellung, wie es die Anleitung bei Rauchentwicklung empfiehlt.
4. Übertemperatur → auf Mindestöffnung drosseln und warnen (Primärluft ist dann ohnehin zu).
5. Handbetrieb jederzeit möglich (Aktor auskuppeln oder Override).

## 5. Projektphasen

| Phase | Inhalt | Ergebnis |
|---|---|---|
| **0 Klärung** | Offene Fragen beantworten, Variante für Sensor und Aktor wählen | Entscheidung, Stückliste v1 |
| **1 Bestandsaufnahme** | Ofen begutachten: vorhandener Fühler/Öffnung? Schieberweg, Kraft, Anschläge, Platz in der Luftbox, Zugang hinter dem Stein | Fotos, Maße, Kraft/Weg |
| **2 Messphase (nur loggen)** | Thermoelement + ESP32 einbauen, mehrere Abbrände **manuell** fahren und Temperatur + Schieberstellung (vorerst notiert oder per Poti) loggen | Temperaturverläufe je Phase, Sollwertbereich, Streckenverhalten (Totzeit, Zeitkonstante) |
| **3 Aktor-Prototyp** | Aktor bauen/montieren, Referenzfahrt, Endlagen, Fail-safe testen (kalt!) | mechanisch funktionierender Antrieb |
| **4 Firmware** | Zustandsautomat, PID, Sicherheitslogik, Logging, UI; erst als Simulation mit den Messdaten aus Phase 2 testen | Firmware v1 |
| **5 Inbetriebnahme** | Zuerst nur „Assistent“ (Empfehlung anzeigen, nicht stellen), dann geregelter Betrieb unter Aufsicht, PID-Tuning | getunte Parameter, Abnahme |
| **6 Ausbau** | Home-Assistant-Integration, Raumtemperatur-Kaskade, Nachlegehinweis, Statistik | Komfortfunktionen |

## 6. Stückliste (vorläufig, abhängig von F1/F2)

- ESP32-Board, Netzteil 5 V, Gehäuse (außerhalb der heißen Zone)
- MAX31856-Modul, Thermoelement Typ K Mantel Inconel 3–6 mm, ausreichend Länge, hitzefeste Ausgleichsleitung
- Schrittmotor NEMA17 + Spindel/Linearführung + TMC2209 **oder** Linearaktor mit Poti-Rückmeldung **oder** Rikatronic-Teile
- Endschalter / Hall-Sensor, Rückstellfeder bzw. Kupplung
- Reed-Kontakt für Feuerraumtür (optional)
- Zweites Thermoelement für Rauchrohr (optional)

## 7. Risiken

- **Zulassung und Gewährleistung:** Der NEX ist als Feuerstätte typgeprüft. Eine Bohrung im Brennraum oder Umbauten an der Luftführung können Gewährleistung und Betriebserlaubnis berühren; vorher mit Schornsteinfeger klären. Variante A (außen am Griff) ist hier am unkritischsten.
- **Verpuffung** bei zu wenig Luft nach dem Nachlegen. Wird durch Mindestöffnung, Nachlege-Erkennung und Sicherheitsregeln adressiert.
- **Sensorhaltbarkeit:** Thermoelement im Flammbereich verrußt und altert (Rikatronic-Anleitung sieht regelmäßige Reinigung vor).
- **Nichtlineare, unbekannte Kennlinie** des Schiebers. Wird in Phase 2 vermessen.
- **Hitze an Elektronik und Aktor:** Elektronik nicht in der Luftbox, Aktortemperatur prüfen.

## 8. Offene Fragen

| Nr. | Frage | Warum relevant |
|---|---|---|
| F1 | Ist am Ofen bereits ein Brennraumfühler oder eine Öffnung/ein Sensorrohr an der beschriebenen Stelle vorhanden? Laut Ersatzteilliste gibt es den nur bei RIKATRONIC4. | entscheidet, ob gebohrt/nachgerüstet werden muss |
| F2 | Welche Aktor-Variante: A außen am Griff, B Rikatronic-Originalteile, C eigener Aktor in der Luftbox? Ist ein Eingriff in den Ofen in Ordnung? | bestimmt Mechanik, Kosten, Zulassungsrisiko |
| F3 | Welche Stellung soll bei Stromausfall/Fehler angefahren werden: Anheizstellung (wie Rikatronic) oder Mittelstellung? | Fail-safe-Konstruktion |
| F4 | Was ist das Hauptziel: sauberer Abbrand, lange Brenndauer pro Auflage, konstante Wärmeabgabe oder Raumtemperaturregelung? | Wahl der Führungsgröße und des Sollwerts |
| F5 | Soll der Regler nach vollständigem Ausbrand automatisch auf Nullstellung schließen (Wärmeverlust über den Kamin vermeiden)? | sicherheitskritisch, braucht sichere Erkennung „Feuer aus“ |
| F6 | Welche Plattform: ESP32 mit ESPHome/Home Assistant, eigene Firmware, oder anderes (Raspberry Pi, SPS)? Gibt es schon Home Assistant? | Software-Architektur |
| F7 | Ist ein Türkontakt für die Nachlege-Erkennung möglich bzw. gewünscht? | robuste Phasenerkennung |
| F8 | 8-kW- oder 6-kW-Ausführung? | Leistungs- und Temperaturwerte unterscheiden sich |
| F9 | Welche Werkzeuge/Erfahrung sind vorhanden (3D-Druck, Metallbearbeitung, Löten, Programmieren)? | Umfang selbst gebaut vs. gekauft |
| F10 | Zusätzlicher Abgasfühler im Rauchrohr gewünscht? | Plausibilisierung, Effizienzanzeige |
