# RIKA NEX in Home Assistant: alle Werte erklärt

Stand: Firmware 0.3.0-luftbox (22.10.). Alle Entitäten hängen am Gerät **RIKA NEX** und werden per MQTT automatisch angelegt. Alle Werte und Ereignisse landen in der HA-Historie, das ist die Datenbasis für die spätere automatische Regelung.

## Ofen

| Wert | Was er bedeutet |
|---|---|
| **Brennraumtemperatur** (°C) | Typ-K-Fühler über MAX6675, leicht geglättet, alle 5 s. Später die Regelgröße. |
| **Feuerraumtür** (offen/zu) | Türkontakt. Öffnen und Schließen landen zusätzlich als Ereignis im Log. Ein Kabelbruch zeigt „offen“, das ist die sichere Seite. |
| **Angeheizt** / **Nachgelegt** (Buttons) | Bewegen nichts. Sie setzen nur eine Zeitmarke ins Log, damit man in den Kurven sieht, wann angefeuert bzw. nachgelegt wurde. |

## Luftbox: Steuerung (Soll)

Skala in Promille: 0 ‰ = ganz zu, 500 ‰ = Übergang Sekundär/Primär, 1000 ‰ = ganz auf.

| Wert | Was er bedeutet |
|---|---|
| **Luftbox Stellung** (Auswahl) | Voreinstellungen, Auswählen fährt sofort hin (Tabelle unten). |
| **Luftklappe** (Regler 0–1000 ‰) | Freie Soll-Stellung in 5er-Schritten. |
| **Luftklappe Stellung** (Text, z. B. „500 ‰ / 1530 µs“) | Was zuletzt an den Servo geschickt wurde: Stellung und zugehöriger Puls. |

| Stellung | Promille |
|---|---|
| Anfeuern | 1000 ‰ |
| Abbrand stark | 500 ‰ |
| Abbrand mittel | 335 ‰ |
| Abbrand leicht | 165 ‰ |
| Glut halten | 0 ‰ (ganz zu) |
| Manuell | erscheint, wenn der Regler auf einem Wert ohne Voreinstellung steht; Manuell selbst auszuwählen bewegt nichts |

**Software-Sperre:** Der Regler fährt nie unter 160 ‰, das ersetzt den alten Hebel am Zwischenanschlag. Ganz zu geht nur bewusst über „Glut halten“.

## Luftbox: Messung (Ist, vom AS5600 am Einlass)

| Wert | Was er bedeutet |
|---|---|
| **Luftbox Stellung Ist** (‰) | Tatsächliche Stellung der Welle, gleiche Skala wie das Soll. |
| **Luftbox Winkel** (°) | Dasselbe in Grad ab „ganz zu“, 0 bis ca. 182°. |
| **Luftklappe Abweichung** (‰) | Ist minus Soll, gemessen 0,5 s nach jeder Fahrt. Nahe 0 = steht, wo sie soll. |
| **Luftklappe Status** | siehe unten |
| **Luftbox Zustand** (Text, ab 0.3.1) | Stellung in Worten aus dem Ist-Wert, z. B. „Abbrand mittel · Sekundärluft 67 %, Primärluft zu“. Innerhalb ±15 ‰ einer Voreinstellung steht deren Name davor. Fehlt der Ist-Wert: Soll mit Zusatz „(Soll, Ist fehlt)“. |
| **Primärluft** / **Sekundärluft** (%, ab 0.3.1) | Getrennte Öffnung in Prozent: 0–500 ‰ öffnet die Sekundärluft, 500–1000 ‰ zusätzlich die Primärluft. Die Grenze bei 500 ‰ ist angenommen, noch nicht an der Box geprüft. |

Status-Werte:
- **bereit (nicht gestellt):** seit dem Start noch kein Befehl
- **fährt:** Servo bekommt gerade seinen Puls
- **ok:** Ist liegt innerhalb ±20 ‰ vom Soll (deckt das axiale Wellenspiel von bis zu ca. 15 ‰ ab)
- **Abweichung ±x ‰:** Ist weicht mehr ab, z. B. Riemen übergesprungen, Klappe klemmt, oder wie jetzt: Servo noch nicht gekoppelt
- **Sensor: …:** AS5600 liefert gerade keinen gültigen Wert
- **Kalibrierung … µs:** letzte Fahrt kam vom Kalibrier-Feld

## Service (Diagnose und Konfiguration)

| Wert | Was er bedeutet |
|---|---|
| **AS5600 Magnet** | „ok“, „zu schwach“, „zu stark“, „fehlt“ oder „außerhalb Bereich (±x°)“. Letzteres heißt: Winkel liegt mehr als 5° außerhalb von ganz zu bis ganz auf. |
| **Nullpunkt setzen** (Button) | Speichert die aktuelle Stellung dauerhaft als 0 ° / 0 ‰. Nur drücken, wenn die Box wirklich ganz zu steht. |
| **Servo-Puls** (Kalibrierung, µs) | Schickt einen rohen Puls (500–2500 µs) direkt an den Servo, ohne Luftbox-Grenzen. Nur zum Einmessen nach dem Koppeln, in kleinen Schritten. |
| **Sensorfehler** | „ok“ oder Fehlercode des Temperaturfühlers, z. B. Fühler offen bzw. Kabelbruch. |
| **Vergleichsstelle** | Temperatur an der Anschlussstelle des Thermoelements. Liefert erst der spätere MAX31856, beim MAX6675 bleibt sie leer. |
| **Netzversorgung** (Netz/Akku) und **Akkuspannung** (V) | Für die spätere Akku-Pufferung. Noch nicht verdrahtet, deshalb steht dort „Akku“ bzw. ca. 0 V. Das ist kein Fehler. |

## Aktueller Stand

- Solange Servo und Box nicht gekoppelt sind, zeigt der Status „Abweichung“. Das ist normal.
- Die Pulse für 0 ‰ und 1000 ‰ (2200 / 860 µs) sind vorläufig und werden nach dem Koppeln mit dem AS5600 eingemessen.
- Die alten Entitäten „Schieberstellung (Hand)“ und „Wellenwinkel“ aus dem Handschieber-Test werden automatisch entfernt.
