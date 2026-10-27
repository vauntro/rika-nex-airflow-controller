#pragma once
// Luftbox-Steuerung: Servo am PCA9685 (Riemen 1:1 auf die Luftbox-Welle) und
// AS5600 als Ist-Wert-Kontrolle. Alle Werte und Befehle laufen über MQTT und
// erscheinen per Discovery im Home-Assistant-Gerät "RIKA NEX".
//
// Stellung in Promille wie bei der Rikatronic: 0 ‰ = ganz zu (Glut halten),
// 500 ‰ = Übergang Sekundär/Primär, 1000 ‰ = ganz auf (Anfeuern).

#include <Arduino.h>
#include <ArduinoJson.h>
#include <PubSubClient.h>

namespace luftbox {

using DiscoveryFn = void (*)(const char* component, const char* objectId, JsonDocument& doc);
using TopicFn = String (*)(const char* suffix);

void begin(PubSubClient& mqtt, DiscoveryFn discovery, TopicFn topic);
// Nach jeder (Neu-)Verbindung mit dem Broker: Discovery und Zustände senden.
void announce();
// true, wenn die Nachricht zur Luftbox gehörte
bool handleMessage(const String& topicSuffix, const String& msg);
void loop();

// Für die serielle Statuszeile
int sollPermille();  // -1 = seit dem Start nicht gestellt
int istPermille();   // -1 = ungültig

}  // namespace luftbox
