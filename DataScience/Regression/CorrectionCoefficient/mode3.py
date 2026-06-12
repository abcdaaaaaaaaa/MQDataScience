import numpy as np
from scipy.optimize import curve_fit
import plotly.graph_objects as go
from plotly.subplots import make_subplots

x_values = np.arange(-10, 55, 5, dtype=float)

MQ = input("Please define the sensor name: ")
input_values = input("Enter Y values: (RH30: y1,y2,y3,y4 ... y13), (RH60: ...), (RH85: ...): ")

input_values = input_values.strip('[]')
rh_values = input_values.split('), (')

y_values_RH30 = np.array([float(val) for val in rh_values[0].replace('(', '').replace(')', '').split(',')])
y_values_RH60 = np.array([float(val) for val in rh_values[1].replace('(', '').replace(')', '').split(',')])
y_values_RH85 = np.array([float(val) for val in rh_values[2].replace('(', '').replace(')', '').split(',')])

def model(x, a, b, c): return a + c * np.exp(b * x)

def get_initial_guess(y):
	a0 = y[-1]
	c0 = y[0] - y[-1]
	b0 = -0.01 if y[-1] < y[0] else 0.01
	return (a0, b0, c0)

popt_RH30, _ = curve_fit(model, x_values, y_values_RH30, p0=get_initial_guess(y_values_RH30), maxfev=100000)
popt_RH60, _ = curve_fit(model, x_values, y_values_RH60, p0=get_initial_guess(y_values_RH60), maxfev=100000)
popt_RH85, _ = curve_fit(model, x_values, y_values_RH85, p0=get_initial_guess(y_values_RH85), maxfev=100000)

a_RH30, b_RH30, c_RH30 = popt_RH30
a_RH60, b_RH60, c_RH60 = popt_RH60
a_RH85, b_RH85, c_RH85 = popt_RH85

def calculate_r_squared(y_true, y_pred):
	residual_sum_of_squares = np.sum((y_true - y_pred) ** 2)
	total_sum_of_squares = np.sum((y_true - np.mean(y_true)) ** 2)
	return 1 - (residual_sum_of_squares / total_sum_of_squares)

R_squared_RH30 = calculate_r_squared(y_values_RH30, model(x_values, *popt_RH30))
R_squared_RH60 = calculate_r_squared(y_values_RH60, model(x_values, *popt_RH60))
R_squared_RH85 = calculate_r_squared(y_values_RH85, model(x_values, *popt_RH85))

new_x_values = np.linspace(min(x_values), max(x_values), 1000)
y_pred_RH30_full = model(new_x_values, a_RH30, b_RH30, c_RH30)
y_pred_RH60_full = model(new_x_values, a_RH60, b_RH60, c_RH60)
y_pred_RH85_full = model(new_x_values, a_RH85, b_RH85, c_RH85)

RH_vals = np.linspace(30, 85, 100)
temp_vals = np.linspace(-10, 50, 100)
temp_grid, RH_grid = np.meshgrid(temp_vals, RH_vals)

def interpolate(value, min_value, max_value, target_min, target_max):
	return target_min + (value - min_value) * (target_max - target_min) / (max_value - min_value)

def CorrectionCoefficient(RH, temp):
	values = []
	for i in range(RH.shape[0]):
		for j in range(RH.shape[1]):
			rh = RH[i, j]
			t = temp[i, j]

			if rh <= 60:
				range_h = 30, 60
				a_pair = a_RH30, a_RH60
				b_pair = b_RH30, b_RH60
				c_pair = c_RH30, c_RH60
			else:
				range_h = 60, 85
				a_pair = a_RH60, a_RH85
				b_pair = b_RH60, b_RH85
				c_pair = c_RH60, c_RH85

			valuea = interpolate(rh, *range_h, *a_pair)
			valueb = interpolate(rh, *range_h, *b_pair)
			valuec = interpolate(rh, *range_h, *c_pair)

			result = valuea + valuec * np.exp(valueb * t)
			values.append(result)

	return np.array(values).reshape(RH.shape)

ratio_grid = CorrectionCoefficient(RH_grid, temp_grid)

color_RH30 = '#10AEFD'
color_RH60 = '#FF5CCD'
color_RH85 = '#FFA500'

fig = make_subplots(
	rows=1, cols=2,
	column_widths=[0.5, 0.5],
	specs=[[{"type": "scatter"}, {"type": "surface"}]],
	subplot_titles=(f"Regression and {MQ} Ratio Analysis for RH30, RH60, RH85", "2D Surface Graphics")
)

fig.add_trace(go.Scatter(x=x_values, y=y_values_RH30, mode='markers', marker=dict(color=color_RH30), name='Real Datas for RH30'))
fig.add_trace(go.Scatter(x=new_x_values, y=y_pred_RH30_full, mode='lines', line=dict(color=color_RH30), name=f'RH30: y={a_RH30:.4f}+{c_RH30:.4f}e^({b_RH30:.4f}t) (R²={R_squared_RH30:.4f})'))

fig.add_trace(go.Scatter(x=x_values, y=y_values_RH60, mode='markers', marker=dict(color=color_RH60), name='Real Datas for RH60'))
fig.add_trace(go.Scatter(x=new_x_values, y=y_pred_RH60_full, mode='lines', line=dict(color=color_RH60), name=f'RH60: y={a_RH60:.4f}+{c_RH60:.4f}e^({b_RH60:.4f}t) (R²={R_squared_RH60:.4f})'))

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

print(f"\nRH30: a={a_RH30:.4f}, b={b_RH30:.4f}, c={c_RH30:.4f}, R²={R_squared_RH30:.4f}")
print(f"RH60: a={a_RH60:.4f}, b={b_RH60:.4f}, c={c_RH60:.4f}, R²={R_squared_RH60:.4f}")
print(f"RH85: a={a_RH85:.4f}, b={b_RH85:.4f}, c={c_RH85:.4f}, R²={R_squared_RH85:.4f}")

fig.write_html(f"{MQ}_dht_surface.html")
