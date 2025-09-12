import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.optimize import curve_fit
import pandas as pd

df = pd.read_excel("Sensor_Datas.xlsx")

SensorName = df["Mode"].iloc[0]
          
def roundf(*args):
    return tuple(round(x, 4) for x in args)

def yaxb(valuea, value, valueb):
    return valuea * np.power(value, valueb)

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def limit(value):
    return np.clip(value, 0, 100)

def fit_time_with_r2(x, y):
    popt, _ = curve_fit(lambda x, a, b: yaxb(a, x, b), x, y)
    a, b = popt
    y_pred = yaxb(a, np.array(x), b)
    ss_res = np.sum((np.array(y) - y_pred) ** 2)
    ss_tot = np.sum((np.array(y) - np.mean(y)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return a, b, r2

time, percentile = np.array(df["Time"], dtype=float), np.array(df["Per"], dtype=float)
percentile = limit(percentile)
SensorValue = percentile / 100

a_percentile_time, b_percentile_time, r2_percentile_time = fit_time_with_r2(time, percentile)
a_percentile_time, b_percentile_time, r2_percentile_time = roundf(a_percentile_time, b_percentile_time, r2_percentile_time)

time_surface = vals(min(time), max(time)*2, 200)
percentile_surface = limit(yaxb(a_percentile_time, time_surface, b_percentile_time))
   
GraphTitle = f"SensorPer% Graph Values"
fig = make_subplots(subplot_titles=[GraphTitle])
   
fig.add_trace(go.Scatter(x=time, y=percentile, mode='markers', marker=dict(color="#636EFA"), name="Real SensorValue%"))
fig.add_trace(go.Scatter(x=time_surface, y=percentile_surface, mode='lines', marker=dict(color="#636EFA"), name=f"SensorValue R² = {r2_percentile_time}"))


fig.update_layout(
    title=f"{SensorName} Model Slope Estimation",
    xaxis=dict(title='X: Time (w)'),
    yaxis=dict(title='Y: SensorValue (z)'),
    template='plotly_dark'
)

fig.write_html(f"{SensorName}_ModelSlope_Estimation.html")
