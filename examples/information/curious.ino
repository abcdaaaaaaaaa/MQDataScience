---------------------------------------------------------------- For those who are curious! ----------------------------------------------------------------
How can I understand if the sensor is MQ131 or MQ-131_LOW?
  1) Check the value ranges it measures, ppm or ppb? ppm --> MQ131, ppb --> MQ-131_LOW
  2) Does it include a curve graph of the Correction Factor depending on temperature and humidity? yes --> MQ131, no--> MQ-131_LOW
  3) Does it look like a square/rectangular kit? yes--> MQ131, no--> MQ131_LOW
  
Why does MQ131 have low sensitivity (MQ131_LOW) while MQ131 (MQ131) has high sensitivity?
  MQ131_LOW is sensitive to measure between 0.1-2 ppm (5-100 ppb),
  MQ131 is sensitive to measuring in the range of 5-100ppm.
  Therefore, MQ131 does not include MQ-131_LOW. The two are complementary to each other.

If MQ series gas sensors can measure more than one gas, why are there so many types of MQ sensors on the project?
  Although MQ series gas sensors operate simultaneously like other multi-purpose sensors (e.g., DHT sensors), they provide output through a single analog line.
  Each type of gas affects this analog value differently due to varying sensitivities. 
  The concentration (ppm) of each gas is estimated from this single value using mathematical calculations.
  As a result, no MQ sensor has identical sensitivity profiles across different gases. 
  For example, the same amount of alcohol in the environment will yield significantly different responses from an MQ-3 and an MQ-135.
  Moreover, increasing only the alcohol level in the environment will also cause the reported ppm of other gases to rise in MQ sensor.
  In short, there are many MQ sensors on the market due to the limitations of each sensor’s specific sensitivity profile and gas selectivity.

If all the sensors are MQ series and the general formula is ppm = a(ratio)ᵇ, why are the sensors approached in 3 different groups?
  Because when the effects of temperature and humidity are included in the datasheet of some sensors, the ratio is considered as Ro/Rs, but in some sensors, when the effects of temperature and humidity are not considered to be so significant, 
  it is considered as Rs/Rs. This results in two different approaches. However, the Sensitivity Characteristics graphs of MQ131 and MQ-131_LOW are in the form of Ro/Rs instead of Rs/Ro. 
  This requires a different approach to examine the third approach, which is Ro/Rs, in the Rs/Ro approach (even though the MQ-131_LOW does not include the effects of temperature and humidity, the ratio is not Rs/Rs). 
  Therefore, even if the main formulas are the same, the sensors are examined under 3 different main groups.

Why do we use the sensors after applying the preheating process?
  Gas sensors consist of a tin dioxide (SnO₂) semiconductor surface as the sensing element and a heating element that maintains this surface at the operating temperature.
  Moisture and adsorbed gas residues may be present on the sensing surface after the manufacturing and storage process. 
  Therefore, the sensors must be preheated by operating them for a certain period under nominal supply conditions before initial use. 
  This process ensures the surface conditions stabilize, contributes to the stabilization of the measurement response, and helps the sensor resistance values ​​settle within the operating range.

If all ppm calculations can already be done on the microcontroller, what is the purpose of JavaScript-based ppm calculation?
  The accuracy of any given current calculation method can never be guaranteed. Therefore, techniques can be updated with better ones over time. 
  Uploading code repeatedly and disassembling the circuit for each new technique updated in the microcontroller can be a cumbersome process. 
  Especially for IoT projects, the ppm calculation part can be made much more practical by transferring it to a script.

Why use the Curve Prediction Platform in 4D?
  This is because the calculation of ppm includes both the sensor's own signal and a correction coefficient calculated based on ambient temperature and relative humidity, along with time.
  In this case too, this necessitates the creation of a new 3D graph beneath the calculated 3D ppm graph based on the sensor signal, 
  to examine the correction coefficient change caused by temperature and humidity, which affects ppm, all within a single graph.
  Therefore, the graphic is being redesigned in 4D.

Why are there 77 different models in the 4D Curve Prediction Platform?
  Because environmental conditions, measurement time intervals, or other factors can cause the air quality of an environment to change along different curves or at different rates. 
  In this case too, This necessitates more predictive models to accurately forecast changes in air quality in that environment.

Why does the 4D Curve Prediction Platform have 77 different models, while the Model Curve Prediction Platform and Sensor Curve Prediction Platform only have 68 different models?
  Because some models make predictions based on sensor percentiles while also considering ambient temperature and/or humidity. 
  However, when the temperature and humidity factors are removed, models such as Multi-Variable Regression (Time + Temperature + Relative Humidity), Multi-Variable Regression (Temperature + Relative Humidity),
  Multi-Variable Regression (Time + Temperature), and Multi-Variable Regression (Time + Relative Humidity) are all grouped under a single umbrella as Multi-Variable Regression. This reduces variation, thus decreasing the number of models.
