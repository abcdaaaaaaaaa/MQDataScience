import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.optimize import curve_fit
import pandas as pd
import EstimateData

df = pd.read_excel("Sensor_Datas.xlsx")

SensorName = df["Mode"].iloc[0]
          
def roundf(*args):
    return tuple(round(x, 4) for x in args)

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def limit(value):
    return np.clip(value, 0, 100)

time, percentile = np.array(df["Time"], dtype=float), np.array(df["Per"], dtype=float)
percentile = limit(percentile)
SensorValue = percentile / 100

time_surface = vals(min(time), max(time)*2, 200)

r2_percentile_time, percentile_surface_raw, model_per = EstimateData.get_best_fit(time, percentile, time_surface)
percentile_surface = limit(percentile_surface_raw)

print(f"Percentile Model: {model_per}")

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
