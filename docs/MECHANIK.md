# Mechanik – Maße und Notizen

## Luftbox (69), Befestigungslöcher an der Stirnseite (Wellenseite)

Gemessen von Nico am 21.10.2026 (Stelle: Kommentar in der Zeichnung
`zeichnungen/luftbox-riemenantrieb-as5600.png`, ca. 52 % von links / 56 % von oben,
untere Ecke der Stirnseite neben dem Wellenstück 68).

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
