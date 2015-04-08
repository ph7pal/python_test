<?php
ini_set('memory_limit', '256M');
ini_set('max_execution_time', '1800');
error_reporting(E_ERROR);

  include 'func.php';
  
  $dir="H:\\agoda\\shouer\\pages";
  $files=myReadDir($dir,false); 
  $page = isset($_GET['page']) ? $_GET['page'] : 1;
  $num = 100;
  $start = ($page - 1) * $num;
  $data = array_slice($files, $start, $num);
  if(!empty($data)){
  	foreach($data as $name){
  		$_dir=$dir.'\\'.$name;
  		$html=file_get_contents($_dir);
  		//echo $html;
  		//exit();
  		myMatch($html);
  		}
  		$success='正在处理第'.$page.'页';
  		$waitSecond=1;
  		$jumpUrl='http://localhost/agoda/a_match.php?page='.($page+1); 
  }else{
  	exit('WELL DONE!!');
  }
  function myMatch($response){
        preg_match('/class=\"fontxlargeb\"[^>]*>(.*?)<\/span>/si', $response, $title);
        preg_match('/<p\s*class=\"fontsmalli\s*sblueboldunder\">(.*?)<\/p>/si', $response, $address);
        preg_match('/latitude=(.*?)&amp;longitude=(.*?)&/si',$response,$latlng);        
        preg_match('/<link\s*rel=\"canonical\"\s*href=\"(.*?)\"/si',$response, $bookurl);


        preg_match('/入住办理时间从<\/div>\s*<div\s*class=\"floatleft\">([^<]+)<\/div>/si', $response, $checkin);
        preg_match('/退房办理时间至<\/div>\s*<div\s*class=\"floatleft\">([^<]+)<\/div>/si', $response, $checkout);
        preg_match('/hstars(\d+)/si',$response,$star);
        $_add=strip_tags($address[1]);
        $_add=str_replace('(显示地图)','',$_add);
        $address_cn = filter($_add);
        preg_match('/id=\"hotelDescription\"[^>]*>(.*?)<\/span>/si', $response, $content);
        $desc = strip_tags($content[1]);
        $data = array();
        $data['columnid'] = 100020;
        $data['title_cn'] = $title[1];
        $data['title_en'] = '';
        $data['address_cn'] = $address_cn;
        $data['address_en'] = '';
        $data['content'] = $desc;
        $data['score'] = 3;
        $data['long'] = $latlng[2];
        $data['lat'] = $latlng[1];
        $data['star'] = $star[1];
        $data['rooms'] = '';
        $data['checkintime'] = filter($checkin[1]);
        $data['checkouttime'] = filter($checkout[1]);
        $data['openTime'] = '';
        $data['pinyin'] = '';
        $data['status'] = 1;
        $data['cTime'] = time();
        $data['bookurl']=filter($bookurl[1]);
        $data['booktitle']='agoda';

        $currentFile = 'agoda_data/shouer/'.uniqid().'.php';
        $fp = fopen($currentFile, 'w+');
        $str = '<?php return ' . var_export($data, true) . ';';
        fputs($fp, $str);
        fclose($fp);
 } 
 ?>
  	
<style>
html, body{margin:0; padding:0; border:0 none;font-family:microsoft yahei,tahoma,simsun,Helvetica,Arial,sans-serif;background: #FFF;}
a{text-decoration:none; color:#174B73;}
a:hover{color:#F60;}
div.message{margin:100px auto 0 auto;clear:both;text-align:center; width:450px;border:1px solid #04AEDA}
.msg,.tip,.error,.success{width:100%;height:50px;line-height:50px}
.msg{background:none;font-size:14px}
.msg{background:none;color:#04AEDA}
.tip{font-size:12px;color:#FFF;background:#04AEDA}
.wait{color:#C71585;font-weight:bold}
.error{color:#C71585}
.success{color:green}
</style>   
<div class="message">	
<div class="msg">
<?php if(!empty($success)){?>
 <p class="success"><?php echo($success); ?></p>   
<?php }else{?>
 <p class="error"><?php echo($error); ?></p>   
<?php }?>   
    
</div>
<div class="tip">
<p class="detail"></p>
<p class="jump">
页面自动 <a id="href" href="<?php echo($jumpUrl); ?>" target="_top">跳转</a> 等待时间： <b id="wait"><?php echo($waitSecond); ?></b>
</p>
</div>
</div>
<script type="text/javascript">
(function(){
var wait = document.getElementById('wait'),href = document.getElementById('href').href;
var interval = setInterval(function(){
	var time = --wait.innerHTML;
	if(time <= 0) {
		location.href = href;
		clearInterval(interval);
	};
}, 1000);
})();
</script>