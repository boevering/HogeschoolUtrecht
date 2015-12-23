<?php
	include_once './Connections/RaspberryPi.php';
?>
<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<title>Server Beheer</title>
</head>

<body>
<h1> Welkom op de beheer pagina voor de servers. </h1>

<?php
if (!isset($_POST["knop"])) {
	$sql = "SELECT * FROM Server;";
	$result = $pi->query($sql);

	echo '<table border="1">';
	echo '<th>ServerID</th><th>Name</th><th>IP Adres</th><th>IP Poort</th><th>MAC Adres</th><th>Operating System</th><th>Aanpassen</th>';
	while ($row = $result->fetch_assoc()) {
		print '<tr><td>' . $row['sID'] . "</td>";
		print '<td>' . $row['Name'] . "</td>";
		print '<td>' . $row['IPAdres'] . "</td>";
		print '<td>' . $row['IPPort'] . "</td>";
		print '<td>' . $row['MACAdres'] . "</td>";
		print '<td>' . $row['OperatingSystem'] . "</td>";
		print '<td><form action="" method="post"><input type="hidden" name="sID" value="'. $row['sID'] .'"  /><input type="submit" value="edit" name="knop" /></form></td></tr>';
	}
	echo '</table>';
	print '<form action="#" method="post"><input type="submit" value="toevoegen" name="knop" /></form></td></tr>';
}

if ($_POST["knop"] == "Server toevoegen") {
	$sql = 'INSERT INTO `Monitor`.`Server` (`IPAdres`, `IPPort`, `MACAdres`, `OperatingSystem`, `Name`) VALUES ("'.$_POST['IPAdres'].'","'.$_POST['IPPort'].'","'.$_POST['MACAdres'].'","'.$_POST['OperatingSystem'].'","'.$_POST['Name'].'");';


	if ($pi->query($sql) === TRUE) {
		echo "New record created successfully";
	}
	else {
		echo "Error: " . $sql . "<br>" . $pi->error;
	}
	$_POST["knop"] == NULL;
	header("Refresh:5");
}
if ($_POST["knop"] == "update") {
	$sql = 'UPDATE `Server` SET `IPAdres`="'.$_POST['IPAdres'].'", `IPPort`="'.$_POST['IPPort'].'", `MACAdres`="'.$_POST['MACAdres'].'", `OperatingSystem`="'.$_POST['OperatingSystem'].'", `Name`="'.$_POST['Name'].'" WHERE `sID`="'.$_POST['sID'].'";';

	if ($pi->query($sql) === TRUE) {
		echo "Record updated successfully";
	}
	else {
		echo "Error: " . $sql . "<br>" . $pi->error;
	}
	$_POST["knop"] == NULL;
	header("Refresh:5");
}
if (($_POST["knop"] == "edit") or ($_POST["knop"] == "toevoegen")) {

	$needToDo = $_POST["knop"];
	if ($needToDo == "edit"){
		$sqlToevoeging = "WHERE sID = ".$_POST['sID'];
		$needToDo = "update";
	}
	else {
		$sqlToevoeging = "WHERE sID = NULL";
		$needToDo = "Server toevoegen";
	}

	$sql = "SELECT * FROM Monitor.Server ".$sqlToevoeging.";";
	$result = $pi->query($sql);
	$row = $result->fetch_assoc();
?>
    <table>
    <form action="" method="post">
    <tr><td> Name: </td><td> <input type="text" name="Name" value="<?php echo $row['Name']; ?>"/> </td></tr>
    <tr><td> IP adres: </td><td> <input type="text" name="IPAdres" value="<?php echo $row['IPAdres']; ?>" /> </td></tr>
    <tr><td> IP Port: </td><td> <input type="text" name="IPPort" value="<?php echo $row['IPPort']; ?>" /> </td></tr>
    <tr><td> MAC Adres: </td><td> <input type="text" name="MACAdres" value="<?php echo $row['MACAdres']; ?>"/> </td></tr>
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
    <tr><td><input type="hidden" name="sID" value="<?php echo $row['sID']; ?>"  /><input type="submit" value="<?php echo $needToDo; ?>" name="knop" /> </td></tr>
    </form>
    <table>

<?php
}
?>
</body>
</html>