# AS5600-Labortest Luftbox – 2026-11-21

Labortest ohne Feuer, Befehle per MQTT, Messung jeweils 4 s nach dem Befehl. Rohlog: `as5600-labortest-2026-11-21-rohlog.csv`.

## Ausgangslage (retained)

- status: online
- luft/soll: 0
- luft/stellung: 0 ‰ / 2360 µs
- luft/ist: 14
- luft/ist_winkel: 2.5
- luft/abweichung: 14
- luft/status: ok
- luft/magnet: ok

Nullpunkt gesetzt, weil ist_winkel 2,5° war (Grenze ±2°): Ereignis `luft:nullpunkt:3241`. Danach ist_winkel 0,0°, ist 0.

## Testreihe

| # | Befehl | soll ‰ | stellung | ist ‰ | ist_winkel ° | abweichung ‰ | status | magnet |
|---|---|---|---|---|---|---|---|---|
| 1 | Glut halten | 0 | 0 ‰ / 2360 µs | 0 | 0.0 | 0 | ok | ok |
| 2 | 160 | 160 | 160 ‰ / 2120 µs | 159 | 28.9 | -1 | ok | ok |
| 3 | 250 | 250 | 250 ‰ / 1985 µs | 262 | 47.8 | 12 | ok | ok |
| 4 | 335 | 335 | 335 ‰ / 1857 µs | 355 | 64.8 | 20 | ok | ok |
| 5 | 400 | 400 | 400 ‰ / 1760 µs | 423 | 77.2 | 23 | Abweichung +23 ‰ | ok |
| 6 | 500 | 500 | 500 ‰ / 1610 µs | 525 | 95.7 | 25 | Abweichung +25 ‰ | ok |
| 7 | 600 | 600 | 600 ‰ / 1460 µs | 614 | 112.0 | 14 | ok | ok |
| 8 | 700 | 700 | 700 ‰ / 1310 µs | 714 | 130.2 | 14 | ok | ok |
| 9 | 800 | 800 | 800 ‰ / 1160 µs | 832 | 151.6 | 32 | Abweichung +32 ‰ | ok |
| 10 | 900 | 900 | 900 ‰ / 1010 µs | 946 | 172.4 | 45 | Abweichung +45 ‰ | ok |
| 11 | 1000 | 1000 | 1000 ‰ / 860 µs | 974 | 177.6 | -26 | Abweichung -26 ‰ | ok |
| 12 | 900 | 900 | 900 ‰ / 1010 µs | 882 | 160.8 | -18 | ok | ok |
| 13 | 800 | 800 | 800 ‰ / 1160 µs | 776 | 141.4 | -24 | Abweichung -24 ‰ | ok |
| 14 | 700 | 700 | 700 ‰ / 1310 µs | 673 | 122.6 | -27 | Abweichung -27 ‰ | ok |
| 15 | 600 | 600 | 600 ‰ / 1460 µs | 580 | 105.6 | -20 | ok | ok |
| 16 | 500 | 500 | 500 ‰ / 1610 µs | 488 | 89.0 | -12 | ok | ok |
| 17 | 400 | 400 | 400 ‰ / 1760 µs | 389 | 70.9 | -10 | ok | ok |
| 18 | 335 | 335 | 335 ‰ / 1857 µs | 321 | 58.4 | -14 | ok | ok |
| 19 | 250 | 250 | 250 ‰ / 1985 µs | 233 | 42.5 | -17 | ok | ok |
| 20 | 160 | 160 | 160 ‰ / 2120 µs | 131 | 23.8 | -29 | Abweichung -29 ‰ | ok |
| 21 | Glut halten | 0 | 0 ‰ / 2360 µs | 0 | 0.0 | 0 | ok | ok |

## Haltetest (500 ‰, 180 s, Servo stromlos)

- Meldungen ist_winkel: 180
- min 95.2°, max 95.3°, Mittel 95.29°
- Stand am Ende: ist 523 ‰, ist_winkel 95.3°, status Abweichung +22 ‰

## Glut halten nach dem Haltetest

- ist 36 ‰, ist_winkel 6.6°, abweichung 36 ‰, status Abweichung +36 ‰, magnet ok

## Ereignisse rika_nex/event

| t (s) | Phase | Ereignis |
|---|---|---|
| 4.1 | nullpunkt | `luft:nullpunkt:3241` |
| 8.2 | schritt1:Glut halten | `luft:0/2360us` |
| 12.2 | schritt2:160 | `luft:160/2120us` |
| 16.2 | schritt3:250 | `luft:250/1985us` |
| 20.1 | schritt4:335 | `luft:335/1857us` |
| 24.1 | schritt5:400 | `luft:400/1760us` |
| 25.6 | schritt5:400 | `luft:abweichung:23` |
| 28.1 | schritt6:500 | `luft:500/1610us` |
| 29.6 | schritt6:500 | `luft:abweichung:25` |
| 32.1 | schritt7:600 | `luft:600/1460us` |
| 36.1 | schritt8:700 | `luft:700/1310us` |
| 40.1 | schritt9:800 | `luft:800/1160us` |
| 41.6 | schritt9:800 | `luft:abweichung:32` |
| 44.1 | schritt10:900 | `luft:900/1010us` |
| 45.6 | schritt10:900 | `luft:abweichung:45` |
| 48.2 | schritt11:1000 | `luft:1000/860us` |
| 49.7 | schritt11:1000 | `luft:abweichung:-26` |
| 52.2 | schritt12:900 | `luft:900/1010us` |
| 56.2 | schritt13:800 | `luft:800/1160us` |
| 57.7 | schritt13:800 | `luft:abweichung:-24` |
| 60.2 | schritt14:700 | `luft:700/1310us` |
| 61.7 | schritt14:700 | `luft:abweichung:-27` |
| 64.2 | schritt15:600 | `luft:600/1460us` |
| 68.2 | schritt16:500 | `luft:500/1610us` |
| 72.2 | schritt17:400 | `luft:400/1760us` |
| 76.2 | schritt18:335 | `luft:335/1857us` |
| 80.2 | schritt19:250 | `luft:250/1985us` |
| 84.2 | schritt20:160 | `luft:160/2120us` |
| 85.6 | schritt20:160 | `luft:abweichung:-29` |
| 88.2 | schritt21:Glut halten | `luft:0/2360us` |
| 92.3 | haltetest_fahrt | `luft:500/1610us` |
| 93.7 | haltetest_fahrt | `luft:abweichung:22` |
| 274.2 | ende | `luft:0/2360us` |
| 275.7 | ende | `luft:abweichung:36` |
