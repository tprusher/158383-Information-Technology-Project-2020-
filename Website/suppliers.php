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

<!-- Website for 158.383 Information Technology Project  -->

<!-- Homepage -->

<html>

<!-- ##############################################     HEAD ELEMENT      ############################################################## -->

<head>

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="supportfiles/reset.css">

    <!-- ************************Page Title********************************* -->
    <title>Stock Ordering System</title>

    <!-- *********************Website Description*************************** -->
    <meta name="description" content="Website for 158.383 Information Technology Project. ">

    <!-- *************************Favicon*********************************** -->
    <link rel="icon" href="files/favicon.ico" type="image/x-icon">

    <!-- ********************** Icon Font ********************************* -->
    <link rel="stylesheet" type="text/css" href="supportfiles/icon_font/style.css">

    <!-- **********************CSS Document********************************* -->
    <link rel="stylesheet" type="text/css" href="styles.css">

    <!-- **********************Google Fonts********************************* -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">



    <!-- *********************Add jQuery************************************ -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>

    <!-- **********************Javascript*********************************** -->
    <script>
        $(document).ready(function() {
            // Hide addSupplier div by setting display to none
            $(".hide-button").click(function() {
                $("#addSupplierBG").css("display", "none");
            });

            // Show addSupplier div by setting display to block
            $(".show-button").click(function() {
                $("#addSupplierBG").css("display", "block");
            });

        });

    </script>

    <!-- Style to remove arrows from number input -->

    <style>
        /* Chrome, Safari, Edge, Opera */
        input::-webkit-outer-spin-button,
        input::-webkit-inner-spin-button {
            -webkit-appearance: none;
            margin: 0;
        }

        /* Firefox */
        input[type=number] {
            -moz-appearance: textfield;
        }

    </style>


    <?php 
    $GETsql = "SELECT * FROM supplier";
    
    $result = $link->query($GETsql);
    
    // Processing form data when form is submitted
    if($_SERVER["REQUEST_METHOD"] == "POST"){
  
        //Set variables from POST data
        $CompanyName = $_POST["CompanyName"];
        $ContactPerson = $_POST["ContactPerson"];
        $Email = $_POST["Email"];
        $Phone = $_POST["Phone"];
        
    $POSTsql =  "INSERT INTO supplier(CompanyName, ContactPerson, Email, Phone) VALUES (?, ?, ?, ?)";
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
    }
    ?>


</head>

<!-- #################################################     PAGE BODY     ############################################################## -->

<body>

    <div id="header">
        <h1>Suppliers</h1>
        <a href="logout.php"><span class="iconFont">(</span> Log Out</a>
        <a href="dashboard.php"><span class="iconFont">!</span> Dashboard</a>
    </div>

    <div id="main">
        <button type="button" class="show-button" id="addSupplierButton"><span class="iconFont">5</span> Add Supplier</button>

        <!-- Hidden div made visible via jQuery -->

        <div id="addSupplierBG">
            <button type="button" class="hide-button" id="hideAddSupplier">Close <span class="iconFont">0</span></button>
            <div id="addSupplier">
                <h2> Enter new supplier details below</h2>
                <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                    <label for="sup-name">Supplier name:</label>
                    <input type="text" id="CompanyName" name="CompanyName" value="">
                    <br>
                    <label for="sup-contactperson">Contact Person:</label>
                    <input type="text" id="ContactPerson" name="ContactPerson" value="">
                    <br>
                    <label for="sup-phone">Phone Number:</label>
                    <input type="number" id="Phone" name="Phone" value="">
                    <br>
                    <label for="sup-email">Email Address:</label>
                    <input type="email" id="Email" name="Email" value="">
                    <br>
                    <input id="submit" type="submit" value="Submit">
                </form>
            </div>
        </div>

        <!-- End of hidden div -->

        <?php if (count($result) > 0): ?>
        <div id="supplierContainer">

            <?php foreach ($result as $row): array_map('htmlentities', $row); ?>
            <div class="supplier">
                <div class="supplierID"><?php echo $row["SupplierID"]; ?></div>
                <h1><?php echo $row["CompanyName"]; ?></h1>
                <h2><?php echo $row["ContactPerson"]; ?></h2>
                <div class="editSupplier">
                    <form action="editSupplier.php" method="post">
                        <button type="submit" name="SupplierID" value="<?php echo $row["SupplierID"]; ?>" class="editSupplierButton"><span class="iconFont">*</span> Edit</button>
                    </form>
                </div>
                <div class="contactContainer">
                    <p><a href="tel:+64211200211"><span class="iconFont">"</span> <?php echo $row["Phone"]; ?></a></p>
                    <p class="email"><a href="mailto:daniel.m@dannys.com" target="_blank"><span class="iconFont">#</span> <?php echo $row["Email"]; ?></a></p>
                </div>
            </div>

            <?php endforeach; ?>
        </div>
        <?php endif ?>

    </div>

    <div id="footer">

    </div>

</body>

</html>
