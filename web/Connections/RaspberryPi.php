<?php
$servername = "localhost";
$username = "monitor";
$password = "raspberry";
$dbname = "Monitor";

// Create connection
$pi = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($pi->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>