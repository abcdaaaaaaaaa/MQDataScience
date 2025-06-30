import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go

df = pd.read_excel("Radioactive_Data.xlsx")

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
    y_pred_log = model.predict(t_masked)
    ss_res = np.sum((log_y - y_pred_log) ** 2)
    ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
    r2 = 1 - ss_res / ss_tot
    def decay_func(time):
        return N0 * np.exp(-lambda_ * time)
    return decay_func, r2

decay_usvhr, r2_usvhr = exponential_decay_regression(times, usvhr_values)
decay_avg, r2_avg = exponential_decay_regression(times, avg_values)
decay_sdCPM, r2_sdCPM = exponential_decay_regression(times, sdCPM_values)
decay_cpm, r2_cpm = exponential_decay_regression(times, cpm_count_values)

t_fine = np.linspace(min(times), max(times), 200)

fig = go.Figure()

fig.add_trace(go.Scatter(x=times, y=usvhr_values, mode='markers', name='Usv/hr Measurements', yaxis='y1'))
fig.add_trace(go.Scatter(x=t_fine, y=decay_usvhr(t_fine), mode='lines', name='Usv/hr Model', yaxis='y1'))

fig.add_trace(go.Scatter(x=times, y=avg_values, mode='markers', name='Avg Measurements', yaxis='y2'))
fig.add_trace(go.Scatter(x=t_fine, y=decay_avg(t_fine), mode='lines', name='Avg Model', yaxis='y2'))

fig.add_trace(go.Scatter(x=times, y=sdCPM_values, mode='markers', name='sdCPM Measurements', yaxis='y3'))
fig.add_trace(go.Scatter(x=t_fine, y=decay_sdCPM(t_fine), mode='lines', name='sdCPM Model', yaxis='y3'))

fig.add_trace(go.Scatter(x=times, y=cpm_count_values, mode='markers', name='CPM Count Measurements', yaxis='y4'))
fig.add_trace(go.Scatter(x=t_fine, y=decay_cpm(t_fine), mode='lines', name='CPM Count Model', yaxis='y4'))

fig.update_layout(
    title="Multidimensional Radioactive Decay Estimation",
    xaxis=dict(title='Time (w)'),
    yaxis=dict(
        title='Usv/hr',
        titlefont=dict(color='#1f77b4'),
        tickfont=dict(color='#1f77b4'),
        anchor='x',
        side='left',
        position=0.0
    ),
    yaxis2=dict(
        title='Avg (CPM)',
        titlefont=dict(color='#ff7f0e'),
        tickfont=dict(color='#ff7f0e'),
        anchor='free',
        overlaying='y',
        side='right',
        position=1.0
    ),
    yaxis3=dict(
        title='sdCPM',
        titlefont=dict(color='#2ca02c'),
        tickfont=dict(color='#2ca02c'),
        anchor='free',
        overlaying='y',
        side='left',
        position=0.15
    ),
    yaxis4=dict(
        title='CPM Count',
        titlefont=dict(color='#d62728'),
        tickfont=dict(color='#d62728'),
        anchor='free',
        overlaying='y',
        side='right',
        position=0.85
    ),
    legend=dict(x=0.5, y=1.1, orientation='h'),
    margin=dict(t=100, b=60, l=60, r=60),
    template='plotly_dark',
    autosize=True
)

fig.add_annotation(text=f"R²={r2_usvhr:.4f}", xref="paper", yref="y domain", x=0.05, y=0.95, showarrow=False, font=dict(color='#1f77b4'))
fig.add_annotation(text=f"R²={r2_avg:.4f}", xref="paper", yref="y domain", x=0.95, y=0.95, showarrow=False, font=dict(color='#ff7f0e'))
fig.add_annotation(text=f"R²={r2_sdCPM:.4f}", xref="paper", yref="y domain", x=0.05, y=0.55, showarrow=False, font=dict(color='#2ca02c'))
fig.add_annotation(text=f"R²={r2_cpm:.4f}", xref="paper", yref="y domain", x=0.95, y=0.55, showarrow=False, font=dict(color='#d62728'))

fig.write_html("Multi_RadioactiveScience.html")
print("Graph saved as 'Multi_RadioactiveScience.html'.")
