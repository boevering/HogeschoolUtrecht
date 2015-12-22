<html>
<head>
    <title>Placeholder</title>
</head>

<body>
<h1>Welkom op de management pagina van THO6 en Scripting2</h1>
<?php

$servername = "10.0.0.14";
$username = "monitor";
$password = "raspberry";

// Create connection
$conn = new mysqli($servername, $username, $password);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
echo "Connected successfully";


$query = "SELECT * FROM Logs";
$results=mysql_query($query);
$row_count=mysql_num_rows($results);
$row_users = mysql_fetch_array($results);

echo "<table>";

while ($row_users = mysql_fetch_array($results)) {
    //output a row here
    echo "<tr><td>".($row_users['email'])."</td></tr>";
}

echo "</table>";

?>

</body>


</html>