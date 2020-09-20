
<?php
        $servername = "autostockordering.cpgtqfncbzrl.us-east-1.rds.amazonaws.com";
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

        $sql = "SELECT od.* FROM order_detail od join ( Max(orderid) from order_header ) oh on od.orderid = oh.orderid ";
        $result = $conn->query($sql);
        ?>

<style>
    h1 { 
        text-align: center; 
        color: #00688B;
    }

    #order_detail_css {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
    }

    #order_detail_css td, #order_detail_css th {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
    }

    #order_detail_css tr:nth-child(even){
        background-color: #f2f2f2;
        }

    #order_detail_css tr:hover {
        background-color: #00BFFF;
        }

    #order_detail_css th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #00688B;
    color: white;
    text-align: center;
    }
</style>


<h1> Tom PHP Test - Table Data from : order_detail</h1> 

<?php if (count($result) > 0): ?>
<table id="order_detail_css">
  <thead>
    <tr>
        <th> OrderLineUUID </th>
        <th> OrderID </th>
        <th> Date </th>
        <th> SupplierID </th>
        <th> ItemID </th>
        <th> Total </th>
        <th> Status </th>
    </tr>
  </thead>
  <tbody>
<?php foreach ($result as $row): array_map('htmlentities', $row); ?>
    <tr>
      <td><?php echo implode('</td><td>', $row); ?></td>
    </tr>
<?php endforeach; ?>
  </tbody>
</table>
<?php endif; ?>


 <!-- Client Business Stuff -->

<p id = "ClientBusiness"> 
                    <br><b>Julian's Berry Farm and Cafe <b><br> 
                    <b> Address: <b> 12 Huna Road, Coastlands, Whakatane 3191<br>
                    <b> Phone:<b> 07-308 4253 <br>
                    <a href=" https://www.juliansberryfarm.co.nz/">
                    <img src="https://www.juliansberryfarm.co.nz/sites/www.juliansberryfarm.co.nz/files/logo.png" width="400" height="200"></a>
                    </p><br>