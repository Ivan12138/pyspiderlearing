#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2019-09-20 01:46:36
# Project: crawlCUITteacherInfo


from pyspider.libs.base_handler import *

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://80s.la/movie/list', callback=self.index_page, validate_cert=False)
        
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.me1.clearfix li a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        #获取下一页地址，将下一页地址放到爬取内容中，再交给本函数去爬取下一页的内容，以实现翻页         
        next = response.doc(".pager > a:nth-last-child(2)").attr.href
        self.crawl(next,callback=self.index_page,validate_cert=False)
        
    @config(priority=2)
    def detail_page(self, response):
        
        return {
           "img":response.doc('.img > img').attr.src
        }