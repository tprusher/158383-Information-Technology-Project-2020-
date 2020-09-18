<html>
    <head>
    </head>
    <body>
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

        <h1> 
            <?php 
            // Get Order ID << CONTEXT >> 
                if (isset($_GET['orderFilterID'])) {
                    echo 'ORDER ID: '.$_GET['orderFilterID'];
                    $z = $_GET['orderFilterID'];
                    } else {
                    echo '** ERROR **';
                }
            ?>
        </h1> 

        <h1> 
            <?php 
                $z = $_GET['orderFilterID'];
                $mySQL = "UPDATE order_header SET Status = 'Approved' WHERE OrderID = ?;";
                // echo $mySQL;

                if($stmt = mysqli_prepare($link,  $mySQL)){
                    // Bind variables to the prepared statement as parameters
                    mysqli_stmt_bind_param($stmt, "s", $z);
                                        
                    // Attempt to execute the prepared statement
                    if(mysqli_stmt_execute($stmt)){

                        //header("location: orders.php");
                        //exit();
                    } else{
                        //header("location: /approveOrder.php?orderFilterID=$z");
                    }
            
                    // Close statement
                    mysqli_stmt_close($stmt);
                }
              
            ?>
        </h1> 
        <h1> 
            <?php 
                $z2 = $_GET['orderFilterID'];
                $mySQL2 = "UPDATE order_detail SET Status = 'Approved' WHERE OrderID = ?;";
                // echo $mySQL;

                if($stmt = mysqli_prepare($link,  $mySQL2)){
                    // Bind variables to the prepared statement as parameters
                    mysqli_stmt_bind_param($stmt, "s", $z2);
                                        
                    // Attempt to execute the prepared statement
                    if(mysqli_stmt_execute($stmt)){

                        header("location: orders.php");
                        exit();
                    } else{
                        header("location: /order_detail.php?orderFilterID=$z");
                    }
            
                    // Close statement
                    mysqli_stmt_close($stmt2);
                }
            ?>
        </h1> 
    </body>
</html>