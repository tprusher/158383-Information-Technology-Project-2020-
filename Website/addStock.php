
<?php

// Initialize the session
 session_start();

    // Include config file
    require_once "config.php";

// Check if the user is logged in, if not then redirect him to login page
if(!isset($_SESSION["loggedin"]) || $_SESSION["loggedin"] !== true){
    header("location: index.php");
    exit;
}
?>


<?php

    //Set variables from POST data
    $Name = $_POST["item-name"];
    $Price = $_POST["price"];
    $ShelfLife = $_POST["shelfLife"];
    $SupplierSKU = $_POST["SupplierSKU"];
    $SupplierID = $_POST["SupplierID"];
?> 

<?php

    // Check input errors before updating the database
    if(empty($new_password_err) && empty($confirm_password_err)){
        // Prepare an update statement
        $sql = "INSERT INTO stock(ProductName, Price, ShelfLife, SupplierID, SupplierSKU) VALUES (?,?,?,?,?)";
        
        if($stmt = mysqli_prepare($link, $sql)){
            // Bind variables to the prepared statement as parameters
            mysqli_stmt_bind_param($stmt, "siiii", $Name, $Price, $ShelfLife, $SupplierID, $SupplierSKU);
             
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