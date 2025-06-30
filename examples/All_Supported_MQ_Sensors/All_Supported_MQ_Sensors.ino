// The library also supports data science applications such as gradient 4D Slope Estimation from Python!
// If you are using this library for IOT Alternatively, you can also perform ppm calculations in javascript with this library!
   
#include <AirQuality.h>
#include <Correction.h>
#include <GasSensor.h>
#include <SensorDefinitions.h>

#define ADC_BIT_RESU (12) // for ESP32
#define pin          (35) // D35 (ADC1)

String selectedModel = "MQ135"; // You can change it with the model you use!
GasSensor sensor(ADC_BIT_RESU, pin);
const SensorModel* sensorModel = nullptr;

void setup() {
    Serial.begin(9600);
    sensor.begin();
    sensorModel = getSensorModel(selectedModel);
    if (!sensorModel) {
        Serial.println("Sensor model not found.");
        while (true);
    }
    Serial.print("Selected sensor: ");
    Serial.println(sensorModel->model);
}

void loop() {
    float temp = 20.0; // DHT22 is recommended °C (Celsius)
    float rh = 33.0;   // DHT22 is recommended %  (Relative Humidity)
    
    /* NOTE: The temperature and humidity of the environment do not have a direct effect on the ppm value of the environment.
    On the other hand, the temperature and humidity of the environment will cause the sensor to detect ppm more or less than normal. 
    The amount of deviation of the erroneous measurement caused by environmental conditions is modeled by the data graphs of each sensor.
    In this case, this error margin calculated with the Correction Coefficient, known as Correction.h, is necessary to correct the incorrect ppm value.
    
    At 20°C, 33% RH, correction = 1.0 is the environmental condition where the sensor accuracy rate is highest.
    If the correction coefficient is greater than 1.0, the sensor will measure values ​​lower​​ than the true value, and if it is less than 1.0, 
    it will measure values higher than the true value. Temperature and humidity are inversely proportional to the correction coefficient. */

    // Correction Coefficient Necessary for all Rs/Ro sensors and MQ131.
    // Correction Coefficient Unnecessary for all Rs/Rs sensors and MQ131_LOW.
     
    float sensorVal = sensor.read();
    float correction = sensorModel->useCorrection ? calculateCorrection(temp, rh, selectedModel) : 1.0;

    // NOTE: MQ307A has no 'Air' value. If using MQ307A, delete this command. Required for all other sensors.
    float Air = sensorVal > 0 ? airConcentration(sensorModel->model, sensorVal) * correction : 0;
    
    // Air gives the overall concentration of the sensor.
    // The ppm air value of gases measured at different sensitivities contains important information about Air Quality.

    /* if you use MQ3 use this code: Air *= 50.0; // Necessary use for MQ3.
     * if you use MQ131_LOW use this code: Air *= 0.02; // Necessary use for MQ131_LOW. */

    Serial.print("Air: ");
    Serial.print(Air);
    Serial.print(" ppm");
    Serial.println();
    Serial.print("Correction Coefficient: "); // This value indicates the accuracy of the sensor due to environmental conditions.
    Serial.print(correction, 4); // writes decimal part and the first four digits of the decimal part
    Serial.println();

    for (byte i = 0; i < sensorModel->gasCount; i++) {
        const GasModel& gasType = sensorModel->gasList[i];

        // for Rs/Ro: MQ135, MQ2, MQ3, MQ4, MQ5, MQ6, MQ7, MQ8, MQ9, MQ136, MQ137, MQ138, MQ214
        float RsRocalValue = sensor.calculateCalValue1(gasType.a, gasType.b, sensorModel->calibrateAir, gasType.minPpm, gasType.maxPpm);
        float ppm = sensor.calculateRsRoPPM(sensorVal, correction, gasType.a, gasType.b, RsRocalValue, sensorModel->air, sensorModel->rlcal, gasType.maxPpm);

        // for Rs/Rs: MQ303A, MQ303B, MQ307A, MQ309A
        // float RsRscalValue = sensor.calculateCalValue2(gasType.a, gasType.b, sensorModel->calibrateAir, gasType.minPpm, gasType.maxPpm);

        /* if you use MQ307A use this code: if (i == 1) float RsRscalValue = 0.999619;
         * if you use MQ309A use this code: if (i >= 2) float RsRscalValue = 0.83393; */

         /* There are exceptions to calibration for some gases of MQ307A and MQ309A. 
          * Using this code you can return the correct value in case of calibration exceptions. */
        
        // float ppm = sensor.calculateRsRsPPM(sensorVal, gasType.a, gasType.b, RsRscalValue, sensorModel->rlcal, gasType.maxPpm);
        
        // for Ro/Rs: MQ131, MQ131_LOW
        // float RoRscalValue = sensor.calculateCalValue1(gasType.a, gasType.b, sensorModel->calibrateAir, gasType.minPpm, gasType.maxPpm);
        // float ppm = sensor.calculateRoRsPPM(sensorVal, correction, gasType.a, gasType.b, RoRscalValue, sensorModel->air, sensorModel->rlcal, gasType.maxPpm);

        /* if you use MQ3 use this code: ppm *= 50.0;
         * if you use MQ131_LOW use this code: ppm *= 0.02; */

        /* The MQ3's data graph does not measure values ​​in ppm, but instead in mg/L.
         * Therefore, after the final value is found, the result must be multiplied by ×50 to convert the value to ppm. */

        /* The MQ131_LOW's (MQ131 Low Sensitivity) data graph does not measure values ​​in ppm, but instead in ppb.
         * Therefore, after the final value is found, the result must be multiplied by ×0.02 to convert the value to ppm. */

        Serial.print(gasType.gasName);
        Serial.print(": ");
        Serial.print(ppm);
        Serial.println(" ppm");
    }

    Serial.println("----------");
    delay(5000);
}

  // WARNING: Necessary for all users, Here are all the resistance values ​​you need to apply for supported sensors:
 /* MQ135:     20  kΩ
  * MQ2:       5   kΩ
  * MQ3:       200 kΩ
  * MQ4:       20  kΩ
  * MQ5:       20  kΩ
  * MQ6:       20  kΩ
  * MQ7:       10  kΩ
  * MQ8:       10  kΩ
  * MQ9:       10  kΩ
  * MQ131_LOW: 20  kΩ
  * MQ131:     20  kΩ
  * MQ136:     20  kΩ
  * MQ137:     47  kΩ
  * MQ138:     20  kΩ
  * MQ214:     50  kΩ
  * MQ303A:    47  kΩ
  * MQ303B:    10  kΩ
  * MQ307A:    1   kΩ
  * MQ309A:    10  kΩ
  */

  /* The graph shows the recommended resistance values specified in each sensor's datasheet as the most accurate operating points.
  *  Although the datasheets also indicate broader operational ranges beyond these ideal values,
  *  the library enforces the use of only the optimal ones to ensure consistent measurement accuracy. */
