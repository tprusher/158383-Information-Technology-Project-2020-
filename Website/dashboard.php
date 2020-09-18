<?php
// Initialize the session
 session_start();
 
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

</head>

<!-- #################################################     PAGE BODY     ############################################################## -->

<body>

    <div id="header">
        <h1>Dashboard</h1>
        <a href="logout.php"><span class="iconFont">(</span> Log Out</a>
    </div>

    <div id="dashboardMain">
        <div id="welcomeMessage">
            <h1>Welcome, 
            <?php
                foreach ($_SESSION as $key=>$val)
                        //echo $key." ".$val."<br/>";
                        if($key=='username'){
                            $z = $val;
                            }
    
                            echo ucwords($z."<br/>");
                            ?> 
            </h1>
        </div>
        <div id="dashboardLinks">
            <div class="dashIconContainer">
                <a href="orders.php">
                    <div class="dashIcon">
                        <img src="webfiles/icons/order.png" alt="Orders">
                        <br>View Orders
                    </div>
                </a>
            </div>

            <div class="dashIconContainer">
                <a href="suppliers.php">
                    <div class="dashIcon">
                        <img src="webfiles/icons/supplier.png" alt="Orders">
                        <br>Suppliers
                    </div>
                </a>
            </div>

            <div class="dashIconContainer">
                <a href="stock.html">
                    <div class="dashIcon">
                        <img src="webfiles/icons/stock.png" alt="Orders">
                        <br>Stock Preferences
                    </div>
                </a>
            </div>

        </div>
    </div>



    <div id="fullFooter">
        <h2>2020</h2>
        <h1>158383 Information Technology Project</h1>
        <h2>Group 1</h2>
    </div>

</body>

</html>
