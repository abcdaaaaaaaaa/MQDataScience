import * as MQInfo from "./MQInfo.js";

let f, standard, Air, correction_coefficient, air, minair, maxair, lastppmvalue;

let SensorName, CalibrateAir, CleanAir, MinAirPpm, MaxAirPpm, gas_params;
let a_RH30, b_RH30, c_RH30, a_RH33, b_RH33, c_RH33, a_RH60, b_RH60, c_RH60, a_RH85, b_RH85, c_RH85;
let SensorRLCalRL, SensorMode, FormulaCoefficient, AirVals, AirValsEqualGasVals, CRMode, FormulaMode;

function round2(value) {
    return Math.round(value * Math.pow(10, 2)) / Math.pow(10, 2);
}

function round4(value) {
    return Math.round(value * Math.pow(10, 4)) / Math.pow(10, 4);
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

function getCorrectionCoefficient(temp, RH) {
    let TH_valuea, TH_valueb, TH_valuec;
	if (CRMode == 3) {
		if (RH <= 60) {
			TH_valuea = interpolate(RH, 30, 60, a_RH30, a_RH60);
			TH_valueb = interpolate(RH, 30, 60, b_RH30, b_RH60);
			TH_valuec = interpolate(RH, 30, 60, c_RH30, c_RH60);
		} else {
			TH_valuea = interpolate(RH, 60, 85, a_RH60, a_RH85);
			TH_valueb = interpolate(RH, 60, 85, b_RH60, b_RH85);
			TH_valuec = interpolate(RH, 60, 85, c_RH60, c_RH85);
		}
	} else {
		TH_valuea = interpolate(RH, 33, 85, a_RH33, a_RH85);
		TH_valueb = interpolate(RH, 33, 85, b_RH33, b_RH85);
		TH_valuec = interpolate(RH, 33, 85, c_RH33, c_RH85);
	}

	return TH_valuea + TH_valuec * Math.exp(TH_valueb * temp);
}

function limit(value, minlim, maxlim) {
    return Math.min(Math.max(value, minlim), maxlim);
}

function convertppm(value) {
    const convertvalue = value * FormulaCoefficient;
    return FormulaMode !== 'ppm' ? convertvalue : value;
}

function getSensorPpm(valuea, valueb, SensorValue, CorrectionCoefficientVal) {
    const SensorRatio_value = Air * SensorRLCalRL * (CalValue * (SensorValue - 1)) / (SensorValue * (CalValue - 1));
    return convertppm(inverseyaxb(valuea, SensorRatio_value / CorrectionCoefficientVal, valueb));
}

function getSensorPpm2(valuea, valueb, SensorValue) {
    const SensorRatio_value = Air * SensorRLCalRL * (CalValue * (SensorValue - 1)) / (SensorValue * (CalValue - 1));
    return convertppm(inverseyaxb(valuea, SensorRatio_value, valueb));
}

window.calculateData = function() {
    if (typeof window.total1 === 'undefined' || window.total1 === 0) return;

    switch (window.total1) {
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
        case 16: f = "MQ216"; break;
        case 17: f = "MQ303A"; break;
        case 18: f = "MQ303B"; break;
        case 19: f = "MQ306A"; break;
        case 20: f = "MQ307A"; break;
        case 21: f = "MQ309A"; break;
    }

    switch (window.total1) { 
        case 1: case 2: case 3: case 4: case 5: case 6: case 7: case 8: case 9: case 10: case 12: case 13: case 14: case 15: case 16: standard = 1; break; 
        default: standard = 0; break; 
    }

    if (MQInfo[f]) { MQInfo[f](); }

    SensorName = MQInfo.SensorName;
    CalibrateAir = MQInfo.CalibrateAir;
    CleanAir = MQInfo.CleanAir;
    MinAirPpm = MQInfo.MinAirPpm;
    MaxAirPpm = MQInfo.MaxAirPpm;
    gas_params = MQInfo.gas_params;

    try { a_RH30 = MQInfo.a_RH30; } catch (e) {}
    try { b_RH30 = MQInfo.b_RH30; } catch (e) {}
    try { c_RH30 = MQInfo.c_RH30; } catch (e) {}
    try { a_RH33 = MQInfo.a_RH33; } catch (e) {}
    try { b_RH33 = MQInfo.b_RH33; } catch (e) {}
    try { c_RH33 = MQInfo.c_RH33; } catch (e) {}
    try { a_RH60 = MQInfo.a_RH60; } catch (e) {}
    try { b_RH60 = MQInfo.b_RH60; } catch (e) {}
    try { c_RH60 = MQInfo.c_RH60; } catch (e) {}
    try { a_RH85 = MQInfo.a_RH85; } catch (e) {}
    try { b_RH85 = MQInfo.b_RH85; } catch (e) {}
    try { c_RH85 = MQInfo.c_RH85; } catch (e) {}

    SensorRLCalRL = MQInfo.SensorRLCalRL;
    SensorMode = MQInfo.SensorMode;
    FormulaCoefficient = MQInfo.FormulaCoefficient;
    AirVals = MQInfo.AirVals;
    AirValsEqualGasVals = MQInfo.AirValsEqualGasVals;
    CRMode = MQInfo.CRMode;
    FormulaMode = MQInfo.FormulaMode;

    if (SensorMode == 'Rs/Rs') { Air = 1; } else { Air = MQInfo.Air; }

    const SensorValue = round4(limit((window.total2 / (Math.pow(2, 12) - 1)), 0, 1));  // analogRead()
    const temperature = round4(limit(((window.total3 / 10) - 140), -10, 50)); // The IOT system you are using may be having problems with negative numbers.
    const rh = round4(limit(((window.total4 / 10) - 100), 0, 100)); // The IOT system you are using may be having problems with negative numbers.
    const SensorValue2 = round4(limit((window.total5 / (Math.pow(2, 12) - 1)), 0, 1)); // analogRead()

    const percentile = SensorValue * 100;
    const percentile2 = SensorValue2 * 100;

    if (standard == 1) {
        correction_coefficient = getCorrectionCoefficient(temperature, rh);
        air = Math.round(limit(exponentialInterpolate(SensorValue, 0, 1, convertppm(MinAirPpm), convertppm(MaxAirPpm)), 1, convertppm(MaxAirPpm)) * correction_coefficient);
    } else {
        if (f == "MQ131_LOW") { 
            air = round2(limit(interpolate(SensorValue, 0, 1, convertppm(MinAirPpm), convertppm(MaxAirPpm)), 0.01, convertppm(MaxAirPpm))); 
        } else { 
            air = Math.round(limit(exponentialInterpolate(SensorValue, 0, 1, convertppm(MinAirPpm), convertppm(MaxAirPpm)), 1, convertppm(MaxAirPpm))); 
        }
    }

    window.value2 = percentile;
    window.value3 = air;
    window.value11 = temperature;
    window.value12 = rh;
    window.value13 = percentile2;

    document.cookie = "value2="+percentile;
    document.cookie = "value3="+air;
    document.cookie = "value11="+temperature;
    document.cookie = "value12="+rh;
    document.cookie = "value13="+percentile2;

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
            minair = convertppm(minair);
            maxair = convertppm(maxair);
            lastppmvalue = Math.round(limit(getSensorPpm(adjusted_valuea, adjusted_valueb, SensorValue, getCorrectionCoefficient(temperature, rh)), 1, maxair * getCorrectionCoefficient(temperature, rh)));
        } else {
            globalThis.CalValue = gas.calvalue ?? interpolate(calAir, minair, maxair, 0, 1);
            minair = convertppm(minair);
            maxair = convertppm(maxair);
            if (f == "MQ131_LOW") { 
                lastppmvalue = round2(limit(getSensorPpm2(adjusted_valuea, adjusted_valueb, SensorValue), 0.01, maxair));
            } else { 
                lastppmvalue = Math.round(limit(getSensorPpm2(adjusted_valuea, adjusted_valueb, SensorValue), 1, maxair)); 
            }
        }
        globalThis[`ppmvalue${i+1}`] = lastppmvalue;
        window[`value${i+4}`] = lastppmvalue;
        document.cookie = `value${i+4}=${globalThis[`ppmvalue${i+1}`]}; path=/`;
    });
};

if (typeof window.total1 !== 'undefined') {
    window.calculateData();
}
