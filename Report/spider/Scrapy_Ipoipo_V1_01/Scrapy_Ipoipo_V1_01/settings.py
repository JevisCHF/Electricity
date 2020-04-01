# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_Ipoipo_V1_01 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_Ipoipo_V1_01'

SPIDER_MODULES = ['Scrapy_Ipoipo_V1_01.spiders']
NEWSPIDER_MODULE = 'Scrapy_Ipoipo_V1_01.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Scrapy_Ipoipo_V1_01 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3

# 文件下载路径
FILES_STORE = 'E:\\报告\\文件'

# 日志文件等级
LOG_LEVEL = 'INFO'

# 重试设置
RETRY_ENABLED = True    # 开始失败重试，默认关闭
RETRY_TIMES = 4
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 404] # 遇到这一类状态码，重试

# 测试集
MONGO_URI = '127.0.0.1:27017'
MONGO_DB = 'Report'

CATES_DICT = {
    "电力": "4001001",
    "风电": "4001002",
    "火电": "4001003",
    "水电": "4001004",
    "核电": "4001005",
    "光伏": "4001006"
}

DOWNLOADER_MIDDLEWARES = {
    # 'Scrapy_Ipoipo_V1_01.middlewares.AddProxyMiddlewares': 543,
    # 'Scrapy_Ipoipo_V1_01.middlewares.MyRetryMiddleware': 533,
    # 'Scrapy_Ipoipo_V1_01.middlewares.ScrapyIpoipoV101DownloaderMiddleware': 533,

    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,

}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Scrapy_Ipoipo_V1_01.pipelines.MongoPipeline': 300,
}