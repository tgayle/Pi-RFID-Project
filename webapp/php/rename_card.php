<?php

$newname = $_POST['name'];
$carduid = $_POST['uid'];

echo file_get_contents('http://localhost:4242/htmlapi/name_card/?uid="' + $carduid + '"&name="' + $name + '"');

?>