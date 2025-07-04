---------------------------------------------------------------- For those who are curious! ----------------------------------------------------------------
How can I understand if the sensor is MQ131 or MQ131_LOW?
  1) Check the value ranges it measures, ppm or ppb? ppm --> MQ131, ppb --> MQ131_LOW
  2) Does it include a curve graph of the Correction Factor depending on temperature and humidity? yes --> MQ131, no--> MQ131_LOW
  3) Does it look like a square/rectangular kit? yes--> MQ131, no--> MQ131_LOW
  
Why does MQ131 have low sensitivity (MQ131_LOW) while MQ131 (MQ131) has high sensitivity?
  MQ131_LOW is sensitive to measure between 0.1-2 ppm (5-100 ppb),
  MQ131 is sensitive to measuring in the range of 5-100ppm.
  Therefore, MQ131 does not include MQ131_LOW. The two are complementary to each other.

If MQ series gas sensors can measure more than one gas, why are there so many types of MQ sensors on the project?
  Although MQ series gas sensors operate simultaneously like other multi-purpose sensors (e.g., DHT sensors), they provide output through a single analog line.
  Each type of gas affects this analog value differently due to varying sensitivities. 
  The concentration (ppm) of each gas is estimated from this single value using mathematical calculations.
  As a result, no MQ sensor has identical sensitivity profiles across different gases. 
  For example, the same amount of alcohol in the environment will yield significantly different responses from an MQ-3 and an MQ-135.
  Moreover, increasing only the alcohol level in the environment will also cause the reported ppm of other gases to rise in MQ sensor.
  In short, there are many MQ sensors on the market due to the limitations of each sensor’s specific sensitivity profile and gas selectivity.
