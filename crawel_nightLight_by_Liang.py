#i!/usr/bin/env python

import urllib.request  as ur
import multiprocessing 
from  lxml  import etree
import os


task=[]
#获取网页链接
homepage="https://ngdc.noaa.gov/eog/viirs/download_dnb_composites_iframe.html"

#下载数据
def getData(url='https://data.ngdc.noaa.gov/instruments/remote-sensing/passive/spectrometers-radiometers/imaging/viirs/dnb_composites/v10//201204/vcmcfg/SVDNB_npp_20120401-20120430_75N060E_vcmcfg_v10_c201605121456.tgz'):
    #filename=url.split('/')[-1]
    cmd="wget -P ./data "+url 	#wget是下载器，并且指定了路径
    os.system(cmd)  #run shell command
    


# get the first page
if __name__=="__main__":
		#读网页链接
        res=ur.urlopen(homepage)
        text=res.read().decode('utf-8')
        print(text)

        #parse the webpage and get the tasklist
        selector=etree.HTML(text)
        tasks=selector.xpath('//*[@id="treemenu1"]/li/ul/li/ul/li/ul/li[3]/ul/li[1]/a/@href')
        task.extend(tasks)	#列表末尾一次性追加另一个序列中的多个值
        print(task)
        print(len(task))

        #use process-pool to get data
		#将通过xpath得到的下载链接，映射到getData函数（下载）来，
        pool = multiprocessing.Pool(5)
        pool. map(getData,task)
        print("done")

