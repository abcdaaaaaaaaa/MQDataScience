#include "AirQuality.h"
#include <math.h>

float exponential_interpolate(float x, float x_min, float x_max, float ppm_min, float ppm_max) {
    float log_min = log10(ppm_min);
    float log_max = log10(ppm_max);
    float ratio = (float)(x - x_min) / (x_max - x_min);
    float log_val = log_min + ratio * (log_max - log_min);
    return pow(10, log_val);
}

float logarithmic_interpolate(float x, float x_min, float x_max, float ppm_min, float ppm_max) {
    float ratio = (float)(x - x_min) / (x_max - x_min);
    float log_val = log10(1 + ratio * 9);
    float norm = log_val / log10(10);
    return ppm_min + norm * (ppm_max - ppm_min);
}

float airConcentration(String m, float sensorVal) {
  float ppm_min, ppm_max;
  if (m == "MQ2" || m == "MQ4" || m == "MQ5" || m == "MQ6" || m == "MQ8" || m == "MQ9" || m == "MQ136" || m == "MQ137" || m == "MQ138" || m == "MQ216") ppm_min = 200, ppm_max = 10000;
  else if (m == "MQ303A" || m == "MQ303B"){ ppm_min = 1.2, ppm_max = 3.45; }
  else if (m == "MQ7"){ ppm_min = 50, ppm_max = 4000; }
  else if (m == "MQ135"){ ppm_min = 10, ppm_max = 200; }
  else if (m == "MQ214"){ ppm_min = 1000; ppm_max = 20000; }
  else if (m == "MQ306A"){ ppm_min = 15; ppm_max = 30; }
  else if (m == "MQ309A"){ ppm_min = 160, ppm_max = 260; }
  else if (m == "MQ3"){ ppm_min = 0.103; ppm_max = 10; } // the result must be multiplied by ×50 to convert the mg/L --> ppm
  else if (m == "MQ131" || m == "MQ131_LOW"){ ppm_min = 5; ppm_max = 100; } // for MQ131_LOW the result must be multiplied by ×0.02 to convert the ppb --> ppm
  else if (m == "MQ307A"){ ppm_min = 0; ppm_max = 0; } // Air concentration value of MQ307A is not available.
  else { ppm_min = 0; ppm_max = 0; }
  return exponential_interpolate(sensorVal, 0, 1, ppm_min, ppm_max);
}

float unsupported_airConcentration(float ppm_min, float ppm_max, float sensorVal) {
  return exponential_interpolate(sensorVal, 0, 1, ppm_min, ppm_max);
}
