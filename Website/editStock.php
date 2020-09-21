
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
                $("#addStockBG").css("display", "none");
            });

            // Show addSupplier div by setting display to block
            $(".show-button").click(function() {
                $("#addStockBG").css("display", "block");
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

</head>

<!-- #################################################     PAGE BODY     ############################################################## -->

<body>

    <?php 
    // RUN ALL THE QUERIES IN THIS BLOCK; 


    // EXAMPLE OF DATA BEING PASSED IN VIA URL
    // http://52.65.44.236/editStock.php?mySupplierID=1&myStockID=10
    
    if (isset($_GET['mySupplierID'])) {
        $supplierIdFilter = $_GET['mySupplierID'];
    } else {
        echo '** ERROR **';
    }

    if (isset($_GET['myStockID'])) {
        $stockIdFilter = $_GET['myStockID'];
    } else {
        echo '** ERROR **';
    }

    $GETsql1 = "SELECT * FROM supplier WHERE SupplierID = $supplierIdFilter";
    $GETsql2 = "SELECT * FROM stock WHERE ItemID = $stockIdFilter";

    $result1 = $link->query($GETsql1);
    $result2 = $link->query($GETsql2);
?> 

    <div id="header">
    
        <!-- <h1>Danny's Drinks</h1> -->
        <h1>
            <?php 
                foreach ($result1 as $row1): array_map('htmlentities', $row);
                echo $row1["CompanyName"];
                endforeach;
            ?>
        </h1>
        
        <a href="suppliers.php"><span class="iconFont">0</span> Cancel</a>
    </div>

    <div id="main">
        <div id="itemDetails">
        <?php 
                foreach ($result2 as $row2): array_map('htmlentities', $row);
                ?>

                <h1> <?php  echo $row2["ProductName"]; ?> </h1>
                <h2> <?php  echo $row2["SupplierSKU"]; ?> </h2>
                <?php endforeach; ?>
        
        </div>
        <div id="editStockForm">
            <form action= "updateStock.php" method='get'>

                <label>Item Name: </label>
                <input type="text" name = 'itemName'><br>
                <label>Price: </label>
                <input type="text" name = 'Price'><br>
                <label>Shelf Life: </label>
                <input type="text" name = 'shelfLife'><br>
                <label>Supplier SKU: </label>
                <input type="text" name = 'supplierSKU'>

                <!-- <label> SUPPLIER FILTER </label> -->
                <input type='hidden' name='supplierFilter' value= '<?php echo $supplierIdFilter ?>'>
                
                <!-- <label> STOCK FILTER </label> -->
                <input type='hidden' name='itemFilter' value= '<?php echo $stockIdFilter ?>'>
            

                <input id="submit" type="submit" value="Save">
                
            </form>
        </div>
    </div>
    <div id="footer">   
    <h1> 
        </h1>

    </div>

</body>

</html>
