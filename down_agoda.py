#!/usr/bin/env python
#coding=utf-8

import urllib2
import re
import threading
import time
import random
import sys
import uuid
import os

imgurl_list = []

#获取图片地址函数
def imgurlList():
    global imgurl_list
    fp=open("urls.txt", "r");
    for eachline in fp:
        eachline=eachline.replace('\r','')
        eachline=eachline.replace('\n','')
        imgurl_list.append(eachline)

#下载图片的类
class getPic(threading.Thread):
    def __init__(self,imgurl_list):
        threading.Thread.__init__(self)
        self.imgurl_list = imgurl_list 
        self.timeout = 600
    def downloadimg(self):
        for imgurl in self.imgurl_list:
            url='http://www.agoda.com/ssr/ajax/ssr/CitySearchV2/103/3/8/8/1/zh-cn'
            req = urllib2.Request(url, imgurl)
            response = urllib2.urlopen(req)
            the_page = response.read()
            pattern = re.compile(r'''"HotelUrl":"(.+?)\?''', re.I | re.M)
            urls=pattern.findall(the_page)
            f=open ('down_urls.txt','wb')
            for url in urls:
                f.write("%s\n" %url)
            f.close()
            print 'ok'
    def run(self):
        self.downloadimg()

if __name__ == "__main__":
    imgurlList()
    getPicThreads = []
print '.'*10+"Total links:%s" %len(imgurl_list) +'.'*10
#开启20个线程随机取一个代理下载图片
for i in range(20):
    t = getPic(imgurl_list[((len(imgurl_list)+19)/20) * i:((len(imgurl_list)+19)/20) * (i+1)])
    getPicThreads.append(t)

for i in range(len(getPicThreads)):
    getPicThreads[i].start()

for i in range(len(getPicThreads)):
    getPicThreads[i].join()

print '.'*10+"total %s files download" %len(imgurl_list) +'.'*10

