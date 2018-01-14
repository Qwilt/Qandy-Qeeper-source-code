<?php
error_reporting(-1);
echo '<script type="text/javascript">alert("Open!")</script>';
// echo $_GET["user"];
$cmd = 'sudo /usr/bin/python /var/www/html/python/BoxControl.py open ';
// echo $cmd;
// echo " ".$_GET["user"] . ' ' . $_GET["pass"];
$cmd.=" ".$_GET["user"] . ' ' . $_GET["pass"];


//$cmd = 'sudo /usr/bin/python /var/www/html/python/BoxControl.py open gali galipass';
//echo $cmd;
shell_exec($cmd);
 
?>