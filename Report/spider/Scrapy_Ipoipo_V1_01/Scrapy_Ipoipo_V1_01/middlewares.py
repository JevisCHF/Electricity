# # -*- coding: utf-8 -*-
#
# # Define here the models for your spider middleware
# #
# # See documentation in:
# # https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#
from scrapy import signals
from scrapy.http import HtmlResponse
import time, requests
#
#
# class ScrapyIpoipoV101SpiderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, dict or Item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Response, dict
#         # or Item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
#
#
# class ScrapyIpoipoV101DownloaderMiddleware(object):
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#
#     # 可以拦截到request请求
#     def process_request(self, request, spider):
#         # 在进行url访问之前可以进行的操作, 更换UA请求头, 使用其他代理等
#         h = request.url.split(':')[0]  # 请求的协议头
#         # 获取IP代理
#         get_prory = requests.get('http://192.168.0.11:5010/get/').json().get('proxy', False)
#
#         proxies = {'http': get_prory,
#                    }
#         if h == 'https':
#             request.meta['proxy'] = 'https://' + get_prory
#             print(request.meta['proxy'])
#         else:
#             request.meta['proxy'] = 'http://' + get_prory
#             print(request.meta['proxy'])
#
#     # 可以拦截到response响应对象(拦截下载器传递给Spider的响应对象)
#     def process_response(self, request, response, spider):
#         """
#         三个参数:
#         # request: 响应对象所对应的请求对象
#         # response: 拦截到的响应对象
#         # spider: 爬虫文件中对应的爬虫类 WangyiSpider 的实例对象, 可以通过这个参数拿到 WangyiSpider 中的一些属性或方法
#         """
#
#         #  对页面响应体数据的篡改, 如果是每个模块的 url 请求, 则处理完数据并进行封装
#         if request.url:
#             spider.d.get(url=request.url)
#             # more_btn = spider.browser.find_element_by_class_name("post_addmore")     # 更多按钮
#             # print(more_btn)
#             js = "window.scrollTo(0,document.body.scrollHeight)"
#             spider.d.execute_script(js)
#             # if more_btn and request.url == "http://news.163.com/domestic/":
#             #     more_btn.click()
#             time.sleep(1)  # 等待加载,  可以用显示等待来优化.
#             row_response = spider.d.page_source
#             # print(row_response)
#             return HtmlResponse(url=spider.d.current_url, body=row_response, encoding="utf8",
#                                 request=request)  # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url
#             # 参数body指要封装成符合HTTP协议的源数据, 后两个参数可有可无
#         else:
#             return response  # 是原来的主页的响应对象
#

# -*- coding: utf-8 -*-

from scrapy import signals
# from fake_useragent import UserAgent
import logging
import time
import requests
import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message

logger = logging.getLogger(__name__)


class Proxy():
    def __init__(self):
        self.url = 'http://192.168.0.11:5010/get/'
        self.del_url = "http://192.168.0.11:5010/delete?proxy={}"
        # 网站是http的就改成http，网站是https的就改成https
        self.proxy_header = 'http://'

    def get_proxy(self):
        proxy = self.proxy_header + requests.get(self.url).json().get('proxy', False)
        return proxy

    def del_proxy(self, proxy):
        # 删除代理池的ip，慎用
        requests.get(self.del_url.format(proxy.lstrip(self.proxy_header)))


class AddProxyMiddlewares():
    def __init__(self):
        # 失效代理的集合
        self.invalid_proxy = set()
        self.proxy = Proxy().get_proxy()

    def process_request(self, request, spider):
        # request.meta['HTTP_USER_AGENT'] = UserAgent().chrome
        # 清空无效代理
        if len(self.invalid_proxy) > 10:
            self.invalid_proxy.clear()
        request.meta["proxy"] = self.proxy
        request.meta['downloader_timeout'] = 20
        return None

    # def process_response(self, request, response, spider):
    #     logger.info("responese:{}".format(request.meta))
    #     if str(response.status).startswith('4') or str(response.status).startswith('5'):
    #         # 获取失效代理并收集,重新获取一个代理
    #         NgProxy = request.meta['proxy']
    #         self.invalid_proxy.add(NgProxy)
    #         self.proxy = Proxy().get_proxy()
    #         logger.warning('代理中间件响应报错，状态码为 {},请求新的代理 {}'.format(str(response.status), self.proxy))
    #     return response

    def process_response(self, request, response, spider):
        """
        三个参数:
        # request: 响应对象所对应的请求对象
        # response: 拦截到的响应对象
        # spider: 爬虫文件中对应的爬虫类 WangyiSpider 的实例对象, 可以通过这个参数拿到 WangyiSpider 中的一些属性或方法
        """

        #  对页面响应体数据的篡改, 如果是每个模块的 url 请求, 则处理完数据并进行封装
        if request.url:
            spider.d.get(url=request.url)
            # more_btn = spider.browser.find_element_by_class_name("post_addmore")     # 更多按钮
            # print(more_btn)
            js = "window.scrollTo(0,document.body.scrollHeight)"
            spider.d.execute_script(js)
            # if more_btn and request.url == "http://news.163.com/domestic/":
            #     more_btn.click()
            time.sleep(1)  # 等待加载,  可以用显示等待来优化.
            row_response = spider.d.page_source
            # print(row_response)
            # return HtmlResponse(url=spider.d.current_url, body=row_response, encoding="utf8",
            #                     request=request)  # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url
            # 参数body指要封装成符合HTTP协议的源数据, 后两个参数可有可无
            # logger.info("responese:{}".format(request.meta))
            if str(response.status).startswith('4') or str(response.status).startswith('5'):
                # 获取失效代理并收集,重新获取一个代理
                NgProxy = request.meta['proxy']
                self.invalid_proxy.add(NgProxy)
                self.proxy = Proxy().get_proxy()
            return HtmlResponse(url=spider.d.current_url, body=row_response, encoding="utf8",
                                request=request)  # 参数url指当前浏览器访问的url(通过current_url方法获取), 在这里参数url也可以用request.url
        else:
            return response  # 是原来的主页的响应对象

    def process_exception(self, request, exception, spider):
        # 进入异常模块，
        NgProxy = request.meta['proxy']

        self.invalid_proxy.add(NgProxy)
        self.proxy = Proxy().get_proxy()
        request.dont_filter = True
        logger.warning('代理中间件异常模块，异常为{}，新的代理为 {},'.format(exception, self.proxy))


class MyRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            logger.warning('返回值异常, 进行重试...')

            with open(str(spider.name) + ".txt", "a") as f:
                f.write(str(request) + "\n")
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and not request.meta.get('dont_retry', False):
            logger.warning('MyRetryMiddleware 连接异常, 加入重试队列...')
            with open(str(spider.name) + ".txt", "a") as f:
                f.write(str(request) + "\n")
            return self._retry(request, exception, spider)
