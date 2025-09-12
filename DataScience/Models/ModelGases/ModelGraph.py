import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.colors as pc
import MQInfo

f = input("SensorMode for ModelGases Visualization: ").strip()
if hasattr(MQInfo, f): getattr(MQInfo, f)()

SensorName = MQInfo.SensorName
Air = MQInfo.Air
CalibrateAir = MQInfo.CalibrateAir
CleanAir = MQInfo.CleanAir
MinAirPpm = MQInfo.MinAirPpm
MaxAirPpm = MQInfo.MaxAirPpm
gas_params = MQInfo.gas_params
SensorRLCalRL = MQInfo.SensorRLCalRL
SensorMode = MQInfo.SensorMode
Air = 1 if (SensorMode == 'Rs/Rs') else Air
FormulaCoefficient = MQInfo.FormulaCoefficient
AirValsEqualGasVals = MQInfo.AirValsEqualGasVals
FormulaMode = MQInfo.FormulaMode

def interpolate(value, old_min, old_max, new_min, new_max):
    return (value - old_min) * (new_max - new_min) / (old_max - old_min) + new_min

def yaxb(valuea, value, valueb):
    return valuea * np.power(value, valueb)

def inverseyaxb(valuea, value, valueb):
    return np.power(value / valuea, 1 / valueb)

def limit(value, minlim, maxlim):
    return np.clip(value, minlim, maxlim)

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def convertppm(value):
    convertvalue = value * FormulaCoefficient if FormulaMode != 'ppm' else value
    return convertvalue

def ppmLimits():
    minvalue = limit(SensorRLCalRL * Air * CalValue / (-maxratio * CalValue + maxratio + SensorRLCalRL * Air * CalValue), 0.001, 1)
    maxvalue = limit(SensorRLCalRL * Air * CalValue / (-minratio * CalValue + minratio + SensorRLCalRL * Air * CalValue), 0.001, 1)
    sensitivity = 100
    if maxvalue <= minvalue:
        sensitivity = 1
        maxvalue = minvalue
    else:
        print(f"{gasname}: {CalValue}")
        print(sensitivity, minvalue, maxvalue)
    return sensitivity, minvalue, maxvalue

def ppm(valuea, valueb, ratio):
    return convertppm(inverseyaxb(valuea, ratio, valueb))

def SensorppmModels(valuea, valueb, SensorValue):
    SensorRatio_value = SensorRLCalRL * Air * CalValue * (SensorValue - 1) / (SensorValue * (CalValue - 1))
    return convertppm(inverseyaxb(valuea, SensorRatio_value, valueb))

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=[f"Ratio", f"Sensor"]
)
    
color_palette = pc.qualitative.Plotly

for i, gas in enumerate(gas_params):
    minair, maxair = (MinAirPpm, MaxAirPpm) if AirValsEqualGasVals else gas['ppmvals']
    gasname = gas['name']
    valuea, valueb = gas['ppm']
    
    if (SensorMode == 'Ro/Rs'):
        valuea = 1 / np.power(valuea, 1 / valueb)
        valueb = 1 / valueb
        
    minratio = yaxb(valuea, maxair, valueb)
    maxratio = yaxb(valuea, minair, valueb)
    
    calAir = inverseyaxb(valuea, CalibrateAir, valueb)
    try: CalValue = gas['calvalue']
    except Exception: CalValue = interpolate(calAir, minair, maxair, 0, 1)

    minair, maxair = convertppm(minair), convertppm(maxair)

    sensitivity, minvalue, maxvalue = ppmLimits()
    ratio_vals = vals(minratio, maxratio, 100)

    SensorValue_vals = vals(minvalue, maxvalue, 100)
    
    color = color_palette[i % len(color_palette)]
    
    ppm_surface_ratio = [ppm(valuea, valueb, ratio) for ratio in ratio_vals]
    fig.add_trace(go.Scatter(
        x=ratio_vals,
        y=ppm_surface_ratio,
        mode='lines',
        name=f"{gasname} Ratio",
        line=dict(color=color)
    ), row=1, col=1)

    
    ppm_surface_sensor = [SensorppmModels(valuea, valueb, SensorValue) for SensorValue in SensorValue_vals]
    fig.add_trace(go.Scatter(
        x=SensorValue_vals,
        y=ppm_surface_sensor,
        mode='lines',
        name=f"{gasname} Sensor",
        line=dict(color=color)
    ), row=1, col=2)

fig.update_layout(
    title=f"PPM Diagrams for {SensorName} Gases",
    xaxis=dict(title='X: Ratio'),
    yaxis=dict(title='Y: Ratio Ppm'),
    xaxis2=dict(title='X: SensorValue'),
    yaxis2=dict(title='Y: Sensor Ppm'),
    template='plotly_dark'
)

fig.write_html(f"{SensorName}_gases_ppm.html")
