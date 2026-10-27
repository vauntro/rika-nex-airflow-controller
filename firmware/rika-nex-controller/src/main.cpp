// RIKA NEX Abbrandregelung – Firmware Phase 2, ESP32 oder ESP8266 (D1 Mini)
//
// Misst Brennraumtemperatur, Türkontakt und Netz/Akku und stellt die Luftbox über
// den Servo (Soll aus Home Assistant: Regler oder Voreinstellung), mit dem AS5600 als
// Ist-Wert-Kontrolle. Noch keine automatische Regelung: die Stellung gibt man in
// Home Assistant vor, alles wird per MQTT mitgeloggt.

#include <Arduino.h>
#include <ArduinoJson.h>
#include <ArduinoOTA.h>
#include <PubSubClient.h>
#if defined(ESP8266)
#include <ESP8266WiFi.h>
#else
#include <WiFi.h>
#endif
#include <Wire.h>

#include "config.h"
#include "luftbox.h"
#include "secrets.h"
#include "temp_sensor.h"

namespace {

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);
TempSensor* sensor = nullptr;

// Messwerte
TempReading lastReading;
float tempFiltered = NAN;
bool doorOpen = true;
bool onMains = true;
float batteryVolts = NAN;

unsigned long lastSample = 0;
unsigned long lastPublish = 0;
unsigned long lastMqttAttempt = 0;

String topic(const char* suffix) { return String(TOPIC_PREFIX) + suffix; }

// ---------------------------------------------------------------------------
// Home Assistant MQTT-Discovery
// ---------------------------------------------------------------------------
void addDevice(JsonDocument& doc) {
  JsonObject dev = doc["device"].to<JsonObject>();
  dev["identifiers"][0] = DEVICE_ID;
  dev["name"] = "RIKA NEX";
  dev["manufacturer"] = "Eigenbau";
  dev["model"] = "Abbrandregelung";
  dev["sw_version"] = FW_VERSION;
  doc["availability_topic"] = topic("status");
}

void publishDiscovery(const char* component, const char* objectId, JsonDocument& doc) {
  addDevice(doc);
  doc["unique_id"] = String(DEVICE_ID) + "_" + objectId;
  doc["object_id"] = String(DEVICE_ID) + "_" + objectId;
  String cfgTopic = String("homeassistant/") + component + "/" + DEVICE_ID + "/" + objectId + "/config";
  String payload;
  serializeJson(doc, payload);
  mqtt.publish(cfgTopic.c_str(), payload.c_str(), true);
}

void announceToHomeAssistant() {
  {
    JsonDocument d;
    d["name"] = "Brennraumtemperatur";
    d["state_topic"] = topic("temp/brennraum");
    d["unit_of_measurement"] = "°C";
    d["device_class"] = "temperature";
    d["state_class"] = "measurement";
    publishDiscovery("sensor", "temp_brennraum", d);
  }
  {
    JsonDocument d;
    d["name"] = "Vergleichsstelle";
    d["state_topic"] = topic("temp/vergleichsstelle");
    d["unit_of_measurement"] = "°C";
    d["device_class"] = "temperature";
    d["entity_category"] = "diagnostic";
    publishDiscovery("sensor", "temp_cj", d);
  }
  {
    JsonDocument d;
    d["name"] = "Sensorfehler";
    d["state_topic"] = topic("temp/fehler");
    d["entity_category"] = "diagnostic";
    publishDiscovery("sensor", "sensor_fault", d);
  }
  {
    JsonDocument d;
    d["name"] = "Feuerraumtür";
    d["state_topic"] = topic("tuer");
    d["payload_on"] = "offen";
    d["payload_off"] = "zu";
    d["device_class"] = "door";
    publishDiscovery("binary_sensor", "tuer", d);
  }
  {
    JsonDocument d;
    d["name"] = "Netzversorgung";
    d["state_topic"] = topic("power");
    d["payload_on"] = "netz";
    d["payload_off"] = "akku";
    d["device_class"] = "power";
    publishDiscovery("binary_sensor", "netz", d);
  }
  {
    JsonDocument d;
    d["name"] = "Akkuspannung";
    d["state_topic"] = topic("akku/spannung");
    d["unit_of_measurement"] = "V";
    d["device_class"] = "voltage";
    d["state_class"] = "measurement";
    d["entity_category"] = "diagnostic";
    publishDiscovery("sensor", "akku_spannung", d);
  }
  // Ersetzte Entitäten aus älteren Firmware-Ständen in Home Assistant entfernen
  for (const char* old : {"homeassistant/select/rika_nex/schieber_hand/config",
                          "homeassistant/sensor/rika_nex/wellenwinkel/config"})
    mqtt.publish(old, "", true);
  luftbox::announce();
  {
    JsonDocument d;
    d["name"] = "Nachgelegt";
    d["command_topic"] = topic("cmd/ereignis");
    d["payload_press"] = "nachgelegt";
    publishDiscovery("button", "nachgelegt", d);
  }
  {
    JsonDocument d;
    d["name"] = "Angeheizt";
    d["command_topic"] = topic("cmd/ereignis");
    d["payload_press"] = "angeheizt";
    publishDiscovery("button", "angeheizt", d);
  }
}

// ---------------------------------------------------------------------------
// MQTT
// ---------------------------------------------------------------------------
void onMqttMessage(char* rawTopic, byte* payload, unsigned int len) {
  String t(rawTopic);
  String msg;
  msg.reserve(len);
  for (unsigned int i = 0; i < len; i++) msg += (char)payload[i];

  if (t.startsWith(TOPIC_PREFIX) && luftbox::handleMessage(t.substring(strlen(TOPIC_PREFIX)), msg)) return;
  if (t == topic("cmd/ereignis")) {
    if (msg == "nachgelegt" || msg == "angeheizt") {
      mqtt.publish(topic("event").c_str(), msg.c_str());
    }
  }
}

void ensureMqtt() {
  if (mqtt.connected() || WiFi.status() != WL_CONNECTED) return;
  if (millis() - lastMqttAttempt < 5000) return;
  lastMqttAttempt = millis();

  if (mqtt.connect(DEVICE_ID, MQTT_USER, MQTT_PASSWORD, topic("status").c_str(), 1, true, "offline")) {
    mqtt.publish(topic("status").c_str(), "online", true);
    mqtt.subscribe(topic("cmd/#").c_str());
    announceToHomeAssistant();
    mqtt.publish(topic("state").c_str(), "luftbox_hand", true);
  }
}

// ---------------------------------------------------------------------------
// Messung
// ---------------------------------------------------------------------------
void sample() {
  lastReading = sensor->read();
  if (lastReading.ok) {
    tempFiltered = isnan(tempFiltered)
                       ? lastReading.celsius
                       : tempFiltered + TEMP_FILTER_ALPHA * (lastReading.celsius - tempFiltered);
  }

  bool nowOpen = digitalRead(PIN_DOOR) == HIGH;  // Pull-up: offen oder Kabelbruch = HIGH
  if (nowOpen != doorOpen) {
    doorOpen = nowOpen;
    if (mqtt.connected()) {
      mqtt.publish(topic("tuer").c_str(), doorOpen ? "offen" : "zu", true);
      mqtt.publish(topic("event").c_str(), doorOpen ? "tuer_auf" : "tuer_zu");
    }
  }

  bool nowMains = PIN_MAINS_SENSE < 0 || digitalRead(PIN_MAINS_SENSE) == HIGH;
  if (nowMains != onMains) {
    onMains = nowMains;
    if (mqtt.connected()) mqtt.publish(topic("event").c_str(), onMains ? "netz_zurueck" : "netzausfall");
  }

#if defined(ESP8266)
  batteryVolts = analogRead(PIN_BATTERY) / 1023.0f * BATTERY_FULLSCALE_V;
#else
  batteryVolts = analogReadMilliVolts(PIN_BATTERY) / 1000.0f * BATTERY_DIVIDER;
#endif
}

void publishMeasurements() {
  if (!mqtt.connected()) return;
  char buf[16];

  if (lastReading.ok) {
    snprintf(buf, sizeof(buf), "%.1f", tempFiltered);
    mqtt.publish(topic("temp/brennraum").c_str(), buf);
  }
  if (!isnan(lastReading.coldJunction)) {
    snprintf(buf, sizeof(buf), "%.1f", lastReading.coldJunction);
    mqtt.publish(topic("temp/vergleichsstelle").c_str(), buf);
  }
  snprintf(buf, sizeof(buf), "0x%02X", lastReading.fault);
  mqtt.publish(topic("temp/fehler").c_str(), lastReading.ok ? "ok" : buf);

  mqtt.publish(topic("tuer").c_str(), doorOpen ? "offen" : "zu", true);
  mqtt.publish(topic("power").c_str(), onMains ? "netz" : "akku", true);
  snprintf(buf, sizeof(buf), "%.2f", batteryVolts);
  mqtt.publish(topic("akku/spannung").c_str(), buf);
}

void setupWifi() {
  WiFi.mode(WIFI_STA);
#if defined(ESP8266)
  WiFi.hostname(DEVICE_ID);
#else
  WiFi.setHostname(DEVICE_ID);
#endif
  WiFi.setAutoReconnect(true);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
}

}  // namespace

void setup() {
  Serial.begin(115200);
#ifdef PIN_DOOR_EXTERNAL_PULLUP
  pinMode(PIN_DOOR, INPUT);
#else
  pinMode(PIN_DOOR, INPUT_PULLUP);
#endif
  if (PIN_MAINS_SENSE >= 0) pinMode(PIN_MAINS_SENSE, INPUT);
#if !defined(ESP8266)
  analogReadResolution(12);
#endif

  sensor = createTempSensor();
  if (!sensor->begin()) Serial.printf("Messverstärker %s nicht gefunden\n", sensor->name());

  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  luftbox::begin(mqtt, publishDiscovery, topic);

  setupWifi();
  ArduinoOTA.setHostname(DEVICE_ID);
  ArduinoOTA.setPassword(OTA_PASSWORD);
  ArduinoOTA.begin();

  mqtt.setServer(MQTT_HOST, MQTT_PORT);
  mqtt.setBufferSize(MQTT_MAX_PACKET_SIZE);
  mqtt.setCallback(onMqttMessage);
}

void loop() {
  ArduinoOTA.handle();
  ensureMqtt();
  mqtt.loop();
  luftbox::loop();

  unsigned long now = millis();
  if (now - lastSample >= SAMPLE_INTERVAL_MS) {
    lastSample = now;
    sample();
  }
  if (now - lastPublish >= PUBLISH_INTERVAL_MS) {
    lastPublish = now;
    publishMeasurements();
    Serial.printf("T=%.1f°C ok=%d tuer=%s netz=%d akku=%.2fV luft soll=%d ist=%d\n", tempFiltered,
                  lastReading.ok, doorOpen ? "offen" : "zu", onMains, batteryVolts, luftbox::sollPermille(),
                  luftbox::istPermille());
  }
}
