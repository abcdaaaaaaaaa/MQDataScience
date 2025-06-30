import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.graph_objects as go
from plotly.subplots import make_subplots

df = pd.read_excel("Radioactive_Datas.xlsx")

times = df['Time'].to_numpy()
usvhr_values = df['Usv/hr'].to_numpy()
avg_values = df['Avg CPM'].to_numpy()
sdCPM_values = df['sdCPM'].to_numpy()
cpm_count_values = df['CPM Count'].to_numpy()

data_dict = {
    "Usv/hr": usvhr_values,
    "Avg": avg_values,
    "sdCPM": sdCPM_values,
    "CPM Count": cpm_count_values
}

def exponential_decay_regression(t, y):
    mask = y > 0
    t = t[mask].reshape(-1, 1)
    y = y[mask]
    log_y = np.log(y)
    model = LinearRegression()
    model.fit(t, log_y)
    lambda_ = -model.coef_[0]
    ln_N0 = model.intercept_
    N0 = np.exp(ln_N0)
    y_pred_log = model.predict(t)
    ss_res = np.sum((log_y - y_pred_log) ** 2)
    ss_tot = np.sum((log_y - np.mean(log_y)) ** 2)
    r2 = 1 - ss_res / ss_tot
    def decay_func(time): return N0 * np.exp(-lambda_ * time)
    return lambda_, N0, decay_func, model, r2

results_single = {}
for label, data in data_dict.items():
    lam, N0, decay_f, model, r2 = exponential_decay_regression(times, data)
    results_single[label] = (lam, N0, decay_f, r2)

y_multi = avg_values
mask = y_multi > 0
log_y_multi = np.log(y_multi[mask])
X_multi = np.vstack([
    times[mask],
    np.log(usvhr_values[mask]),
    np.log(sdCPM_values[mask]),
    np.log(cpm_count_values[mask])
]).T

multi_model = LinearRegression()
multi_model.fit(X_multi, log_y_multi)

def multi_decay(t, usvhr, sdCPM, cpm_count):
    X = np.array([t, np.log(usvhr), np.log(sdCPM), np.log(cpm_count)]).reshape(1, -1)
    log_pred = multi_model.predict(X)[0]
    return np.exp(log_pred)

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=["Usv/hr", "Avg", "sdCPM", "CPM Count"],
    vertical_spacing=0.15,
    horizontal_spacing=0.1
)

t_fine = np.linspace(min(times), max(times), 200)

colors = {
    "Usv/hr": "#636EFA",
    "Avg": "#EF553B",
    "sdCPM": "#00CC96",
    "CPM Count": "#AB63FA",
    "Multi": "#FFA15A"
}

for i, (label, (lam, N0, decay_f, r2)) in enumerate(results_single.items(), start=1):
    row = 1 if i <= 2 else 2
    col = i if i <= 2 else i - 2

    fig.add_trace(go.Scatter(
        x=times,
        y=data_dict[label],
        mode='markers',
        marker=dict(color=colors[label]),
        name=f"{label} Measurements",
        showlegend=(i==1)
    ), row=row, col=col)

    fig.add_trace(go.Scatter(
        x=t_fine,
        y=decay_f(t_fine),
        mode='lines',
        line=dict(color=colors[label]),
        name=f"{label} Exponential Model",
        showlegend=False
    ), row=row, col=col)

    fig.add_annotation(
        text=f"R² = {r2:.4f}",
        xref="x domain", yref="y domain",
        x=0.95, y=0.95,
        showarrow=False,
        row=row, col=col,
        font=dict(size=12, color=colors[label])
    )

avg_usvhr = np.mean(usvhr_values)
avg_sdCPM = np.mean(sdCPM_values)
avg_cpm_count = np.mean(cpm_count_values)
multi_pred = [multi_decay(t, avg_usvhr, avg_sdCPM, avg_cpm_count) for t in t_fine]

fig.add_trace(go.Scatter(
    x=t_fine,
    y=multi_pred,
    mode='lines',
    line=dict(color=colors["Multi"], dash='dash'),
    name="Multivariate Model (Avg)",
    showlegend=True
), row=2, col=1)

fig.update_layout(
    title_text="Multidimensional Radioactive Decay Estimation",
    template="plotly_dark",
    legend=dict(x=0.8, y=0.95)
)

fig.update_xaxes(title_text="Time (w)", row=1, col=1)
fig.update_xaxes(title_text="Time (w)", row=1, col=2)
fig.update_xaxes(title_text="Time (w)", row=2, col=1)
fig.update_xaxes(title_text="Time (w)", row=2, col=2)

fig.update_yaxes(title_text="Usv/hr", row=1, col=1)
fig.update_yaxes(title_text="Avg (CPM)", row=1, col=2)
fig.update_yaxes(title_text="sdCPM", row=2, col=1)
fig.update_yaxes(title_text="CPM Count", row=2, col=2)

fig.write_html("2D_RadioactiveScience.html")
print("Graph saved as '2D_RadioactiveScience.html'.")
