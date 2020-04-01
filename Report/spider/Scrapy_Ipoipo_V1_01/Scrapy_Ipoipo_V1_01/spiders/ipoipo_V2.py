# -*- coding: utf-8 -*-
import scrapy
import scrapy, time, re, os, requests
from selenium import webdriver
from lxml import etree
from Scrapy_Ipoipo_V1_01.items import ScrapyIpoipoV101Item
from Scrapy_Ipoipo_V1_01.zip_rename import un_zip
from Scrapy_Ipoipo_V1_01.settings import CATES_DICT
from Scrapy_Ipoipo_V1_01.get_content import get_content

class IpoipoV2Spider(scrapy.Spider):
    name = 'ipoipo_V2'
    allowed_domains = ['ipoipo.cn']
    start_urls = ['http://www.ipoipo.cn/']

    def parse(self, response):
        b = get_content()
        # print(b)
        for i in b:
            item = ScrapyIpoipoV101Item()
            item['paper'] = i['paper']
            item['parent_id'] = i['parent_id']
            # item['parent_id'] = i['']
            item['abstract'] = i['abstract']
            item['title'] = i['title']
            item['paper_url'] = i['paper_url']
            item['date'] = i['date']
            item['author'] = i['author']
            item['paper_from'] = i['paper_from']
            # 清洗位
            item['cleaning_status'] = 0
            yield item
            print(item)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'ipoipo_V2'])
