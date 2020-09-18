<?php
        $servername = "autostockordering.cwhehy370roy.ap-southeast-2.rds.amazonaws.com";
        $username = "admin_Tom";
        $password = "q2vGUCYoA1PgDS9EFd5L";
        $dbname = "MainDB";

        // Create connection
        //$conn = new mysqli($servername, $username, $password);
        $conn = new mysqli($servername, $username, $password, $dbname);

    
        // Check connection
        if ($conn->connect_error) {
            die("Connection failed: " . $conn->connect_error);
        } 


            $sql = "SELECT * FROM order_header";
            $result = $conn->query($sql);

            if ($result->num_rows > 0) {
            // output data of each row
            while($row = $result->fetch_assoc()) {
                echo "id: " . $row["OrderID"]. " - Created: " . $row["DateCreated"]. " Status: " . $row["Status"]. "<br>";
            }
            } else {
            echo "0 results";
            }
            $conn->close();
?>

        