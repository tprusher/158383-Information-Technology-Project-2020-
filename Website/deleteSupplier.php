<?php 
    // Include config file
    require_once "config.php";

    $SupplierID = $_POST["SupplierID"];

    $POSTsql = "DELETE FROM supplier WHERE SupplierID = $SupplierID";

    $link->query($POSTsql);

    header("location: suppliers.php");
    exit();
?>