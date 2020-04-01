# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyAimeiV101Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 名称
    indic_name = scrapy.Field()
    # 数据目录
    parent_id = scrapy.Field()
    # 根目录id
    root_id = scrapy.Field()
    # 年
    data_year = scrapy.Field()
    # 月
    data_month = scrapy.Field()
    # 日
    data_day = scrapy.Field()
    # 频率
    frequency = scrapy.Field()
    # 单位
    unit = scrapy.Field()
    # 数据来源(网站名)
    data_source = scrapy.Field()
    # 地区
    region = scrapy.Field()
    # 国家
    country = scrapy.Field()
    # 数据产生时间
    create_time = scrapy.Field()
    # 数据插入时间（爬取时间）
    update_time = scrapy.Field()
    # 数值
    data_value = scrapy.Field()
    # 个人编号
    sign = scrapy.Field()
    # 0:无效  1: 有效
    status = scrapy.Field()
    # 0 : 未清洗  1 ： 清洗过
    cleaning_status = scrapy.Field()