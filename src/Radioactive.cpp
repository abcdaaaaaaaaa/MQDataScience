#include "Radioactive.h"

GeigerCounter::GeigerCounter(bool uSvhr, bool Avg1, bool CPM_Count, bool sdCPMbool, int LOG_PERIOD1, byte pin2)
{
  _pin2 = pin2;
  _usvhrbool = uSvhr;
  _Avgbool = Avg1;
  _cpmcountbool = CPM_Count;
  _sdCPMbool = sdCPMbool;
  _LOG_PERIOD = LOG_PERIOD1;
  _counts = 0;
  _currentCPM = 0;
  previousMillis = 0;
}

float GeigerCounter::outputSieverts(float x) {
  return x * 0.0057;
}

volatile unsigned long interruptCounts = 0;

void impulseISR() {
  interruptCounts++;
}

void GeigerCounter::begin()
{
  _counts = 0;
  pinMode(_pin2, INPUT);
  attachInterrupt(digitalPinToInterrupt(_pin2), impulseISR, FALLING);
}

void GeigerCounter::radioactive() {
  _counts = interruptCounts;
  count = _cpmcountbool ? _counts : 0;

  unsigned long currentMillis = millis();
  if (currentMillis - previousMillis > _LOG_PERIOD) {
    previousMillis = currentMillis;
    _CPMArray[_currentCPM] = _counts * 2;
    usvhr = _usvhrbool ? outputSieverts(_CPMArray[_currentCPM]) : 0;

    interruptCounts = 0;
    _averageCPM = 0; _sdCPM = 0;

    for (int i = 0; i <= _currentCPM; i++) _averageCPM += _CPMArray[i];
    _averageCPM /= (_currentCPM + 1);

    for (int i = 0; i <= _currentCPM; i++) _sdCPM += sq(_CPMArray[i] - _averageCPM);
    _sdCPM = sqrt(_sdCPM / _currentCPM) / sqrt(_currentCPM + 1);

    Avg = _Avgbool ? outputSieverts(_averageCPM) : 0;
    sdCPM = _sdCPMbool ? outputSieverts(_sdCPM) : 0;
    _currentCPM++;
  }
}
