<?php
	include_once './Connections/RaspberryPi.php';
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
	$sql = 'INSERT INTO `Monitor`.`Server` (`IPAdres`, `IPPort`, `MACAdres`, `OperatingSystem`, `Name`) VALUES ("'.$_POST['IPAdres'].'","'.$_POST['IPPort'].'","'.$_POST['MACAdres'].'","'.$_POST['OperatingSystem'].'","'.$_POST['Name'].'");';
	$retval = mysql_query( $sql, $pi );
	if(! $retval ) {
      	die('Could not enter data: ' . mysql_error());
   	 }
   	echo "Data is succesvol in de database geplaatst";
   mysql_close($pi);
}
else {
?>

<table>
<form action="#" method="post">
<tr><td> Name: </td><td> <input type="text" name="Name" value=""/> </td></tr>
<tr><td> IP adres: </td><td> <input type="text" name="IPAdres" value="" /> </td></tr>
<tr><td> IP Port: </td><td> <input type="text" name="IPPort" value="" /> </td></tr>
<tr><td> MAC Adres: </td><td> <input type="text" name="MACAdres" value=""/> </td></tr>
<tr><td> Operating System: </td><td>
<select name="OperatingSystem">
  <option value="win32">Windows 10</option>
  <option value="win32">Windows 8.1</option>
  <option value="win32">Windows 8</option>
  <option value="win32">Windows 7</option>
  <option value="win32">Windows XP</option>
  <option value="linux2">Ubuntu</option>
  <option value="linux2">Debian</option>
  <option value="linux2">Other</option>
</select> </td></tr>
<tr><td> <input type="submit" value="Toevoegen" name="knop" /> </td></tr>
</form>
<table>
<?php
}
?>
</body>
</html>