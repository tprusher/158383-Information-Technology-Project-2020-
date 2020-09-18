
<html> 
<head> 
    <title> Add Supplier </title> 
</head>
<body>
<h1> ADD SUPPLIER </h1>
<?php 

    // Include config file
    require_once "config.php";

    $sql =  "INSERT INTO supplier(CompanyName, ContactPerson, Email, Phone) VALUES (?, ?, ?, ?)";
   //$stmt = mysqli_prepare($link,$sql);
    // mysqli_stmt_bind_param($stmt, 'ssss', $CompanyName, $ContactPerson, $Email, $Phone);

    if($stmt = mysqli_prepare($link, $sql)){
        // Bind variables to the prepared statement as parameters
        mysqli_stmt_bind_param($stmt, "ssss", $CompanyName, $ContactPerson, $Email, $Phone);
        
         // Set parameters
        $CompanyName = trim('TOM TEST');
        $ContactPerson = trim('testCompany');
        $Email = trim('tom@testCompany.com');
        $Phone = trim('021 789 123');

        // Attempt to execute the prepared statement
        if(mysqli_stmt_execute($stmt)){
            // Password updated successfully. Destroy the session, and redirect to login page
            session_destroy();
            header("location: suppliers.php");
            exit();
        } else{
            header("location: dashboard.php");
        }

        // Close statement
        mysqli_stmt_close($stmt);
    }
    ?>



</body>
</html>