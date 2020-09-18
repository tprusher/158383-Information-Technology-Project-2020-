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


    <!-- ************************Page Title********************************* -->
    <title> USER LIST - TOM </title>

    <!-- *********************Website Description*************************** -->
    <meta name="description" content="Website for 158.383 Information Technology Project. ">

    <!-- *************************Favicon*********************************** -->
    <link rel="icon" href="files/favicon.ico" type="image/x-icon">


    <!-- **********************Google Fonts********************************* -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@100;200;300;400;500;600;700;800;900&display=swap" rel="stylesheet">

    <?php 
    $sql = "SELECT * FROM user_list";
    $result = $link->query($sql); 
    ?>

</head>

<body>

    <div id="header">
        <h1>View User DB</h1>
    </div>

    <div id="main">
        <!-- <h1>Hello</h1> -->
        <?php if (count($result) > 0): ?>
        <table id="user_detail_css">
            <thead>
                <tr>
                    <th>User_Id</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>Password</th>
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
    </div>

    <div id="footer">
    <a href="dashboard.php"> <button class="button button2"> Dashboard </button> </a>
    <a href="logout.php">    <button class="button button1">Log Out </button></a><br>
    
<?php
    session_start();
    echo "<h3> PHP List All Session Variables</h3>";
    foreach ($_SESSION as $key=>$val)
        echo $key." ".$val."<br/>";
        if($key=='username'){
            $z = $val;
        }
    
    echo $z."  NSAFjkasn <br/>";
?>

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
}

.button1 {background-color: grey;} /* Green */
.button2 {background-color: white;} /* Blue */


#user_detail_css {
    font-family: "Trebuchet MS", Arial, Helvetica, sans-serif;
    border-collapse: collapse;
    width: 100%;
    }

    #user_detail_css td, #user_detail_css th {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
    }

    #user_detail_css tr:nth-child(even){
        background-color: #e6e6e6;
        }
    
    #user_detail_css tr:nth-child(odd){
        background-color: #ffffff;
        }

    #user_detail_css tr:hover {
        background-color: #00BFFF;
        }

    #user_detail_css th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #00688B;
    color: white;
    text-align: center;
    }
    
    body {
      background-image: url('background-2721731__340.jpg');
      background-repeat: no-repeat;
      background-attachment: fixed;
      background-size: 100% 100%;
      color: black;

    }

    #footer {
        color: white;
    }
    
    h1, .outsideBox  { 
        text-align: center; 
        padding-bottom: 2.5%;
        padding-top: 2.5%;
        color: white;
    }
    
    .wrapper {
      margin: auto;
      width: 50%;
      height: 50%; 
      border: 3px solid white;
      padding: 10px;
      background-color: white;
    }
    
    a {
      color: red;
    }
    
    a:hover { 
        color: black;
        font-size: 16px;
    }
    
    #logo {
        background-color: white;
        display: block;
      margin-left: auto;
      margin-right: auto;
      width: 50%;
    }
    .center {
      margin-top: 1%;
      display: block;
      margin-left: auto;
      margin-right: auto;
      width: 50%;
    }
    
    .button {
        background-color: #4CAF50; /* Green */
    }
    
    </style> 
</body>
</html>