


<?php
    define('servername', 'autostockordering.cpgtqfncbzrl.us-east-1.rds.amazonaws.com');
    define('username', 'admin_Tom');
    define('password', 'q2vGUCYoA1PgDS9EFd5L');
    define('dbname', 'MainDB');

    // $servername = "autostockordering.cpgtqfncbzrl.us-east-1.rds.amazonaws.com";
    // $username = "admin_Tom";
    // $password = "q2vGUCYoA1PgDS9EFd5L";
    // $dbname = "MainDB";

    // Create connection
    //$conn = new mysqli($servername, $username, $password);

    $link = mysqli_connect(servername, username, password, dbname);

    
// Check connection
if($link === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
?>