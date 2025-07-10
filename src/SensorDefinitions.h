#ifndef SENSOR_DEFINITIONS_H
#define SENSOR_DEFINITIONS_H

#include <Arduino.h>

struct GasModel {
    const char* gasName;
    float a;
    float b;
    float minPpm;
    float maxPpm;
};

struct SensorModel {
    const char* model;
    float air;
    float calibrateAir;
    float rlcal;
    bool useCorrection;
    const GasModel* gasList;
    uint8_t gasCount;
};

bool isMQSensor(String model, String mqList[], int listSize);
SensorModel* getSensorModel(const String& modelName);

#endif
