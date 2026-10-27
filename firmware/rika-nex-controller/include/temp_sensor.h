#pragma once
// Austauschbare Schnittstelle für den Brennraumfühler.
// Welche Implementierung genutzt wird, legt TEMP_SENSOR_TYPE in config.h fest.

#include <Arduino.h>
#include "config.h"

struct TempReading {
  bool ok = false;       // gültiger Messwert
  float celsius = NAN;   // Brennraumtemperatur
  float coldJunction = NAN;  // nur Thermoelement: Vergleichsstellentemperatur
  uint8_t fault = 0;     // Fehlerbits des Messverstärkers (0 = kein Fehler)
};

class TempSensor {
 public:
  virtual ~TempSensor() = default;
  virtual bool begin() = 0;
  virtual TempReading read() = 0;
  virtual const char* name() const = 0;
};

TempSensor* createTempSensor();
