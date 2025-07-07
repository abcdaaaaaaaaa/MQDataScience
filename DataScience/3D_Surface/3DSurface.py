import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
import MQInfo

f = input("SensorMode for 3D Visualization: ").strip()
if hasattr(MQInfo, f): getattr(MQInfo, f)()

SensorName = MQInfo.SensorName
Air = MQInfo.Air
CalibrateAir = MQInfo.CalibrateAir
CleanAir = MQInfo.CleanAir
MinAirPpm = MQInfo.MinAirPpm
MaxAirPpm = MQInfo.MaxAirPpm
gas_params = MQInfo.gas_params

try: a_RH30 = MQInfo.a_RH30
except Exception: pass

try: b_RH30 = MQInfo.b_RH30
except Exception: pass

try: a_RH33 = MQInfo.a_RH33
except Exception: pass

try: b_RH33 = MQInfo.b_RH33
except Exception: pass

try: a_RH60 = MQInfo.a_RH60
except Exception: pass

try: b_RH60 = MQInfo.b_RH60
except Exception: pass

try: a_RH85 = MQInfo.a_RH85
except Exception: pass

try: b_RH85 = MQInfo.b_RH85
except Exception: pass

SensorRLCalRL = MQInfo.SensorRLCalRL
SensorMode = MQInfo.SensorMode
FormulaCoefficient = MQInfo.FormulaCoefficient
AirVals = MQInfo.AirVals
AirValsEqualGasVals = MQInfo.AirValsEqualGasVals
CRMode = MQInfo.CRMode
FormulaMode = MQInfo.FormulaMode

def interpolate(value, old_min, old_max, new_min, new_max):
    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

def yaxb(valuea, value, valueb):
    return valuea * np.power(value, valueb)

def inverseyaxb(valuea, value, valueb):
    return np.power(value / valuea, 1 / valueb)

def CorrectionCoefficient(temp, RH):
    if CRMode != 3:
        TH_valuea, TH_valueb = interpolate(RH, 33, 85, a_RH33, a_RH85), interpolate(RH, 33, 85, b_RH33, b_RH85)
        temp_scaled = (temp + 25) / 15 if CRMode == 1 else (temp + 15) / 5
        lastcr = yaxb(TH_valuea, temp_scaled, TH_valueb)
    else:
        temp_scaled = (temp + 15) / 5
        if isinstance(RH, int):
            if (RH <= 60):
                range_a = 30, 60
                a_RH = a_RH30, a_RH60
                range_b = 30, 60
                b_RH = b_RH30, b_RH60
            else:
                range_a = 60, 85
                a_RH = a_RH60, a_RH85
                range_b = 60, 85
                b_RH = b_RH60, b_RH85
            TH_valuea, TH_valueb = interpolate(RH, *range_a, *a_RH), interpolate(RH, *range_b, *b_RH)
            lastcr = yaxb(TH_valuea, temp_scaled, TH_valueb)
        else:
            values = []
            for i in range(RH.shape[0]):
                for j in range(RH.shape[1]):
                    rh = RH[i, j]
                    t = temp_scaled[i, j]
                    
                    if rh <= 60:
                        range_a = 30, 60
                        a_RH = a_RH30, a_RH60
                        range_b = 30, 60
                        b_RH = b_RH30, b_RH60
                    else:
                        range_a = 60, 85
                        a_RH = a_RH60, a_RH85
                        range_b = 60, 85
                        b_RH = b_RH60, b_RH85

                    valuea = interpolate(rh, *range_a, *a_RH)
                    valueb = interpolate(rh, *range_b, *b_RH)

                    result = valuea * np.power(t, valueb)
                    values.append(result)

            values_array = np.array(values)
            lastcr = values_array.reshape(RH.shape)
    return lastcr

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def limit(value, minlim, maxlim):
    return np.minimum(np.maximum(value, minlim), maxlim)

def convertppm(value):
    convertvalue = value * FormulaCoefficient if FormulaMode != 'ppm' else value
    return convertvalue

def ppmLimits():
    minvalue = limit(SensorRLCalRL * Air * CalValue / (-maxratio * CalValue + maxratio + SensorRLCalRL * Air * CalValue), 0.0001, 1)
    maxvalue = limit(SensorRLCalRL * Air * CalValue / (-minratio * CalValue + minratio + SensorRLCalRL * Air * CalValue), 0.0001, 1)
    sensitivity = 100
    if maxvalue <= minvalue:
        sensitivity = 1
        maxvalue = minvalue
    else:
        print(f"{gasname}: {CalValue}")
        print(sensitivity, minvalue, maxvalue)
    return sensitivity, minvalue, maxvalue

def ppm(valuea, valueb, ratio, RH, temp):
    return limit(convertppm(inverseyaxb(valuea, ratio / CorrectionCoefficient(temp, RH), valueb)), 0, maxair * CorrectionCoefficient(temp, RH))

def Sensorppm(valuea, valueb, SensorValue, RH, temp):
    SensorRatio_value = Air * SensorRLCalRL * (CalValue * (SensorValue - 1)) / (SensorValue * (CalValue - 1))
    return limit(convertppm(inverseyaxb(valuea, SensorRatio_value / CorrectionCoefficient(temp, RH), valueb)), 0, maxair * CorrectionCoefficient(temp, RH))

def LowSensitivityppm(valuea, valueb, ratio, RH, temp):
    return limit(ppm(valuea, valueb, ratio, RH, temp), 0, maxair * CorrectionCoefficient(temp, RH))

def LowSensitivitySensorppm(valuea, valueb, SensorValue, RH, temp):
    return limit(Sensorppm(valuea, valueb, SensorValue, RH, temp), 0, maxair * CorrectionCoefficient(temp, RH))

minrh = 30 if CRMode == 3 else 33

temp_vals, RH_vals = vals(-10, 50, 100), vals(minrh, 85, 100)
temp_grid, RH_grid = np.meshgrid(temp_vals, RH_vals)

mincr, maxcr = CorrectionCoefficient(50, 85), CorrectionCoefficient(-10, minrh)

scene_camera = dict(eye=dict(x=1.5, y=1.5, z=0.01))

for gas in gas_params:
    minair, maxair = (MinAirPpm, MaxAirPpm) if AirValsEqualGasVals else gas['ppmvals']
    gasname = gas['name']
    valuea, valueb = gas['ppm']
    
    if (SensorMode == 'Ro/Rs'):
        valuea = 1 / np.power(valuea, 1 / valueb)
        valueb = 1 / valueb

    minratio = yaxb(valuea, maxair, valueb) * mincr
    maxratio = yaxb(valuea, minair, valueb) * maxcr

    calAir = inverseyaxb(valuea, CalibrateAir, valueb)
    CalValue = limit(interpolate(calAir, minair, maxair, 0, 1), 0.01, 0.99)
    
    minair, maxair = convertppm(minair), convertppm(maxair)

    sensitivity, minvalue, maxvalue = ppmLimits()
    if (sensitivity == 1):
        minratio = yaxb(valuea, maxair, valueb) * maxcr
        maxratio = yaxb(valuea, minair, valueb) * mincr
        sensitivity, minvalue, maxvalue = ppmLimits()
        sensitivity = 50
    ratio_vals = vals(minratio, maxratio, 100)
    SensorValue_vals = vals(minvalue, maxvalue, 100)
    
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(f"Ratio {gasname}", f"Sensor {gasname}"),
        specs=[[{'type': 'surface'}, {'type': 'surface'}]]
    )
    
    for ratio in ratio_vals:
        ppm_surface = ppm(valuea, valueb, ratio, RH_grid, temp_grid)
        if (sensitivity == 50):
            ppm_surface = LowSensitivityppm(valuea, valueb, ratio, RH_grid, temp_grid)
        fig.add_trace(go.Surface(
            showscale=False,
            z=ppm_surface,
            x=temp_vals,
            y=RH_vals,
            colorscale='Viridis',
            name = f"Ratio: {ratio:.4f}"
        ), row=1, col=1)
    
    for SensorValue in SensorValue_vals:
        ppm_surface = Sensorppm(valuea, valueb, SensorValue, RH_grid, temp_grid)
        if (sensitivity == 50):
            ppm_surface = LowSensitivitySensorppm(valuea, valueb, SensorValue, RH_grid, temp_grid)
        fig.add_trace(go.Surface(
            showscale=False,
            z=ppm_surface,
            x=temp_vals,
            y=RH_vals,
            colorscale='Viridis',
            name = f"Sensor: {SensorValue:.4f}"
        ), row=1, col=2)

    fig.update_layout(
        title=f"3D PPM Surface Diagram for {SensorName} Gases",
        scene=dict(
            xaxis_title="Temperature (°C)",
            yaxis_title="RH (%)",
            zaxis_title="PPM Values",
            aspectmode="cube",
            camera=scene_camera
        ),
        scene2=dict(
            xaxis_title="Temperature (°C)",
            yaxis_title="RH (%)",
            zaxis_title="PPM Values",
            aspectmode="cube",
            camera=scene_camera
        ),
        template='plotly_dark'
    )
    

    fig.write_html(f"{SensorName}_{gasname}_ppm.html")
