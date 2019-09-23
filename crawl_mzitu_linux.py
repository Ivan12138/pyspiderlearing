#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-9- 21 16:34
# Project: crawl images
# Author: ivan

#request：run in linux environment because of the dir_path.
#introduction：crawl mzitu.com ,and 


from pyspider.libs.base_handler import *
import re

#指定改脚本运行文件的路径
DIR_PATH = '/home/ivan/python/Pyspider'

class Handler(BaseHandler):
	#配置图片防盗链
    crawl_config = {
        'headers' : {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36',
            'Connection': 'Keep-Alive',
            'Referer': 'http://www.mzitu.com/',
        }
    }
	
	#定义一个初始化函数
    def __init__(self):
        self.root_url = 'http://www.mzitu.com/all/'
        self.deal = Deal()
	
	#开始
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.root_url, callback=self.index_page)

	#当前页
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        # 通过匹配链接后面的数字来获取套图url，再将处理过得链接交给detail_page处理
        for each in response.doc('a[href^="http"]').items():
            if re.match('http://www.mzitu.com/\d.*$', each.attr.href):
                self.crawl(each.attr.href, callback=self.detail_page)
	
	#详情页
    @config(priority=2)
    def detail_page(self, response):
        # 获取当前页面图片链接
        for each in response.doc('p img').items():
            img_url = each.attr.src
        # 获取下一页url，再通过爬取下一页的连接，交给当前函数，以实现翻页。
        for each in response.doc('.pagenavi > a:last-child').items():
            self.crawl(each.attr.href, callback=self.detail_page)
		
		#1.用获取到的链接来创造文件夹名称
        split_url = img_url.split('/')
        dir_name = split_url[-3] + '/' + split_url[-2]
        dir_path = self.deal.mkDir(dir_name)
        file_name = split_url[-1]
		#配置图片防盗链
        self.crawl_config['headers']['Referer'] = response.url
		
		#将爬到的图片链接交给save_img处理，2.以实现保存图片链接		save表示传递参数，可以通过response.save访问
        self.crawl(img_url, callback=self.save_img, save={'dir_path': dir_path, 'file_name': file_name})

        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }

    # 保存图片
    def save_img(self, response):
		#传递二进制数据
        content = response.content
		#response.save访问传递的值
        dir_path = response.save['dir_path']
        file_name = response.save['file_name']
        file_path = dir_path + '/' + file_name
		#调用图片 写入文件
        self.deal.saveImg(content, file_path)


import os


class Deal:
    def __init__(self):
        self.path = DIR_PATH
        if not self.path.endswith('/'):
            self.path = self.path + '/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def mkDir(self, path):
        path = path.strip()
        dir_path = self.path + path
        exists = os.path.exists(dir_path)
        if not exists:
            os.makedirs(dir_path)
            return dir_path
        else:
            return dir_path

    def saveImg(self, content, path):
        f = open(path, 'wb')
        f.write(content)
        f.close()

    def saveBrief(self, content, dir_path, name):
        file_name = dir_path + "/" + name + ".txt"
        f = open(file_name, "w+")
        f.write(content.encode('utf-8'))

    def getExtension(self, url):
        extension = url.split('.')[-1]
        return extension
