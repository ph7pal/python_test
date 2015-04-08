<?php

$total=1092;
for($i=1;$i<=$total/30;$i++){
	$one_line='context=%7B%22SearchId%22%3A%22991110408152956001%22%2C%22CurrencyCode%22%3A%22USD%22%2C%22PageNo%22%3A'.$i.'%2C%22PageSize%22%3A30%2C%22SortId%22%3A1%2C%22SortParameter%22%3A%22%22%2C%22Filters%22%3A%7B%22HotelName%22%3A%22%22%2C%22AreaID%22%3A0%2C%22Facilities%22%3A%22%22%2C%22MinPrice%22%3A-1%2C%22MaxPrice%22%3A-1%2C%22ExtendedFilters%22%3A%5B%5D%2C%22AreaList%22%3A%22%22%7D%2C%22RealLanguageId%22%3A8%2C%22LanguageId%22%3A8%2C%22AbUser%22%3A%22A%22%2C%22PageTypeId%22%3A103%2C%22UrlVersion%22%3A1%2C%22LanguageDomain%22%3A%22zh-cn%22%2C%22CultureName%22%3A%22zh-cn%22%2C%22MaximumLoop%22%3A10%2C%22WaitTime%22%3A1000%2C%22ActionType%22%3A4%2C%22ASQ%22%3A%22mbtnRq82z%2BseDpxq%2BleSn7QRBsidwx7HfcJYwTm6TkOj%2FiTIUs9mU3%2BwoVhZ10HYSPQi4sxxP%2BtRJJxIj%2BtkbnAor8ICMvuEwOe3afsIPEC1kZDlZQE9pdrUG%2BuSju1w0NR51pLpkyaGEdUC02z%2FzYFoyJaFh3VT6BoENjJxzTeS7m7ZId2y3tU5YfHtY46TbUoEH8BR6t9zIx2I08CRSEMRz7vyDVfetG3boTADNPshStW%2F5cdn%2F6TuzRBxMjpjkbaDieS%2B2QrSnhh7DirSjt6ReJQocPGxfbJ%2BnFPfU0EZf6SBK1Pkk4HOHXIpnuZ5boLBR6mYnnPWcfXkPciGtw%3D%3D%22%2C%22LoopCount%22%3A1%2C%22StoreFrontId%22%3A3%2C%22CheckInDate%22%3A%22%22%2C%22CheckOutDate%22%3A%22%22%2C%22ReviewTravellerType%22%3A-1%2C%22IsMapSearch%22%3Afalse%7D';
	file_put_contents('urls.txt',$one_line.PHP_EOL,FILE_APPEND);		
}
echo 'done';