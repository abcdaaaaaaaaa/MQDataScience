import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import warnings
warnings.filterwarnings('ignore')

def calculate_r2(y, y_pred):
    ss_res = np.sum((y - y_pred) ** 2)
    ss_tot = np.sum((y - np.mean(y)) ** 2)
    if ss_tot == 0: return 0.0
    return 1 - (ss_res / ss_tot)

def yaxb(valuea, value, valueb):
    return valuea * np.power(np.abs(value), valueb)

def gauss(x, a, b, c):
    c = max(1e-5, c)
    return a * np.exp(-(x - b)**2 / (2 * c**2))

def get_best_fit(t, y, t_surface, temp=None, temp_surface=None):
    best_r2 = -float('inf')
    best_y_surface = None
    best_model_name = "None"
    
    t = np.array(t, dtype=float)
    y = np.array(y, dtype=float)
    t_surface = np.array(t_surface, dtype=float)
    
    try:
        w = 2 * np.pi / 86400.0
        X = np.column_stack([np.ones_like(t), np.sin(w*t), np.cos(w*t)])
        coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
        y_pred = coeffs[0] + coeffs[1]*np.sin(w*t) + coeffs[2]*np.cos(w*t)
        r2 = calculate_r2(y, y_pred)
        if r2 > best_r2:
            best_r2, best_y_surface = r2, coeffs[0] + coeffs[1]*np.sin(w*t_surface) + coeffs[2]*np.cos(w*t_surface)
            best_model_name = "Sinusoidal / Harmonic Model"
    except Exception: pass

    if temp is not None and temp_surface is not None:
        try:
            temp_np = np.array(temp, dtype=float)
            X = np.column_stack([np.ones_like(temp_np), temp_np])
            coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
            y_pred = coeffs[0] + coeffs[1]*temp_np
            r2 = calculate_r2(y, y_pred)
            if r2 > best_r2:
                best_r2, best_y_surface = r2, coeffs[0] + coeffs[1]*np.array(temp_surface, dtype=float)
                best_model_name = "Temperature-Dependent (Inverse) Model"
        except Exception: pass

    try:
        coeffs = np.polyfit(t, y, 3)
        p = np.poly1d(coeffs)
        y_pred = p(t)
        r2 = calculate_r2(y, y_pred)
        if r2 > best_r2:
            best_r2, best_y_surface = r2, p(t_surface)
            best_model_name = "3rd Degree Polynomial Regression"
    except Exception: pass

    try:
        coeffs = np.polyfit(t, y, 4)
        p = np.poly1d(coeffs)
        y_pred = p(t)
        r2 = calculate_r2(y, y_pred)
        if r2 > best_r2:
            best_r2, best_y_surface = r2, p(t_surface)
            best_model_name = "4th Degree Polynomial Regression"
    except Exception: pass

    try:
        w = 2 * np.pi / 86400.0
        X = np.column_stack([np.ones_like(t), np.sin(w*t), np.cos(w*t), np.sin(2*w*t), np.cos(2*w*t)])
        coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
        y_pred = coeffs[0] + coeffs[1]*np.sin(w*t) + coeffs[2]*np.cos(w*t) + coeffs[3]*np.sin(2*w*t) + coeffs[4]*np.cos(2*w*t)
        r2 = calculate_r2(y, y_pred)
        if r2 > best_r2:
            best_r2, best_y_surface = r2, coeffs[0] + coeffs[1]*np.sin(w*t_surface) + coeffs[2]*np.cos(w*t_surface) + coeffs[3]*np.sin(2*w*t_surface) + coeffs[4]*np.cos(2*w*t_surface)
            best_model_name = "2nd Degree Fourier Series"
    except Exception: pass

    if temp is not None and temp_surface is not None:
        try:
            temp_np = np.array(temp, dtype=float)
            X = np.column_stack([np.ones_like(t), t, temp_np])
            coeffs, *_ = np.linalg.lstsq(X, y, rcond=None)
            y_pred = coeffs[0] + coeffs[1]*t + coeffs[2]*temp_np
            r2 = calculate_r2(y, y_pred)
            if r2 > best_r2:
                best_r2, best_y_surface = r2, coeffs[0] + coeffs[1]*t_surface + coeffs[2]*np.array(temp_surface, dtype=float)
                best_model_name = "Multi-Variable Regression (Time & Temp)"
        except Exception: pass

    try:
        spl = UnivariateSpline(t, y, s=len(t)*1.5)
        y_pred = spl(t)
        r2 = calculate_r2(y, y_pred)
        if r2 > best_r2:
            best_r2, best_y_surface = r2, spl(t_surface)
            best_model_name = "B-Spline (Piecewise Curve)"
    except Exception: pass

    try:
        mean_t = np.mean(t)
        std_t = np.std(t)
        popt, _ = curve_fit(gauss, t, y, p0=[np.max(y), mean_t, std_t], maxfev=2000)
        y_pred = gauss(t, *popt)
        r2 = calculate_r2(y, y_pred)
        if r2 > best_r2:
            best_r2, best_y_surface = r2, gauss(t_surface, *popt)
            best_model_name = "Gaussian Model"
    except Exception: pass

    try:
        popt, _ = curve_fit(lambda x, a, b: yaxb(a, x, b), t, y, maxfev=2000)
        y_pred = yaxb(popt[0], t, popt[1])
        r2 = calculate_r2(y, y_pred)
        if r2 > best_r2:
            best_r2, best_y_surface = r2, yaxb(popt[0], t_surface, popt[1])
            best_model_name = "Power Regression"
    except Exception: pass

    if best_y_surface is None or best_r2 < -100:
        best_y_surface = np.full_like(t_surface, np.mean(y))
        best_r2 = 0
        best_model_name = "Average Value (Fallback)"

    return round(best_r2, 4), best_y_surface, best_model_name
