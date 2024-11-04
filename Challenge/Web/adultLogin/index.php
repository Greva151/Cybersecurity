<?php

$db = mysqli_connect($_ENV['DB_HOST'], $_ENV['DB_USER'], $_ENV['DB_PASSWD'], $_ENV['DB_NAME']);
if (!$db) {
    die("db connection failed");
}

$message = '';
if (isset($_POST['username']) && isset($_POST['password'])) {
    $result = mysqli_query($db, "select password from users where username = '" . $_POST['username'] . "'");
    if ($result->num_rows > 0) {
        $row = mysqli_fetch_assoc($result);
        if ($_POST['password'] !== $row['password']) {
            $message = "Wrong password";
        } else {
            $message = "You are authenticated! You have the flag right?";
        }
    } else {
        $message = "Wrong username";
    }
}

?>

<html lang="en">
<head>
    <title>adult login</title>
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
