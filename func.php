<?php

function myReadDir($dir, $name = true) {
    $name_arr = array();
    if (is_dir($dir)) {
      if ($dh = opendir($dir)) {
        while (($file = readdir($dh)) !== false) {
          if ($file != "." && $file != "..") {
            if ($name) {
              $_tmp = explode('.', $file);
              $name_arr[] = $_tmp[0];
            } else {
              $name_arr[] = $file;
            }
          }
        }
        closedir($dh);
      }
    }
    return $name_arr;
  }
  function filter($content) {
    $content = str_replace(
            array('&#39;', '&#160;', '&#183;', '&#176;', '&#233;', '&amp;', '&nbsp;', '&#47;', "　", "\t", "\n", "\r"), array("'", " ", "·", '°', 'é', '&', ' ', '/'," ", "", "", ""), $content
    );
    $content = trim($content);
    return $content;
  }
  function test($data) {
    echo '<pre>';
    print_r($data);
    echo '</pre>';
  }