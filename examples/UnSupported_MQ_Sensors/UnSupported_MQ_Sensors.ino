#include <AirQuality.h>
#include <Correction.h>
#include <GasSensor.h>

#define ADC_BIT_RESU (12) // for ESP32
#define pin          (35) // D35 (ADC1)

float sensorVal, Air, ppm, temp, rh, correction;

GasSensor sensor(ADC_BIT_RESU, pin);

/* Fill these sections according to your sensor:
float MySensorModel =

// When you see a sentence like this in the datasheet:
// 1) is shows the typical sensitivity characters of the MQ-X for several gases. RL=akΩ
// 2) we recommended that you calibrate detector for ... ppm or ... ppm concentration and use value of Load Resistance RL about bkΩ(ckΩ to dkΩ)

calibrateAir --> [you calibrate detector for ... ppm or ... ppm] (...)ppm 1* Look typical sensitivity characters of the MQ-X for several gases.
calibrateAir --> [X: (...)ppm, Y: (Rs/Ro or Ro/Rs or Rs/Rs)ratio] which ratio? 2* Then see ratio value from recommended ppm value.

float calibrateAir =

SensorRL --> This is the sensor resistance that is desired when taking readings after calibrating the sensor. [MQ-X for several gases. RL=akΩ] --> akΩ
CalRL --> This is the desired sensor resistance when calibrating the sensor. [RL about bkΩ(ckΩ to dkΩ)] --> bkΩ
rlcal --> SensorRLCalRL: This value is the ratio of SensorRL to CalRL. float rlcal = (SensorRL / CalRL) --> akΩ / bkΩ
NOTE: Most of the time this ratio is 1 since the same resistance is desired in both conditions. (often: rlcal = 1.0)

WARNING: The SensorRL value indicates that you need to connect a resistance of aKΩ value to get correct results when operating your sensor.

float rlcal =

// Define the ppm range of your sensor data graph (typical sensitivity characters of the MQ-X for several gases) for "Air" (gas ratio independent).
float min_air_ppm =
float max_air_ppm =

// Note: min_gas_ppm, max_gas_ppm: Define the ppm range of your sensor data graph (typical sensitivity characters of the MQ-X for several gases) for gas
// WARNING: The ppm range of air and the ppm range of gases can sometimes be different, please make sure you define it correctly.

// Define the air value (ratio) of your sensor data graph (typical sensitivity characters of the MQ-X for several gases) for "Air" (gas ratio independent).
float air =

// https://github.com/abcdaaaaaaaaa/MQDataScience/tree/main/DataScience/Regression/CorrectionCoefficient
// Run the codes in the link according to your sensor's correction coefficient calculation mode.
float a_RH30 =
float b_RH30 =
float a_RH33 =
float b_RH33 =
float a_RH85 =
float b_RH85 =
int scale_mode = 1; // (mode1)

 * To understand what you will define, just click on the link and run the code, the code will tell you in detail what you need to transfer:
 https://github.com/abcdaaaaaaaaa/MQDataScience/tree/main/DataScience/Regression/CorrectionCoefficient 
 * mode1: In the graph, the temperature is between -10°C and 50°C and the defined points are defined at 15°C intervals. 
 * Relative Humidity is defined in two different curves as 33% and 85%. (like MQ2)
 * mode2: In the graph, the temperature is between -10°C and 50°C and the defined points are defined at 5°C intervals.
 * Relative Humidity is defined in two different curves as 33% and 85%. (like MQ3)
 * mode3: In the graph, the temperature is between -10°C and 50°C and the defined points are defined at 5°C intervals.
 * Relative Humidity is defined in three different curves as 30%, %60 and 85%. (like MQ131) */

/* If you have difficulty defining it, we have defined it for MQ-2 as an example:
 * String MySensorModel = "MQ2";
 * SensorRL --> 5kΩ
 * CalRL --> 20kΩ
 * float rlcal = 0.25;
 * calibrateAir: 1000ppm LPG --> 0.78 ratio
 * float calibrateAir = 0.78;
 * float air = 9.8;
 * int scale_mode = 1;
 * float a_RH33 = 1.6867; // It is not directly included in the datasheet but was calculated from mode1.py.
 * float b_RH33 = -0.4263; // It is not directly included in the datasheet but was calculated from mode1.py.
 * float a_RH85 = 1.5291; // It is not directly included in the datasheet but was calculated from mode1.py.
 * float b_RH85 = -0.422; // It is not directly included in the datasheet but was calculated from mode1.py.
 * float min_air_ppm = 200;
 * float max_air_ppm = 10000;
 */
 
String MySensorModel = "MQ2";
float calibrateAir = 0.78;
float rlcal = 0.25;
float air = 9.8;
int scale_mode = 1;

float a_RH33 = 1.6867;
float b_RH33 = -0.4263;
float a_RH85 = 1.5291;
float b_RH85 = -0.422;

float min_air_ppm = 200;
float max_air_ppm = 10000;

void setup() {
    Serial.begin(9600);
    sensor.begin();
    Serial.print("Selected sensor: ");
    Serial.println(MySensorModel);
}

void loop() {
    temp = 20.0; // DHT22 is recommended °C (Celsius)
    rh = 33.0;   // DHT22 is recommended %  (Relative Humidity)
    
    /* NOTE: The temperature and humidity of the environment do not have a direct effect on the ppm value of the environment.
    On the other hand, the temperature and humidity of the environment will cause the sensor to detect ppm more or less than normal. 
    The amount of deviation of the erroneous measurement caused by environmental conditions is modeled by the data graphs of each sensor.
    In this case, this error margin calculated with the Correction Coefficient, known as Correction.h, is necessary to correct the incorrect ppm value.
    
    At 20°C, 33% RH, correction = 1.0 is the environmental condition where the sensor accuracy rate is highest.
    If the correction coefficient is greater than 1.0, the sensor will measure values ​​lower​​ than the true value, and if it is less than 1.0, 
    it will measure values higher than the true value. Temperature and humidity are inversely proportional to the correction coefficient. */
     
    sensorVal = sensor.read();
    correction = unsupported_calculateCorrection1(temp, rh, a_RH33, b_RH33, a_RH85, b_RH85, scale_mode); // for mode1 and mode2
    // correction = unsupported_calculateCorrection2(temp, rh, a_RH30, b_RH30, a_RH60, b_RH60, a_RH85, b_RH85); // for mode3

    Air = sensorVal > 0 ? unsupported_airConcentration(min_air_ppm, max_air_ppm, sensorVal) * correction : 0;
    // Air gives the overall concentration of the sensor.
    // The ppm air value of gases measured at different sensitivities contains important information about Air Quality.

    Serial.print("Air: ");
    Serial.print(Air);
    Serial.print(" ppm");
    Serial.println();
    Serial.print("Correction Coefficient: "); // This value indicates the accuracy of the sensor due to environmental conditions.
    Serial.print(correction, 4); // writes decimal part and the first four digits of the decimal part
    Serial.println();

    // --------GAS-1-------- Please fill in these sections according to your sensor.
    // sensor_gases(gasname, valuea, valueb, min_gas_ppm, max_gas_ppm, calibrateAir, rlcal, correction, sensorVal);
    // --------GAS-2-------- Please fill in these sections according to your sensor.
    // sensor_gases(gasname, valuea, valueb, min_gas_ppm, max_gas_ppm);

    sensor_gases("LPG", 17.6135, -0.4539, 200, 10000); // Example for MQ-2
    sensor_gases("Propane", 19.5575, -0.461, 200, 10000); // Example for MQ-2

    Serial.println("----------");
    delay(5000);
}

void sensor_gases(String gasname, float valuea, float valueb, float minPpm, float maxPpm) {
    // for Rs/Ro:
    float RsRocalValue = sensor.calculateCalValue1(valuea, valueb, calibrateAir, minPpm, maxPpm);
    float ppm = sensor.calculateRsRoPPM(sensorVal, correction, valuea, valueb, RsRocalValue, air, rlcal, maxPpm);

    // for Rs/Rs:
    // float RsRscalValue = sensor.calculateCalValue2(valuea, valueb, calibrateAir, minPpm, maxPpm);
    // float ppm = sensor.calculateRsRsPPM(sensorVal, valuea, valueb, RsRscalValue, rlcal, maxPpm);
    
    // for Ro/Rs:
    // float RoRscalValue = sensor.calculateCalValue1(valuea, valueb, calibrateAir, minPpm, maxPpm);
    // float ppm = sensor.calculateRoRsPPM(sensorVal, correction, valuea, valueb, RoRscalValue, air, rlcal, maxPpm);

    Serial.print(gasname);
    Serial.print(": ");
    Serial.print(ppm);
    Serial.println(" ppm");
}


