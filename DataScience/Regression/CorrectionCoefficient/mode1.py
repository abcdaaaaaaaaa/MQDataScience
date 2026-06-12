import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go
from plotly.subplots import make_subplots

x_values = np.array([-10, 5, 20, 50], dtype=float)

MQ = input("Please define the sensor name: ")
input_values = input("Enter the Y (Rs/Ro) values: (RH33: y1,y2,y3,y4), (RH85: y1,y2,y3,y4): ")

input_values = input_values.strip('[]')
rh_values = input_values.split('), (')

y_values_RH33 = np.array([float(val) for val in rh_values[0].replace('(', '').replace(')', '').split(',')])
y_values_RH85 = np.array([float(val) for val in rh_values[1].replace('(', '').replace(')', '').split(',')])

def model(x, a, b, c): return a + c * np.exp(b * x)

def get_initial_guess(y):
	a0 = y[-1]
	c0 = y[0] - y[-1]
	b0 = -0.01 if y[-1] < y[0] else 0.01
	return (a0, b0, c0)

popt_RH33, _ = curve_fit(model, x_values, y_values_RH33, p0=get_initial_guess(y_values_RH33), maxfev=100000)
popt_RH85, _ = curve_fit(model, x_values, y_values_RH85, p0=get_initial_guess(y_values_RH85), maxfev=100000)

a_RH33, b_RH33, c_RH33 = popt_RH33
a_RH85, b_RH85, c_RH85 = popt_RH85

def calculate_r_squared(y_true, y_pred):
	residual_sum_of_squares = np.sum((y_true - y_pred) ** 2)
	total_sum_of_squares = np.sum((y_true - np.mean(y_true)) ** 2)
	return 1 - (residual_sum_of_squares / total_sum_of_squares)

R_squared_RH33 = calculate_r_squared(y_values_RH33, model(x_values, *popt_RH33))
R_squared_RH85 = calculate_r_squared(y_values_RH85, model(x_values, *popt_RH85))

new_x_values = np.linspace(min(x_values), max(x_values), 1000)
y_pred_RH33_full = model(new_x_values, a_RH33, b_RH33, c_RH33)
y_pred_RH85_full = model(new_x_values, a_RH85, b_RH85, c_RH85)

RH_vals = np.linspace(33, 85, 100)
temp_vals = np.linspace(-10, 50, 100)
temp_grid, RH_grid = np.meshgrid(temp_vals, RH_vals)

def interpolate(value, min_value, max_value, target_min, target_max):
    return target_min + (value - min_value) * (target_max - target_min) / (max_value - min_value)

def CorrectionCoefficient(RH, temp):
	valuea = interpolate(RH, 33, 85, a_RH33, a_RH85)
	valueb = interpolate(RH, 33, 85, b_RH33, b_RH85)
	valuec = interpolate(RH, 33, 85, c_RH33, c_RH85)
	return valuea + valuec * np.exp(valueb * temp)

ratio_grid = CorrectionCoefficient(RH_grid, temp_grid)

color_RH33 = '#10AEFD'
color_RH85 = '#FFA500'

fig = make_subplots(
	rows=1, cols=2,
	column_widths=[0.5, 0.5],
	specs=[[{"type": "scatter"}, {"type": "surface"}]],
	subplot_titles=(f"Regression and {MQ} (Rs/Ro) Analysis for RH33 and RH85", "2D Surface Graphics")
)

fig.add_trace(go.Scatter(x=x_values, y=y_values_RH33, mode='markers', marker=dict(color=color_RH33), name='Real Datas for RH33'))
fig.add_trace(go.Scatter(x=new_x_values, y=y_pred_RH33_full, mode='lines', line=dict(color=color_RH33), name=f'RH33: y={a_RH33:.4f}+{c_RH33:.4f}e^({b_RH33:.4f}t) (R²={R_squared_RH33:.4f})'))

fig.add_trace(go.Scatter(x=x_values, y=y_values_RH85, mode='markers', marker=dict(color=color_RH85), name='Real Datas for RH85'))
fig.add_trace(go.Scatter(x=new_x_values, y=y_pred_RH85_full, mode='lines', line=dict(color=color_RH85), name=f'RH85: y={a_RH85:.4f}+{c_RH85:.4f}e^({b_RH85:.4f}t) (R²={R_squared_RH85:.4f})'))

fig.add_trace(go.Surface(x=temp_grid, y=RH_grid, z=ratio_grid, colorscale='Viridis', showscale=True, hoverinfo='x+y+z', colorbar=dict(thickness=15, len=0.75, y=0.5, yanchor="middle")))

fig.update_layout(
	template='plotly_dark',
	autosize=True,
	scene=dict(
		camera=dict(eye=dict(x=0, y=-2, z=0.088)),
		xaxis=dict(title="Temperature (°C)"),
		yaxis=dict(title="Humidity RH"),
		zaxis=dict(title="CorrectionCoefficient")
	),
	showlegend=True,
	margin=dict(l=70, r=70, t=70, b=70)
)

fig.update_xaxes(title_text="Temperature (°C)")
fig.update_yaxes(title_text="Rs/Ro")

print(f"\nRH33: a={a_RH33:.4f}, b={b_RH33:.4f}, c={c_RH33:.4f}, R²={R_squared_RH33:.4f}")
print(f"RH85: a={a_RH85:.4f}, b={b_RH85:.4f}, c={c_RH85:.4f}, R²={R_squared_RH85:.4f}")

fig.write_html(f"{MQ}_dht_surface.html")
