<html>
<head>
    <title>Placeholder</title>
</head>

<body>
<h1>Welkom op de management pagina van THO6 en Scripting2</h1>
<?PHP

$user_name = "monitor";
$password = "raspberry";
$database = "Monitor";
$server = "10.0.0.14";

$db_handle = mysql_connect($server, $user_name, $password);
$db_found = mysql_select_db($database, $db_handle);

if ($db_found) {

$SQL = "SELECT * FROM Logs";
$result = mysql_query($SQL);

echo '<table>';
echo '<th>LogID</th><th>ServerID</th><th>Time Stamp</th><th>R1</th><th>R2</th><th>R3</th><th>R4</th><th>R5</th><th>R6</th><th>R7</th><th>R8</th><th>R9</th><th>R10</th><th>R11</th>';
while ($db_field = mysql_fetch_assoc($result) ) {

print '<tr><td>' . $db_field['lID'] . "</td>";
print '<td>' . $db_field['sID'] . "</td>";
print '<td>' . $db_field['TimeStamp'] . "</td>";
print '<td>' . $db_field['r1'] . "</td>";
print '<td>' . $db_field['r2'] . "</td>";
print '<td>' . $db_field['r3'] . "</td>";
print '<td>' . $db_field['r4'] . "</td>";
print '<td>' . $db_field['r5'] . "</td>";
print '<td>' . $db_field['r6'] . "</td>";
print '<td>' . $db_field['r7'] . "</td>";
print '<td>' . $db_field['r8'] . "</td>";
print '<td>' . $db_field['r9'] . "</td>";
print '<td>' . $db_field['r10'] . "</td>";
print '<td>' . $db_field['r11'] . "</td></tr>";
}

echo '</table>';

mysql_close($db_handle);

}
else {

print "Database NOT Found ";
mysql_close($db_handle);

}

?>

</body>
</html>