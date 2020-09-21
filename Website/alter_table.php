


<!DOCTYPE HTML>


<html>

<!-- ##############################################     HEAD ELEMENT      ############################################################## -->

<head>

</head>

<body>

<h1> ALTER TABLE SCRIPT </h1>



<?php

// Initialize the session
 session_start();

    // Include config file
    // require_once "config.php";

// Check if the user is logged in, if not then redirect him to login page
if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
    header("location: login.php");
    exit;
}

    $sql = 'ALTER TABLE stock CHANGE COLUMN `Name` ProductName VARCHAR(100) NOT NULL;

        // Bind variables to the prepared statement as parameters
        //mysqli_stmt_bind_param($stmt, "ss", $param_password, $username);
        
        
        // Attempt to execute the prepared statement
        if(mysqli_stmt_execute($stmt)){
            // Password updated successfully. Destroy the session, and redirect to login page
            //session_destroy();
            //header("location: index.php");
            //exit();
            echo 'TABLE CHANGED'
        } else{
            //header("location: reset-password.php");
            echo 'ERROR'
        }

        // Close statement
        mysqli_stmt_close($stmt);
    // Close connection
mysqli_close($link);



?>



</body>
</html>
