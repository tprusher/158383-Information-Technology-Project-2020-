

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
?>


<!DOCTYPE HTML>


<html>

<!-- ##############################################     HEAD ELEMENT      ############################################################## -->

<head>

</head>

<body>

<h1> UPDATE SCRIPT </h1>
<p>
    <?php 
    echo 
    $supplierIdFilter = $_GET["supplierFilter"];
    $stockIdFilter = $_GET["itemFilter"];
    $item_name = $_GET["itemName"];
    $item_price = $_GET["Price"];
    $item_life = $_GET["shelfLife"];
    $item_supplSKU = $_GET["supplierSKU"];
    ?>
</p>


<?php

    // UPDATE stock SET ProductName = 'FANTA 1.0', Price = 123 , ShelfLife = 456, SupplierSKU = 789 WHERE ItemID = 10 


    // Check input errors before updating the database
    if(empty($new_password_err) && empty($confirm_password_err)){
        // Prepare an update statement
        $sql = "UPDATE stock SET ProductName = ?, Price = ?, ShelfLife = ?, SupplierSKU = ? WHERE ItemID = ?";
        
        if($stmt = mysqli_prepare($link, $sql)){
            // Bind variables to the prepared statement as parameters
            mysqli_stmt_bind_param($stmt, "siiii", $item_name, $item_price, $item_life, $item_supplSKU,  $stockIdFilter);
             
            // Attempt to execute the prepared statement
            if(mysqli_stmt_execute($stmt)){
                // Password updated successfully. Destroy the session, and redirect to login page
               // session_destroy();
                header("location: suppliers.php");
              //  exit();
            } else{
                echo "Oops! Something went wrong. Please try again later.";
            }

            // Close statement
            mysqli_stmt_close($stmt);
        }
    }
   
    // Close connection
    mysqli_close($link);

?>



</body>
</html>

