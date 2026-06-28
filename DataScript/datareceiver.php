<?php
include_once 'db.php'; // Please do not forget to edit this file.

$apiKey = 'REPLACE_WITH YOUR_API_KEY';

function getTableName($mode) {
    switch ($mode) {
        case 1: return "MQ135"; case 2: return "MQ2"; case 3: return "MQ3";
        case 4: return "MQ4"; case 5: return "MQ5"; case 6: return "MQ6";
        case 7: return "MQ7"; case 8: return "MQ8"; case 9: return "MQ9";
        case 10: return "MQ131"; case 11: return "MQ131_LOW"; case 12: return "MQ136";
        case 13: return "MQ137"; case 14: return "MQ138"; case 15: return "MQ214";
        case 16: return "MQ216"; case 17: return "MQ303A"; case 18: return "MQ303B";
        case 19: return "MQ306A"; case 20: return "MQ307A"; case 21: return "MQ309A";
        default: return "MQ135";
    }
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (!isset($_POST['api_key']) || $_POST['api_key'] !== $apiKey) {
        http_response_code(403);
        exit;
    }

    if (isset($_POST['update_calculated']) && $_POST['update_calculated'] === "1") {
        $total1 = isset($_POST['total1']) ? intval($_POST['total1']) : 1;
        $table = getTableName($total1);
        $v3 = floatval($_POST['value3'] ?? 0);
        $v4 = floatval($_POST['value4'] ?? 0);
        $v5 = floatval($_POST['value5'] ?? 0);
        $v6 = floatval($_POST['value6'] ?? 0);
        $v7 = floatval($_POST['value7'] ?? 0);
        $v8 = floatval($_POST['value8'] ?? 0);
        $v9 = floatval($_POST['value9'] ?? 0);
        $v10 = floatval($_POST['value10'] ?? 0);
        
        $sql = "";
        switch ($total1) {
            case 1: $sql = "UPDATE $table SET Air='$v3', Acetone='$v4', Toluene='$v5', Alcohol='$v6', CO2='$v7', NH4='$v8', CO='$v9' ORDER BY id DESC LIMIT 1"; break;
            case 2: $sql = "UPDATE $table SET Air='$v3', LPG='$v4', propane='$v5', H2='$v6', alcohol='$v7', CH4='$v8', smoke='$v9', CO='$v10' ORDER BY id DESC LIMIT 1"; break;
            case 3: $sql = "UPDATE $table SET Air='$v3', Alcohol='$v4', Benzene='$v5', Hexane='$v6', LPG='$v7', CO='$v8', CH4='$v9' ORDER BY id DESC LIMIT 1"; break;
            case 4: $sql = "UPDATE $table SET Air='$v3', CH4='$v4', LPG='$v5', H2='$v6', smoke='$v7', alcohol='$v8', CO='$v9' ORDER BY id DESC LIMIT 1"; break;
            case 5: $sql = "UPDATE $table SET Air='$v3', LPG='$v4', CH4='$v5', H2='$v6', alcohol='$v7', CO='$v8' ORDER BY id DESC LIMIT 1"; break;
            case 6: $sql = "UPDATE $table SET Air='$v3', LPG='$v4', CH4='$v5', H2='$v6', Alcohol='$v7', CO='$v8' ORDER BY id DESC LIMIT 1"; break;
            case 7: $sql = "UPDATE $table SET Air='$v3', H2='$v4', CO='$v5', LPG='$v6', CH4='$v7', Alcohol='$v8' ORDER BY id DESC LIMIT 1"; break;
            case 8: $sql = "UPDATE $table SET Air='$v3', H2='$v4', alcohol='$v5', LPG='$v6', CH4='$v7', CO='$v8' ORDER BY id DESC LIMIT 1"; break;
            case 9: $sql = "UPDATE $table SET Air='$v3', CO='$v4', LPG='$v5', CH4='$v6' ORDER BY id DESC LIMIT 1"; break;
            case 10: $sql = "UPDATE $table SET Air='$v3', O3='$v4', CL2='$v5', NOx='$v6' ORDER BY id DESC LIMIT 1"; break;
            case 11: $sql = "UPDATE $table SET Air='$v3', O3='$v4', CL2='$v5', NOx='$v6' ORDER BY id DESC LIMIT 1"; break;
            case 12: $sql = "UPDATE $table SET Air='$v3', H2S='$v4', NH4='$v5', CO='$v6' ORDER BY id DESC LIMIT 1"; break;
            case 13: $sql = "UPDATE $table SET Air='$v3', CO='$v4', Ethanol='$v5', NH3='$v6' ORDER BY id DESC LIMIT 1"; break;
            case 14: $sql = "UPDATE $table SET Air='$v3', n_Hexane='$v4', propane='$v5', Benzene='$v6', alcohol='$v7', CH4='$v8', smoke='$v9', CO='$v10' ORDER BY id DESC LIMIT 1"; break;
            case 15: $sql = "UPDATE $table SET Air='$v3', CH4='$v4' ORDER BY id DESC LIMIT 1"; break;
            case 16: $sql = "UPDATE $table SET Air='$v3', LPG='$v4', propane='$v5', i_butane='$v6', alcohol='$v7', CH4='$v8' ORDER BY id DESC LIMIT 1"; break;
            case 17: $sql = "UPDATE $table SET Air='$v3', Hydrogen='$v4', Ethanol='$v5', IsoButane='$v6' ORDER BY id DESC LIMIT 1"; break;
            case 18: $sql = "UPDATE $table SET Air='$v3', Hydrogen='$v4', Ethanol='$v5', IsoButane='$v6' ORDER BY id DESC LIMIT 1"; break;
            case 19: $sql = "UPDATE $table SET Air='$v3', Ethanol='$v4', Hydrogen='$v5', Methane='$v6', IsoButane='$v7' ORDER BY id DESC LIMIT 1"; break;
            case 20: $sql = "UPDATE $table SET CO='$v4', H2='$v5' ORDER BY id DESC LIMIT 1"; break;
            case 21: $sql = "UPDATE $table SET Air='$v3', H2='$v4', CH4='$v5', alcohol='$v6', CO='$v7' ORDER BY id DESC LIMIT 1"; break;
        }

        if ($sql != "") $conn->query($sql);
        $conn->close();
        exit;
    }

    $total1 = isset($_POST['field1']) ? intval($_POST['field1']) : 1;
    $table = getTableName($total1);

    $timeCheckSql = "SELECT reading_time FROM $table ORDER BY id DESC LIMIT 1";
    $timeCheckResult = $conn->query($timeCheckSql);
    if ($timeCheckResult && $row = $timeCheckResult->fetch_assoc()) {
        $last_time = strtotime($row['reading_time']);
        if (time() - $last_time < 5) {
            http_response_code(429);
            exit;
        }
    }

    $total2 = isset($_POST['field2']) ? floatval($_POST['field2']) : 0;
    $total3 = isset($_POST['field3']) ? floatval($_POST['field3']) : 0;
    $total4 = isset($_POST['field4']) ? floatval($_POST['field4']) : 0;
    $total5 = isset($_POST['field5']) ? floatval($_POST['field5']) : 0;
    $field6 = isset($_POST['field6']) ? floatval($_POST['field6']) : 0;
    $field7 = isset($_POST['field7']) ? floatval($_POST['field7']) : 0;

    $SensorValue = round(min(max(($total2 / 4095.0), 0), 1), 4);
    $temperature = round(min(max((($total3 / 10.0) - 140), -10), 50), 4);
    $rh = round(min(max((($total4 / 10.0) - 100), 0), 100), 4);
    $SensorValue2 = round(min(max(($total5 / 4095.0), 0), 1), 4);

    $value2 = $SensorValue * 100;
    $value13 = $SensorValue2 * 100;
    $DHT = $temperature . '°C %' . $rh;
    $value14 = round(($field6 * pow(10, -7)) - 90, 7);
    $value15 = round(($field7 * pow(10, -7)) - 180, 7);

    $sql = "";
    switch ($total1) {
        case 1: $sql = "INSERT INTO MQ135 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 2: $sql = "INSERT INTO MQ2 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 3: $sql = "INSERT INTO MQ3 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 4: $sql = "INSERT INTO MQ4 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 5: $sql = "INSERT INTO MQ5 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 6: $sql = "INSERT INTO MQ6 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 7: $sql = "INSERT INTO MQ7 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 8: $sql = "INSERT INTO MQ8 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 9: $sql = "INSERT INTO MQ9 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 10: $sql = "INSERT INTO MQ131 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 11: $sql = "INSERT INTO MQ131_LOW (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 12: $sql = "INSERT INTO MQ136 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 13: $sql = "INSERT INTO MQ137 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 14: $sql = "INSERT INTO MQ138 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 15: $sql = "INSERT INTO MQ214 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 16: $sql = "INSERT INTO MQ216 (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 17: $sql = "INSERT INTO MQ303A (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 18: $sql = "INSERT INTO MQ303B (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 19: $sql = "INSERT INTO MQ306A (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 20: $sql = "INSERT INTO MQ307A (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
        case 21: $sql = "INSERT INTO MQ309A (DHT, SpaceData100, SpaceData200, lat, lng) VALUES ('$DHT', '$value2', '$value13', '$value14', '$value15')"; break;
    }

    if ($sql != "") $conn->query($sql);
    $conn->close();
    exit;

} elseif ($_SERVER["REQUEST_METHOD"] == "GET") {
    if (!isset($_GET['api_key']) || $_GET['api_key'] !== $apiKey) {
        http_response_code(403);
        exit;
    }

    $results = isset($_GET['results']) ? (int)$_GET['results'] : 1;

    $tables = [
        1 => 'MQ135', 2 => 'MQ2', 3 => 'MQ3', 4 => 'MQ4', 5 => 'MQ5',
        6 => 'MQ6', 7 => 'MQ7', 8 => 'MQ8', 9 => 'MQ9', 10 => 'MQ131',
        11 => 'MQ131_LOW', 12 => 'MQ136', 13 => 'MQ137', 14 => 'MQ138',
        15 => 'MQ214', 16 => 'MQ216', 17 => 'MQ303A', 18 => 'MQ303B',
        19 => 'MQ306A', 20 => 'MQ307A', 21 => 'MQ309A'
    ];

    $latest_time = null;
    $latest_table_id = 1;

    foreach ($tables as $id => $tableName) {
        $q = "SELECT `reading_time` FROM `$tableName` ORDER BY `reading_time` DESC LIMIT 1";
        $res = $conn->query($q);
        if ($res && $res->num_rows > 0) {
            $row = $res->fetch_assoc();
            $row_time = strtotime($row['reading_time']);
            if ($latest_time === null || $row_time > $latest_time) {
                $latest_time = $row_time;
                $latest_table_id = $id;
            }
        }
    }

    $activeTable = $tables[$latest_table_id];
    $sql = "SELECT * FROM `$activeTable` ORDER BY id DESC LIMIT ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("i", $results);
    $stmt->execute();
    $result = $stmt->get_result();
    
    $feeds = [];
    while ($row = $result->fetch_assoc()) {
        $row['field1'] = $latest_table_id;
        
        $dht = $row['DHT'] ?? '0°C %0';
        $dhtParts = explode(' %', $dht);
        $tempStr = str_replace('°C', '', $dhtParts[0] ?? '0');
        $temp = is_numeric($tempStr) ? floatval($tempStr) : 0;
        $rh = isset($dhtParts[1]) ? floatval($dhtParts[1]) : 0;

        $row['field2'] = isset($row['SpaceData100']) ? ($row['SpaceData100'] / 100) * 4095 : 0;
        $row['field3'] = ($temp + 140) * 10;
        $row['field4'] = ($rh + 100) * 10;
        $row['field5'] = isset($row['SpaceData200']) ? ($row['SpaceData200'] / 100) * 4095 : 0;
        $row['field6'] = isset($row['lat']) ? ($row['lat'] + 90) * 10000000 : 0;
        $row['field7'] = isset($row['lng']) ? ($row['lng'] + 180) * 10000000 : 0;
        $row['created_at'] = $row['reading_time'] ?? gmdate('Y-m-d\TH:i:s\Z');
        
        $feeds[] = $row;
    }
    
    header('Content-Type: application/json');
    echo json_encode(["feeds" => array_reverse($feeds)]);
    $stmt->close();
}
?>
