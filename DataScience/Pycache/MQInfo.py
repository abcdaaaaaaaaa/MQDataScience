CleanAir = 1
SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH30, b_RH30, a_RH60, b_RH60, a_RH85, b_RH85, SensorRLCalRL, SensorMode, FormulaCoefficient, AirVals, AirValsEqualGasVals, CRMode, FormulaMode = [None] * 19

def MQ2():
    global SensorName, Air, CalibrateAir, SensorRLCalRL, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-2'
    Air = 9.8
    CalibrateAir = 0.78
    SensorRLCalRL = 0.25
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'LPG', 'ppm': (17.6135, -0.4539)},
        {'name': 'propane', 'ppm': (19.5575, -0.461)},
        {'name': 'H2', 'ppm': (25.7473, -0.4731)},
        {'name': 'alcohol', 'ppm': (19.2641, -0.3604)},
        {'name': 'CH4', 'ppm': (20.7074, -0.36)},
        {'name': 'smoke', 'ppm': (26.4698, -0.3876)},
        {'name': 'CO', 'ppm': (28.024, -0.3182)}
    ]
    a_RH33 = 1.6867
    b_RH33 = -0.4263
    a_RH85 = 1.5291
    b_RH85 = -0.422
    group1_subgroup3()

def MQ3():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-3'
    Air = 60.53
    MinAirPpm, MaxAirPpm = 0.103, 10 # 5.15 500 ppm
    gas_params = [
        {'name': 'Alcohol', 'ppm': (0.5565, -0.6333)},
        {'name': 'Benzene', 'ppm': (1.7957, -0.369)},
        {'name': 'Hexane', 'ppm': (22.9337, -0.358)},
        {'name': 'LPG', 'ppm': (27.8286, -0.2847)},
        {'name': 'CO', 'ppm': (31.9559, -0.2325)},
        {'name': 'CH4', 'ppm': (44.8389, -0.0476)}
    ]
    a_RH33 = 1.6671
    b_RH33 = -0.2467
    a_RH85 = 1.4112
    b_RH85 = -0.2257
    group1_subgroup6()

def MQ4():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-4'
    Air = 4.4
    CalibrateAir = 1.28
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'CH4', 'ppm': (11.5517, -0.3541)},
        {'name': 'LPG', 'ppm': (14.1866, -0.3227)},
        {'name': 'H2', 'ppm': (9.6432, -0.1765)},
        {'name': 'smoke', 'ppm': (7.05, -0.1065)},
        {'name': 'alcohol', 'ppm': (5.7994, -0.0696)},
        {'name': 'CO', 'ppm': (5.49, -0.0495)}
    ]
    a_RH33 = 1.2767
    b_RH33 = -0.2204
    a_RH85 = 1.1013
    b_RH85 = -0.2482
    group1_subgroup2()
    
def MQ5():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-5'
    Air = 6.5
    CleanAir = 0.983
    CalibrateAir = CleanAir
    CleanAir = 1
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'LPG', 'ppm': (6.1067, -0.4102)},
        {'name': 'CH4', 'ppm': (6.987, -0.3777)},
        {'name': 'H2', 'ppm': (7.4265, -0.2847)},
        {'name': 'alcohol', 'ppm': (10.8274, -0.2104)},
        {'name': 'CO', 'ppm': (8.2236, -0.1492)}
    ]
    a_RH33 = 1.3645
    b_RH33 = -0.2977
    a_RH85 = 1.1315
    b_RH85 = -0.2874
    group1_subgroup2()

def MQ6():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-6'
    Air = 10
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'LPG', 'ppm': (20.3079, -0.4349)},
        {'name': 'CH4', 'ppm': (22.011, -0.4029)},
        {'name': 'H2', 'ppm': (26.9497, -0.2956)},
        {'name': 'Alcohol', 'ppm': (19.3261, -0.1655)},
        {'name': 'CO', 'ppm': (13.4917, -0.0777)}
    ]
    a_RH33 = 1.3128
    b_RH33 = -0.2428
    a_RH85 = 1.1252
    b_RH85 = -0.2496
    group1_subgroup1()

def MQ7():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-7'
    Air = 26
    CalibrateAir = 0.6436
    MinAirPpm, MaxAirPpm = 50, 4000
    gas_params = [
        {'name': 'H2', 'ppm': (21.1794, -0.7174)},
        {'name': 'CO', 'ppm': (20.89, -0.6568)},
        {'name': 'LPG', 'ppm': (14.9745, -0.1329)},
        {'name': 'CH4', 'ppm': (19.8094, -0.09)},
        {'name': 'Alcohol', 'ppm': (20.2524, -0.0655)}
    ]
    a_RH33 = 1.4296
    b_RH33 = -0.3238
    a_RH85 = 1.1733
    b_RH85 = -0.2842
    group1_subgroup2()

def MQ8():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-8'
    Air = 70
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'H2', 'ppm': (18391.5667, -1.4494)},
        {'name': 'alcohol', 'ppm': (468.8045, -0.5574)},
        {'name': 'LPG', 'ppm': (152.1255, -0.2922)},
        {'name': 'CH4', 'ppm': (117.9639, -0.1448)},
        {'name': 'CO', 'ppm': (126.605, -0.1173)}
    ]
    a_RH33 = 1.1474
    b_RH33 = -0.1958
    a_RH85 = 1.0783
    b_RH85 = -0.1824
    group1_subgroup1()

def MQ9():
    global SensorName, Air, CalibrateAir, SensorRLCalRL, MinAirPpm, MaxAirPpm, gas_params, a_RH30, b_RH30, a_RH60, b_RH60, a_RH85, b_RH85
    SensorName = 'MQ-9'
    Air = 9.7
    SensorRLCalRL = 0.5
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'CO', 'ppmvals': (MinAirPpm, 1000), 'ppm': (16.8797, -0.4445)},
        {'name': 'LPG', 'ppmvals': (MinAirPpm, MaxAirPpm), 'ppm': (24.918, -0.4695)},
        {'name': 'CH4', 'ppmvals': (MinAirPpm, MaxAirPpm), 'ppm': (21.8247, -0.3663)}
    ]
    """
    a_RH33 = 1.4292
    b_RH33 = -0.3206
    a_RH85 = 1.1735
    b_RH85 = -0.2801
    """
    a_RH30 = 1.876
    b_RH30 = -0.2284
    a_RH60 = 1.5885
    b_RH60 = -0.2271
    a_RH85 = 1.3842
    b_RH85 = -0.2282
    group1_subgroup5()

def MQ131():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH30, b_RH30, a_RH60, b_RH60, a_RH85, b_RH85
    SensorName = 'MQ131'
    Air = 12
    MinAirPpm, MaxAirPpm = 5, 100
    gas_params = [
        {'name': 'O3', 'ppm': (16.0871, -0.8603)},
        {'name': 'CL2', 'ppm': (18.9693, -0.7132)},
        {'name': 'NOx', 'ppm': (16.7059, -0.4684)}
    ]
    a_RH30 = 1.876
    b_RH30 = -0.2284
    a_RH60 = 1.5885
    b_RH60 = -0.2271
    a_RH85 = 1.3842
    b_RH85 = -0.2282
    group3_subgroup1()

def MQ131_LOW():
    global SensorName, Air, CalibrateAir, SensorRLCalRL, MinAirPpm, MaxAirPpm, gas_params
    SensorName = 'MQ-131_LOW'
    Air = 12
    CalibrateAir = 0.5
    SensorRLCalRL = 0.2
    MinAirPpm, MaxAirPpm = 5, 100 # 0.1, 2 ppm
    gas_params = [
        {'name': 'O3', 'ppm': (16.0871, -0.8603)},
        {'name': 'CL2', 'ppm': (18.9693, -0.7132)},
        {'name': 'NOx', 'ppm': (16.7059, -0.4684)}
    ]
    group3_subgroup2()
    
def MQ135():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-135'
    Air = 3.6
    MinAirPpm, MaxAirPpm = 10, 200
    gas_params = [
        {'name': 'Acetone', 'ppm': (2.7988, -0.2913)},
        {'name': 'Toluene', 'ppm': (2.9788, -0.2892)},
        {'name': 'Alcohol', 'ppm': (3.8623, -0.3126)},
        {'name': 'CO2', 'ppm': (5.2278, -0.3585)},
        {'name': 'NH4', 'ppm': (6.2968, -0.3892)},
        {'name': 'CO', 'ppm': (5.0533, -0.2541)}
    ]
    a_RH33 = 1.6867
    b_RH33 = -0.4263
    a_RH85 = 1.5291
    b_RH85 = -0.422
    group1_subgroup1()

def MQ136():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-136'    
    Air = 3.54
    CleanAir = 1.44
    CalibrateAir = CleanAir
    CleanAir = 1
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'H2S', 'ppm': (17.6135, -0.4539)},
        {'name': 'NH4', 'ppm': (19.5575, -0.461)},
        {'name': 'CO', 'ppm': (28.024, -0.3182)}
    ]
    a_RH33 = 1.6867
    b_RH33 = -0.4263
    a_RH85 = 1.5291
    b_RH85 = -0.422
    group1_subgroup2()

def MQ137():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-137'    
    Air = 3.54
    CleanAir = 1.44
    CalibrateAir = CleanAir
    CleanAir = 1
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'CO', 'ppm': (17.6135, -0.4539)},
        {'name': 'Ethanol', 'ppm': (19.5575, -0.461)},
        {'name': 'NH3', 'ppm': (28.024, -0.3182)}
    ]
    a_RH33 = 1.6867
    b_RH33 = -0.4263
    a_RH85 = 1.5291
    b_RH85 = -0.422
    group1_subgroup2()

def MQ138():
    global SensorName, Air, CalibrateAir, SensorRLCalRL, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-138'
    Air = 9.8
    CalibrateAir = 2.914
    SensorRLCalRL = 20/47
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'n-Hexane', 'ppm': (17.6135, -0.4539)},
        {'name': 'propane', 'ppm': (19.5575, -0.461)},
        {'name': 'Benzene', 'ppm': (25.7473, -0.4731)},
        {'name': 'alcohol', 'ppm': (19.2641, -0.3604)},
        {'name': 'CH4', 'ppm': (20.7074, -0.36)},
        {'name': 'smoke', 'ppm': (26.4698, -0.3876)},
        {'name': 'CO', 'ppm': (28.024, -0.3182)}
    ]
    a_RH33 = 1.6867
    b_RH33 = -0.4263
    a_RH85 = 1.5291
    b_RH85 = -0.422
    group1_subgroup3()

def MQ214():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-214'
    Air = 595.18
    CleanAir = 105.554
    CalibrateAir = CleanAir
    CleanAir = 1
    MinAirPpm, MaxAirPpm = 1000, 20000
    gas_params = [{'name': 'CH4', 'ppmvals': (3000, MaxAirPpm), 'ppm': (2669.39, -0.3784)}]
    a_RH33 = 1.6867
    b_RH33 = -0.4263
    a_RH85 = 1.5291
    b_RH85 = -0.422
    group1_subgroup4()

def MQ216():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params, a_RH33, b_RH33, a_RH85, b_RH85
    SensorName = 'MQ-216'
    Air = 9.8
    MinAirPpm, MaxAirPpm = 200, 10000
    gas_params = [
        {'name': 'LPG', 'ppm': (17.6135, -0.4539)},
        {'name': 'propane', 'ppm': (19.5575, -0.461)},
        {'name': 'i-butane', 'ppm': (25.7473, -0.4731)},
        {'name': 'alcohol', 'ppm': (19.2641, -0.3604)},
        {'name': 'CH4', 'ppm': (20.7074, -0.36)}
    ]
    a_RH33 = 1.6867
    b_RH33 = -0.4263
    a_RH85 = 1.5291
    b_RH85 = -0.422
    group1_subgroup1()

def MQ303A():
    global SensorName, Air, CalibrateAir, SensorRLCalRL, MinAirPpm, MaxAirPpm, gas_params
    SensorName = 'MQ303A'
    Air = CleanAir
    CalibrateAir = 0.27
    SensorRLCalRL = 47/50
    MinAirPpm, MaxAirPpm = 1.2, 3.45
    gas_params = [
        {'name': 'Hydrogen', 'ppmvals': (10, 10000), 'ppm': (1.7955, -0.3767)},
        {'name': 'Ethanol', 'ppmvals': (10, 10000), 'ppm': (1.7007, -0.4214)},
        {'name': 'IsoButane', 'ppmvals': (100, 10000), 'ppm': (1.8622, -0.3374)}
    ]
    group2_subgroup3()

def MQ303B():
    global SensorName, Air, CalibrateAir, MinAirPpm, MaxAirPpm, gas_params
    SensorName = 'MQ303B'
    Air = CleanAir
    CalibrateAir = 0.258
    MinAirPpm, MaxAirPpm = 1.2, 3.45
    gas_params = [
        {'name': 'Hydrogen', 'ppmvals': (10, 10000), 'ppm': (1.7955, -0.3767)},
        {'name': 'Ethanol', 'ppmvals': (10, 10000), 'ppm': (1.7007, -0.4214)},
        {'name': 'IsoButane', 'ppmvals': (100, 10000), 'ppm': (1.8622, -0.3374)}
    ]
    group2_subgroup1()

def MQ306A():
    global SensorName, Air, CalibrateAir, SensorRLCalRL, MinAirPpm, MaxAirPpm, gas_params
    SensorName = 'MQ306A'
    Air = 1.66
    CalibrateAir = 0.1
    SensorRLCalRL = 0.2;
    MinAirPpm, MaxAirPpm = 15, 30
    gas_params = [
        {'name': 'Hydrogen', 'ppmvals': (10, 10000), 'ppm': (1.7955, -0.3767)},
        {'name': 'Ethanol', 'ppmvals': (10, 10000), 'ppm': (1.7007, -0.4214)},
        {'name': 'IsoButane', 'ppmvals': (100, 10000), 'ppm': (1.8622, -0.3374)}
    ]
    group2_subgroup3()
    
def MQ307A():
    global SensorName, Air, CalibrateAir, SensorRLCalRL, MinAirPpm, MaxAirPpm, gas_params
    SensorName = 'MQ307A'
    Air, MinAirPpm, MaxAirPpm = None, None, None
    SensorRLCalRL = 0.02
    gas_params = [
        {'name': 'CO', 'ppmvals': (30, 1000), 'ppm': (2336.2698, -1.7255)},
        {'name': 'H2', 'ppmvals': (1000, 3000), 'ppm': (25051.8177, -0.8318), 'calvalue': 0.999619}
    ]
    group2_subgroup4()

def MQ309A():
    global SensorName, Air, CalibrateAir, SensorRLCalRL, MinAirPpm, MaxAirPpm, gas_params
    SensorName = 'MQ309A'
    Air = 11
    SensorRLCalRL = 0.2
    MinAirPpm, MaxAirPpm = 160, 260
    gas_params = [
        {'name': 'H2', 'ppmvals': (10, 10000), 'ppm': (44.8077, -0.5156)},
        {'name': 'CH4', 'ppmvals': (10, 10000), 'ppm': (67.5665, -0.6088)},
        {'name': 'alcohol', 'ppmvals': (100, 10000), 'ppm': (34.1956, -0.2666), 'calvalue': 0.83393},
        {'name': 'CO', 'ppmvals': (100, 10000), 'ppm': (30.3019, -0.2336), 'calvalue': 0.83393}
    ]
    group2_subgroup2()

def MQ_Calculation_Mode(set1, set2, set3, set4, set5, set6, set7, set8):
    global SensorMode, FormulaCoefficient, AirVals, AirValsEqualGasVals, CalMode, CRMode, SensorRLCalRL, CalibrateAir, FormulaMode
    SensorMode = set1
    FormulaCoefficient = set2
    AirVals = set3
    AirValsEqualGasVals = set4
    CRMode = set5
    SensorRLCalRL = set6
    CalibrateAir = set7
    FormulaMode = set8
    
#######################

def group1_subgroup1():
    MQ_Calculation_Mode('Rs/Ro', None, True, True, 1, 1, CleanAir, 'ppm')
    # MQ-6, MQ-8, MQ-135, MQ-216

def group1_subgroup2():
    MQ_Calculation_Mode('Rs/Ro', None, True, True, 1, 1, CalibrateAir, 'ppm')
    # MQ-4, MQ-5, MQ-7, MQ-136, MQ-137
    
def group1_subgroup3():
    MQ_Calculation_Mode('Rs/Ro', None, True, True, 1, SensorRLCalRL, CalibrateAir, 'ppm')
    # MQ-2, MQ-138

def group1_subgroup4():
    MQ_Calculation_Mode('Rs/Ro', None, True, False, 1, 1, CalibrateAir, 'ppm')
    # MQ-214

def group1_subgroup5():
    MQ_Calculation_Mode('Rs/Ro', None, True, False, 3, SensorRLCalRL, CleanAir, 'ppm')
    # MQ-9

def group1_subgroup6():
    MQ_Calculation_Mode('Rs/Ro', 50, True, True, 2, 1, CleanAir, 'mg/L')
    # MQ-3

#######################

def group2_subgroup1():
    MQ_Calculation_Mode('Rs/Rs', None, True, False, 0, 1, CalibrateAir, 'ppm')
    # MQ303B

def group2_subgroup2():
    MQ_Calculation_Mode('Rs/Rs', None, True, False, 0, SensorRLCalRL, CleanAir, 'ppm')
    # MQ309A

def group2_subgroup3():
    MQ_Calculation_Mode('Rs/Rs', None, True, False, 0, SensorRLCalRL, CalibrateAir, 'ppm')
    # MQ303A, MQ306A

def group2_subgroup4():
    MQ_Calculation_Mode('Rs/Rs', None, False, False, 0, SensorRLCalRL, CleanAir, 'ppm')
    # MQ307A
    
#######################

def group3_subgroup1():
    MQ_Calculation_Mode('Ro/Rs', None, True, True, 3, 1, CleanAir, 'ppm')
    # MQ131 HIGH

def group3_subgroup2():
    MQ_Calculation_Mode('Ro/Rs', 0.02, True, True, 0, SensorRLCalRL, CalibrateAir, 'ppb')
    # MQ-131 LOW

#######################
