import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

df = pd.read_excel("Radioactive_Datas.xlsx")

times = df['Time'].to_numpy()
usvhr_values = df['Usv/hr'].to_numpy()
avg_values = df['Avg CPM'].to_numpy()
sdCPM_values = df['sdCPM'].to_numpy()
cpm_count_values = df['CPM Count'].to_numpy()

def exponential_decay_regression(t, y):
    mask = y > 0
    t_masked = t[mask].reshape(-1, 1)
    y_masked = y[mask]
    log_y = np.log(y_masked)
    model = LinearRegression()
    model.fit(t_masked, log_y)
    lambda_ = -model.coef_[0]
    ln_N0 = model.intercept_
    N0 = np.exp(ln_N0)
    def decay_func(time): return N0 * np.exp(-lambda_ * time)
    y_pred_log = model.predict(t_masked)
    ss_res = np.sum((log_y - y_pred_log) ** 2)
    ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
    r2 = 1 - ss_res / ss_tot
    return decay_func, r2

decay_usvhr, r2_usvhr = exponential_decay_regression(times, usvhr_values)
decay_avg, r2_avg = exponential_decay_regression(times, avg_values)
decay_sdCPM, r2_sdCPM = exponential_decay_regression(times, sdCPM_values)
decay_cpm, r2_cpm = exponential_decay_regression(times, cpm_count_values)

future_times = np.linspace(min(times), max(times) * 2, 400)
predicted_avg = decay_avg(future_times)
predicted_cpm = decay_cpm(future_times)
predicted_sdCPM = decay_sdCPM(future_times)
predicted_usvhr = decay_usvhr(future_times)

marker_size = np.interp(sdCPM_values, (min(sdCPM_values), max(sdCPM_values)), (4, 15))

fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=times, y=cpm_count_values, z=avg_values,
    mode='markers',
    name='Real Datas',
    marker=dict(
        size=marker_size,
        color=usvhr_values,
        colorscale='Jet',
        colorbar=dict(title='Usv/hr', thickness=15),
    ),
    hovertemplate=(
        "Time: %{x}<br>"
        "CPM Count: %{y}<br>"
        "Avg CPM: %{z}<br>"
        "sdCPM: %{marker.size:.2f}<br>"
        "Usv/hr: %{marker.color:.4f}<br>"
        "Type: Real Datas"
    )
))

fig.add_trace(go.Scatter3d(
    x=future_times, y=predicted_cpm, z=predicted_avg,
    mode='lines',
    name='Estimation Curves',
    line=dict(
        color=predicted_usvhr,
        colorscale='Jet',
        width=5
    ),
    hovertemplate=(
        "Time: %{x}<br>"
        "CPM Count: %{y:.2f}<br>"
        "Avg CPM: %{z:.2f}<br>"
        "Usv/hr: %{line.color:.4f}<br>"
        "Type: Estimation Curves"
    )
))


fig.update_layout(
    title=dict(
        text="Multidimensional Radioactive Decay Estimation",
    ),
    scene=dict(
        camera=dict(eye=dict(x=1.6, y=1.6, z=0.8)),
        xaxis_title='X: Time (w)',
        yaxis_title='Y: CPM Count',
        zaxis_title='Z: Avg CPM'
    ),
    margin=dict(t=50, b=50, l=50, r=50),
    template='plotly_dark',
    legend=dict(
        x=0.01,
        y=0.95,
        bgcolor='rgba(0,0,0,0.5)',
        bordercolor='white',
        borderwidth=1,
        font=dict(size=12),
    ),
    annotations=[
        dict(
            text=(
                f" R² Usv/hr = {r2_usvhr:.4f}<br>"
                f" R² Avg = {r2_avg:.4f}<br>"
                f" R² sdCPM = {r2_sdCPM:.4f}<br>"
                f" R² CPM Count = {r2_cpm:.4f} "
            ),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0.01,
            y=0.80,
            align='left',
            font=dict(size=12),
            bordercolor='white',
            borderwidth=1,
            bgcolor='black',
        ),
    ]
)

fig.write_html("RadioactiveScience.html", include_plotlyjs='cdn', full_html=True, auto_open=False)

print("Graph successfully saved as 'RadioactiveScience.html'.")
