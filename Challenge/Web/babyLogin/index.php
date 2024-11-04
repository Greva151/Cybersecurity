<?php

$db = mysqli_connect($_ENV['DB_HOST'], $_ENV['DB_USER'], $_ENV['DB_PASSWD'], $_ENV['DB_NAME']);
if (!$db) {
    die("db connection failed");
}

$message = '';
if (isset($_POST['username']) && isset($_POST['password'])) {
    $result = mysqli_query($db, "select * from users where username = '" . $_POST['username'] . "' and password = '" . $_POST['password'] . "'");
    if ($result->num_rows > 0) {
        $message = "You are authenticated! Flag: " . $_ENV["FLAG"];
    } else {
        $message = "Wrong username or password";
    }
}

?>

<html lang="en">
<head>
    <title>baby login</title>
</head>
<body>
<form action="/" method="post">
    <label>
        Username
        <input type="text" name="username">
    </label>
    <label>
        Password
        <input type="password" name="password">
    </label>
    <input type="submit">
</form>

<?php if ($message) { ?>
    <h2><?php echo $message ?></h2>
<?php } ?>
</body>
</html>
