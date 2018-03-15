<?php
    $uid = $_POST['uid'];

    echo file_get_contents('http://localhost:4242/htmlapi/get_card_name/?uid="' + $uid + '"');
?>