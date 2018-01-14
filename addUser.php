<?php
error_reporting(-1);
//echo '<script type="text/javascript">alert("open")</script>';
// echo $_GET["user"];
$cmd = 'sudo /usr/bin/python /var/www/html/python/BoxControl.py adduser ';
// echo $cmd;
// echo " ".$_GET["user"] . ' ' . $_GET["pass"];
$cmd.=" ".$_GET["admin"] . ' ' . $_GET["user"] . ' ' . $_GET["pass"] . ' ' . $_GET["times"];


//$cmd = 'sudo /usr/bin/python /var/www/html/python/BoxControl.py open gali galipass';
//echo $cmd;
shell_exec($cmd);
 
?>