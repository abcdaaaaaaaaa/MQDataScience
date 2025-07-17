#include "SensorDefinitions.h"

// MQ135
GasModel MQ135_Gases[] = {
    {"Acetone",   2.7988,     -0.2913, 10,    200},
    {"Toluene",   2.9788,     -0.2892, 10,    200},
    {"Alcohol",   3.8623,     -0.3126, 10,    200},
    {"CO2",       5.2278,     -0.3585, 10,    200},
    {"NH4",       6.2968,     -0.3892, 10,    200},
    {"CO",        5.0533,     -0.2541, 10,    200}
};
SensorModel MQ135 = {"MQ135", 3.6, 1.0, 1.0, true, MQ135_Gases, sizeof(MQ135_Gases)/sizeof(GasModel)};

// MQ2
GasModel MQ2_Gases[] = {
    {"LPG",       17.6135,    -0.4539, 200,   10000},
    {"Propane",   19.5575,    -0.461,  200,   10000},
    {"H2",        25.7473,    -0.4731, 200,   10000},
    {"Alcohol",   19.2641,    -0.3604, 200,   10000},
    {"CH4",       20.7074,    -0.36,   200,   10000},
    {"Smoke",     26.4698,    -0.3876, 200,   10000},
    {"CO",        28.024,     -0.3182, 200,   10000}
};
SensorModel MQ2 = {"MQ2", 9.8, 0.78, 0.25, true, MQ2_Gases, sizeof(MQ2_Gases)/sizeof(GasModel)};

// MQ3
GasModel MQ3_Gases[] = {
    {"Alcohol",   0.5565,     -0.6333, 0.103, 10},
    {"Benzene",   1.7957,     -0.3690, 0.103, 10},
    {"Hexane",    22.9337,    -0.3580, 0.103, 10},
    {"LPG",       27.8286,    -0.2847, 0.103, 10},
    {"CO",        31.9559,    -0.2325, 0.103, 10},
    {"CH4",       44.8389,    -0.0476, 0.103, 10}
};
SensorModel MQ3 = {"MQ3", 60.53, 1.0, 1.0, true, MQ3_Gases, sizeof(MQ3_Gases)/sizeof(GasModel)};

// MQ4
GasModel MQ4_Gases[] = {
    {"CH4",       11.5517,    -0.3541, 200,   10000},
    {"LPG",       14.1866,    -0.3227, 200,   10000},
    {"H2",        9.6432,     -0.1765, 200,   10000},
    {"Smoke",     7.05,       -0.1065, 200,   10000},
    {"Alcohol",   5.7994,     -0.0696, 200,   10000},
    {"CO",        5.49,       -0.0495, 200,   10000}
};
SensorModel MQ4 = {"MQ4", 4.4, 1.28, 1.0, true, MQ4_Gases, sizeof(MQ4_Gases)/sizeof(GasModel)};

// MQ5
GasModel MQ5_Gases[] = {
    {"LPG",       6.1067,    -0.4102, 200,    10000},
    {"CH4",       6.987,     -0.3777, 200,    10000},
    {"H2",        7.4265,    -0.2847, 200,    10000},
    {"Alcohol",   10.8274,   -0.2104, 200,    10000},
    {"CO",        8.2236,    -0.1492, 200,    10000}
};
SensorModel MQ5 = {"MQ5", 6.5, 0.983, 1.0, true, MQ5_Gases, sizeof(MQ5_Gases)/sizeof(GasModel)};

// MQ6
GasModel MQ6_Gases[] = {
    {"LPG",       20.3079,    -0.4349, 200,   10000},
    {"CH4",       22.011,     -0.4029, 200,   10000},
    {"H2",        26.9497,    -0.2956, 200,   10000},
    {"Alcohol",   19.3261,    -0.1655, 200,   10000},
    {"CO",        13.4917,    -0.0777, 200,   10000}
};
SensorModel MQ6 = {"MQ6", 10.0, 1.0, 1.0, true, MQ6_Gases, sizeof(MQ6_Gases)/sizeof(GasModel)};

// MQ7
GasModel MQ7_Gases[] = {
    {"H2",        21.1794,    -0.7174, 50,    4000},
    {"CO",        20.89,      -0.6568, 50,    4000},
    {"LPG",       14.9745,    -0.1329, 50,    4000},
    {"CH4",       19.8094,    -0.09,   50,    4000},
    {"Alcohol",   20.2524,    -0.0655, 50,    4000}
};
SensorModel MQ7 = {"MQ7", 26.0, 0.6436, 1.0, true, MQ7_Gases, sizeof(MQ7_Gases)/sizeof(GasModel)};

// MQ8
GasModel MQ8_Gases[] = {
    {"H2",        18391.5667, -1.4494, 200,   10000},
    {"Alcohol",   468.8045,   -0.5574, 200,   10000},
    {"LPG",       152.1255,   -0.2922, 200,   10000},
    {"CH4",       117.9639,   -0.1448, 200,   10000},
    {"CO",        126.605,    -0.1173, 200,   10000}
};
SensorModel MQ8 = {"MQ8", 70.0, 1.0, 1.0, true, MQ8_Gases, sizeof(MQ8_Gases)/sizeof(GasModel)};

// MQ9
GasModel MQ9_Gases[] = {
    {"CO",        16.8797,    -0.4445, 200,   1000},
    {"LPG",       24.918,     -0.4695, 200,   10000},
    {"CH4",       21.8247,    -0.3663, 200,   10000}
};
SensorModel MQ9 = {"MQ9", 9.7, 1.0, 0.5, true, MQ9_Gases, sizeof(MQ9_Gases)/sizeof(GasModel)};

// MQ131
GasModel MQ131_Gases[] = {
    {"O3",        16.0871,    -0.8603, 5,     100},
    {"CL2",       18.9693,    -0.7132, 5,     100},
    {"NOx",       16.7059,    -0.4684, 5,     100}
};
SensorModel MQ131 = {"MQ131", 12.0, 1.0, 1.0, true, MQ131_Gases, sizeof(MQ131_Gases)/sizeof(GasModel)};


// MQ131_LOW
GasModel MQ131_LOW_Gases[] = {
    {"O3",        16.0871,    -0.8603, 5,     100},
    {"CL2",       18.9693,    -0.7132, 5,     100},
    {"NOx",       16.7059,    -0.4684, 5,     100}
};
SensorModel MQ131_LOW = {"MQ131_LOW", 12.0, 0.5, 0.2, false, MQ131_Gases, sizeof(MQ131_Gases)/sizeof(GasModel)};

// MQ136
GasModel MQ136_Gases[] = {
    {"H2S",       17.6135,    -0.4539, 200,   10000},
    {"NH4",       19.5575,    -0.461,  200,   10000},
    {"CO",        28.024,     -0.3182, 200,   10000}
};
SensorModel MQ136 = {"MQ136", 3.54, 1.44, 1.0, true, MQ136_Gases, sizeof(MQ136_Gases)/sizeof(GasModel)};

// MQ137
GasModel MQ137_Gases[] = {
    {"CO",        17.6135,    -0.4539, 200,   10000},
    {"Ethanol",   19.5575,    -0.461,  200,   10000},
    {"NH3",       28.024,     -0.3182, 200,   10000}
};
SensorModel MQ137 = {"MQ137", 3.54, 1.44, 1.0, true, MQ137_Gases, sizeof(MQ137_Gases)/sizeof(GasModel)};

// MQ138
GasModel MQ138_Gases[] = {
    {"n-Hexane",  17.6135,    -0.4539, 200,   10000},
    {"Propane",   19.5575,    -0.461,  200,   10000},
    {"Benzene",   25.7473,    -0.4731, 200,   10000},
    {"Alcohol",   19.2641,    -0.3604, 200,   10000},
    {"CH4",       20.7074,    -0.36,   200,   10000},
    {"Smoke",     26.4698,    -0.3876, 200,   10000},
    {"CO",        28.024,     -0.3182, 200,   10000}
};
SensorModel MQ138 = {"MQ138", 9.8, 2.914, 20.0/47.0, true, MQ138_Gases, sizeof(MQ138_Gases)/sizeof(GasModel)};

// MQ214
GasModel MQ214_Gases[] = {
    {"CH4",       2669.39,    -0.3784, 3000,  20000}
};
SensorModel MQ214 = {"MQ214", 595.18, 105.554, 1.0, true, MQ214_Gases, sizeof(MQ214_Gases)/sizeof(GasModel)};

// MQ216
GasModel MQ216_Gases[] = {
    {"LPG",       17.6135,    -0.4539, 200,   10000},
    {"Propane",   19.5575,    -0.461,  200,   10000},
    {"i-butane",  25.7473,    -0.4731, 200,   10000},
    {"Alcohol",   19.2641,    -0.3604, 200,   10000},
    {"CH4",       20.7074,    -0.36,   200,   10000}
};
SensorModel MQ216 = {"MQ216", 9.8, 1.0, 1.0, true, MQ216_Gases, sizeof(MQ216_Gases)/sizeof(GasModel)};

// MQ303A
GasModel MQ303A_Gases[] = {
    {"Hydrogen",  1.7955,     -0.3767, 10,    10000},
    {"Ethanol",   1.7007,     -0.4214, 10,    10000}, // Old Curve
    {"IsoButane", 1.8622,     -0.3374, 100,   10000}
};
SensorModel MQ303A = {"MQ303A", 1.0, 0.17, 47.0/50.0, false, MQ303A_Gases, sizeof(MQ303A_Gases)/sizeof(GasModel)};

// MQ306A
GasModel MQ306A_Gases[] = {
    {"Ethanol",   3.3559,     -0.3563, 100,   3000},
    {"Hydrogen",  3.6812,     -0.4308, 100,   10000},
    {"Methane",   7.3489,     -0.5979, 100,   10000},
    {"IsoButane", 2.7521,     -0.4732, 100,   10000}
};
SensorModel MQ306A = {"MQ306A", 1.66, 0.1, 0.2, false, MQ306A_Gases, sizeof(MQ306A_Gases)/sizeof(GasModel)};

// MQ303B
GasModel MQ303B_Gases[] = {
    {"Hydrogen",  1.7955,     -0.3767, 10,    10000},
    {"Ethanol",   1.7007,     -0.4214, 10,    10000}, // Old Curve
    {"IsoButane", 1.8622,     -0.3374, 100,   10000}
};
SensorModel MQ303B = {"MQ303B", 1.0, 0.2632, 1.0, false, MQ303B_Gases, sizeof(MQ303B_Gases)/sizeof(GasModel)};

// MQ307A
GasModel MQ307A_Gases[] = {
    {"CO",        2336.2698,  -1.7255, 30,    1000},
    {"H2",        25051.8177, -0.8318, 1000,  3000}
};
SensorModel MQ307A = {"MQ307A", NULL, 1.0, 0.02, true, MQ307A_Gases, sizeof(MQ307A_Gases)/sizeof(GasModel)};

// MQ309A
GasModel MQ309A_Gases[] = {
    {"H2",        44.8077,    -0.5156, 10,    10000},
    {"CH4",       67.5665,    -0.6088, 10,    10000},
    {"Alcohol",   34.1956,    -0.2666, 100,   10000},
    {"CO",        30.3019,    -0.2336, 100,   10000}
};
SensorModel MQ309A = {"MQ309A", 11.0, 1.0, 0.2, true, MQ309A_Gases, sizeof(MQ309A_Gases)/sizeof(GasModel)};

bool isMQSensor(String model, String mqList[], int listSize) {
  for (int i = 0; i < listSize; i++) {
    if (model == mqList[i]) return true;
  }
  return false;
}

// Return pointer based on name
SensorModel* getSensorModel(const String& modelName) {
    if (modelName == "MQ135") return &MQ135;
    if (modelName == "MQ2") return &MQ2;
    if (modelName == "MQ3") return &MQ3;
    if (modelName == "MQ4") return &MQ4;
    if (modelName == "MQ5") return &MQ5;
    if (modelName == "MQ6") return &MQ6;
    if (modelName == "MQ7") return &MQ7;
    if (modelName == "MQ8") return &MQ8;
    if (modelName == "MQ9") return &MQ9;
    if (modelName == "MQ131") return &MQ131;
    if (modelName == "MQ131_LOW") return &MQ131_LOW;
    if (modelName == "MQ136") return &MQ136;
    if (modelName == "MQ137") return &MQ137;
    if (modelName == "MQ138") return &MQ138;
    if (modelName == "MQ214") return &MQ214;
    if (modelName == "MQ303A") return &MQ303A;
    if (modelName == "MQ303B") return &MQ303B;
    if (modelName == "MQ307A") return &MQ307A;
    if (modelName == "MQ309A") return &MQ309A;
    return nullptr;
}
