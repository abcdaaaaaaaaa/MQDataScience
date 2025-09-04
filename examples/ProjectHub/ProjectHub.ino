// (1) The library also supports data science applications such as gradient 4D Slope Estimation from Python!:
// (1) https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/4D_Slope
// (2) If you are using this library for IOT Alternatively, you can also perform ppm calculations in javascript with this library!
// (2) https://github.com/abcdaaaaaaaaa/MQDataScience/tree/main/DataScript

// You can access the wokwi simulation of the project here:
// https://wokwi.com/projects/436822004887407617
   
#include <AirQuality.h>
#include <Correction.h>
#include <GasSensor.h>
#include <SensorDefinitions.h>

#include <LiquidCrystal_I2C.h>

#define ADC_BIT_RESU (12) // for ESP32
#define pin          (35) // D35 (ADC1)
#define pot          (34) // D35 (ADC1)

int Air, ppm;
float sensorVal, temp, rh, correction;
String selectedModel, mode;

GasSensor sensor(ADC_BIT_RESU, pin);
SensorModel* sensorModel = nullptr;

String mqList1[] = { "MQ135", "MQ2", "MQ3", "MQ4", "MQ5", "MQ6", "MQ7", "MQ8", "MQ9", "MQ136", "MQ137", "MQ138", "MQ214", "MQ216" };
String mqList2[] = { "MQ303A", "MQ303B", "MQ306A", "MQ307A", "MQ309A" };
String mqList3[] = { "MQ131", "MQ131_LOW" };

int lcdColumns = 16;
int lcdRows = 2;

LiquidCrystal_I2C lcd(0x27, lcdColumns, lcdRows); 

void setup() {
    Serial.begin(115200); // for ESP32
    sensor.begin();
    lcd.init();
    lcd.backlight();
    // WARNING: Please run the code after connecting the appropriate resistance specified 
    // in the Required_MQ_LoadResistor.ino file to the sensor mode you selected, 
    // otherwise the results will not reflect the reality.
}

void loop() {
    int val = map(analogRead(pot), 0, (1 << ADC_BIT_RESU) - 1, 1, 19);

    if (val >= 1 && val <= 13) selectedModel = mqList1[val - 1];
    else if (val >= 14 && val <= 17) selectedModel = mqList2[val - 14];
    else if (val >= 18 && val <= 19) selectedModel = mqList3[val - 18];

    sensorModel = getSensorModel(selectedModel);
    if (!sensorModel) {
        Serial.println("Sensor model not found.");
        while (true);
    }
    Serial.print("Selected sensor: ");
    Serial.println(sensorModel->model);
    mode = sensorModel->model;
   
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
    correction = sensorModel->useCorrection ? calculateCorrection(temp, rh, selectedModel) : 1.0;

    Air = sensorVal > 0 && mode != "MQ307A" ? airConcentration(mode, sensorVal) * correction : 0;
   
    if (mode == "MQ3") Air *= 50.0; // mg/L --> ppm
    if (mode == "MQ131_LOW") Air *= 0.02; // ppb --> ppm
   
    lcd.setCursor(0, 0);
    lcd.print("Air: " + String(Air));

    lcd.setCursor(16 - mode.length(), 0);
    lcd.print(mode);

    lcd.setCursor(0, 1); // Correction --> CR
    lcd.print("CR: x" + String(correction, 4));

    lcd.setCursor(13, 1);
    lcd.print("ppm");

    delay(3000);
    lcd.clear();

    for (byte i = 0; i < sensorModel->gasCount; i++) {
        const GasModel& gasType = sensorModel->gasList[i];

        if (isMQSensor(mode, mqList1, sizeof(mqList1) / sizeof(mqList1[0]))) {
          float RsRocalValue = sensor.calculateCalValue1(gasType.a, gasType.b, sensorModel->calibrateAir, gasType.minPpm, gasType.maxPpm);
          ppm = sensor.calculateRsRoPPM(sensorVal, correction, gasType.a, gasType.b, RsRocalValue, sensorModel->air, sensorModel->rlcal, gasType.maxPpm);
          if (mode == "MQ3") ppm *= 50.0;
        } 

        else if (isMQSensor(mode, mqList2, sizeof(mqList2) / sizeof(mqList2[0]))) {
          float RsRscalValue = sensor.calculateCalValue2(gasType.a, gasType.b, sensorModel->calibrateAir, gasType.minPpm, gasType.maxPpm);
          if (mode == "MQ306A" && i == 0) RsRscalValue = 0.873876;
          if (mode == "MQ307A" && i == 1) RsRscalValue = 0.999619;
          if (mode == "MQ309A" && i >= 2) RsRscalValue = 0.83393;
          ppm = sensor.calculateRsRsPPM(sensorVal, gasType.a, gasType.b, RsRscalValue, sensorModel->rlcal, gasType.maxPpm);
        }

        else if (isMQSensor(mode, mqList3, sizeof(mqList3) / sizeof(mqList3[0]))) {
          float RoRscalValue = sensor.calculateCalValue1(gasType.a, gasType.b, sensorModel->calibrateAir, gasType.minPpm, gasType.maxPpm);
          ppm = sensor.calculateRoRsPPM(sensorVal, correction, gasType.a, gasType.b, RoRscalValue, sensorModel->air, sensorModel->rlcal, gasType.maxPpm);
          if (mode == "MQ131_LOW") ppm *= 0.02;
        }

        lcd.setCursor(0, 0);
        lcd.print("Air: " + String(Air));
	
        lcd.setCursor(16 - mode.length(), 0);
        lcd.print(mode);

        lcd.setCursor(0, 1);
        lcd.print(String(gasType.gasName) + ": " + String(ppm));

        lcd.setCursor(13, 1);
        lcd.print("ppm");

        delay(1500);
        lcd.clear();
    }

    Serial.println("----------");
    delay(5000); // You can customize the waiting time according to the sensor you use.
}
