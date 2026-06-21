#ifndef GASSENSOR_H
#define GASSENSOR_H

#include <Arduino.h>

class GasSensor {
public:
    GasSensor(int bitadc, byte pin);
    void begin();
    float read();
    float calculateRsRoPPM(float sensorVal, float correction, float a, float b, float calValue, float air, float rlcal, float maxPpm);
    float calculateRsRsPPM(float sensorVal, float a, float b, float calValue, float rlcal, float maxPpm);
    float calculateRoRsPPM(float sensorVal, float correction, float a, float b, float calValue, float air, float rlcal, float maxPpm);
    float calculateCalValue1(float a, float b, float calibrateAir, float minPpm, float maxPpm);
    float calculateCalValue2(float a, float b, float calibrateAir, float minPpm, float maxPpm);

private:
    byte _pin;
    int _bitadc;
    float fmap(float x, float in_min, float in_max, float out_min, float out_max);
    float inverseYaxb(float a, float y, float b);
    float limit(float value, float minVal, float maxVal);
};

#endif
