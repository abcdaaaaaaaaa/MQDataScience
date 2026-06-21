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

float calculateCorrection(float temp, float rh, const String& model) {
    float temp1 = limit(temp, -10.0f, 50.0f);
    
    // Group 3: CRMode == 3 (MQ9, MQ131)
    if (model == "MQ131" || model == "MQ9") {
        float rh2 = limit(rh, 30.0f, 85.0f);
        float a, b, c;
        if (rh2 <= 60.0f) {
            a = fmap(rh2, 30.0f, 60.0f, -2.5404f, -1.6874f);
            b = fmap(rh2, 30.0f, 60.0f, -0.0037f, -0.0043f);
            c = fmap(rh2, 30.0f, 60.0f, 4.1019f, 3.0105f);
        } else {
            a = fmap(rh2, 60.0f, 85.0f, -1.6874f, -1.2399f);
            b = fmap(rh2, 60.0f, 85.0f, -0.0043f, -0.0047f);
            c = fmap(rh2, 60.0f, 85.0f, 3.0105f, 2.3914f);
        }
        return a + c * exp(b * temp1);
    }

    // Standard Group: 33 to 85 RH range
    float rh1 = limit(rh, 33.0f, 85.0f);
    float a, b, c;

    if (model == "MQ2" || model == "MQ135" || model == "MQ136" || model == "MQ137" || model == "MQ138" || model == "MQ214" || model == "MQ216") {
        a = fmap(rh1, 33.0f, 85.0f, 0.8579f, 0.7818f);
        b = fmap(rh1, 33.0f, 85.0f, -0.0543f, -0.0554f);
        c = fmap(rh1, 33.0f, 85.0f, 0.4912f, 0.4378f);
        return a + c * exp(b * temp1);
    } else if (model == "MQ3") {
        a = fmap(rh1, 33.0f, 85.0f, 0.7897f, 0.7319f);
        b = fmap(rh1, 33.0f, 85.0f, -0.0423f, -0.0446f);
        c = fmap(rh1, 33.0f, 85.0f, 0.5355f, 0.4069f);
        return a + c * exp(b * temp1);
    } else if (model == "MQ4") {
        a = fmap(rh1, 33.0f, 85.0f, 0.8597f, 0.5838f);
        b = fmap(rh1, 33.0f, 85.0f, -0.0381f, -0.0218f);
        c = fmap(rh1, 33.0f, 85.0f, 0.2861f, 0.4064f);
        return a + c * exp(b * temp1);
    } else if (model == "MQ5") {
        a = fmap(rh1, 33.0f, 85.0f, 0.8098f, 0.6066f);
        b = fmap(rh1, 33.0f, 85.0f, -0.0413f, -0.0283f);
        c = fmap(rh1, 33.0f, 85.0f, 0.3686f, 0.3891f);
        return a + c * exp(b * temp1);
    } else if (model == "MQ6") {
        a = fmap(rh1, 33.0f, 85.0f, 0.8714f, 0.7287f);
        b = fmap(rh1, 33.0f, 85.0f, -0.044f, -0.0412f);
        c = fmap(rh1, 33.0f, 85.0f, 0.2883f, 0.2648f);
        return a + c * exp(b * temp1);
    } else if (model == "MQ7") {
        a = fmap(rh1, 33.0f, 85.0f, 0.8315f, 0.6708f);
        b = fmap(rh1, 33.0f, 85.0f, -0.0462f, -0.033f);
        c = fmap(rh1, 33.0f, 85.0f, 0.3813f, 0.358f);
        return a + c * exp(b * temp1);
    } else if (model == "MQ8") {
        a = fmap(rh1, 33.0f, 85.0f, 0.8559f, 0.8201f);
        b = fmap(rh1, 33.0f, 85.0f, -0.0611f, -0.0606f);
        c = fmap(rh1, 33.0f, 85.0f, 0.1673f, 0.1492f);
        return a + c * exp(b * temp1);
    } /* else if (model == "MQ9") {
        a = fmap(rh1, 33.0f, 85.0f, 0.839f, 0.6884f);
        b = fmap(rh1, 33.0f, 85.0f, -0.0469f, -0.0349f);
        c = fmap(rh1, 33.0f, 85.0f, 0.3742f, 0.3403f);
        return a + c * exp(b * temp1);
    } */

    return 1.0f;
}

float unsupported_calculateCorrection1(float temp, float rh, float a_RH33, float b_RH33, float c_RH33, float a_RH85, float b_RH85, float c_RH85) {
    float rh1 = limit(rh, 33.0f, 85.0f);
    float temp1 = limit(temp, -10.0f, 50.0f);
    
    float a = fmap(rh1, 33.0f, 85.0f, a_RH33, a_RH85);
    float b = fmap(rh1, 33.0f, 85.0f, b_RH33, b_RH85);
    float c = fmap(rh1, 33.0f, 85.0f, c_RH33, c_RH85);

    return a + c * exp(b * temp1);
}

float unsupported_calculateCorrection2(float temp, float rh, float a_RH30, float b_RH30, float c_RH30, float a_RH60, float b_RH60, float c_RH60, float a_RH85, float b_RH85, float c_RH85) {
    float rh2 = limit(rh, 30.0f, 85.0f);
    float temp1 = limit(temp, -10.0f, 50.0f);
    
    float a, b, c;

    if (rh2 <= 60.0f) {
        a = fmap(rh2, 30.0f, 60.0f, a_RH30, a_RH60);
        b = fmap(rh2, 30.0f, 60.0f, b_RH30, b_RH60);
        c = fmap(rh2, 30.0f, 60.0f, c_RH30, c_RH60);
    } else {
        a = fmap(rh2, 60.0f, 85.0f, a_RH60, a_RH85);
        b = fmap(rh2, 60.0f, 85.0f, b_RH60, b_RH85);
        c = fmap(rh2, 60.0f, 85.0f, c_RH60, c_RH85);
    }
    return a + c * exp(b * temp1);
}
