---------- For Library Terms ----------
  Correction Coefficient: Mathematical modeling of the compensation of incorrect ppm rate measured due to negative effects of environmental conditions based on temperature and humidity of the sensor.
  
  Standard Gases: Gases measured by correction coefficient supported "Standard Sensors".
  Different Model Gases: Gases measured by "Standard Sensors" without correction coefficient support.

  Standart Sensors: Sensors supported in this library.
  Different Model Sensors:  Sensors unsupported in this library.

---------- For Data Science ----------
  For data science applications: https://github.com/abcdaaaaaaaaa/MQDataScience/tree/main/DataScience
  For correction coefficient assisted 4d ppm slope estimation in Data Science Applications: https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/4D_Slope/4DSlope.py
  For only read and estimate current ppm values with correction coefficient (does not include 4D axis features) in Data Science Applications: https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/4D_Slope/readppm.py
  For model gases ppm estimation in Data Science Applications: https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/Models/ModelGases/ModelSlope.py
  For 3D air quality graphical sensor simulation with correction coefficient support in data science applications: https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/3D_Surface/3DSurface.py
  For air quality graphical sensor simulation of model gases in data science applications: https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/Models/ModelGases/ModelGraph.py
  For slope estimation of sensors not supported in Data Science Application: https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/Models/ModelSensor/SensorSlope.py
  To generate regression curves of all supported MQ series gases: https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/Regression/SensorCurves/Curves.py

---------- For UnSupported MQ Sensors ----------
  To calculate correction coefficients for sensors not supported by customized modes in Data Science Applications: https://github.com/abcdaaaaaaaaa/MQDataScience/tree/main/DataScience/Regression/CorrectionCoefficient
  To calculate the power regression constants for converting the ratios of unsupported MQ sensors to ppm: https://github.com/abcdaaaaaaaaa/MQDataScience/blob/main/DataScience/Regression/SensorCurves/Curves.py
  For the microcontroller to process the information obtained from the data graphs of unsupported MQ sensors by data science applications: UnSupported_MQ_Sensors.ino

---------- For JS and IoT Projects ----------
  To do these ppm calculations in javascript instead of microcontroller in IoT projects: https://github.com/abcdaaaaaaaaa/MQDataScience/tree/main/DataScript

---------- Library Examples Files ----------
  For the microcontroller to process the information obtained from the data graphs of unsupported MQ sensors by data science applications: UnSupported_MQ_Sensors.ino
  For accurate ppm results, you need to provide the following resistance values to the sensor: Required_MQ_LoadResistor.ino
  To access the codes for the latest version of the library published on the Arduino Project Hub for easy use of the library: ProjectHub.ino
  To process supported MQ sensors to the microcontroller: All_Supported_MQ_Sensors.ino
  To obtain more concrete information about gas sensors: curious.ino
  To have general information about all the files in the library: information.ino
