# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_FdBjx_V1_01 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_FdBjx_V1_01'

SPIDER_MODULES = ['Scrapy_FdBjx_V1_01.spiders']
NEWSPIDER_MODULE = 'Scrapy_FdBjx_V1_01.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy_FdBjx_V1_01 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16
DOWNLOADER_MIDDLEWARES = {
    'Scrapy_FdBjx_V1_01.middlewares.AddProxyMiddlewares': 543,
    'Scrapy_FdBjx_V1_01.middlewares.MyRetryMiddleware': 533,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Scrapy_FdBjx_V1_01.pipelines.MongoPipeline': 301,
}

# 正式集
# MONGO_URI = '192.168.0.11'
# MONGO_DATABASE = 'industry'

# 测试集
MONGO_URI = '127.0.0.1'
MONGO_DATABASE = 'win_power_generation'

# 日志文件等级
LOG_LEVEL = 'INFO'

# 重试设置
RETRY_ENABLED = True  # 默认开启失败重试，一般关闭
RETRY_TIMES = 3  # 失败后重试次数，默认两次
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]  # 碰到这些验证码，才开启重试