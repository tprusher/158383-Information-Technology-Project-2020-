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

    <?php 
    $sql = "
    -- Order ID 	Creation 	Status 	Detail

    Select
        oh.OrderID, 
        oh.DateCreated,
        od.CompanyName,
        oh.Status
    
    From
        MainDB.order_header oh 
        
        Join (
            Select 
                od.OrderID,
                s.CompanyName,
                count(*) LineCount
            
            From   
            MainDB.order_detail od 
            
            Join MainDB.supplier s 
                on od.SupplierID = s.SupplierID
                
            Group by od.OrderID, s.SupplierID
            ) od on	oh.OrderID = od.OrderID
            
        Order By oh.DateCreated;";

        
    $sql2 = "Select OrderID from order_detial;";

    $result = $link->query($sql); 
    $result2 = $link->query($sql2); 
    
    ?>

</head>

<!-- #################################################     PAGE BODY     ############################################################## -->

<body>


    <div id="header">
        <h1>View Orders</h1>
        <a href="logout.php"><span class="iconFont">(</span> Log Out</a>
        <a href="dashboard.php"><span class="iconFont">!</span> Dashboard</a>
    </div>

    <div id="main">
        <!-- <h1>Hello</h1> -->
        <?php if (count($result) > 0): ?>
        <table id="ordersTable">
            <thead>
                <tr>
                    <th> Order ID </th>
                    <th> Creation </th>
                    <th> Supplier </th>
                    <th> Status </th>
                    <th> Detail </th> 
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
                    <td><a href=<?php echo '/order_detail.php?orderFilterID='.$row['OrderID'] ?>> Order Detail </a></td> 

                </tr>

                <?php endforeach; ?>
            </tbody>
        </table>
        <?php endif; ?>
    </div>

    <div id="footer">

    </div>

<style> 
a:hover {
    color: red; 
    font-size: 15px;
}

#TRUE { 
    background-color: rgba(0, 255, 0, 0.2);
    }  /* green with opacity */


#FALSE { 
    background-color:  rgba(253, 227, 167, 0.4);  /* red with opacity */
}



</style> 

</body>

</html>
