WARNING: To run the code, move the MQInfo.py and PredictData.py files from the Requirements folder to the following paths: C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\MQInfo.py and C:\Users\user\AppData\Local\Programs\Python\Python311\Lib\site-packages\PredictData.py. Include any other libraries in the requirements.txt file from the Requirements folder using `pip install -r requirements.txt`. (Necessary)

NOTE: This code is suitable for gas sensors measuring standard gases.

Sensor modes measuring "Standard Gases": MQ135, MQ2, MQ3, MQ4, MQ5, MQ6, MQ7, MQ8, MQ9, MQ131, MQ136, MQ137, MQ138, MQ214, MQ216

This code aims to predict future data based on past data. 
This code uses 77 different models for each section when making predictions and selects the one with the highest accuracy rate for each.

Please update the xlsx excel file to the sensor mode you are using and the past results you have obtained.
The data you need to measure for this code: Gas Sensor Percentage, Celsius Temperature, Relative Humidity (DHT22, recommended).

-- WARNING --
If you are using MQ131, make sure it measures with low sensitivity.
To understand the sensitivity of MQ131, look at its concentration range (if ppb --> low ModelCurve.py) (if ppm --> high 4DCurve.py).

If the sensor you are working with is not listed, please check the list of "Model Gases". (ModelCurve.py)

NOTE: If you are going to use this system "only" for ppm reading and predicting in a python project: you can use readppm.py (Does not include create 4d curve html file).
