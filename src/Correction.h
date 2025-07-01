#ifndef CORRECTION_H
#define CORRECTION_H

#include <Arduino.h>

float fmap(float x, float in_min, float in_max, float out_min, float out_max);
float limit(float value, float minVal, float maxVal);
float scaleTemperature(float temp, int mode);
float calculateCorrection(float temp, float rh, const String& model);
float unsupported_calculateCorrection1(float temp, float rh, float a_RH33, float b_RH33, float a_RH85, float b_RH85, int scale_mode);
float unsupported_calculateCorrection2(float temp, float rh, float a_RH30, float b_RH30, float a_RH60, float b_RH60, float a_RH85, float b_RH85);

#endif

