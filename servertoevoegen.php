<?php
	include_once 'Connections/RaspberryPi.php';
?>

<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Server Toevoegen</title>
</head>

<body>

<?php
if (isset($_POST["knop"])) {


?>


<table>
<form action="#" method="post">
<tr><td> Name: </td><td> <input type="text" name="Name" value=""/> </td></tr>
<tr><td> IP adres: </td><td> <input type="text" name="IPAdres" value="" /> </td></tr>
<tr><td> IP Port: </td><td> <input type="text" name="IPPort" value="" /> </td></tr>
<tr><td> MAC Adres: </td><td> <input type="text" name="MACAdres" value=""/> </td></tr>
<tr><td> Operating System: </td><td> <input type="text" name="OperatingSystem" value="" /> </td></tr>
<tr><td> <input type="submit" value="Toevoegen" name="knop" /> </td></tr>
</form>
<table>





</body>
</html>