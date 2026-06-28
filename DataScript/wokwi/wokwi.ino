// Air Analyser Example Sensor Simulation: https://wokwi.com/projects/427335044024480769

#include <WiFi.h>
#include <DHT.h>
#include <TinyGPS++.h>
#include <HTTPClient.h>
#include <NetworkClientSecure.h>
#include <TM1637.h>

#define ADC_BIT_RESU (12)
#define analogPin    (35)
#define gasPin       (34)
#define dhtPin       (33)
#define potPin       (32)
#define CLK          (18)
#define DIO          (5)

TM1637 tm(CLK,DIO);
HardwareSerial neogps(2); 
TinyGPSPlus gps;
DHT dht(dhtPin, DHT22);

int sec;
String latitude, longitude;

const char* ssid = "Wokwi-GUEST";  
const char* password = ""; 
const char* serverName = "https://example.com/datareceiver.php";

static const char * myWriteAPIKey1 = "REPLACE_WITH YOUR_API_KEY";

unsigned long int lastTime1 = 0;
unsigned long int timerDelay1 = 15000;

void setup() {
  Serial.begin(115200);
  tm.init();
  tm.set(BRIGHT_TYPICAL);
  tm.display(0, 1);
  tm.display(1, 2);
  tm.display(2, 3);
  tm.display(3, 4);
  dht.begin();
  pinMode(potPin, INPUT);
  pinMode(gasPin, INPUT);
  pinMode(analogPin, INPUT);
  WiFi.mode(WIFI_STA);
  Serial.println("Connecting to WiFi ");
  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
  
  neogps.begin(9600, SERIAL_8N1, RX2, TX2);
}

void loop() {
  sec = map(analogRead(potPin), 0, (1 << ADC_BIT_RESU) - 1, 1, 21);
  switch(sec){
  case (1):
  {
  tm.display(3,5);
  tm.display(2,3);
  tm.display(1,1);
  tm.display(0,0);
  }
  break;
  case 2: case 3: case 4: case 5: case 6: case 7: case 8: case 9: normal(); break;
  case (10):
  {
  tm.display(3,1);
  tm.display(2,3);
  tm.display(1,1);
  tm.display(0,1);
  }
  break;
  case (11):
  {
  tm.display(3,1);
  tm.display(2,3);
  tm.display(1,1);
  tm.display(0,0);
  }
  break;
  case (12):
  {
  tm.display(3,6);
  tm.display(2,3);
  tm.display(1,1);
  tm.display(0,0);
  }
  break;
  case (13):
  {
  tm.display(3,7);
  tm.display(2,3);
  tm.display(1,1);
  tm.display(0,0);
  }
  break;
  case (14):
  {
  tm.display(3,8);
  tm.display(2,3);
  tm.display(1,1);
  tm.display(0,0);
  }
  break;
  case (15):
  {
  tm.display(3,4);
  tm.display(2,1);
  tm.display(1,2);
  tm.display(0,0);
  }
  break;
  case (16):
  {
  tm.display(3,6);
  tm.display(2,1);
  tm.display(1,2);
  tm.display(0,0);
  }
  break;
  case (17):
  {
  tm.display(3,10);
  tm.display(2,3);
  tm.display(1,0);
  tm.display(0,3);
  }
  break;
  case (18):
  {
  tm.display(3,11);
  tm.display(2,3);
  tm.display(1,0);
  tm.display(0,3);
  }
  break;
  case (19):
  {
  tm.display(3,10);
  tm.display(2,6);
  tm.display(1,0);
  tm.display(0,3);
  }
  case (20):
  {
  tm.display(3,10);
  tm.display(2,7);
  tm.display(1,0);
  tm.display(0,3);
  }
  case (21):
  {
  tm.display(3,10);
  tm.display(2,9);
  tm.display(1,0);
  tm.display(0,3);
  }
  break;
  }

  if ((millis() - lastTime1) > timerDelay1) {
    latitude  = String((random(-90, 90) + (random(0, pow(10, 6) + 1) / pow(10, 7)) + 90) * pow(10,6));
    longitude = String((random(-180, 180) + (random(0, pow(10, 6) + 1) / pow(10, 7)) + 180) * pow(10,6));
    if (neogps.available()) {
      char c = neogps.read();
      if (gps.encode(c)) {
        if (gps.location.isValid()) {
         latitude  = String((gps.location.lat() + 90) * pow(10, 7));
         longitude = String((gps.location.lng() + 180) * pow(10, 7)); 
        }
      }
    }

    String httpRequestData = "api_key=" + String(myWriteAPIKey1) + 
                             "&field1=" + String(sec) + 
                             "&field2=" + String(analogRead(analogPin)) + 
                             "&field3=" + String((dht.readTemperature() + 140) * 10) + 
                             "&field4=" + String((dht.readHumidity() + 100) * 10) + 
                             "&field5=" + String(analogRead(gasPin)) + 
                             "&field6=" + latitude + 
                             "&field7=" + longitude;

    NetworkClientSecure *client = new NetworkClientSecure;
    if(client) {
        client->setInsecure();
        HTTPClient http;
        if (http.begin(*client, serverName)) {
            http.addHeader("Content-Type", "application/x-www-form-urlencoded");
            int httpResponseCode = http.POST(httpRequestData);
            http.end();
        }
        delete client;
    }

    lastTime1 = millis();
  }
}

void normal(){
tm.display(3,sec);
tm.display(2,sec);
tm.display(1,sec);
tm.display(0,sec);
}

// DHT22 : [GND --> GND] [PIN --> D33] [VCC --> 5V]
// GPS : [GND --> GND] [TX --> D3] [RX --> D1] [VCC --> 5V]
// MQ-X: [PIN --> D35] [GND --> GND] [VCC --> 3.3V]
// Other Sensor: [PIN --> D34] [GND --> GND] [VCC --> 3.3V]
// Potentiometer: [PIN --> D32] [GND --> GND] [VCC --> 3.3V]
// TM1637: [CLK --> D18] [DIO --> D5] [VCC --> 5V] [GND --> GND]