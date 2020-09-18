<?php 

    // Include config file
    require_once "config.php";

    //Set variables from POST data
    $Name = $_POST["item-name"];
    $Price = $_POST["price"];
    $ShelfLife = $_POST["shelfLife"];
    $SupplierSKU = $_POST["SupplierSKU"];
    $SupplierID = $_POST["SupplierID"];

    echo $Name . $Price . $ShelfLife . $SupplierSKU . $SupplierID;
        
    $POSTsql =  "INSERT INTO stock(Name, Price, ShelfLife, SupplierID, SupplierSKU) VALUES (?,?,?,?,?)";
    //$stmt = mysqli_prepare($link,$sql);
    // mysqli_stmt_bind_param($stmt, 'ssss', $CompanyName, $ContactPerson, $Email, $Phone);
    if($stmt = mysqli_prepare($link, $POSTsql)) {
    // Bind variables to the prepared statement as parameters
    mysqli_stmt_bind_param($stmt, "sssss", $stmt_Name, $stmt_Price, $stmt_ShelfLife, $stmt_SupplierID, $stmt_SupplierSKU);
        
         // Set parameters
        $stmt_Name = $Name;
        $stmt_Price = $Price;
        $stmt_ShelfLife =  $ShelfLife;
        $stmt_SupplierSKU =  $SupplierSKU;
        $stmt_SupplierID = $SupplierID;

        // Attempt to execute the prepared statement
        if(mysqli_stmt_execute($stmt)){
            header("location: suppliers.php");
            exit();
        } else{
            header("location: dashboard.php");
        }

        // Close statement
        mysqli_stmt_close($stmt);
    }

?>