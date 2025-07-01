#include "Correction.h"
#include <math.h>

float fmap(float x, float in_min, float in_max, float out_min, float out_max) {
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min; // Arduino ide's map function does not support float structure.
}

float limit(float value, float minVal, float maxVal) {
    if (value < minVal) return minVal;
    if (value > maxVal) return maxVal;
    return value;
}

float scaleTemperature(float temp, int mode) {
    switch(mode) {
		case 1: return (temp + 25.0f) / 15.0f;
		default: return (temp + 15.0f) / 5.0f;
	}
}

float calculateCorrection(float temp, float rh, const String& model) {
  	float rh1 = limit(rh, 33, 85);
  	float rh2 = limit(rh, 30, 85);
  	float temp1 = limit(temp, -10, 50);
  	
    float t1 = scaleTemperature(temp1, 1);
  	float t2 = scaleTemperature(temp1, 2);
  	float t3 = scaleTemperature(temp1, 3);

    if (model == "MQ2" || model == "MQ135" || model == "MQ138" || model == "MQ214") {		
        float a = fmap(rh1, 33, 85, 1.6867, 1.5291);
        float b = fmap(rh1, 33, 85, -0.4263, -0.422);
        return a * pow(t1, b);
    }
    if (model == "MQ4") {
        float a = fmap(rh1, 33, 85, 1.2767, 1.1013);
        float b = fmap(rh1, 33, 85, -0.2204, -0.2482);
        return a * pow(t1, b);
    }
    if (model == "MQ5") {
        float a = fmap(rh1, 33, 85, 1.3645, 1.1315);
        float b = fmap(rh1, 33, 85, -0.2977, -0.2874);
        return a * pow(t1, b);
    }
    if (model == "MQ6") {
        float a = fmap(rh1, 33, 85, 1.3128, 1.1252);
        float b = fmap(rh1, 33, 85, -0.2428, -0.2496);
        return a * pow(t1, b);
    }
    if (model == "MQ7") {
        float a = fmap(rh1, 33, 85, 1.4296, 1.1733);
        float b = fmap(rh1, 33, 85, -0.3238, -0.2842);
        return a * pow(t1, b);
    }
    if (model == "MQ8") {
        float a = fmap(rh1, 33, 85, 1.1474, 1.0783);
        float b = fmap(rh1, 33, 85, -0.1958, -0.1824);
        return a * pow(t1, b);
    }
    if (model == "MQ9") {
        float a = fmap(rh1, 33, 85, 1.4292, 1.1735);
        float b = fmap(rh1, 33, 85, -0.3206, -0.2801);
        return a * pow(t1, b);
    }
    if (model == "MQ136" || model == "MQ137") {
        float a = fmap(rh1, 33, 85, 1.6867, 1.5291);
        float b = fmap(rh1, 33, 85, -0.4263, -0.422);
        return a * pow(t1, b);
    }
  	if (model == "MQ3") {
  		float a = fmap(rh1, 33, 85, 1.6671, 1.4112);
  		float b = fmap(rh1, 33, 85, -0.2467, -0.2257);
  		return a * pow(t2, b);
  	}
  	if (model == "MQ131") {
  		if (rh2 <= 60) {
  			float a = fmap(rh2, 30, 60, 1.876, 1.5885);
  			float b = fmap(rh2, 30, 60, -0.2284, -0.2271);
        return a * pow(t3, b);
  		} else {
  			float a = fmap(rh2, 60, 85, 1.5885, 1.3842);
  			float b = fmap(rh2, 60, 85, -0.2271, -0.2282);
        return a * pow(t3, b);
  		}
  	}
    return 1.0;
}

float unsupported_calculateCorrection1(float temp, float rh, float a_RH33, float b_RH33, float a_RH85, float b_RH85, int scale_mode) {
    float rh1 = limit(rh, 33, 85);
    float temp1 = limit(temp, -10, 50);
    
    float t1 = scaleTemperature(temp1, 1);
    float t2 = scaleTemperature(temp1, 2);

    float a = fmap(rh1, 33, 85, a_RH33, a_RH85);
    float b = fmap(rh1, 33, 85, b_RH33, b_RH85);

    if (scale_mode == 1) return a * pow(t1, b);
    if (scale_mode == 2) return a * pow(t2, b);
    
    return 1.0;
}

float unsupported_calculateCorrection2(float temp, float rh, float a_RH30, float b_RH30, float a_RH60, float b_RH60, float a_RH85, float b_RH85) {
    float rh2 = limit(rh, 30, 85);
    float temp1 = limit(temp, -10, 50);
    
    float t3 = scaleTemperature(temp1, 3);

    if (rh2 <= 60) {
      float a = fmap(rh2, 30, 60, a_RH30, a_RH60);
      float b = fmap(rh2, 30, 60, b_RH30, b_RH60);
      return a * pow(t3, b);
    } else {
      float a = fmap(rh2, 60, 85, a_RH60, a_RH85);
      float b = fmap(rh2, 60, 85, b_RH60, b_RH85);
      return a * pow(t3, b);
    }
    return 1.0;
}
