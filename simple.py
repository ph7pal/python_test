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
    fp=open("tmp.txt", "r");
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
            suffix= uuid.uuid1()
            pic_name = 'shouer/pages/%s.html' %(suffix)
            cookies = urllib2.HTTPCookieProcessor()
            opener = urllib2.build_opener(cookies)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            urllib2.install_opener(opener)              
            try:
                data_img = opener.open(imgurl,timeout=self.timeout)
                f = open (pic_name,'wb')
                f.write(data_img.read())
                f.close()                
                print pic_name+'--OK!!'
            except:
                f= open("failed.txt",'a+')
                f.write("%s\n" %imgurl)
                f.close()
                print imgurl+'--Failed!!'
                continue
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

