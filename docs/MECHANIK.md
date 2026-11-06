# Mechanik – Maße und Notizen

## Luftbox (69), Befestigungslöcher an der Stirnseite (Wellenseite)

Gemessen von Nico am 21.10.2026 (Stelle: untere Ecke der Stirnseite neben dem Wellenstück 68).

| Maß                                   | Wert    |
|---------------------------------------|---------|
| Loch außen (Deckel/Stirnseite)        | 5,6 mm  |
| Kanal im Alu-Strangprofil (Schraubkanal) | 2,6 mm |

Folgerung:
- Schraubkanal 2,6 mm passt für gewindefurchende Schrauben M3 (z. B. DIN 7500 / Torx,
  Kernloch M3 in Alu ca. 2,7 mm) bzw. Blechschrauben 3,5 mm – Originalschraube prüfen.
- Halterwinkel (Servohalter, Sensorwinkel) können an diesen Kanälen befestigt werden:
  Originalschraube durch eine gleichartige, um die Winkeldicke längere ersetzen.
  Bohrung im Winkel 3,2–3,5 mm. Einschraubtiefe im Kanal mindestens ca. 8 mm.

## Luftbox-Welle

- Durchmesser **8,0 mm** (gemessen von Nico, 22.10.2026)
- Passende Teile: GT2-Riemenrad 20T mit **8-mm-Bohrung** (die 20T-Räder aus dem vorhandenen Set
  haben 5 mm und passen nur auf der Servoseite), Stellring 8 mm (z. B. für Vorspannung/Anlage),
  Kunststoffkappe mit 8-mm-Bohrung für den Magneten.

## Noch offen
- ~~Durchmesser Wellenstück 68~~ → 8 mm
- Abstand Wellenmitte 68 bis Unterkante Luftbox
- Typ/Länge der Originalschrauben an der Stirnseite

## Axialspiel der Luftbox-Welle (22.10.2026)

- Nico: Die Welle der Luftbox lässt sich minimal nach vorn und hinten schieben.
- Vermutete Ursache für die Streuung der AS5600-Werte an den Anschlägen (ca. −0,5° … +1°,
  siehe rika-nex-servotest/KALIBRIERUNG.md): Der Abstand Magnet–Chip ändert sich, bei nicht
  exakt zentriertem Magneten verschiebt sich dadurch auch der gemessene Winkel.
- Abhilfe (Vorschlag): Axialspiel festlegen, z. B. Stellring auf der Welle gegen das Gehäuse,
  Passscheibe/Unterlegscheibe, oder Vorspannung in eine Richtung mit Wellfeder/Federscheibe.
  Später kann auch die Nabe des Riemenrads als Anlage dienen.
- Nachtrag 22.10.2026, 17:07: Beim ersten Spieltest war die Luftbox nicht richtig verschraubt.
  Die Streuung lag also zumindest teilweise an der losen Verschraubung. Messung „vorn“
  (17:03, 181,1° / 994 ‰) verworfen, Spieltest wird mit fest verschraubter Box wiederholt.
- Spieltest mit fest verschraubter Box (22.10.2026, 17:07–17:08), Box auf „ganz zu“, nur axial
  geschoben, nicht gedreht:
  - Welle vorn: 0,4° (2 ‰)
  - Welle hinten: 3,2° (ca. 18 ‰)
  - **Differenz 2,8° ≈ 15 ‰**, mehrfach hin und her reproduzierbar (0,4° ↔ 3,2°).
  - agc/mag werden vom Servo-Testprogramm nicht gesendet, daher nicht erfasst.
- Folgerung: Das Axialspiel verfälscht den Winkel deutlich (mehr als die ±5°-Toleranz
  nur an den Anschlägen abfängt, im Arbeitsbereich direkt als Fehler sichtbar). Axialspiel vor
  der Servo-Kalibrierung beseitigen (Stellring / Passscheibe / Federvorspannung).
- Entscheidung Nico (22.10.2026, 17:09): Das Axialspiel wird vorerst nicht beseitigt (baulich
  sehr aufwendig, vermutlich herstellungsbedingt).
- Konsequenz für die Firmware: Der Servo ist für die Stellung führend; der AS5600 dient als
  Plausibilitätskontrolle mit Toleranz ca. ±20 ‰ (Störung erst bei größerer Abweichung, z. B.
  Riemen übergesprungen, Klappe klemmt).
- Option für später ohne Eingriff an der Box: Feder-/Wellscheibe zwischen Riemenrad-Nabe und
  Gehäuse als axiale Vorspannung. Magnet beim nächsten Setzen mit Zentrierhilfe exakt auf die
  Achse bringen (dann wirkt Axialspiel fast nur auf die Feldstärke, kaum auf den Winkel).

## Servo-Antrieb – Stand 22.10.2026

- Servo-Riemenrad: eigenes Druckteil GT2 20T mit 25T-Aufnahme (teile/servo-riemenrad-25t/),
  bei JLC3DP bestellt in allen drei Varianten, je 2 Stück:
  - Spiel 0,05 mm – SLA, 8228 Resin
  - Spiel 0,10 mm – MJF, PA12-HP Nylon, schwarz gefärbt
  - Spiel 0,20 mm – MJF, PA12-HP Nylon, schwarz gefärbt
  Befestigung: kurze Schraube M3 × 6–8 von oben in den Servo (Länge nach Einschraubtiefe wählen).
- Wellenseite: GT2 20T Alu-Riemenrad mit 8-mm-Bohrung (Saipor), Riemen-Set Youmile 2GT 6 mm.
- Verworfen (Entscheidung Nico): Alu-Disc + Riemenrad, Messingrohr/Distanzhülsen, Kupplungen,
  Gewindeadapter – das Druckteil ersetzt alles.
- Servohalter und weitere Halter baut Nico selbst.

## Dauer- und Stresstest Antrieb (28.10.2026)

Aufbau: DS3225MG, gedrucktes GT2-20T-Riemenrad mit 25T-Aufnahme, Riemen auf die Luftbox-Welle. AS5600 nicht angeschlossen, Beurteilung der Mechanik durch Sichtprüfung (Nico).

| Test | Ablauf | Ergebnis Steuerung |
|---|---|---|
| Testreihe | 10 s je Stellung, Voreinstellungen und 250/750 ‰, abgebrochen nach 16 Schritten | 16/16 Befehle quittiert |
| Stresstest | 1,5 s je Fahrt (Minimum, bei dem ein voller Hub im 1-s-Puls fertig wird), 120 Fahrten in ca. 3 min: ganz auf → zufällig 160–1000 ‰ → ganz zu → zufällige Voreinstellung | 120/120 quittiert, kein Neustart, keine I²C-Fehler, Sperre nie ausgelöst; 60 volle Hübe an die Anschläge |

Mechanik nach dem Stresstest:
- Servo kalt.
- Markierung am Riemenrad stimmt bei „Anfeuern“ und „Glut halten“ exakt, kein Riemensprung.
- Kein Brummen an den Anschlägen, keine Riemengeräusche.

**Ergebnis: Antrieb freigegeben.** Nächster Schritt: AS5600 anschließen, Nullpunkt bei „Glut halten“ setzen, Linearität bei 1000/500/335/165 ‰ prüfen.

### Nachtest nach Riemenjustage (28.10.2026, abends)

Servo mit Unterlegscheiben unter allen vier Laschen nach vorn versetzt, weil der Riemen leicht am inneren Bord des Riemenrads anlief. Danach 8 Fahrten im 10-s-Takt und 48 im 3-s-Takt (manuell gestoppt): alle quittiert, keine Fehler. Endlage „Anfeuern“ (860 µs) geprüft: Fahrweg passt, kein Anschlagen. Firmware unverändert.

### 10-Minuten-Stresstest und Riemensprung (28.10.2026, spät)

200 Fahrten im 3-s-Takt, alle quittiert, keine Fehler, darunter 18 volle Hübe zwischen „Anfeuern“ und „Glut halten“. Danach schloss „Glut halten“ ca. 1 mm nicht mehr vollständig, obwohl weiter 2360 µs gesendet wurden: Der Riemen ist vermutlich um einen Zahn übergesprungen, wahrscheinlich weil er nach dem Versetzen des Servos zu locker war. Abhilfe: Riemen bei „Glut halten“ neu auflegen, Klappe dabei von Hand ganz zu, strammer spannen, beide Endlagen prüfen. Pulswerte unverändert. Später erkennt der AS5600 einen Riemensprung als „Abweichung“.

## AS5600-Sensorbrücke (Rückseite Luftbox) – Stand 06.11.2026

Abgestimmt mit Nico am 30.10. und 06.11.2026. Ersetzt den früheren Plan „Winkel aus Flachprofil 30 × 2 an einer
Gehäuseschraube“ (E16). Dateien und Montage: `hardware/sensorbruecke-as5600/`.

- Ort: Rückseite der Luftbox (Servo und Riemen sitzen auf der Gegenseite). Der Magnet Ø 6 × 2,5 ist mittig
  auf dem Wellenende verklebt und steht **1 mm** vor der Ebene der seitlichen Laschen.
- Befestigung an den beiden freien mittleren Laschenlöchern (Ø 6,8, Abstand **147 mm** Mitte–Mitte, gesamt
  160 mm über die Laschen) mit **M5 × 30** (Laschen 6,2 dick, gemessen Nico 06.11.) und **Distanzhülsen 12 mm** (Entscheidung Nico: flach mit Hülsen
  statt gekantet, „bekomme ich genauer hin“).
- Brücke aus 2-mm-Alublech (Nicos Platte 300 × 200 × 2), liegt über der mittleren Querrippe (3 mm breit).
  Auf Nicos Wunsch so schmal wie möglich (wenig Luftwiderstand): Steg 8 mm, Augen Ø 14 um die M5-Löcher,
  Mittelplatte 24 × 24, Länge 161 (06.11.; erster Stand Steg 16, Platte 32 × 32). Untergrenze Steg ca. 6 mm,
  darunter biegt sich das Blech auf 147 mm beim Anziehen und Hantieren.
- AS5600-Platine 23,2 × 22,7 mm, Löcher Ø 3,6, Lochmitten 16,1 × 16,3 mm (gemessen Nico). Stiftleisten
  auf der Rückseite (Chip-Gegenseite) eingelötet; sie gehen durch ein Fenster 17 × 11 in der Brücke.
- Höhenkette: Magnet 1 + Luftspalt ca. 1,9 + Chip 1,5 + Platine 1,6 + Abstandshalter M3 × 6 = Hülse 12.

