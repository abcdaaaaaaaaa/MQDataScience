<?php
    include_once 'db.php';
        
    $data1 = $_COOKIE["data1"] ?? null;
    $data2 = $_COOKIE["data2"] ?? null;
    $data3 = $_COOKIE["data3"] ?? null;
    $data4 = $_COOKIE["data4"] ?? null;
    $data5 = $_COOKIE["data5"] ?? null;
    $value1 = $_COOKIE["value1"] ?? null;
    $value2 = $_COOKIE["value2"] ?? null;
    $value3 = $_COOKIE["value3"] ?? null;
    $value4 = $_COOKIE["value4"] ?? null;
    $value5 = $_COOKIE["value5"] ?? null;
    $value6 = $_COOKIE["value6"] ?? null;
    $value7 = $_COOKIE["value7"] ?? null;
    $value8 = $_COOKIE["value8"] ?? null;
    $value9 = $_COOKIE["value9"] ?? null;
    $value10 = $_COOKIE["value10"] ?? null;
    $value11 = $_COOKIE["value11"] ?? null;
    $value12 = $_COOKIE["value12"] ?? null;

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        switch ($data1) {
            case 1:
            $sql = "INSERT INTO MQ135 (Percentile, Air, Temperature, RH, Percentile2, Acetone, Toluene, Alcohol, CO2, NH4, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "', '" . $value11 . "')";
            break;
            
            case 2:
            $sql = "INSERT INTO MQ2 (Percentile, Air, Temperature, RH, Percentile2, LPG, Propane, H2, Alcohol, CH4, Smoke, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "', '" . $value11 . "', '" . $value12 . "')";
            break;

            case 3:
            $sql = "INSERT INTO MQ3 (Percentile, Air, Temperature, RH, Percentile2, Alcohol, Benzene, Hexane, LPG, CO, CH4)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "', '" . $value11 . "')";                
            break;

            case 4:
            $sql = "INSERT INTO MQ4 (Percentile, Air, Temperature, RH, Percentile2, CH4, LPG, H2, Smoke, Alcohol, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "', '" . $value11 . "')";
            break;

            case 5:
            $sql = "INSERT INTO MQ5 (Percentile, Air, Temperature, RH, Percentile2, LPG, CH4, H2, Alcohol, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "')";
            break;

            case 6:
            $sql = "INSERT INTO MQ6 (Percentile, Air, Temperature, RH, Percentile2, LPG, CH4, H2, Alcohol, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "')";
            break;

            case 7:
            $sql = "INSERT INTO MQ7 (Percentile, Air, Temperature, RH, Percentile2, H2, CO, LPG, CH4, Alcohol)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "')";
            break;

            case 8:
            $sql = "INSERT INTO MQ8 (Percentile, Air, Temperature, RH, Percentile2, H2, Alcohol, LPG, CH4, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "')";
            break;

            case 9:
            $sql = "INSERT INTO MQ9 (Percentile, Air, Temperature, RH, Percentile2, CO, LPG, CH4)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "')";
            break;

            case 10:
            $sql = "INSERT INTO MQ131 (Percentile, Air, Temperature, RH, Percentile2, O3, CL2, NOx)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "')";
            break;

            case 11:
            $sql = "INSERT INTO MQ131_LOW (Percentile, Air, Temperature, RH, Percentile2, O3, CL2, NOx)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "')";
            break;

            case 12:
            $sql = "INSERT INTO MQ136 (Percentile, Air, Temperature, RH, Percentile2, H2S, NH4, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "')";
            break;

            case 13:
            $sql = "INSERT INTO MQ137 (Percentile, Air, Temperature, RH, Percentile2, CO, Ethanol, NH3)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "')";
            break;

            case 14:
            $sql = "INSERT INTO MQ138 (Percentile, Air, Temperature, RH, Percentile2, n_Hexane, Propane, Benzene, Alcohol, CH4, Smoke, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "', '" . $value11 . "', '" . $value12 . "')";
            break;

            case 15:
            $sql = "INSERT INTO MQ214 (Percentile, Air, Temperature, RH, Percentile2, CH4)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "')";
            break;

            case 16:
            $sql = "INSERT INTO MQ216 (Percentile, Air, Temperature, RH, Percentile2, LPG, Propane, i_butane, Alcohol, CH4)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "', '" . $value10 . "')";
            break;

            case 17:
            $sql = "INSERT INTO MQ303A (Percentile, Air, Temperature, RH, Percentile2, Hydrogen, Ethanol, IsoButane)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "')";
            break;

            case 18:
            $sql = "INSERT INTO MQ303B (Percentile, Air, Temperature, RH, Percentile2, Hydrogen, Ethanol, IsoButane)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "')";
            break;

            case 19:
            $sql = "INSERT INTO MQ306A (Percentile, Air, Temperature, RH, Percentile2, Ethanol, Hydrogen, Methane, IsoButane)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "')";
            break;

            case 20:
            $sql = "INSERT INTO MQ307A (Percentile, Air, Temperature, RH, Percentile2, CO, H2)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "')";
            break;

            case 21:
            $sql = "INSERT INTO MQ309A (Percentile, Air, Temperature, RH, Percentile2, H2, CH4, Alcohol, CO)
                    VALUES ('" . $value1 . "', '" . $value2 . "', '" . $value3 . "', '" . $value4 . "', '" . $value5 . "', '" . $value6 . "', '" . $value7 . "', '" . $value8 . "', '" . $value9 . "')";
            break;
        }
            
        if (isset($sql)) {
            if ($conn->query($sql) === TRUE) {
            } 
            else {
                echo "Error: " . $sql . "<br>" . $conn->error;
            }
        }
        $conn->close();
    }
?>

<script>
    <?php
        if (isset($data1)) echo "const data1 = $data1;\n\t";
        if (isset($data2)) echo "const data2 = $data2;\n\t";
        if (isset($data3)) echo "const data3 = $data3;\n\t";
        if (isset($data4)) echo "const data4 = $data4;\n\t";
        if (isset($data5)) echo "const data5 = $data5;\n\t";
        if (isset($value1)) echo "const value1 = $value1;\n\t";
        if (isset($value2)) echo "const value2 = $value2;\n\t";
        if (isset($value3)) echo "const value3 = $value3;\n\t";
        if (isset($value4)) echo "const value4 = $value4;\n\t";
        if (isset($value5)) echo "const value5 = $value5;\n\t";
        if (isset($value6)) echo "const value6 = $value6;\n\t";
        if (isset($value7)) echo "const value7 = $value7;\n\t";
        if (isset($value8)) echo "const value8 = $value8;\n\t";
        if (isset($value9)) echo "const value9 = $value9;\n\t";
        if (isset($value10)) echo "const value10 = $value10;\n\t";
        if (isset($value11)) echo "const value11 = $value11;\n\t";
        if (isset($value12)) echo "const value12 = $value12;\n\t";
    ?>
</script>
