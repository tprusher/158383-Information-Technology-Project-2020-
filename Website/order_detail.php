
158383-Information-Technology-Project-2020-/Supplier_Email.py

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

<!DOCTYPE HTML>

<!-- Website for 158.383 Information Technology Project  -->

<!-- Homepage -->

<html>

<!-- ##############################################     HEAD ELEMENT      ############################################################## -->

<head>

    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="supportfiles/reset.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>

    <!-- ************************Page Title********************************* -->
    <title>Stock Ordering System - Order Detail</title>

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

    <?php 
        if (isset($_GET['orderFilterID'])) {
            echo $_GET['orderFilterID'];
            $z = $_GET['orderFilterID'];
        } else {
            echo '** ERROR **';
        }

    $sql = "
        SELECT
            od.OrderID, 
           -- od.OrderLineUUID,
            od.Date,
            su.CompanyName,
            s.SupplierSKU,
            s.ProductName as ProductName,
            case when (s.MinSOH - s.SOH) >= s.MOQ then (s.MinSOH - s.SOH) else (s.MaxSOH - s.SOH) end OrderQty,
            od.Total,
            od.Status

        FROM
            order_detail od 
            Join stock s on od.ItemID = s.ItemID 
            Join supplier su on od.SupplierID = su.SupplierID

        WHERE
            od.OrderID =  $z

          ORDER BY Date
          ;";

    $result = $link->query($sql); 
    

    ?>



</head>

<!-- #################################################     PAGE BODY     ############################################################## -->

<body>


    <div id="header">
        <h1>View Order Detail</h1>
        <a href="logout.php"><span class="iconFont">(</span> Log Out</a>
        <a href="dashboard.php"><span class="iconFont">!</span> Dashboard</a>
    </div>

    <div id="main">
        <?php if (count($result) > 0): ?>
        <table id="ordersTable">
            <thead>
                <tr>
                    <th>Order ID </th>
                    <!-- <th>Order Line ID </th> -->
                    <th>Creation </th>
                    <th> Supplier </th> 
                    <th> Supplier SKU </th>
                    <th> Product </th>
                    <th> Order Qty </th>  
                    <th> Value </th>
                    <th> Status </th>
                </tr>
            </thead>
            <tbody>
                <?php foreach ($result as $row): array_map('htmlentities', $row); ?>
                
                <tr id = '<?php 
                            if ($row['Status'] === 'Approved') {
                                echo 'TRUE';
                            } else {
                                echo "FALSE";
                            }
                        ?>'>
                    <td><?php echo implode('</td><td>', $row); ?></td>

                    <!-- <td><a href='#'> TEST </a></td>  -->
                </tr>
                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>
        <a href="<?php echo '/approveOrder.php?orderFilterID='.$row['OrderID'] ?>" id='<?php 
                            if ($row['Status'] === 'Approved') {
                                echo 'HIDDEN_TRUE';
                            } else {
                                echo "FALSE";
                            }
                        ?>'>
             <button class="button button1"> Approve </button></a>




        <a href="<?php echo '/editOrder.php?orderFilterID='.$row['OrderID'] ?>" id='<?php 
                            if ($row['Status'] === 'Approved') {
                                echo 'HIDDEN_TRUE';
                            } else {
                                echo "FALSE";
                            }
                        ?>'>   
            <button class="button button2"> Edit </button></a>




        <a href="<?php echo '/deleteOrder.php?orderFilterID='.$row['OrderID'] ?>" id='<?php 
                            if ($row['Status'] === 'Approved') {
                                echo 'HIDDEN_TRUE';
                            } else {
                                echo "FALSE";
                            }
                        ?>'> <button class="button button4"> Delete </button></a>


        <a href="<?php echo '/orders.php' ?>">    <button class="button button3"> Back </button></a>
    </div>

    <div id="footer">

    </div>

<style>

    .button {
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border-radius: 12px;
    }

    .button1 {background-color: green;} /* Green */
    .button2 {background-color: orange;} /* Blue */
    .button3 {background-color: grey;} /* Blue */
    .button4 {background-color: black;} /* Blue */

    #TRUE { 
    background-color: rgba(0, 255, 0, 0.2);
    }  /* green with opacity */


    #FALSE { 
        background-color:  rgba(253, 227, 167, 0.4);  /* red with opacity */
    }

    #HIDDEN_TRUE { 
        display: none;
    }

</style>




</body>
</html>
