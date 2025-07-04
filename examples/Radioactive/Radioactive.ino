// The library also supports data science (RadioactiveScience folder) applications such as gradient Multidimensional Radioactive Decay Estimation from Python!

#include <Radioactive.h>

// Define true to the values ​​you want to calculate as false you don't want.
// The values ​​you define as false will be 0 on the screen output.

#define uSvhr1      (true)
#define Avg1        (true)
#define CPM_Count1  (true)
#define sdCPM1      (true)
#define LOG_PERIOD1 (30000)
#define GeigerPin1  (35) // for ESP32 D35 (ADC1)

GeigerCounter Radioactive(uSvhr1, Avg1, CPM_Count1, sdCPM1, LOG_PERIOD1, GeigerPin1);

void setup() {
    Serial.begin(115200); // for ESP32
    Radioactive.begin();
}

void loop() {
    Radioactive.radioactive();
    delay(LOG_PERIOD1);
  
    Serial.print("Usv/hr: ");
    Serial.println(Radioactive.usvhr);
  
    Serial.print("Avg: ");
    Serial.println(String(Radioactive.Avg) + "+/-" + String(Radioactive.sdCPM));
  
    Serial.print("CPM Count: ");
    Serial.println(Radioactive.count);
}
