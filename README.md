# MQSpaceData v5.1.0

## MQDataScience What can be create?
"The first and only Arduino library where MQ Sensors combine with Data Science"

## 1) Advanced Data Science System for Regression Calculations
![MQ-135_gas_curves](https://github.com/user-attachments/assets/e8d6e1bf-6f61-40c8-9cc8-fd0cd7189c22)

## 2) Ppm Analysis of Different Model Gases
![MQ303A_Ppm_Analysis](https://github.com/user-attachments/assets/91be952f-5374-41a7-a64f-4d0e24a1af0e)

## 3) Formulated Correction Coefficients depending on Temperature and Humidity
![MQ-135_correction_coefficient](https://github.com/user-attachments/assets/8783b3a5-7956-47f1-a61b-ae300041e047)

## 4) 3D Surface Diagram for MQ-135 Gases
![MQ135_CO2_3D)](https://github.com/user-attachments/assets/5295ad32-65e2-4e4a-bbdb-d2a98b173e86)

## 5) Slope Estimation in Time-Dependent 4D Space
![4D_Slope_Estimation](https://github.com/user-attachments/assets/82f412d6-53f8-409c-9ce6-84a03cc2b30f)

## 4D Axis Features:

<img width="750" alt="4dformullas" src="https://github.com/user-attachments/assets/7c5a1464-fcb9-4a8f-9693-c2c473f1ec1a" />


## Ppm Formullas

![loghello)](https://github.com/user-attachments/assets/5b251bec-9677-421d-9101-ccb1e3ad4d2e)

<img width="1264" alt="image1" src="https://github.com/user-attachments/assets/780ca3d6-2bdb-4c64-8ced-ccb9c8a60c7b" />

<img width="1264" alt="image2" src="https://github.com/user-attachments/assets/a786298d-2df1-430b-bea5-ee53dec6692e" />

        if r_squared >= 0.9995:
            print("R-squared value for {gas name} is above 0.9995, plotting against first and last values.")
            
            x0, y0 = x[0], y[0]
            xn, yn = x[-1], y[-1]
            b = np.log10(yn/y0) / np.log10(xn/x0)
            a = 10**(np.log10(yn) - b * np.log10(xn))
            b2 = np.log10(yn) - b * np.log10(xn)
            b2_rounded = round(b2, 4)
            a_rounded = round(a, 4)
            b_rounded = round(b, 4)

The first formula is determined according to all points (OldCurve.py, OldCurve), while the second formula is determined according to the first and last point. Therefore, in order to collect them all in the same formula and to increase the accuracy rate, we used the method in the second formula and took the logarithm (if R^2 = 1 (%100) always: logm = valueb, logb = log10(valuea)) for slopes greater than 99.95% and collected them all in the first formula, thus we increased the accuracy rate without having to use 2 different formulas (Regression.py, NewCurve).

## y = ax^b  --> ppm = a×ratio^b
<b> Therefore, we need to make a transition according to the formula:

<img width="400" alt="image3" src="https://github.com/user-attachments/assets/5fe512c5-d0d3-413d-98c7-8516969f58cd" />

<b> In data graphs, the x-axis is given as ppm and the y-axis is given as ratio.

## V = I × R

<img width="1264" alt="image4" src="https://github.com/user-attachments/assets/c25bac78-f531-4c46-a028-47b723c10dd1" />

<img width="700" alt="image5" src="https://github.com/user-attachments/assets/0beab7d0-b9b8-472e-b17f-3cb0fc5eb048" />

## Calculate Ratio

(1) if ratio = Rs / Ro: Ratio = Ratio

(2) if ratio = Rs / Rs: RsRoMQAir = 1 --> Ratio = Ratio

(3) if ratio = Ro / Rs: a = 1 / a^(1 / b) & b = 1 / b --> Ratio = Ratio

(3) if ratio is inverted: ratio --> 1 / ratio

(ratio / a)^(1/b) --> (1 / (a * ratio))^(1/b) --> (1 / a)^(1/b) * (1 / ratio)^(1/b) --> [(1 / a)^(1/b)] * [1 / ratio^(1/b)] 

(ratio / a′)^(1/b′) --> ratio^(1/b′) / a′^(1/b′)

if both sides are equal: (1 / a)^(1/b) * 1 / ratio^(1/b) = ratio^(1/b′) / a′^(1/b′) -> 1 / a′ = (1 / a)^(1/b) & b′ = 1 / b

## Ratio for Sensors
STATUS 1: MQ-2, MQ-3, MQ-4, MQ-5, MQ-6, MQ-7, MQ-8, MQ-9, MQ-135, MQ-136, MQ-137 [Almost All & Standart]

STATUS 2: MQ303A, MQ303B, MQ307A, MQ309A [A & B models]

STATUS 3: MQ-131_LOW, MQ131 [MQ131 models]

## Inclusion of Correction Factor

ppm = (ratio / CorrectionCoefficient / a)^(1/b)  ppm = ([1 / CorrectionCoefficient / Air × SensorRLCalRL × (CalValue × (SensorValue – 1)) / (SensorValue × (CalValue – 1))]/a)^(1/b)

ppm=([1/interpolate(RH,33,85,a_RH33,a_RH85)((temp+15)/5)^interpolate(RH,33,85,b_RH33,b_RH85)×Air×SensorRLCalRL×(CalValue×(SensorValue–1))/(SensorValue×(CalValue–1))]/a)^(1/b)

interpolate(RH, 33, 85, a_RH33, a_RH85) --> (RH-33)×(a_RH85-a_RH33)+a_RH33

interpolate(RH, 33, 85, b_RH33, b_RH85) --> (RH-33)×(b_RH85-b_RH33)+b_RH33

</b>

<img width="750" alt="ppmformulla" src="https://github.com/user-attachments/assets/e37d3148-be7a-4d9f-9886-e4e48c7663fb" />

## STEL Limit For Gases
![STEL_LIMIT_FOR_GASES](https://github.com/user-attachments/assets/e092705a-1e45-4375-9aee-470e366a51de)

## SuggestedRL For MQ Sensors
![suggestedRL](https://github.com/user-attachments/assets/605c711b-61a5-4d5a-98fa-4014ebb26356)

## For detailed explanation, You can also check out the github <a href="https://github.com/abcdaaaaaaaaa/MQSpaceData.h/wiki">Wiki Page!

## You can access the library's article <a href="https://www.spacepedia.info/MQDataScience">Here!
