#include "GasSensor.h"
#include <math.h>

GasSensor::GasSensor(int bitadc, byte pin)
{
  _bitadc = pow(2,bitadc)-1;
  _pin = pin;
}

void GasSensor::begin() {
    pinMode(_pin, INPUT);
}

float GasSensor::read() {
    int adc = analogRead(_pin);
    float SensorVal = (float)adc / (float)_bitadc;
    return SensorVal;
}

float GasSensor::fmap(float x, float in_min, float in_max, float out_min, float out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min; // Arduino ide's map function does not support float structure.
}

float GasSensor::yaxb(float a, float x, float b) {
    return a * pow(x, b);
}

float GasSensor::inverseYaxb(float a, float y, float b) {
    return pow(y / a, 1.0 / b);
}

float GasSensor::limit(float value, float minVal, float maxVal) {
    if (value < minVal) return minVal;
    if (value > maxVal) return maxVal;
    return value;
}

float GasSensor::calculateCalValue1(float a, float b, float calibrateAir, float minPpm, float maxPpm) {
    float calAir = inverseYaxb(a, calibrateAir, b);
    return limit(fmap(calAir, minPpm, maxPpm, 0, 1), 0.01, 0.99);
}

float GasSensor::calculateCalValue2(float a, float b, float calibrateAir, float minPpm, float maxPpm) {
    float calAir = inverseYaxb(a, calibrateAir, b);
    return fmap(calAir, minPpm, maxPpm, 0, 1);
}
float GasSensor::calculateRsRoPPM(float sensorVal, float correction, float a, float b, float calValue, float air, float rlcal, float maxPpm) {
    float ratio = air * rlcal * (calValue * (sensorVal - 1)) / (sensorVal * (calValue - 1));
    return limit(inverseYaxb(a, ratio / correction, b), 0, maxPpm * correction);
}

float GasSensor::calculateRsRsPPM(float sensorVal, float a, float b, float calValue, float rlcal, float maxPpm) {
    float ratio = rlcal * (calValue * (sensorVal - 1)) / (sensorVal * (calValue - 1));
    return limit(inverseYaxb(a, ratio, b), 0, maxPpm);
}

float GasSensor::calculateRoRsPPM(float sensorVal, float correction, float a, float b, float calValue, float air, float rlcal, float maxPpm) {
    float ratio = air * rlcal * (calValue * (sensorVal - 1)) / (sensorVal * (calValue - 1));
    return limit(inverseYaxb(1 / pow(a, 1 / b), ratio / correction, 1 / b), 0, maxPpm * correction);
}
