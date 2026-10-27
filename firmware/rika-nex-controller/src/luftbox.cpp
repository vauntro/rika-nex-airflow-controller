#include "luftbox.h"

#include <EEPROM.h>
#include <Wire.h>

#include "config.h"

namespace luftbox {
namespace {

PubSubClient* mq = nullptr;
DiscoveryFn publishDiscovery = nullptr;
TopicFn topic = nullptr;

// --- Zustand -----------------------------------------------------------------
bool pcaOk = false;
int soll = -1;                  // Soll-Stellung in ‰, -1 = seit dem Start nicht gestellt
int ist = -1;                   // Ist-Stellung (AS5600) in ‰, -1 = ungültig
int asRawClosed = AS_RAW_CLOSED_DEFAULT;
unsigned long pulseUntil = 0;   // 0 = kein Puls aktiv
unsigned long checkAt = 0;      // Zeitpunkt der Plausibilitätsprüfung nach einer Fahrt
bool calibrationMove = false;   // letzte Fahrt kam vom Kalibrier-Puls
unsigned long lastAsRead = 0;
unsigned long lastAsPublish = 0;
int lastAsRawPublished = -1000;
String lastSensorStatus;
String lastStatus;

struct Preset { const char* name; int permille; };
const Preset kPresets[] = {AIR_PRESETS};
const char* const kManual = "Manuell";

void pub(const char* suffix, const String& value, bool retain = false) {
  if (mq && mq->connected()) mq->publish(topic(suffix).c_str(), value.c_str(), retain);
}

void event(const String& e) { pub("event", e); }

// --- PCA9685 (ein Servo-Kanal, 50 Hz) -----------------------------------------
bool pcaWrite(uint8_t reg, uint8_t val) {
  Wire.beginTransmission(PCA9685_ADDR);
  Wire.write(reg);
  Wire.write(val);
  return Wire.endTransmission() == 0;
}

bool pcaBegin() {
  if (!pcaWrite(0x00, 0x10)) return false;  // Sleep
  pcaWrite(0xFE, 121);                       // Prescaler 50 Hz
  pcaWrite(0x01, 0x04);                      // Totem-Pole
  pcaWrite(0x00, 0x20);                      // Auto-Increment, aufwachen
  delay(5);
  pcaWrite(0x00, 0xA0);                      // Restart
  return true;
}

void pcaSet(uint16_t on, uint16_t off) {
  Wire.beginTransmission(PCA9685_ADDR);
  Wire.write(0x06 + 4 * SERVO_CHANNEL);
  Wire.write(on & 0xFF);
  Wire.write(on >> 8);
  Wire.write(off & 0xFF);
  Wire.write(off >> 8);
  Wire.endTransmission();
}

void pulseOff() {
  pcaSet(0, 0x1000);  // FULL_OFF: kein Puls, Servo kraftlos
  pulseUntil = 0;
}

bool pulse(int us) {
  if (!pcaOk) pcaOk = pcaBegin();  // z. B. nach Umstecken bei laufendem Board
  if (!pcaOk) {
    event("luft:pca9685_fehlt");
    return false;
  }
  pcaSet(0, (uint16_t)(us * 4096UL / 20000UL));
  pulseUntil = millis() + SERVO_MOVE_MS;
  if (pulseUntil == 0) pulseUntil = 1;
  checkAt = pulseUntil + AIR_CHECK_DELAY_MS;
  return true;
}

// --- Umrechnung ‰ <-> µs ---------------------------------------------------------
int permilleToUs(int p) {
  p = constrain(p, 0, 1000);
  int us = AIR_US_AT_0 + (int)lroundf(p * (AIR_US_AT_1000 - AIR_US_AT_0) / 1000.0f);
  return constrain(us, min(AIR_US_AT_0, AIR_US_AT_1000), max(AIR_US_AT_0, AIR_US_AT_1000));
}

const char* presetName(int permille) {
  for (const Preset& p : kPresets)
    if (p.permille == permille) return p.name;
  return kManual;
}

void setStatus(const String& s) {
  if (s == lastStatus) return;
  lastStatus = s;
  pub("luft/status", s, true);
}

// Fährt die Luftbox auf eine Stellung. viaPreset = bewusste Auswahl (darf unter die Sperre).
void moveTo(int permille, bool viaPreset) {
  permille = constrain(permille, 0, 1000);
  if (!viaPreset && permille < AIR_LOCK_PERMILLE) {
    // Software-Sperre wie der Hebel am Original-Schieber: ganz zu nur über "Glut halten"
    permille = AIR_LOCK_PERMILLE;
    event("luft:sperre");
  }
  int us = permilleToUs(permille);
  if (!pulse(us)) return;
  soll = permille;
  calibrationMove = false;
  pub("luft/soll", String(soll), true);
  pub("luft/preset", presetName(soll), true);
  pub("luft/stellung", String(soll) + " ‰ / " + String(us) + " µs", true);
  event("luft:" + String(soll) + "/" + String(us) + "us");
  setStatus("fährt");
}

// --- Zustand in Worten -------------------------------------------------------------
// Rikatronic-Aufteilung: 0–500 ‰ öffnet die Sekundärluft (Primär zu),
// 500–1000 ‰ öffnet zusätzlich die Primärluft (Sekundär voll offen).
String describe(int p) {
  p = constrain(p, 0, 1000);
  int sek = min(p, 500) / 5;           // %
  int pri = max(p - 500, 0) / 5;       // %
  String luft;
  if (p <= 10) luft = "ganz zu";
  else if (p >= 990) luft = "ganz auf";
  else if (pri == 0) luft = "Sekundärluft " + String(sek) + " %, Primärluft zu";
  else luft = "Sekundärluft offen, Primärluft " + String(pri) + " %";
  // nächstgelegene Voreinstellung, wenn nah genug
  for (const Preset& pr : kPresets)
    if (abs(p - pr.permille) <= AIR_PRESET_NEAR_PERMILLE) return String(pr.name) + " · " + luft;
  return luft;
}

void publishDescription() {
  int p = ist >= 0 ? ist : soll;
  if (p < 0) return;
  String text = describe(p);
  if (ist < 0) text += " (Soll, Ist fehlt)";
  pub("luft/zustand", text, true);
  pub("luft/primaer", String(max(constrain(p, 0, 1000) - 500, 0) / 5), true);
  pub("luft/sekundaer", String(min(constrain(p, 0, 1000), 500) / 5), true);
}

// --- AS5600 ---------------------------------------------------------------------
bool asRead(uint8_t reg, uint8_t* buf, uint8_t n) {
  Wire.beginTransmission(AS5600_ADDR);
  Wire.write(reg);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom((uint8_t)AS5600_ADDR, n) != n) return false;
  for (uint8_t i = 0; i < n; i++) buf[i] = Wire.read();
  return true;
}

void loadZero() {
  EEPROM.begin(16);
  uint16_t magic = EEPROM.read(0) | (EEPROM.read(1) << 8);
  int raw = EEPROM.read(2) | (EEPROM.read(3) << 8);
  if (magic == EEPROM_MAGIC && raw >= 0 && raw < 4096) asRawClosed = raw;
}

void saveZero(int raw) {
  EEPROM.write(0, EEPROM_MAGIC & 0xFF);
  EEPROM.write(1, EEPROM_MAGIC >> 8);
  EEPROM.write(2, raw & 0xFF);
  EEPROM.write(3, raw >> 8);
  EEPROM.commit();
}

void readAngle() {
  uint8_t b[2], st;
  if (!asRead(0x0C, b, 2) || !asRead(0x0B, &st, 1)) {
    ist = -1;
    if (lastSensorStatus != "keine Antwort") {
      lastSensorStatus = "keine Antwort";
      pub("luft/magnet", lastSensorStatus, true);
    }
    return;
  }
  int raw = ((b[0] & 0x0F) << 8) | b[1];
  String status = !(st & 0x20) ? "fehlt" : (st & 0x08) ? "zu stark" : (st & 0x10) ? "zu schwach" : "ok";
  // Weg ab "ganz zu" modulo 4096 (Umbruch liegt im Arbeitsbereich). ±5° an den Anschlägen
  // werden auf 0 bzw. Vollausschlag geklemmt, alles weiter außerhalb ist eine Störung.
  int rel = ((raw - asRawClosed) % 4096 + 4096) % 4096;
  bool inRange = true;
  if (rel >= 4096 - AS_TOL_RAW) rel = 0;
  else if (rel > AS_RAW_SPAN && rel <= AS_RAW_SPAN + AS_TOL_RAW) rel = AS_RAW_SPAN;
  else if (rel > AS_RAW_SPAN) inRange = false;
  if (status == "ok" && !inRange) {
    int dev = rel - AS_RAW_SPAN < 4096 - rel ? rel - AS_RAW_SPAN : -(4096 - rel);
    char tb[40];
    snprintf(tb, sizeof(tb), "außerhalb Bereich (%+.1f°)", dev * 360.0f / 4096.0f);
    status = tb;
  }
  if (status != lastSensorStatus) {
    lastSensorStatus = status;
    pub("luft/magnet", status, true);
  }
  if (status != "ok") {
    ist = -1;
    return;
  }
  ist = (int)lroundf(rel * 1000.0f / AS_RAW_SPAN);
  int d = abs(raw - lastAsRawPublished);
  d = min(d, 4096 - d);
  if (d < AS_CHANGE_RAW && millis() - lastAsPublish < AS_PUBLISH_MS) return;
  lastAsRawPublished = raw;
  lastAsPublish = millis();
  char buf[16];
  snprintf(buf, sizeof(buf), "%.1f", rel * 360.0f / 4096.0f);
  pub("luft/ist_winkel", buf);
  pub("luft/ist", String(ist));
  publishDescription();
}

// Nach jeder Fahrt: stimmt die gemessene Stellung mit dem Soll überein?
void checkPosition() {
  if (soll < 0 || calibrationMove) return;
  if (ist < 0) {
    setStatus("Sensor: " + lastSensorStatus);
    return;
  }
  int diff = ist - soll;
  pub("luft/abweichung", String(diff), true);
  if (abs(diff) > AIR_CHECK_TOL_PERMILLE) {
    setStatus("Abweichung " + String(diff > 0 ? "+" : "") + String(diff) + " ‰");
    event("luft:abweichung:" + String(diff));
  } else {
    setStatus("ok");
  }
}

// --- Home Assistant ---------------------------------------------------------------
void discoverSensor(const char* id, const char* name, const char* stateSuffix, const char* unit,
                    const char* icon, bool diagnostic = false) {
  JsonDocument d;
  d["name"] = name;
  d["state_topic"] = topic(stateSuffix);
  if (unit) {
    d["unit_of_measurement"] = unit;
    d["state_class"] = "measurement";
  }
  d["icon"] = icon;
  if (diagnostic) d["entity_category"] = "diagnostic";
  publishDiscovery("sensor", id, d);
}

}  // namespace

void begin(PubSubClient& mqtt, DiscoveryFn discovery, TopicFn topicFn) {
  mq = &mqtt;
  publishDiscovery = discovery;
  topic = topicFn;
  loadZero();
  // Nach dem Start kein Puls: der Servo bewegt sich erst auf Befehl
  pcaOk = pcaBegin();
  if (pcaOk) pulseOff();
  else Serial.println("PCA9685 nicht gefunden");
}

void announce() {
  {
    JsonDocument d;
    d["name"] = "Luftklappe";
    d["command_topic"] = topic("cmd/luft_soll");
    d["state_topic"] = topic("luft/soll");
    d["min"] = 0;
    d["max"] = 1000;
    d["step"] = 5;
    d["mode"] = "slider";
    d["unit_of_measurement"] = "‰";
    d["icon"] = "mdi:valve";
    publishDiscovery("number", "luftklappe", d);
  }
  {
    JsonDocument d;
    d["name"] = "Luftbox Stellung";
    d["command_topic"] = topic("cmd/luft_preset");
    d["state_topic"] = topic("luft/preset");
    JsonArray opts = d["options"].to<JsonArray>();
    opts.add(kManual);
    for (const Preset& p : kPresets) opts.add(p.name);
    d["icon"] = "mdi:fire";
    publishDiscovery("select", "luftbox_stellung", d);
  }
  discoverSensor("luftklappe_stellung", "Luftklappe Stellung", "luft/stellung", nullptr, "mdi:valve");
  discoverSensor("luftbox_stellung_ist", "Luftbox Stellung Ist", "luft/ist", "‰", "mdi:angle-acute");
  discoverSensor("luftbox_winkel", "Luftbox Winkel", "luft/ist_winkel", "°", "mdi:angle-acute");
  discoverSensor("luftklappe_abweichung", "Luftklappe Abweichung", "luft/abweichung", "‰", "mdi:delta");
  discoverSensor("luftklappe_status", "Luftklappe Status", "luft/status", nullptr, "mdi:check-decagram");
  discoverSensor("luftbox_zustand", "Luftbox Zustand", "luft/zustand", nullptr, "mdi:weather-windy");
  discoverSensor("primaerluft", "Primärluft", "luft/primaer", "%", "mdi:arrow-up-bold-box-outline");
  discoverSensor("sekundaerluft", "Sekundärluft", "luft/sekundaer", "%", "mdi:arrow-down-bold-box-outline");
  discoverSensor("as5600_magnet", "AS5600 Magnet", "luft/magnet", nullptr, "mdi:magnet", true);
  {
    JsonDocument d;
    d["name"] = "Nullpunkt setzen";
    d["command_topic"] = topic("cmd/luft_nullpunkt");
    d["payload_press"] = "setzen";
    d["icon"] = "mdi:target";
    d["entity_category"] = "config";
    publishDiscovery("button", "nullpunkt", d);
  }
  {
    // Nur zum Kalibrieren: roher Servo-Puls ohne Grenzen der Luftbox
    JsonDocument d;
    d["name"] = "Servo-Puls (Kalibrierung)";
    d["command_topic"] = topic("cmd/servo_puls");
    d["state_topic"] = topic("servo/puls");
    d["min"] = 500;
    d["max"] = 2500;
    d["step"] = 5;
    d["mode"] = "box";
    d["unit_of_measurement"] = "µs";
    d["icon"] = "mdi:tune-variant";
    d["entity_category"] = "config";
    publishDiscovery("number", "servo_puls", d);
  }
  // Zustände nach (Neu-)Verbindung erneut senden
  if (soll >= 0) {
    pub("luft/soll", String(soll), true);
    pub("luft/preset", presetName(soll), true);
  }
  lastSensorStatus = "";
  lastStatus = "";
  lastAsRawPublished = -1000;
  setStatus(soll < 0 ? "bereit (nicht gestellt)" : "ok");
}

bool handleMessage(const String& t, const String& msg) {
  if (t == "cmd/luft_soll") {
    if (msg.length()) moveTo((int)lroundf(msg.toFloat()), false);
    return true;
  }
  if (t == "cmd/luft_preset") {
    for (const Preset& p : kPresets) {
      if (msg == p.name) {
        moveTo(p.permille, true);
        return true;
      }
    }
    return true;  // "Manuell" bewegt nichts
  }
  if (t == "cmd/luft_nullpunkt") {
    uint8_t b[2];
    if (asRead(0x0C, b, 2)) {
      asRawClosed = ((b[0] & 0x0F) << 8) | b[1];
      saveZero(asRawClosed);
      lastAsRawPublished = -1000;
      event("luft:nullpunkt:" + String(asRawClosed));
    } else {
      event("luft:nullpunkt_fehler");
    }
    return true;
  }
  if (t == "cmd/servo_puls") {
    int us = constrain((int)lroundf(msg.toFloat()), 500, 2500);
    if (pulse(us)) {
      calibrationMove = true;
      pub("servo/puls", String(us), true);
      event("luft:kalibrierung:" + String(us) + "us");
      setStatus("Kalibrierung " + String(us) + " µs");
    }
    return true;
  }
  return false;
}

void loop() {
  unsigned long now = millis();
  if (pulseUntil && (long)(now - pulseUntil) >= 0) pulseOff();
  if (mq && mq->connected() && now - lastAsRead >= AS_INTERVAL_MS) {
    lastAsRead = now;
    readAngle();
  }
  if (checkAt && (long)(now - checkAt) >= 0) {
    checkAt = 0;
    checkPosition();
  }
}

int sollPermille() { return soll; }
int istPermille() { return ist; }

}  // namespace luftbox
