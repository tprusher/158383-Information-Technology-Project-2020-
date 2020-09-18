<?php 

// Initialize the session
 session_start();

    // Include config file
    require_once "config.php";

// Check if the user is logged in, if not then redirect him to login page
if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
    header("location: login.php");
    exit;
}

    //Set variables from POST data
    $CompanyName = $_POST["CompanyName"];
    $ContactPerson = $_POST["ContactPerson"];
    $Email = $_POST["Email"];
    $Phone = $_POST["Phone"];
        
    $POSTsql =  "INSERT INTO supplier(CompanyName, ContactPerson, Email, Phone) VALUES (?, ?, ?, ?) WHERE SupplierID = $SupplierID";
    //$stmt = mysqli_prepare($link,$sql);
    // mysqli_stmt_bind_param($stmt, 'ssss', $CompanyName, $ContactPerson, $Email, $Phone);
    if($stmt = mysqli_prepare($link, $POSTsql)){
        // Bind variables to the prepared statement as parameters
        mysqli_stmt_bind_param($stmt, "ssss", $stmt_CompanyName, $stmt_ContactPerson, $stmt_Email, $stmt_Phone);
        
         // Set parameters
        $stmt_CompanyName = $CompanyName;
        $stmt_ContactPerson = $ContactPerson;
        $stmt_Email = $Email;
        $stmt_Phone = $Phone;

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