<?
$conf_str = file_get_contents('config.js');
$s = str_replace('const Config = ', '', $conf_str);
$s = preg_replace('/([a-zA-Z_]+):/', '"$1":', $s);
$s = preg_replace("/'([^']+)'/", '"$1"', $s);
$cnf = json_decode($s, true);
$lang = $cnf[$cnf['lang']];
$shop = $cnf['email_address'];
$cust = $_POST['email'];
$order = htmlspecialchars($_POST['orderletter']);

mail($shop, $shop, $lang['order'], $o);
mail($shop, $cust, $lang['order_confirm'], $o);
?>
<!DOCTYPE html>
<html>
<head>
    <title>Potvrď objednávku</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="{{ site_root }}/style.css">
</head>
<body>
    <a href="{{ site_root }}/">Eshop</a>
    <h2>Ďakujeme za Vašu objednávku</h2>
    <pre id="order"><?= $order ?></pre>
    <script src="{{ site_root }}/config.js"></script>
    <script src="{{ site_root }}/lang.js"></script>
    <script src="{{ site_root }}/shop.js"></script>
    <script>window.addEventListener("load", CartData.clear);</script>
</body>
</html>
