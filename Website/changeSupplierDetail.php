<?php  

    // Include config file
    require_once "config.php";

    //Set variables from POST data
    $CompanyName = $_POST["CompanyName"];
    $ContactPerson = $_POST["ContactPerson"];
    $Email = $_POST["Email"];
    $Phone = $_POST["Phone"];
    $SupplierID = $_POST["SupplierID"];
        
    $POSTsql =  "UPDATE supplier SET CompanyName = ?, ContactPerson= ?, Email= ?, Phone= ? WHERE SupplierID= ?";
    //$stmt = mysqli_prepare($link,$sql);
    // mysqli_stmt_bind_param($stmt, 'ssss', $CompanyName, $ContactPerson, $Email, $Phone);
    if($stmt = mysqli_prepare($link, $POSTsql)) {
    // Bind variables to the prepared statement as parameters
    mysqli_stmt_bind_param($stmt, "sssss", $stmt_CompanyName, $stmt_ContactPerson, $stmt_Email, $stmt_Phone, $stmt_SupplierID);
        
         // Set parameters
        $stmt_CompanyName = $CompanyName;
        $stmt_ContactPerson = $ContactPerson;
        $stmt_Email =  $Email;
        $stmt_Phone =  $Phone;
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