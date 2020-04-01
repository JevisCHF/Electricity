# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_Robodata_V1_02 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_Robodata_V1_02'

SPIDER_MODULES = ['Scrapy_Robodata_V1_02.spiders']
NEWSPIDER_MODULE = 'Scrapy_Robodata_V1_02.spiders'

ROBOTSTXT_OBEY = False


DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

MONGO_URI = "127.0.0.1:27017"
MONGO_DB = "Robo"  # 库名
RETRY_ENABLED = True  # 打开重试开关
RETRY_TIMES = 3  #重试次数
DOWNLOAD_TIMEOUT = 5  # 超时
RETRY_HTTP_CODES = [503, 500, 502, 404, 400, 403]

SPIDER_MIDDLEWARES = {
    'Scrapy_Robodata_V1_02.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_RoBoDatabase_V1_15.middlewares.ScrapyRobodatabaseV115SpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Scrapy_Robodata_V1_02.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_RoBoDatabase_V1_15.middlewares.ScrapyRobodatabaseV115DownloaderMiddleware': 543,
}

ITEM_PIPELINES = {
    'Scrapy_Robodata_V1_02.pipelines.ScrapyRobodataV102Pipeline': 300,
}

base_url = ['https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input=',  # 输入关键字
            # 'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input=%E7%94%B5%E5%8A%9B&macro=%E8%A1%8C%E4%B8%9A%E7%BB%8F%E6%B5%8E&catelog=2000000001-2020000001-2020000002-2020001492-2020001510',
            'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/',  # 输入编号
            'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input=电力&macro=国际宏观&catelog=',
            'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/query?input=电力&macro=特色数据&catelog=']

root_id = {
    '热力': '4001001',
    '电力': '4001002',
    '火电': '4001003',
    '风电': '4001004',
    '核电': '4001005',
    '水电': '4001006',
    '太阳能': '4001007',
    '生物质能': '4001008',
}

urls = {}

# 日志等级
LOG_LEVEL = 'INFO'
