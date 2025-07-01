import * as MQInfo from "./MQInfo.js";

let f, standard, Air, scaledTemperature, correction_coefficient, air, minair, maxair, lastppmvalue;

switch (data1) {
    case 1: f = "MQ135"; break;
    case 2: f = "MQ2"; break;
    case 3: f = "MQ3"; break;
    case 4: f = "MQ4"; break;
    case 5: f = "MQ5"; break;
    case 6: f = "MQ6"; break;
    case 7: f = "MQ7"; break;
    case 8: f = "MQ8"; break;
    case 9: f = "MQ9"; break;
    case 10: f = "MQ131"; break;
    case 11: f = "MQ131_LOW"; break;
    case 12: f = "MQ136"; break;
    case 13: f = "MQ137"; break;
    case 14: f = "MQ138"; break;
    case 15: f = "MQ214"; break;
    case 16: f = "MQ303A"; break;
    case 17: f = "MQ303B"; break;
    case 18: f = "MQ307A"; break;
    case 19: f = "MQ309A"; break;
}

switch (data1) { 
    case 1: case 2: case 3: case 4: case 5: case 6: case 7: case 8: case 9: case 10: case 12: case 13: case 14: case 15: standard = 1; break; 
    default: standard = 0; break; 
}

if (MQInfo[f]) { MQInfo[f](); }

const SensorName = MQInfo.SensorName;
const CalibrateAir = MQInfo.CalibrateAir;
const CleanAir = MQInfo.CleanAir;
const MinAirPpm = MQInfo.MinAirPpm;
const MaxAirPpm = MQInfo.MaxAirPpm;
const gas_params = MQInfo.gas_params;

let a_RH30, b_RH30, a_RH33, b_RH33, a_RH60, b_RH60, a_RH85, b_RH85;

try { a_RH30 = MQInfo.a_RH30; } catch (e) {}
try { b_RH30 = MQInfo.b_RH30; } catch (e) {}
try { a_RH33 = MQInfo.a_RH33; } catch (e) {}
try { b_RH33 = MQInfo.b_RH33; } catch (e) {}
try { a_RH60 = MQInfo.a_RH60; } catch (e) {}
try { b_RH60 = MQInfo.b_RH60; } catch (e) {}
try { a_RH85 = MQInfo.a_RH85; } catch (e) {}
try { b_RH85 = MQInfo.b_RH85; } catch (e) {}

const SensorRLCalRL = MQInfo.SensorRLCalRL;
const SensorMode = MQInfo.SensorMode;
const FormulaCoefficient = MQInfo.FormulaCoefficient;
const AirVals = MQInfo.AirVals;
const AirValsEqualGasVals = MQInfo.AirValsEqualGasVals;
const CRMode = MQInfo.CRMode;
const FormulaMode = MQInfo.FormulaMode;

if (SensorMode == 'Rs/Rs') { Air = 1; } else { Air = MQInfo.Air; }

function round2(value) {
    return Math.round(value * Math.pow(10, 2)) / Math.pow(10, 2);
}

function round4(value) {
    return Math.round(value * Math.pow(10, 4)) / Math.pow(10, 4);
}

function yaxb(valuea, value, valueb) {
    return valuea * Math.pow(value, valueb);
}

function inverseyaxb(valuea, value, valueb) {
    return Math.pow(value / valuea, 1 / valueb);
}

function interpolate(value, min_value, max_value, target_min, target_max) {
    return target_min + (value - min_value) * (target_max - target_min) / (max_value - min_value);
}

function exponentialInterpolate(value, minValue, maxValue, targetMin, targetMax) {
    const logMin = Math.log10(targetMin);
    const logMax = Math.log10(targetMax);
    const ratio = (value - minValue) / (maxValue - minValue);
    const logVal = logMin + ratio * (logMax - logMin);
    return Math.pow(10, logVal);
}

function ScaleTemp(temp, mode) {
    let temp_scaled;
    if (mode === '+') {
        temp_scaled = (temp + 25) / 15;
        if (CRMode !== 1) temp_scaled = (temp + 15) / 5;
    } else if (mode === '-') {
        temp_scaled = 15 * temp - 25;
        if (CRMode !== 1) temp_scaled = 5 * temp - 15;
    }
    return temp_scaled;
}

function CorrectionCoefficient(temp, RH) {
    let TH_valuea, TH_valueb;
    if (CRMode !== 3) {
        TH_valuea = interpolate(RH, 33, 85, a_RH33, a_RH85);
        TH_valueb = interpolate(RH, 33, 85, b_RH33, b_RH85);
    } else {
        if (RH <= 60) {
	  TH_valuea = interpolate(RH, 30, 60, a_RH30, a_RH60);
	  TH_valueb = interpolate(RH, 30, 60, b_RH30, b_RH60);
        } else {
	  TH_valuea = interpolate(RH, 60, 85, a_RH60, a_RH85);
	  TH_valueb = interpolate(RH, 60, 85, b_RH60, b_RH85);
        }
    }
    return yaxb(TH_valuea, temp, TH_valueb);
}

function limit(value, minlim, maxlim) {
    return Math.min(Math.max(value, minlim), maxlim);
}

function convertppm(value) {
    const convertvalue = value * FormulaCoefficient;
    return FormulaMode !== 'ppm' ? convertvalue : value;
}

function Sensorppm(valuea, valueb, SensorValue, CorrectionCoefficient) {
    const SensorRatio_value = Air * SensorRLCalRL * (CalValue * (SensorValue - 1)) / (SensorValue * (CalValue - 1));
    return convertppm(inverseyaxb(valuea, SensorRatio_value / CorrectionCoefficient, valueb));
}

function Sensorppm2(valuea, valueb, SensorValue) {
    const SensorRatio_value = Air * SensorRLCalRL * (CalValue * (SensorValue - 1)) / (SensorValue * (CalValue - 1));
    return convertppm(inverseyaxb(valuea, SensorRatio_value, valueb));
}

const SensorValue = round4(limit((data2 / (Math.pow(2, 12) - 1)), 0, 1)); // analogRead()
const temperature = round4(limit(((data3 / 10) - 140), -10, 50)); // The IOT system you are using may be having problems with negative numbers.
const rh = round4(limit(((data4 / 10) - 100), 0, 100)); // The IOT system you are using may be having problems with negative numbers.
const SensorValue2 = round4(limit((data5 / (Math.pow(2, 12) - 1)), 0, 1)); // analogRead()

const percentile = SensorValue * 100;
const percentile2 = SensorValue2 * 100;

if (standard == 1) {
    scaledTemperature = ScaleTemp(temperature, '+');
    correction_coefficient = CorrectionCoefficient(scaledTemperature, rh);
    air = Math.round(limit(exponentialInterpolate(SensorValue, 0, 1, convertppm(MinAirPpm), convertppm(MaxAirPpm)), 1, convertppm(MaxAirPpm)) * correction_coefficient);
} else {
    if (f == "MQ131_LOW") { 
    air = round2(limit(interpolate(SensorValue, 0, 1, convertppm(MinAirPpm), convertppm(MaxAirPpm)), 0.01, convertppm(MaxAirPpm))); 
    } else { air = Math.round(limit(exponentialInterpolate(SensorValue, 0, 1, convertppm(MinAirPpm), convertppm(MaxAirPpm)), 1, convertppm(MaxAirPpm))) }
}

document.cookie = "value1="+percentile;
document.cookie = "value2="+air;
document.cookie = "value3="+temperature;
document.cookie = "value4="+rh;
document.cookie = "value5="+percentile2;

gas_params.forEach((gas, i) => {
    
    if (AirValsEqualGasVals) {
        minair = MinAirPpm;
        maxair = MaxAirPpm;
    } else {
        minair = gas.ppmvals[0];
        maxair = gas.ppmvals[1];
    }

    let { name: gasname, ppm: [valuea, valueb] } = gas;

    let adjusted_valuea = valuea, adjusted_valueb = valueb;
    if (SensorMode == 'Ro/Rs') {
        adjusted_valuea = 1 / Math.pow(valuea, 1 / valueb);
        adjusted_valueb = 1 / valueb;
    }
    
    let calAir = inverseyaxb(adjusted_valuea, CalibrateAir, adjusted_valueb);
    
    if (standard == 1) {
        globalThis.CalValue = limit(interpolate(calAir, minair, maxair, 0, 1), 0.01, 0.99);
        minair = convertppm(minair)
        maxair = convertppm(maxair);
        lastppmvalue = Math.round(limit(Sensorppm(adjusted_valuea, adjusted_valueb, SensorValue, CorrectionCoefficient(scaledTemperature, rh)), 1, yaxb(adjusted_valuea, maxair, adjusted_valueb) * CorrectionCoefficient(scaledTemperature, rh)));
    } else {
        globalThis.CalValue = gas.calvalue ?? interpolate(calAir, minair, maxair, 0, 1);
        minair = convertppm(minair)
        maxair = convertppm(maxair);
        if (f == "MQ131_LOW") { 
            lastppmvalue = round2(limit(Sensorppm2(adjusted_valuea, adjusted_valueb, SensorValue), 0.01, yaxb(adjusted_valuea, maxair, adjusted_valueb) * CorrectionCoefficient(scaledTemperature, rh)));
        } else { lastppmvalue = Math.round(limit(Sensorppm2(adjusted_valuea, adjusted_valueb, SensorValue), 1, yaxb(adjusted_valuea, maxair, adjusted_valueb) * CorrectionCoefficient(scaledTemperature, rh))) }
    }
    
    globalThis[`ppmvalue${i+1}`] = lastppmvalue;
    document.cookie = `value${i+6}=${globalThis[`ppmvalue${i+1}`]}`;

});
