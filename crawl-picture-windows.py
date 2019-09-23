#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-03-29 14:56:10
# Project: BaiduPictures

from pyspider.libs.base_handler import *
import os

#图片存放目录
DIR_PATH = "D:\python_workspace\pyspider_baiduPicture"
class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.base_url = "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=%E7%8C%AB%E5%92%AA&oq=%E7%8C%AB%E5%92%AA&rsp=-1"
        self.dir_path = DIR_PATH
        self.tool = Tool()

    @every(minutes=24 * 60)
    def on_start(self):
        #validate_cert:是否验证SSL；fetch_type：为了支持JS
        self.crawl(self.base_url, callback=self.index_page, validate_cert=False, fetch_type="js")

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        count = 1
        #获取图片详情链接标签列表
        for each in response.doc('.imgbox a').items():
            url = each.attr.href
            #进入图片详情页
            self.crawl(url, callback=self.detail_page,validate_cert=False, fetch_type="js",save={"count":count})
            count +=1

    @config(priority=2)
    def detail_page(self, response):
        #获取图片标签
        imgElem = response.doc(".currentImg")
        #获取图片地址
        imgUrl = imgElem.attr.src
        if imgUrl:
            #获取图片文件后缀
            extension = self.tool.get_extension(imgUrl)
            #拼接图片名
            file_name = str(response.save["count"]) + "." + extension
            self.crawl(imgUrl,callback=self.save_img,save={"file_name":file_name},validate_cert=False)

    #保存图片
    def save_img(self,response):
        content = response.content
        file_name = response.save["file_name"]
        file_path = self.dir_path + os.path.sep + file_name
        self.tool.save_img(content,file_path)

#工具类    
class Tool:
    def __init__(self):
        self.dir = DIR_PATH
        #创建文件夹（如果不存在）
        if not os.path.exists(self.dir):                         
            os.makedirs(self.dir)                                         
    #保存图片
    def save_img(self,content,path):
        f = open(path,"wb" )
        f.write(content)
        f.close()

    #获取url后缀名
    def get_extension(self,url):                            
        extension = url.split(".")[-1]
        return extension       
