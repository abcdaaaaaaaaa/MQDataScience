import numpy as np
from scipy.optimize import curve_fit
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

def vals(minval, maxval, count):
    return np.linspace(minval, maxval, count)

def limit(value, minlim, maxlim):
    return np.clip(value, minlim, maxlim)

def convertppm(value):
    convertvalue = value * FormulaCoefficient if FormulaMode != 'ppm' else value
    return convertvalue

def Sensorppm(valuea, valueb, SensorValue, CorrectionCoefficient):
    SensorRatio_value = Air * SensorRLCalRL * (CalValue * (SensorValue - 1)) / (SensorValue * (CalValue - 1))
    return convertppm(inverseyaxb(valuea, SensorRatio_value / CorrectionCoefficient, valueb))

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

    
    ppm = limit(Sensorppm(valuea, valueb, SensorValue, correction_coefficient), 0, maxair * correction_coefficient)
    ppm_surface = limit(Sensorppm(valuea, valueb, SensorValue_surface, correction_coefficient_surface), 0, maxair * correction_coefficient_surface)

    print(f"Gas: {gasname} | R²_Per={r2_percentile_time} | R²_Temp={r2_temp_time} | R²_Rh={r2_rh_time}")
    for t_val, temp_val, rh_val, sv_val, corr_val, ppm_val, air_val in zip(time, temperature, rh, SensorValue, correction_coefficient, ppm, air):
        print(f"t={t_val:.4f}s Sensor={sv_val:.4f} Air={air_val:.4f} temp={temp_val:.4f} rh={rh_val:.4f} corr={corr_val:.4f} ppm={ppm_val:.4f}")
    print("")
    
    for t_val, temp_val, rh_val, sv_val, corr_val, ppm_val, air_val in zip(time_surface, temperature_surface, rh_surface, SensorValue_surface, correction_coefficient_surface, ppm_surface, air_surface):
        print(f"t={t_val:.4f}s Sensor={sv_val:.4f} Air={air_val:.4f} temp={temp_val:.4f} rh={rh_val:.4f} corr={corr_val:.4f} ppm={ppm_val:.4f}")
    print("")


