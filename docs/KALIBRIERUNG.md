# Servo-Kalibrierung TD-8125MG 360° (Dauerdreher) am PCA9685, Kanal 1

Gemessen am 18.10.2026 am Testaufbau, Servo ohne Last. Pulswerte sind Sollwerte
der Firmware (PCA9685, 50 Hz, Prescaler 121, interner Oszillator ~25 MHz) –
der echte Puls kann wegen Oszillatortoleranz einige Prozent abweichen, die
Werte gelten daher für genau diesen PCA9685.

| Puls (µs) | Verhalten (Blick des Beobachters) |
|-----------|-----------------------------------|
| 1370      | rechts, sehr schnell              |
| 1390      | rechts, viel schneller            |
| 1410      | rechts, schneller                 |
| 1430      | rechts, langsam                   |
| 1440–1540 | Stillstand (Totband)              |
| 1560      | links, langsam                    |
| 1570      | links                             |
| 1590      | links, schneller                  |
| 1610      | links, noch schneller             |
| 1630      | links, viel schneller             |

- Totband ca. 1435–1555 µs, Mitte ca. **1495 µs**
- Kleinster Puls, der sicher dreht: rechts **1430 µs**, links **1560 µs**
- Kein Puls (FULL_OFF): Servo steht kraftlos

# Positionsservo DS3225MG 270° am PCA9685, Kanal 1

Gemessen am 21.10.2026 am Testaufbau (Nico), Arm montiert, ohne Last.

- Optische Mitte des Arms bei ca. **1530 µs** (nicht 1500).
- Kleinster sicherer Schritt: 5 µs in gleicher Richtung (ab ca. 1520 zuverlässig),
  bei Richtungswechsel mindestens 10 µs (1510 → 1515 bewegt nicht, 1520 → 1510 schon).
- Ursache: Getriebespiel + Totband des Servos; eine PCA9685-Stufe = 4,9 µs ≈ 0,66°.
- Folgerung für die Firmware: Ziele immer aus derselben Richtung anfahren,
  Änderungen < 10 µs ignorieren, Endpunkte 0 ‰ / 1000 ‰ am echten Aufbau kalibrieren.

## Vorläufige Endwerte (21.10.2026, Geodreieck, 90° auf 1530 µs)

| Stellung | Puls     |
|----------|----------|
| 0°       | 860 µs   |
| 90°      | 1530 µs  |
| 180°     | 2200 µs  |

- 1340 µs für 180° → 7,44 µs pro Grad → 1 ‰ ≈ 1,34 µs
- Welcher Wert 0 ‰ (alles zu) und welcher 1000 ‰ (Primärluft voll offen) ist, legt
  erst die Kopplung an der Welle fest. Danach Endwerte am echten Anschlag nachmessen
  und je 20 µs Abstand zum Anschlag lassen.

## Offener Punkt: Zwischenanschlag vor „ganz zu“ (21.10.2026)

Der Original-Luftschieber hat kurz vor der Stellung „ganz zu“ einen Zwischenanschlag.
Erst nach Ziehen eines kleinen Hebels lässt sich die Luftbox komplett schließen
(Stellung „Glut halten“).

- Geklärt (Nico, 21.10.): Der Anschlag sitzt nur in der Box des Schiebers, nicht in
  der Luftbox. Mit Servo gibt es ihn also mechanisch nicht mehr; die Welle lässt sich
  bis „ganz zu“ fahren. Die Sperre muss bei Bedarf in der Software nachgebildet werden.
- Pulswert ermitteln, der der Stellung des Zwischenanschlags entspricht (Schieber bis
  an den Anschlag schieben, Wellenwinkel ablesen bzw. später mit dem AS5600 messen).
- Geplant: Software-Sperre. Regler und spätere Regelung fahren nur bis knapp vor die
  Position des alten Zwischenanschlags; „Glut halten“ (ganz zu) nur über die bewusste
  Auswahl in Home Assistant, wie der Hebel beim Original.
- Position des Anschlags noch offen, Nico liest sie ab.
- Mechanisch besteht keine Gefahr für den Servo; offen ist nur die Sicherheitsfunktion
  gegen versehentliches Ganz-Zu bei Feuer.

## Voreinstellungen Home Assistant (Servo-Testprogramm)

| Auswahl         | Puls     | ‰ (vorläufig) |
|-----------------|----------|---------------|
| Anfeuern        | 860 µs   | 1000          |
| Abbrand stark   | 1530 µs  | 500           |
| Abbrand mittel  | 1750 µs  | 336 (vorläufig) |
| Abbrand leicht  | 1980 µs  | 164 (vorläufig) |
| Glut halten     | 2200 µs  | 0             |

## Luftbox-Winkel AS5600 (22.10.2026)

Ausgebaute Luftschieberbox, Diametralmagnet auf der Ausgangswelle, AS5600 am Test-D1-Mini
(rika-nex-as5600test). Nullpunkt = „ganz zu“. Drehrichtung: positiv Richtung „ganz auf“.

| Marke | Stellung                     | raw  | absolut | relativ zu „ganz zu“ |
|-------|------------------------------|------|---------|----------------------|
| 0     | ganz zu (hinter Zwischenanschlag) | 2776 | 244,0°  | 0,0°   |
| 1     | Zwischenanschlag             | 3068 | 269,6°  | +25,7°  |
| 2     | genau mittig                 | 3845 | 337,9°  | +94,0°  |
| 3     | ganz auf                     | 823  | 72,3°   | +188,3° |

- Der Monitor zeigt bei „ganz auf“ rel = −171,7°, weil die Anzeige bei ±180° umbricht.
  Tatsächlich: (823 − 2776 + 4096) / 4096 × 360° = +188,3°.
- Gesamter Drehweg der Welle ca. 188° (nicht 180°); Mitte bei 94° passt genau zur Hälfte.
- Der Zwischenanschlag liegt 25,7° vor „ganz zu“ (≈ 14 % des Wegs).
- Magnet bei allen Stellungen ok, agc 112–118, mag ≈ 2120–2130.

## Alternative Position Einlass (22.10.2026)

Magnet und AS5600 hinten am Einlass der Luftbox (statt am Wellenende). Freier Durchlauf
ohne Nullpunkt, 14:59:39–15:00:39, 604 Messwerte, langsam von Anschlag zu Anschlag (2×).

| Endlage | raw  | absolut | angefahren |
|---------|------|---------|------------|
| A = ganz auf | 1507 | 132,5°  | 3× (Start, 15:00:06, 15:00:26), Streuung ±1 raw |
| B = ganz zu  | 3530 | 310,3°  | 2× (15:00:03, 15:00:23), Streuung ±1 raw |

- Zuordnung bestätigt von Nico (15:01): Endlage A (132,5°) = „ganz auf“, B (310,3°) = „ganz zu“.
- Drehweg ganz zu → ganz auf: **182,2°**. Der Weg läuft über den 0/360°-Übergang
  (310,3° → 360°/0° → 132,5°), geprüft am Verlauf 15:00:19–15:00:23. Die zuerst
  genannten 177,8° waren der kürzere Gegenweg und sind falsch.
- Drehrichtung: Öffnen = steigender Rohwinkel (mit Umbruch). Relativ zu „ganz zu“:
  rel = ((raw − 3530) mod 4096) × 360 / 4096 → ganz auf = 182,2°.
- Die Firmware muss modular rechnen, weil der Umbruch mitten im Arbeitsbereich liegt
  (bei rel ≈ 49,7°). Alternativ Magnet/Sensor so drehen, dass der Umbruch außerhalb liegt.
- Magnet in 100 % der Messungen ok, agc 19–45, mag 2048–2142 (sehr konstant, Magnet mittig).
- Keine Sprünge; Endlagen auf ca. 0,1° wiederholbar.
- Vergleich Wellenende (22.10.): 188,3° – Abweichung ca. 6°, Ursache noch offen
  (anderes Bauteil/Übersetzung oder Anschlag nicht ganz erreicht).
- Letzter Test 15:03:18–15:03:57 (389 Messwerte): ganz zu 310,3° (raw 3530), ganz auf
  132,4° (raw 1506), Drehweg 182,3°, Magnet 100 % ok, agc 37–47, mag 2049–2141, keine Sprünge.
  Bestätigt die Werte oben; der 0/360°-Übergang liegt weiterhin im Arbeitsbereich.

### Kontrolldurchlauf nach dem Kleben (22.10.2026, 16:07–16:12)

| Stellung          | raw        | absolut        | relativ zu „ganz zu“ (raw 3530) |
|-------------------|------------|----------------|---------------------------------|
| ganz zu           | 3525–3530  | 309,8–310,3°   | 0°                              |
| Zwischenanschlag  | 3844       | 337,9°         | +27,6° (Marke 16:12:00)         |
| ganz auf          | 1503–1516  | 132,1–133,2°   | +181,8 … +182,9°                |

- Endlagen stimmen mit den Werten vor dem Kleben überein (Abweichung ≤ 1°, Streuung
  durch unterschiedlich festes Andrücken an den Anschlag). Kleber hat nichts verschoben.
- Drehweg ca. 182–183°. Zwischenanschlag +27,6° (Wellenende-Messung: +25,7°).
- Magnet 2649/2649 Messungen ok, agc 13–63, mag 2046–2144.
- 3 „Sprünge“ um 16:09:57 = sehr schnelles Drehen (ca. 400°/s), kein Messfehler.
- Für die Firmware: 0 ‰ = ganz zu (raw 3530), Zwischenanschlag ≈ 152 ‰ (27,6/182,2),
  1000 ‰ = ganz auf (raw 1507). Umbruch 0/360° bei ca. +49,7° (≈ 273 ‰).

## Servo an der Luftbox gekoppelt – Endwerte (27.10.2026)

| Stellung | Puls | Quelle |
|---|---|---|
| ganz zu (0 ‰, „Glut halten“) | **2360 µs** | Nico, über „Servo-Puls (Kalibrierung)“ angetastet: vollständig geschlossen |
| ganz auf (1000 ‰, „Anfeuern“) | **860 µs** | Nico, 28.10.: Markierung am Riemenrad stimmt mit der von Hand erprobten Endlage überein → bestätigt |

- In der Firmware 0.3.2-luftbox eingetragen (AIR_US_AT_0 = 2360), geflasht 27.10.2026.
- Weg 2360 → 860 µs = 1500 µs; bei ca. 7,4 µs/° wären das ca. 200° – mehr als die
  gemessenen ca. 182–188° der Box. Das offene Ende liegt vermutlich zwischen ca. 980 und 1000 µs
  (bzw. 860 µs drückt bereits an den Anschlag) → beim Antasten prüfen.

### Endwerte bestätigt (28.10.2026)

- 0 ‰ = 2360 µs, 1000 ‰ = 860 µs. Firmware unverändert (beide Werte schon in 0.3.2).
- Der Servo braucht über den Riemen ca. 8,0 µs/° statt der geschätzten 7,4 µs/°; die Sorge „860 µs drückt an den Anschlag“ ist damit erledigt.
- Zwischenstellungen (linear): Abbrand stark 500 ‰ = 1610 µs, mittel 335 ‰ ≈ 1858 µs, leicht 165 ‰ ≈ 2113 µs, Reglersperre 160 ‰ ≈ 2120 µs.
- Offen, sobald der AS5600 wieder angeschlossen ist: auf „Glut halten“ fahren und „Nullpunkt setzen“; dann 1000/500/335/165 ‰ fahren und prüfen, dass „Luftklappe Abweichung“ überall unter ±20 ‰ bleibt.

## AS5600 an der Sensorbrücke – Labortest (21.11.2026)

Erster Test nach Montage der Sensorbrücke (Rückseite Luftbox, `hardware/sensorbruecke-as5600/`).
**Labortest ohne Feuer**, Firmware 0.3.2-luftbox unverändert. Fahrten per MQTT ausgelöst, Werte jeweils
4 s nach dem Befehl abgelesen. Rohdaten: [`messungen/as5600-labortest-2026-11-21-rohlog.csv`](messungen/as5600-labortest-2026-11-21-rohlog.csv),
Tabelle: [`messungen/as5600-labortest-2026-11-21-ergebnis.md`](messungen/as5600-labortest-2026-11-21-ergebnis.md).

- I²C und Magnet: Sensor antwortet, Magnetstatus in allen Messungen „ok“ (Luftspalt passt).
- Drehrichtung: Öffnen = steigender Winkel, DIR auf GND bleibt richtig.
- **Neuer Nullpunkt** bei „ganz zu“ (Glut halten): **raw 3241** (Ereignis `luft:nullpunkt:3241`, im EEPROM).
  Vorher 3530 an der Einlass-Position. Vor dem Setzen zeigte der alte Wert 2,5° bei geschlossener Box.

### Fahrten über den ganzen Weg

| Soll ‰ | Puls µs | Ist ‰ aufwärts | Winkel ° | Ist ‰ abwärts | Winkel ° | Mitte ‰ | Breite ‰ |
|---|---|---|---|---|---|---|---|
| 0    | 2360 | 0   | 0,0   | 0   | 0,0   | 0   | 0  |
| 160  | 2120 | 159 | 28,9  | 131 | 23,8  | 145 | 28 |
| 250  | 1985 | 262 | 47,8  | 233 | 42,5  | 248 | 29 |
| 335  | 1857 | 355 | 64,8  | 321 | 58,4  | 338 | 34 |
| 400  | 1760 | 423 | 77,2  | 389 | 70,9  | 406 | 34 |
| 500  | 1610 | 525 | 95,7  | 488 | 89,0  | 507 | 37 |
| 600  | 1460 | 614 | 112,0 | 580 | 105,6 | 597 | 34 |
| 700  | 1310 | 714 | 130,2 | 673 | 122,6 | 694 | 41 |
| 800  | 1160 | 832 | 151,6 | 776 | 141,4 | 804 | 56 |
| 900  | 1010 | 946 | 172,4 | 882 | 160,8 | 914 | 64 |
| 1000 | 860  | 974 | 177,6 | –   | –     | –   | –  |

„Mitte“ = Mittel aus auf- und abwärts, „Breite“ = Unterschied auf/ab bei gleichem Puls.

- **Kennlinie linear:** Die Mitte liegt bis 900 ‰ innerhalb −15 … +14 ‰ vom Soll. Die Endwerte
  2360/860 µs und die lineare Abbildung passen.
- **Hysterese:** Aufwärts liegt der Ist-Wert immer über dem Soll (+12 … +45 ‰), abwärts immer darunter
  (−10 … −29 ‰). Die Welle bleibt also in Fahrtrichtung vorne stehen. Breite ca. 30–40 ‰ (5–7°), oben
  bis 64 ‰. Dadurch meldet die Plausibilitätsprüfung (±20 ‰) bei 10 von 22 Fahrten „Abweichung“.
  Ursache noch offen: Schwung bei der schnellen Fahrt (ca. 95° in 0,3 s) mit anschließend stromlosem
  Servo, oder Spiel in Servogetriebe und Riemen.
- **Einschwingen:** Jede Fahrt ist nach 0,2–0,4 s fertig, danach ändert sich der Wert nicht mehr
  (kein Kriechen).
- **Ganz auf:** Bei 860 µs nur 177,6° (974 ‰) statt der hinterlegten 182,3° (`AS_RAW_SPAN 2074`).
  Geklärt (Nico, 21.11., 19:41): Welle stromlos von Hand bis zum Anschlag „ganz auf“ gedreht (Stößel berühren
  die Klappe nicht mehr): **177,1°**, 11 Messwerte ohne Schwankung. Der Servo erreicht mit 860 µs also den Anschlag
  (177,6°). Der Drehweg an dieser Sensorposition ist ca. **177,3°** statt 182,3°.
  → `AS_RAW_SPAN` 2074 → **2018** (177,3° × 4096 / 360). Die Servo-Endwerte 2360/860 µs bleiben.
  Vor dem Anschlag gibt es ein kurzes Stück, auf dem die Klappe schon ganz offen ist und die Stößel frei laufen.
- **Ganz zu nicht immer erreicht:** Von 160 ‰ aus kommt „Glut halten“ auf 0,0°, direkt von 500 ‰ aus
  blieb die Welle bei 6,6° (36 ‰) stehen. Auch vor dem Test stand sie bei 2,5°.
  Nico (21.11., 19:32): Bei 6,6° sah die Luftbox zu aus, ließ sich von Hand aber noch 1–2 mm weiter schließen.
  Sie war also **nicht ganz zu**. Die Meldung „Abweichung +36 ‰“ war berechtigt.
- **Rauschen und Halten (E21, kalt):** 180 s auf 500 ‰ mit stromlosem Servo, 180 Messwerte, 95,2–95,3°
  (±0,05°). Kein Rauschen, keine Drift. Der Riemenantrieb hält kalt die Stellung.

### Zweite Testreihe mit 0.3.3-luftbox (Nachstellen), 21.11.2026, 20:08

Riemen neu aufgelegt bei „ganz zu“ (Box und Servo 2360 µs), Ausgangslage 0,0°, kein neuer Nullpunkt nötig.
Wartezeit 7 s pro Schritt. Rohdaten liegen bei Nico unter `messungen/as5600-labortest-2026-11-21-v033-*`.

| Soll ‰ | aufwärts: Ist ‰ (Nachstellfahrten, Abweichung davor) | abwärts: Ist ‰ (Nachstellfahrten) |
|---|---|---|
| 0    | 0 (–)                       | 30 (2, beide wirkungslos) → „Abweichung +30“ |
| 160  | 157 (0)                     | 156 (1, vorher +51) |
| 250  | 264 (0)                     | 240 (1, vorher +67) |
| 335  | 346 (2: +27, +23)           | 334 (0) |
| 400  | 399 (2: +40, +27)           | 405 (0) |
| 500  | 500 (2: +45, +31)           | 505 (0) |
| 600  | 611 (2: +40, +33)           | 598 (0) |
| 700  | 706 (2: +45, +32)           | 693 (0) |
| 800  | 802 (2: +60, +27)           | 799 (0) |
| 900  | 920 (1: +74)                | 908 (0) |
| 1000 | 1000 (0), 177,4°            | – |

- **Zwischenstellungen ok:** Nach dem Nachstellen liegen alle Stellungen von 160 bis 1000 ‰ innerhalb −10 … +20 ‰.
  Ohne Nachstellen wären es aufwärts bis +74 ‰ gewesen.
- Eine Korrekturfahrt holt nur etwa ein Drittel bis die Hälfte der Abweichung zurück (z. B. +45 → +31 mit 68 µs).
  Der Richtungswechsel frisst einen Teil des Pulses (Spiel). Deshalb braucht es meist beide Fahrten.
- Abwärts ist die Abweichung diesmal klein (−7 … +8 ‰), nur unten (250/160 ‰) wurde nachgestellt.
- Ganz auf: 860 µs → 177,4° = 1000 ‰. Der neue Drehweg (`AS_RAW_SPAN 2018`) stimmt.
- **„Glut halten“ aus offener Stellung bleibt offen:** In allen 5 Fällen (aus 160, 2× aus 500, aus 1000, nach dem
  Haltetest) stand die Welle danach bei 4,0–7,3° (+23 … +41 ‰). Das Wiederholen mit 2360 µs bewegt nichts, weil
  der Servo seine Position schon erreicht hat. Die Box ist dann nicht ganz zu.
- Haltetest 500 ‰, 120 s, Servo stromlos: nach dem Nachstellen konstant 91,8° (117 Meldungen), keine Drift.
