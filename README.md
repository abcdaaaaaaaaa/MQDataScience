# MQSpaceData v4.5.0

## MQDataScience What can be create?
"The first and only Arduino library where Geiger Counter and MQ Sensors combine with Data Science"

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

<b> 1) ppm = a*ratio^b (a: valuea b: valueb)
2) ppm = 10^[(log10(ratio)-b)/m] (m: logm b: logb)

If R^2 equals 1 :

a*ratio^b = 10^[(log10(ratio)-b)/m]                                                                                                                                             
logm = valueb, logb = log10(valuea)

![loghello)](https://github.com/user-attachments/assets/5b251bec-9677-421d-9101-ccb1e3ad4d2e)

1] [(1,10), (2,4), (3,3)]

loge(b) = ln(b) 

(ln(1),ln(10)) for ≈ (0,2.3026) 

(ln(2),ln(4)) ≈ (0.6931,1.3863) and 

(ln(3),ln(3)) ≈ (1.0986,1.0986) 

b = ∑ i=1 n (x i − x ˉ ) 2 ∑ i=1 n (xi − xˉ)(yi−yˉ) 

ln(x):(0,0.6931,1.0986)ln(y):(2.3026,1.3863,1.0986)ln(y)ˉ=(2.3026+1.3863+1.0986)/3≈1.5958

ln(x)ˉ=(0+0.6931+1.0986)/3≈0.5972

b = (0−0.5972)(2.3026−1.5958)+(0.6931−0.5972)(1.3863−1.5958)+(1.0986−0.5972)(1.0986−1.5958)/(0−0.5972)^2+(0.6931−0.5972)^2+(1.0986−0.5972)^2 ≈ -1.2


ln(a) = − ln ˉ (y) - b ln ˉ (x) ≈ 1.5958−(−1.2)⋅0.5972≈2.31244

a=e^2.31244 ≈ 9.947

b  ≈ -1.2

a ≈ 9.947

2] y = mx+ n                                                                                                                                                                       
n = b                                                                                                                                                                                                                                                                                                                                 
log10(y) = m*log10(x) + b

-b = m*log10(x) - log10(y)

last b = log10(y) - m*log10(x)

m = (y - y0) / (x - x0)

m = (log10(y) - log10(y0)) / (log10(x) - log10(x0))

if y= a*x^b:

last m = log10(y/y0) / log10(x/x0)

m = slope of the line

b = intersection point

m = log10(y/y0) / log10(x/x0)

b = log10(y) - m*log10(x)

</b>


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

## y = ax^b  --> ppm = a*ratio^b
<b>Therefore, we need to make a transition according to the formula:
In data graphs, the x-axis is given as ppm and the y-axis is given as ratio.

ratio = a*ppm^b --> ppm = (ratio / a)^1/b

## V = I x R
V = I x R -> VRL = [VC / (RS + RL)] x RL -> VRL = (VC x RL) / (RS + RL)

RS: -> VRL x (RS + RL) = VC x RL -> (VRL x RS) + (VRL x RL) = VC x RL -> (VRL x RS) = (VC x RL) - (VRL x RL)

RS = [(VC x RL) - (VRL x RL)] / VRL -> RS = [(VC x RL) / VRL] – RL

Rs = (voltage * Rload) / (voltage/2^n-1)) - (Rload)

SensorValue / 2^(AdcBitResulation1-1) -> SensorCalibrationValue / 2^(AdcBitResulation2-1) 

Rs = 2^(AdcBitResulation1-1) * [Rload / SensorValue - Rload] -> calibrationRs = 2^(AdcBitResulation2-1) * [Rload / SensorCalibrationValue – Rload]

Ro = calibrationRs / Air ||| ratio = Rs / Ro -> ratio = Rs / (calibrationRs / Air) -> ratio = Rs x Air / calibrationRs

Ratio = (2^(AdcBitResulation1-1) * [Rload1 / SensorValue – Rload1]) * RsRoMQAir / (2^(AdcBitResulation2-1) * [Rload2 / SensorCalibrationValue – Rload2]) [Rs / Ro]

If Sensor Calibration and Sensor Measurement are Under the Same Conditions:

Rload1 = Rload2 && 2^(AdcBitResulation1-1) = 2^(AdcBitResulation2-1)

SensorRange = [0 - 2^(AdcBitResulation-1)]

if MinSensorValue == 0 && MaxSensorValue == 1: SensorRange [0 - 1]

if SensorRange [0 - 1]: 0 <= (SensorValue) <= 1 && 0 <= SensorCalibrationValue <= 1 

Ratio = (MaxSensorValue * [Rload / SensorValue – Rload]) * RsRoMQAir / (MaxSensorValue * [Rload / SensorCalibrationValue – Rload]) [Rs / Ro]

Ratio = [Rload / SensorValue – Rload] * RsRoMQAir / [Rload / SensorCalibrationValue – Rload] [Rs / Ro]

Ratio = f(R) * RsRoMQAir

f(R) = [R / S - R] / [R / C - R] -> [(R - R*S) / S] / [(R - R*C) / C] -> [(R - R*S) / S] * [C / (R - R*C)]

f(R) = [(R - R*S) / S] * [C / (R - R*C)] = [C * (R - R*S) / S (R - R*C)]

g(x) = (R - R*x1) / (R - R*x2) -> g(x) = (1 - x1) / (1 - x2)

f(R) = [(R - R*S) / S] * [C / (R - R*C)] = [C * (1 - S) / S (1 - C)]

Ratio = [SensorCalibrationValue * (1 - SensorValue)] * RsRoMQAir / [SensorValue * (1 - SensorCalibrationValue)] [Rs / Ro]

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

## Multidimensional Radioactive Decay Estimations
![3D_preview](https://github.com/user-attachments/assets/586d16b4-6088-4917-b9ea-e49ebb4a5876)
## 
![2D_preview](https://github.com/user-attachments/assets/1ddea30f-7e8e-4b35-a259-23b3520053ac)

This repository presents a multivariable exponential regression model to estimate **Average CPM** (counts per minute) based on **Time**, **Radiation dose rate (Usv/hr)**, **Standard Deviation of CPM (sdCPM)**, and **Total CPM Count**.

## 1) Model Equation

The predicted average CPM is defined by the following equation:

<img width="750" alt="formullas" src="https://github.com/user-attachments/assets/6f94b3f0-cd1f-4432-82df-316aa9cb570a" />

Where:

<img width="750" alt="formullas2" src="https://github.com/user-attachments/assets/4ceb5d3a-1599-4932-bd29-cc81fadf0e23" />

## 2) Algorithm Logic

1. **Input features**:  
   - `Time`  
   - `Usv/hr` (radiation dose rate)  
   - `sdCPM` (standard deviation of CPM)  
   - `CPM Count` (total count)

2. Apply **natural logarithm** (`ln`) to all features except time to linearize exponential behavior.

3. Fit a **linear regression** model to:

<img width="750" alt="logformulla" src="https://github.com/user-attachments/assets/a9037f56-0f8d-488d-baa1-ff7c6fa4f279" />

4. Final prediction is obtained by **exponentiating** the output.

## STEL Limit For Gases
![STEL_LIMIT_FOR_GASES](https://github.com/user-attachments/assets/e092705a-1e45-4375-9aee-470e366a51de)

## SuggestedRL For MQ Sensors
![suggestedRL](https://github.com/user-attachments/assets/605c711b-61a5-4d5a-98fa-4014ebb26356)

## For detailed explanation, You can also check out the github <a href="https://github.com/abcdaaaaaaaaa/MQSpaceData.h/wiki">Wiki Page!

## You can access the library's article <a href="https://www.spacepedia.info/MQDataScience">Here!
