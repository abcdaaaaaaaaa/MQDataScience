#ifndef AIRQUALITY_H
#define AIRQUALITY_H

#include <Arduino.h>

float exponential_interpolate(float x, float x_min, float x_max, float ppm_min, float ppm_max);
float logarithmic_interpolate(float x, float x_min, float x_max, float ppm_min, float ppm_max);
float airConcentration(String m, float sensorVal);
float unsupported_airConcentration(float ppm_min, float ppm_max, float sensorVal);

#endif
