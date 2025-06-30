#ifndef RADIOACTIVE_H
#define RADIOACTIVE_H

#include <Arduino.h>

class GeigerCounter
{
private:
  byte _pin2;
  bool _Avgbool, _usvhrbool, _cpmcountbool, _sdCPMbool;
  int _LOG_PERIOD;
  float _averageCPM, _sdCPM;
  float _CPMArray[100];
  int _currentCPM;
  unsigned long previousMillis;
  unsigned long _counts;

  float outputSieverts(float x);

public:
  GeigerCounter(bool uSvhr, bool Avg1, bool CPM_Count, bool sdCPMbool, int LOG_PERIOD1, byte pin2);
  void begin();
  void radioactive();

  float usvhr;
  float count;
  float Avg;
  float sdCPM;
};

#endif
