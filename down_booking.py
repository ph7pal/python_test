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
#是否从本地已失败的链接获取下载地址
dntGetByFaild=True
#获取图片地址函数
def imgurlList():
    global post_data,dntGetByFaild
    if dntGetByFaild:            
        total=557
        for i in range(1,total/50+2):
            offset=(i-1)*50
            one_line="http://www.booking.com/searchresults.zh-cn.html?sid=6f235e47f95b9ff60478c66605814bb1;dcid=4;city=-246227;class_interval=1;csflt=%7B%7D;dtdisc=0;hlrd=0;hyb_red=0;inac=0;nha_red=0;redirected_from_city=0;redirected_from_landmark=0;redirected_from_region=0;review_score_group=empty;score_min=0;ss_all=0;ssb=empty;sshis=0&;rows=50;offset={0}".format(offset)
            post_data.append(one_line)
    else:
        fp=open("shouer.txt", "r");
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
            cookies = urllib2.HTTPCookieProcessor()
            opener = urllib2.build_opener(cookies)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            urllib2.install_opener(opener)
            try:
                data_img = opener.open(imgurl,timeout=self.timeout)
                urldata=data_img.read()
                pattern = re.compile(r'''class="hotel_name_link\s*url"\s*href="(.+?)\?''', re.I | re.M)
                urls=pattern.findall(urldata)
                f=open ('down_urls_booking.txt','a+')
                for url in urls:
                    pageurl="http://www.booking.com%s" %url
                    pageurl_list.append(pageurl)
                    f.write("%s\n" %pageurl)
                f.close()
                print 'ok' 
            except:
                f= open("down_urls_failed.txt",'a+')
                f.write("%s\n" %imgurl)
                f.close()
                continue
            
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
            pic_name = 'dongjing/pages/%s.html' %(suffix)
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

