<?php
# FileName="Connection_php_mysql.htm"
# Type="MYSQL"
# HTTP="true"
$hostname_pi = "localhost";
$database_pi = "Monitor";
$username_pi = "monitor";
$password_pi = "raspberry";
$pi = mysql_pconnect($hostname_pi, $username_pi, $password_pi) or trigger_error(mysql_error(),E_USER_ERROR);
?>