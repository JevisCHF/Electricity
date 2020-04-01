# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyIpoipoV101Item(scrapy.Item):

    # 1.摘要
    abstract = scrapy.Field()
    # 2.标题
    title = scrapy.Field()
    # 3.文件下载地址
    paper_url = scrapy.Field()
    # 4.时间
    date = scrapy.Field()
    # 5.文件来源
    paper_from = scrapy.Field()
    # 6.文件路径
    paper = scrapy.Field()
    # 7.作者
    author = scrapy.Field()
    # 8.父级菜单
    parent_id = scrapy.Field()
    # 9.清洗位
    cleaning_status = scrapy.Field()
