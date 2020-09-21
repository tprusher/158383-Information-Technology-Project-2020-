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
            
            // Hide confirm div by setting display to none
            $(".no-button").click(function() {
                $("#confirmBG").css("display", "none");
            });

            // Show addSupplier div by setting display to block
            $(".confirm-button").click(function() {
                $("#confirmBG").css("display", "block");
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
    
    $SupplierID = $_POST["SupplierID"];
    
    $GETsql1 = "SELECT * FROM supplier WHERE SupplierID = $SupplierID";
    $GETsql2 = "SELECT stock.ItemID, stock.ProductName, stock.Price, stock.ShelfLife, stock.SupplierID, stock.SupplierSKU FROM stock join supplier on stock.SupplierID = supplier.SupplierID WHERE stock.SupplierID = $SupplierID";
    
    $result1 = $link->query($GETsql1);
    $result2 = $link->query($GETsql2);

    ?>


</head>

<!-- #################################################     PAGE BODY     ############################################################## -->

<body>
    <?php if (count($result1) > 0): ?>
    <div id="header">
        <h1>
            <?php foreach ($result1 as $row1): array_map('htmlentities', $row);
                echo $row1["CompanyName"];
                endforeach;
            ?>
        </h1>
        <h2>ID: <?php echo $SupplierID; ?></h2>
        <a href="suppliers.php"><span class="iconFont">0</span> Cancel</a>
    </div>

    <div id="main">
        <div id="deleteButton">
        <button type="button" class="confirm-button">
            <span class="iconFont">+</span> Delete Supplier
        </button>
        </div>
            <!-- Hidden div made visible via jQuery -->

            <div id="confirmBG">
                <div id="confirm">
                    <h2> Are you sure you want to delete <?php foreach ($result1 as $row1): array_map('htmlentities', $row);
                echo $row1["CompanyName"];
                endforeach; ?>?</h2>
                    <form action="deleteSupplier.php" method="post">
                        <button type="submit"><span class="iconFont">1</span> Yes</button>
                        <button type="button" class="no-button"><span class="iconFont">0</span> No</button>
                        <input type="hidden" id="hiddenSupplierID" name="SupplierID" value="<?php echo $SupplierID; ?>">
                    </form>
                </div>
            </div>

            <!-- End of hidden div -->
        <div id="editSupplierForm">
            <form action="changeSupplierDetail.php" method="post">
                <label>Supplier Name: </label>
                <input type="text" value="<?php foreach ($result1 as $row1): array_map('htmlentities', $row);
                echo $row1["CompanyName"];
                endforeach;
            ?>" name="CompanyName"><br>
                <label>Contact Person: </label>
                <input type="text" value="<?php foreach ($result1 as $row1): array_map('htmlentities', $row);
                echo $row1["ContactPerson"];
                endforeach;
            ?>" name="ContactPerson"><br>
                <label>Contact Phone: </label>
                <input type="text" value="<?php foreach ($result1 as $row1): array_map('htmlentities', $row);
                echo $row1["Phone"];
                endforeach;
            ?>" name="Phone"><br>
                <label>Contact Email: </label>
                <input type="email" value="<?php foreach ($result1 as $row1): array_map('htmlentities', $row);
                echo $row1["Email"];
                endforeach;
            ?>" name="Email">
                <input type="hidden" id="hiddenSupplierID" name="SupplierID" value="<?php echo $SupplierID; ?>">
                <button type="submit" id="save"><span class="iconFont">&</span> Save</button>
            </form>
        </div>
        <div id="editSupplierTable">
            <button type="button" class="show-button" id="addStockButton"><span class="iconFont">5</span> Add</button>
            <h1>Stock Items</h1>
            <?php endif; ?>

            <!-- Hidden div made visible via jQuery -->

            <div id="addStockBG">
                <button type="button" class="hide-button" id="hideAddStock"><span class="iconFont">0</span></button>
                <div id="addStock">
                    <h2> Enter new stock details below</h2>
                    <form action="addStock.php" method="post">
                        <label for="item-name">Item name:</label>
                        <input type="text" id="item-name" name="item-name" value="">
                        <br>
                        <label for="price">Price:</label>
                        <input type="text" id="price" name="price" value="">
                        <br>
                        <label for="shelfLife">Shelf Life:</label>
                        <input type="number" id="shelfLife" name="shelfLife" value="">
                        <br>
                        <label for="SupplierSKU">Supplier SKU:</label>
                        <input type="text" id="SupplierSKU" name="SupplierSKU" value="">
                        <br>
                        <input type="hidden" id="hiddenSupplierID" name="SupplierID" value="<?php echo $SupplierID; ?>">
                        <input id="submit" type="submit" value="Submit">
                    </form>
                </div>
            </div>

            <!-- End of hidden div -->

            <?php if (count($result2) > 0): ?>
            <div id="stockTable">
                <table>
                    <thead>
                        <tr>
                            <th>Item ID</th>
                            <th>Name</th>
                            <th>Price</th>
                            <th>Shelf Life</th>
                            <th>Supplier ID</th>
                            <th>Supplier SKU</th>
                            <th>Edit </th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($result2 as $row2): array_map('htmlentities', $row); ?>
                        <tr>
                            <td><?php echo implode('</td><td>', $row2); ?></td>
                            <td >
                            <!-- <form action="editStock.php" method="post"> -->

                            <a href=<?php echo '/editStock.php?mySupplierID='.$row2['SupplierID'].'&myStockID='.$row2['ItemID']

                             ?>> EDIT 
                             </a></td> 

                        </tr>
                        <?php endforeach; ?>
                        <?php endif; ?>
                    </tbody>
                </table>
            </div>
        </div>

    </div>

    <div id="footer">

    </div>

</body>

</html>
