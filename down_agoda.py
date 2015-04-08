#!/usr/bin/env python
#coding=utf-8
import urllib
import urllib2
import re
import threading
import time
import random
import sys
import uuid
import os

post_data = []
pageurl_list=[]
#获取图片地址函数
def imgurlList():
    global post_data
##    total=30
##    for i in range(total/30):
##        page=i+1
##        one_line={'context':{"SearchId":"991110408094838001","CurrencyCode":"USD","PageNo":page,"PageSize":30,"SortId":1,"SortParameter":"","Filters":{"HotelName":"","AreaID":0,"Facilities":"","MinPrice":-1,"MaxPrice":-1,"ExtendedFilters":[],"AreaList":""},"RealLanguageId":8,"LanguageId":8,"AbUser":"A","PageTypeId":103,"UrlVersion":1,"LanguageDomain":"zh-cn","CultureName":"zh-cn","MaximumLoop":10,"WaitTime":1000,"ActionType":4,"ASQ":"mbtnRq82z+seDpxq+leSn7QRBsidwx7HfcJYwTm6TkNuzXvBOYos5GpN9lR+MUAG7gZANVdzENvMKaIevSV3PEZQ79FrvVQmObA3achlSY53S9SXO1cpjd+A5W/k4oiWXUPBvmZ/Pz3v6aZlqNPv5BDO7Z8xO7/RoIDIMPuc4bxQomoKhu7IpTy6Ab8zIhzkJOaQwY7Giya55zNO7FWl2zLgaak3CB/pik83D0ZcYgg399ywXZxQZOZB4Xrx5MidlPc7+KlLTf4XcdZZSDI5Z0GXQFVtxB1ElwtXITA/9j+D2cxHwwk320UiGr2RW2Wm","LoopCount":1,"StoreFrontId":3,"CheckInDate":"","CheckOutDate":"","ReviewTravellerType":-1,"IsMapSearch":0}}
##        data=urllib.urlencode(one_line)
##        post_data.append(data)
##    print post_data
##    sys.exit()	
    fp=open("urls.txt", "r");
    for eachline in fp:
        eachline=eachline.replace('\r','')
        eachline=eachline.replace('\n','')
        post_data.append(eachline)

#下载图片的类
class getPic(threading.Thread):
    def __init__(self,post_data):
        threading.Thread.__init__(self)
        self.post_data = post_data 
        self.timeout = 600
    def downloadimg(self):
        global pageurl_list
        for imgurl in self.post_data:
            url='http://www.agoda.com/ssr/ajax/ssr/CitySearchV2/103/3/8/8/1/zh-cn'            
            req = urllib2.Request(url, imgurl)
            response = urllib2.urlopen(req)
            the_page = response.read()
            pattern = re.compile(r'''"HotelUrl":"(.+?)\?''', re.I | re.M)
            urls=pattern.findall(the_page)
            f=open ('down_urls.txt','a+')
            for url in urls:
                pageurl="http://www.agoda.com%s" %url
                pageurl_list.append(pageurl)
                f.write("%s\n" %pageurl)
            f.close()
            print 'ok'
    def run(self):
        self.downloadimg()
#下载页面的类
class getPage(threading.Thread):
    def __init__(self,pageurl_list):
        threading.Thread.__init__(self)
        self.pageurl_list = pageurl_list 
        self.timeout = 600
    def downPage(self):
        for pageurl in self.pageurl_list:
            suffix= uuid.uuid1()
            pic_name = 'pages/%s.html' %(suffix)
            cookies = urllib2.HTTPCookieProcessor()
            opener = urllib2.build_opener(cookies)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            urllib2.install_opener(opener)            
            try:
                data_img = opener.open(pageurl,timeout=self.timeout)
                urldata=data_img.read()
                f = open (pic_name,'wb')
                f.write(urldata)
                f.close()
                print pic_name+'--OK!!' 
            except:
                f= open("failed.txt",'a+')
                f.write("%s\n" %pageurl)
                f.close()
                continue    
    def run(self):
        self.downPage()
if __name__ == "__main__":
    imgurlList()
    getPicThreads = []
    getPageThreads = []
    
print '.'*10+"Total links:%s" %len(post_data) +'.'*10
#开启20个线程随机取一个代理下载图片
for i in range(20):
    t = getPic(post_data[((len(post_data)+19)/20) * i:((len(post_data)+19)/20) * (i+1)])
    getPicThreads.append(t)

for i in range(len(getPicThreads)):
    getPicThreads[i].start()

for i in range(len(getPicThreads)):
    getPicThreads[i].join()
#根据下载的地址下载页面    
for i in range(20):
    t = getPage(pageurl_list[((len(pageurl_list)+19)/20) * i:((len(pageurl_list)+19)/20) * (i+1)])
    getPageThreads.append(t)

for i in range(len(getPageThreads)):
    getPageThreads[i].start()

for i in range(len(getPageThreads)):
    getPageThreads[i].join()
    
print '.'*10+"total %s files download" %len(post_data) +'.'*10

