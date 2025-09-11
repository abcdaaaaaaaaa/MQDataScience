import numpy as np
import plotly.graph_objects as go
from scipy.optimize import curve_fit
import plotly.colors as pc
import pandas as pd
from datetime import datetime
import MQInfo

df = pd.read_excel("4D_Datas.xlsx")

f = df["Mode"].iloc[0].strip()
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

now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

print("")
print("")
print(SensorName + " " + formatted)
print("")
print("")

with open("DataReport.txt", "a") as f:
    f.write("\n")
    f.write(SensorName + " " + formatted)
    f.write("\n")
    f.write("\n")
    f.write("\n")

with open("EstimationReport.txt", "a") as f:
    f.write("\n")
    f.write(SensorName + " " + formatted)
    f.write("\n")
    f.write("\n")
    f.write("\n")

def roundf(*args):
    return tuple(round(x, 4) for x in args)

def round2(value):
    return round(value, 2)

def yaxb(valuea, value, valueb):
    return valuea * np.power(value, valueb)

def inverseyaxb(valuea, value, valueb):
    return np.power(value / valuea, 1 / valueb)

def interpolate(value, min_value, max_value, target_min, target_max):
    return target_min + (value - min_value) * (target_max - target_min) / (max_value - min_value)

def exponential_interpolate(value, min_value, max_value, target_min, target_max):
    log_min = np.log10(target_min)
    log_max = np.log10(target_max)
    ratio = (value - min_value) / (max_value - min_value)
    log_val = log_min + ratio * (log_max - log_min)
    return np.power(10, log_val)

def function(constant, mini_slope):
    return constant * mini_slope + constant

def ScaleTemp(temp, mode):
    if mode == '+': temp_scaled = (temp + 25) / 15 if CRMode == 1 else (temp + 15) / 5
    elif mode == '-': temp_scaled = 15 * temp - 25 if CRMode == 1 else 5 * temp - 15
    return temp_scaled

def CorrectionCoefficient(temp, RH):
    if CRMode != 3:
        TH_valuea, TH_valueb = interpolate(RH, 33, 85, a_RH33, a_RH85), interpolate(RH, 33, 85, b_RH33, b_RH85)
        return yaxb(TH_valuea, temp, TH_valueb)
    else:
        if isinstance(RH, np.float64):
            if RH <= 60: range_a, a_RH, range_b, b_RH = (30, 60), (a_RH30, a_RH60), (30, 60), (b_RH30, b_RH60)
            else: range_a, a_RH, range_b, b_RH = (60, 85), (a_RH60, a_RH85), (60, 85), (b_RH60, b_RH85)
            TH_valuea, TH_valueb = interpolate(RH, *range_a, *a_RH), interpolate(RH, *range_b, *b_RH)
            return yaxb(TH_valuea, temp, TH_valueb)
        else:
            values = []
            for t, rh in enumerate(RH):
                if rh <= 60: range_a, a_RH, range_b, b_RH = (30, 60), (a_RH30, a_RH60), (30, 60), (b_RH30, b_RH60)
                else: range_a, a_RH, range_b, b_RH = (60, 85), (a_RH60, a_RH85), (60, 85), (b_RH60, b_RH85)
                TH_valuea, TH_valueb = interpolate(rh, *range_a, *a_RH), interpolate(rh, *range_b, *b_RH)
                values.append(yaxb(TH_valuea, temp[t], TH_valueb))
            return np.array(values)

def fit_time_with_r2(x, y):
    popt, _ = curve_fit(lambda x, a, b: yaxb(a, x, b), x, y)
    a, b = popt
    y_pred = yaxb(a, np.array(x), b)
    ss_res = np.sum((np.array(y) - y_pred) ** 2)
    ss_tot = np.sum((np.array(y) - np.mean(y)) ** 2)
    r2 = 1 - (ss_res / ss_tot)
    return a, b, r2

def filter_repeats(x, y):
    filtered_x = [x[0]]
    filtered_y = [y[0]]
    for i in range(1, len(y)):
        if (y[i - 1] != minair) and (y[i - 1] != maxair):
            filtered_x.append(x[i])
            filtered_y.append(y[i])
    return filtered_x, filtered_y

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def limit(value, minlim, maxlim):
    return np.minimum(np.maximum(value, minlim), maxlim)

def convertppm(value):
    convertvalue = value * FormulaCoefficient if FormulaMode != 'ppm' else value
    return convertvalue

def Sensorppm(valuea, valueb, SensorValue, CorrectionCoefficient):
    SensorRatio_value = Air * SensorRLCalRL * (CalValue * (SensorValue - 1)) / (SensorValue * (CalValue - 1))
    return convertppm(inverseyaxb(valuea, SensorRatio_value / CorrectionCoefficient, valueb))

def differentiation(valuea, value, valueb):
    slope = valuea * valueb * np.power(value, valueb-1)
    slope = limit(slope, -1, 1)
    mini_slope = slope / 4
    return mini_slope
    # return True if slope >= 0 else False

def create_cube(center, xmin, xmax, ymin, ymax, zmin, zmax):
    x0, y0, z0 = center
    vertices = [[x0 + xmin, y0 + ymin, z0 + zmin], [x0 + xmax, y0 + ymin, z0 + zmin], [x0 + xmax, y0 + ymax, z0 + zmin], [x0 + xmin, y0 + ymax, z0 + zmin], [x0 + xmin, y0 + ymin, z0 + zmax], [x0 + xmax, y0 + ymin, z0 + zmax], [x0 + xmax, y0 + ymax, z0 + zmax], [x0 + xmin, y0 + ymax, z0 + zmax]]
    return np.array(vertices)

def add_cube_edges(fig, vertices, color, trace_name):
    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 5), (7, 4), (4, 5), (3, 7)]
    for start, end in edges: fig.add_trace(go.Scatter3d(x=[vertices[start, 0], vertices[end, 0]], y=[vertices[start, 1], vertices[end, 1]], z=[vertices[start, 2], vertices[end, 2]], mode='lines+text', line=dict(color=color, width=4), text=[trace_name, trace_name], textposition="middle center", name=trace_name, hoverinfo='text+name', textfont=dict(size=15, color=color, weight='bold')))

def add_cube_faces(fig, vertices, color, trace_name):
    faces = [[0, 1, 2], [0, 2, 3], [0, 1, 5], [0, 5, 4], [0, 3, 7], [0, 7, 4]]
    fig.add_trace(go.Mesh3d(x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2], i=[face[0] for face in faces], j=[face[1] for face in faces], k=[face[2] for face in faces], color=color, opacity=0.3, name=trace_name, flatshading=True, hoverinfo='none'))

def add_z_faces(fig, outer_vertices, inner_vertices, color, trace_name):
    z_faces = [(0, 1, 5, 4), (4, 5, 1, 0), (0, 3, 7, 4), (4, 7, 3, 0)]
    for face in z_faces: fig.add_trace(go.Mesh3d(x=[outer_vertices[face[i], 0] for i in range(4)] + [inner_vertices[face[i], 0] for i in range(4)], y=[outer_vertices[face[i], 1] for i in range(4)] + [inner_vertices[face[i], 1] for i in range(4)], z=[outer_vertices[face[i], 2] for i in range(4)] + [inner_vertices[face[i], 2] for i in range(4)], color=color, opacity=0.3, name=trace_name, flatshading=True, hoverinfo='none'))

time, percentile, temperature, rh = np.array(df["Time"], dtype=float), np.array(df["Per"], dtype=float), np.array(df["Temp"], dtype=float), np.array(df["Rh"], dtype=float)
percentile, temperature, rh = limit(percentile, 0, 100), limit(temperature, -10, 50), limit(rh, 0, 100)

SensorValue = percentile / 100
temperature = ScaleTemp(temperature, '+')
correction_coefficient = CorrectionCoefficient(temperature, rh)
air = limit(exponential_interpolate(SensorValue, 0, 1, convertppm(MinAirPpm), convertppm(MaxAirPpm)), 0, convertppm(MaxAirPpm)) * correction_coefficient

a_temp_time, b_temp_time, r2_temp_time = fit_time_with_r2(time, temperature)
a_rh_time, b_rh_time, r2_rh_time = fit_time_with_r2(time, rh)
a_percentile_time, b_percentile_time, r2_percentile_time = fit_time_with_r2(time, percentile)

a_temp_time, b_temp_time, r2_temp_time = roundf(a_temp_time, b_temp_time, r2_temp_time)
a_rh_time, b_rh_time, r2_rh_time = roundf(a_rh_time, b_rh_time, r2_rh_time)
a_percentile_time, b_percentile_time, r2_percentile_time = roundf(a_percentile_time, b_percentile_time, r2_percentile_time)

time_surface = vals(min(time), max(time)*2, 200)
temperature_surface = limit(yaxb(a_temp_time, time_surface, b_temp_time), ScaleTemp(-10, '+'), ScaleTemp(50, '+'))
rh_surface = limit(yaxb(a_rh_time, time_surface, b_rh_time), 0, 100)
correction_coefficient_surface = CorrectionCoefficient(temperature_surface, rh_surface)
percentile_surface = limit(yaxb(a_percentile_time, time_surface, b_percentile_time), 0, 100)
SensorValue_surface = percentile_surface / 100
air_surface = limit(exponential_interpolate(SensorValue_surface, 0, 1, convertppm(MinAirPpm), convertppm(MaxAirPpm)), 0, convertppm(MaxAirPpm)) * correction_coefficient_surface

temperature = ScaleTemp(temperature, '-')
temperature_surface = ScaleTemp(temperature_surface, '-')

mintime = np.min(time_surface)
maxtime = np.max(time_surface)

ppm_range = []
ppms_range = []

xmin, xmax = np.min([np.min(temperature), np.min(temperature_surface)]), np.max([np.max(temperature), np.max(temperature_surface)])
ymin, ymax = np.min([np.min(rh), np.min(rh_surface)]), np.max([np.max(rh), np.max(rh_surface)])
zmin, zmax = np.min([np.min(air), np.min(air_surface)]), np.max([np.max(air), np.max(air_surface)])

mincr, maxcr = np.min([np.min(correction_coefficient), np.min(correction_coefficient_surface)]), np.max([np.max(correction_coefficient), np.max(correction_coefficient_surface)])

x_middle_min = (xmax-xmin)/4
x_middle_max = x_middle_min*3
x_middle = (xmax+xmin)/2

y_middle_min = (ymax-ymin)/4
y_middle_max = y_middle_min*3
y_middle = (ymax+ymin)/2

z_middle_min = (zmax-zmin)/4
z_middle_max = z_middle_min*3
z_middle = (zmax+zmin)/2

x_middle_min += xmin
x_middle_max += xmin
y_middle_min += ymin
y_middle_max += ymin
z_middle_min += zmin
z_middle_max += zmin

outer_cube = create_cube(center=(0, 0, 0), xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax, zmin=zmin, zmax=zmax)
inner_cube = create_cube(center=(0, 0, 0), xmin=x_middle_min, xmax=x_middle_max, ymin=y_middle_min, ymax=y_middle_max, zmin=z_middle_min, zmax=z_middle_max)

fig = go.Figure()

def add_cubes_faces():
    add_cube_faces(fig, outer_cube, 'blue', "x")
    add_cube_faces(fig, inner_cube, 'red', "y")
    add_z_faces(fig, outer_cube, inner_cube, 'green', "z")

def add_cubes_edges():
    add_cube_edges(fig, outer_cube, 'blue', "x")
    add_cube_edges(fig, inner_cube, 'red', "y")
    
    for i in range(8):
        if i == 6 or i == 2: continue
        
        fig.add_trace(go.Scatter3d(x=[outer_cube[i, 0], inner_cube[i, 0]], y=[outer_cube[i, 1], inner_cube[i, 1]], z=[outer_cube[i, 2], inner_cube[i, 2]], mode='lines+text', line=dict(color='green', width=2), text=["z", "z"], textposition="middle center", name="z", hoverinfo='text+name', textfont=dict(size=15, color='green', weight='bold')))
    xgrid_lines = vals(x_middle_min, x_middle_max, 10)
    ygrid_lines = vals(y_middle_min, y_middle_max, 10)
    zgrid_lines = vals(z_middle_min, z_middle_max, 10)

    for g in xgrid_lines:
        fig.add_trace(go.Scatter3d(x=[g, g], y=[y_middle_min, y_middle_min], z=[z_middle_max, z_middle_min], mode='lines', line=dict(color='red', width=1), name="x", hoverinfo='none'))
        fig.add_trace(go.Scatter3d(x=[g, g], y=[y_middle_max, y_middle_min], z=[z_middle_min, z_middle_min], mode='lines+text', line=dict(color='red', width=1), text=[str(round2(interpolate(g, x_middle_min, x_middle_max, xmin, xmax)))], textposition="middle center", name="x", hoverinfo='text+name', textfont=dict(size=9, color='white')))

    for g in ygrid_lines:
        fig.add_trace(go.Scatter3d(x=[x_middle_min, x_middle_min], y=[g, g], z=[z_middle_max, z_middle_min], mode='lines', line=dict(color='red', width=1), name="y", hoverinfo='none'))
        fig.add_trace(go.Scatter3d(x=[x_middle_max, x_middle_min], y=[g, g], z=[z_middle_min, z_middle_min], mode='lines+text', line=dict(color='red', width=1), text=[str(round2(interpolate(g, y_middle_min, y_middle_max, ymin, ymax)))], textposition="middle center", name="y", hoverinfo='text+name', textfont=dict(size=9, color='white')))

    for g in zgrid_lines:
        fig.add_trace(go.Scatter3d(x=[x_middle_min, x_middle_min], y=[y_middle_max, y_middle_min], z=[g, g], mode='lines', line=dict(color='red', width=1), name="z", hoverinfo='none'))
        fig.add_trace(go.Scatter3d(x=[x_middle_max, x_middle_min], y=[y_middle_min, y_middle_min], z=[g, g], mode='lines+text', line=dict(color='red', width=1), text=[str(round2(interpolate(g, z_middle_min, z_middle_max, mincr, maxcr)))], textposition="middle center", name="z", hoverinfo='text+name', textfont=dict(size=9, color='white')))
        
    xvalues = [xmin, x_middle_min, x_middle_max, xmax]
    yvalues = [ymin, y_middle_min, y_middle_max, ymax]
    zvalues = [zmin, z_middle_min, z_middle_max, zmax]
    colors = ['purple', 'orange', 'purple']

    for i in range(3):
        fig.add_trace(go.Scatter3d(x=[xvalues[i], xvalues[i+1]], y=[y_middle, y_middle], z=[z_middle, z_middle], mode='lines+text', line=dict(color=colors[i], width=4), text=["x", "x"], textposition="middle center", name="x", hoverinfo='text+name', textfont=dict(size=15, color=colors[i], weight='bold')))
        fig.add_trace(go.Scatter3d(x=[x_middle, x_middle], y=[yvalues[i], yvalues[i+1]], z=[z_middle, z_middle], mode='lines+text', line=dict(color=colors[i], width=4), text=["y", "y"], textposition="middle center", name="y", hoverinfo='text+name', textfont=dict(size=15, color=colors[i], weight='bold')))
        fig.add_trace(go.Scatter3d(x=[x_middle, x_middle], y=[y_middle, y_middle], z=[zvalues[i], zvalues[i+1]], mode='lines+text', line=dict(color=colors[i], width=4), text=["z", "z"], textposition="middle center", name="z", hoverinfo='text+name', textfont=dict(size=15, color=colors[i], weight='bold')))

add_cubes_faces()
add_cubes_edges()

fig.add_trace(go.Scatter3d(
    x=temperature,
    y=rh,
    z=air,
    mode='markers',
    marker=dict(size=6, colorscale='Viridis', symbol='circle', color=time, cmin=min(time_surface), cmax=max(time_surface)),
    name='Real Datas',
    hoverinfo='x+y+z',
    hovertemplate=( 
        'SensorAir (z): %{z}<br>' +
        'Time (w): %{customdata[0]:.4f}<br>' +
        'CorrectionCoefficient: %{customdata[3]:.4f}<br>' +
        'Temperature°C (x): %{customdata[1]:.4f}<br>' +
        'RH (y): %{customdata[2]:.4f}'
    ),
    customdata=np.stack((time, temperature, rh, CorrectionCoefficient(ScaleTemp(temperature, '+'), rh)), axis=-1)
))

fig.add_trace(go.Scatter3d(
    x=temperature_surface,
    y=rh_surface,
    z=air_surface,
    mode='lines',
    line=dict(width=10, colorscale='Viridis', color=time_surface, cmin=min(time_surface), cmax=max(time_surface), colorbar=dict(title='Time(w)')),
    name='Regression Curves',
    hoverinfo='x+y+z',
    hovertemplate=( 
        'SensorAir (z): %{customdata[4]:.4f}<br>' +
        'Time (w): %{customdata[0]:.4f}<br>' +
        'CorrectionCoefficient: %{customdata[3]:.4f}<br>' +
        'Temperature°C (x): %{customdata[1]:.4f}<br>' +
        'RH (y): %{customdata[2]:.4f}'
    ),
    customdata=np.stack((time_surface, temperature_surface, rh_surface, correction_coefficient_surface, air_surface), axis=-1)
))

fig.add_trace(go.Scatter3d(
    x=interpolate(temperature, xmin, xmax, x_middle_min, x_middle_max),
    y=interpolate(rh, ymin, ymax, y_middle_min, y_middle_max),
    z=interpolate(CorrectionCoefficient(ScaleTemp(temperature, '+'), rh), mincr, maxcr, z_middle_min, z_middle_max),
    mode='markers',
    marker=dict(size=6, colorscale='Viridis', symbol='circle', color=time, cmin=min(time_surface), cmax=max(time_surface)),
    name='Correction Coefficient Datas',
    hoverinfo='x+y+z',
    hovertemplate=( 
        'CorrectionCoefficient: %{customdata[3]:.4f}<br>' +
        'Time (w): %{customdata[0]:.4f}<br>' +
        'Temperature°C (x): %{customdata[1]:.4f}<br>' +
        'RH (y): %{customdata[2]:.4f}'
    ),
    customdata=np.stack((time, temperature, rh, CorrectionCoefficient(ScaleTemp(temperature, '+'), rh)), axis=-1)
))

fig.add_trace(go.Scatter3d(
    x=interpolate(temperature_surface, xmin, xmax, x_middle_min, x_middle_max),
    y=interpolate(rh_surface, ymin, ymax, y_middle_min, y_middle_max),
    z=interpolate(correction_coefficient_surface, mincr, maxcr, z_middle_min, z_middle_max),
    mode='lines',
    line=dict(width=10, colorscale='Viridis', color=time_surface, cmin=min(time_surface), cmax=max(time_surface)),
    name='Correction Coefficient Curves',
    hoverinfo='x+y+z',
    hovertemplate=( 
        'CorrectionCoefficient: %{customdata[3]:.4f}<br>' +
        'Time (w): %{customdata[0]:.4f}<br>' +
        'Temperature°C (x): %{customdata[1]:.4f}<br>' +
        'RH (y): %{customdata[2]:.4f}'
    ),
    customdata=np.stack((time_surface, temperature_surface, rh_surface, correction_coefficient_surface), axis=-1)
))

# colornum = 0

color_palette = pc.qualitative.Plotly

for i, gas in enumerate(gas_params):
    minair, maxair = (MinAirPpm, MaxAirPpm) if AirValsEqualGasVals else gas['ppmvals']
    gasname = gas['name']
    valuea, valueb = gas['ppm']
    if (SensorMode == 'Ro/Rs'):
        valuea = 1 / np.power(valuea, 1 / valueb)
        valueb = 1 / valueb
    calAir = inverseyaxb(valuea, CalibrateAir, valueb)
    CalValue = limit(interpolate(calAir, minair, maxair, 0, 1), 0.01, 0.99)
    minair, maxair = convertppm(minair), convertppm(maxair)
    """
    colornum += 1
    match colornum:
        case 1: color = "#32CD32"  # Lime Green
        case 2: color = "#FF4500"  # Red-Orange
        case 3: color = "#4B0082"  # Deep Violet
        case 4: color = "#5D3A9B"  # Indigo
        case 5: color = "#0074D9"  # Blue (Light Blue)
        case 6: color = "#0000FF"  # Blue
        case 7: color = "#000080"  # Navy (Dark Blue)
        case _: color = "Unknown"
    """
    color = color_palette[i % len(color_palette)]

    ppm = limit(Sensorppm(valuea, valueb, SensorValue, CorrectionCoefficient(ScaleTemp(temperature, '+'), rh)), 0, maxair * CorrectionCoefficient(ScaleTemp(temperature, '+'), rh))
    x1, y1 = filter_repeats(time, ppm)
    ppm_range.append(ppm)
    fig.add_trace(go.Scatter(x=x1, y=y1, mode='markers', marker=dict(color=color), name=gasname))

    ppm_surface = limit(Sensorppm(valuea, valueb, SensorValue_surface, correction_coefficient_surface), 0, maxair * correction_coefficient_surface)
    x2, y2 = filter_repeats(time_surface, ppm_surface)
    ppms_range.append(ppm_surface)
    fig.add_trace(go.Scatter(x=x2, y=y2, mode='lines', marker=dict(color=color), name=gasname))

    print(f"Gas: {gasname} | R²_Per={r2_percentile_time} | R²_Temp={r2_temp_time} | R²_Rh={r2_rh_time}")
    with open("DataReport.txt", "a") as f:
        f.write(f"Gas: {gasname} | R²_Per={r2_percentile_time} | R²_Temp={r2_temp_time} | R²_Rh={r2_rh_time}\n")

    for t_val, temp_val, rh_val, sv_val, corr_val, ppm_val, air_val in zip(time, temperature, rh, SensorValue, correction_coefficient, ppm, air):
        print(f"t={t_val:.4f}s Sensor={sv_val:.4f} Air={air_val:.4f} temp={temp_val:.4f} rh={rh_val:.4f} corr={corr_val:.4f} ppm={ppm_val:.4f}")
        with open("DataReport.txt", "a") as f:
            f.write(f"t={t_val:.4f}s Sensor={sv_val:.4f} Air={air_val:.4f} temp={temp_val:.4f} rh={rh_val:.4f} corr={corr_val:.4f} ppm={ppm_val:.4f}\n")
    print("")
    with open("DataReport.txt", "a") as f:
        f.write("\n")

    with open("EstimationReport.txt", "a") as f:
        f.write(f"Gas: {gasname} | R²_Per={r2_percentile_time} | R²_Temp={r2_temp_time} | R²_Rh={r2_rh_time}\n")

    for t_val, temp_val, rh_val, sv_val, corr_val, ppm_val, air_val in zip(time_surface, temperature_surface, rh_surface, SensorValue_surface, correction_coefficient_surface, ppm_surface, air_surface):
        print(f"t={t_val:.4f}s Sensor={sv_val:.4f} Air={air_val:.4f} temp={temp_val:.4f} rh={rh_val:.4f} corr={corr_val:.4f} ppm={ppm_val:.4f}")
        with open("EstimationReport.txt", "a") as f:
            f.write(f"t={t_val:.4f}s Sensor={sv_val:.4f} Air={air_val:.4f} temp={temp_val:.4f} rh={rh_val:.4f} corr={corr_val:.4f} ppm={ppm_val:.4f}\n")
    print("")
    with open("EstimationReport.txt", "a") as f:
        f.write("\n")
    
ppm_graph = [np.min(ppms_range), np.min(ppm_range), np.max(ppms_range), np.max(ppm_range)]
graphmin, graphmax = np.min(ppm_graph), np.max(ppm_graph)

cam1 = function(1.75, differentiation(a_temp_time, maxtime, b_temp_time))
cam2 = function(1.09375, differentiation(a_rh_time, maxtime, b_rh_time))
cam3 = function(0.088, differentiation(a_percentile_time, maxtime, b_percentile_time))

fig.update_layout(
    scene=dict(
        camera=dict(eye=dict(x=cam1, y=cam2, z=cam3)),
        xaxis_title=f"X: Temp (°C) R² = {r2_temp_time}",
        yaxis_title=f"Y: RH (%) R² = {r2_rh_time}",
        zaxis_title=f"Z: Air (ppm) R² = {r2_percentile_time}",
        xaxis=dict(range=[xmin, xmax], nticks=10, showbackground=False),
        yaxis=dict(range=[ymin, ymax], nticks=10, showbackground=False),
        zaxis=dict(range=[zmin, zmax], nticks=10, showbackground=False),
        aspectmode='cube',
        domain=dict(x=[0.01, 0.51])
    ),
    showlegend=False,
    coloraxis=dict(colorscale='Viridis'),
    template='plotly_dark',
    margin=dict(t=20, b=20, l=20, r=20),
    xaxis=dict(title='X: Time (w)', domain=[0.52, 1]),
    yaxis=dict(title='Y: SensorPpm (z)', domain=[0.07, 0.82])
)

fig.add_annotation(text="4D Slope Estimation", x=0.18, y=0.98, showarrow=False, font=dict(size=19), xref="paper", yref="paper")
fig.add_annotation(text=f"{SensorName} Air Time-based PPM Calculation", x=0.89, y=0.98, showarrow=False, font=dict(size=19), xref="paper", yref="paper")

fig.write_html(f"{SensorName}_4D_Slope_Estimation.html")
