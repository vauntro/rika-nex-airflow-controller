#include "temp_sensor.h"

#if TEMP_SENSOR_TYPE == SENSOR_MAX31856
#include <Adafruit_MAX31856.h>

// Thermoelement Typ K über MAX31856 (erkennt offenen Fühler und Kurzschluss)
class Max31856Sensor : public TempSensor {
 public:
  Max31856Sensor()
      : max_(PIN_SPI_CS, PIN_SPI_MOSI, PIN_SPI_MISO, PIN_SPI_SCK) {}

  bool begin() override {
    if (!max_.begin()) return false;
    max_.setThermocoupleType(MAX31856_TCTYPE_K);
    max_.setConversionMode(MAX31856_CONTINUOUS);
    max_.setNoiseFilter(MAX31856_NOISE_FILTER_50HZ);
    return true;
  }

  TempReading read() override {
    TempReading r;
    r.fault = max_.readFault();
    r.celsius = max_.readThermocoupleTemperature();
    r.coldJunction = max_.readCJTemperature();
    r.ok = (r.fault == 0) && !isnan(r.celsius) && r.celsius > -50 && r.celsius < 1300;
    return r;
  }

  const char* name() const override { return "MAX31856/TypK"; }

 private:
  Adafruit_MAX31856 max_;
};

TempSensor* createTempSensor() { return new Max31856Sensor(); }

#elif TEMP_SENSOR_TYPE == SENSOR_MAX31865
#include <Adafruit_MAX31865.h>

// PT1000 über MAX31865 (2-Leiter-Anschluss wie am Originalsensor zu erwarten)
class Max31865Sensor : public TempSensor {
 public:
  Max31865Sensor()
      : max_(PIN_SPI_CS, PIN_SPI_MOSI, PIN_SPI_MISO, PIN_SPI_SCK) {}

  bool begin() override { return max_.begin(MAX31865_2WIRE); }

  TempReading read() override {
    TempReading r;
    r.celsius = max_.temperature(MAX31865_RNOMINAL, MAX31865_RREF);
    r.fault = max_.readFault();
    if (r.fault) max_.clearFault();
    r.ok = (r.fault == 0) && r.celsius > -50 && r.celsius < 1000;
    return r;
  }

  const char* name() const override { return "MAX31865/PT1000"; }

 private:
  Adafruit_MAX31865 max_;
};

TempSensor* createTempSensor() { return new Max31865Sensor(); }

#elif TEMP_SENSOR_TYPE == SENSOR_MAX6675
#include <max6675.h>

// Thermoelement Typ K über MAX6675 (nur Lesen, 0,25 °C, bis 1024 °C).
// Erkennt nur einen offenen Fühler, keinen Kurzschluss; für den Dauerbetrieb
// ist der MAX31856 die bessere Wahl.
class Max6675Sensor : public TempSensor {
 public:
  Max6675Sensor() : max_(PIN_SPI_SCK, PIN_SPI_CS, PIN_SPI_MISO) {}

  bool begin() override {
    delay(500);  // erste Wandlung abwarten
    return true;
  }

  TempReading read() override {
    TempReading r;
    r.celsius = max_.readCelsius();  // NAN bei offenem Fühler
    r.fault = isnan(r.celsius) ? 0x01 : 0;
    r.ok = !isnan(r.celsius) && r.celsius > -10 && r.celsius < 1024;
    return r;
  }

  const char* name() const override { return "MAX6675/TypK"; }

 private:
  MAX6675 max_;
};

TempSensor* createTempSensor() { return new Max6675Sensor(); }

#else
#error "TEMP_SENSOR_TYPE in config.h setzen"
#endif
