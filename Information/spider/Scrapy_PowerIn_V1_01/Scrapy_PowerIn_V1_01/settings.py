# -*- coding: utf-8 -*-

# Scrapy settings for Scrapy_PowerIn_V1_01 project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Scrapy_PowerIn_V1_01'

SPIDER_MODULES = ['Scrapy_PowerIn_V1_01.spiders']
NEWSPIDER_MODULE = 'Scrapy_PowerIn_V1_01.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Scrapy_PowerIn_V1_01 (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 1
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "zh-CN,zh;q=0.9",
#     "Cache-Control": "max-age=0",
#     "Connection": "keep-alive",
#     "Cookie": "Hm_lvt_084cd9740267c61cb6e361f94f60f798=1577677418; Hm_lvt_76395d13b9b91025737800738bf3cb55=1577180941,1577677418; PHPSESSID=ca58oubuk33l959ier6f1fmdu2; Hm_lpvt_76395d13b9b91025737800738bf3cb55=1577761668; Hm_lpvt_084cd9740267c61cb6e361f94f60f798=1577761668",
#     "Host": "power.in-en.com",
#     "Sec-Fetch-Mode": "navigate",
#     "Sec-Fetch-Site": "same-origin",
#     "Sec-Fetch-User": "?1",
#     "Upgrade-Insecure-Requests": "1",
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Scrapy_PowerIn_V1_01.middlewares.ScrapyPowerinV101SpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'Scrapy_PowerIn_V1_01.middlewares.ScrapyPowerinV101DownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'Scrapy_PowerIn_V1_01.pipelines.ScrapyPowerinV101Pipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# DOWNLOADER_MIDDLEWARES = {
#     'Scrapy_PowerIn_V1_01.middlewares.AddProxyMiddlewares': 543,
#     'Scrapy_PowerIn_V1_01.middlewares.MyRetryMiddleware': 533,
#     'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
#     'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
# }

SPIDER_MIDDLEWARES = {
    'Scrapy_PowerIn_V1_01.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_RoBoDatabase_V1_15.middlewares.ScrapyRobodatabaseV115SpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'Scrapy_PowerIn_V1_01.middlewares.ProxyMiddleWare': 543,
    # 'Scrapy_RoBoDatabase_V1_15.middlewares.ScrapyRobodatabaseV115DownloaderMiddleware': 543,
}


# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Scrapy_PowerIn_V1_01.pipelines.MongoPipeline': 301,
}

# 正式集
# MONGO_URI = '192.168.0.11'
# MONGO_DATABASE = 'industry'

# 测试集
MONGO_URI = '127.0.0.1'
MONGO_DATABASE = 'Information'

# 日志文件等级
LOG_LEVEL = 'INFO'

# 重试设置
RETRY_ENABLED = True  # 默认开启失败重试，一般关闭
RETRY_TIMES = 3  # 失败后重试次数，默认两次
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408]  # 碰到这些验证码，才开启重试
