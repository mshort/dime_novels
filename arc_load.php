
<?php

/* ARC2 static class inclusion */
include_once('/var/www/drupal/htdocs/sites/all/libraries/arc2/ARC2.php');

/* configuration */
$config = array(
  /* db */
  'db_host' => 'localhost', /* optional, default is localhost */
  'db_name' => 'arc2',
  'db_user' => 'xxxx',
  'db_pwd' => 'xxxx',

  /* store name (= table prefix) */
  'store_name' => 'dimenovels_store',
);

/* instantiation */
$store = ARC2::getStore($config);

if (!$store->isSetUp()) {
  $store->setUp();
}

$q = 'LOAD <file:///var/www/drupal/htdocs/sites/all/scripts/dimenovels.nt>';

$store->query($q);
?>
