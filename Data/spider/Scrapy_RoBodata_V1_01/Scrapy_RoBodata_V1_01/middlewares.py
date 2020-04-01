# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import Scrapy_RoBodata_V1_01.proxy as Proxy
import logging

logger = logging.getLogger(__name__)


class ScrapyRobodatabaseV115SpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyRobodatabaseV115DownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleWare(object):
    '''
    设置Proxy
    '''

    def __init__(self):
        self.invalid_proxy = set()
        self.proxy = Proxy.get_proxy()

    def process_request(self, request, spider):
        # 对 request 加上 proxy
        # proxy = get_proxy()
        request.meta['proxy'] = self.proxy['https']
        start_num = Proxy.get_status()
        logger.info('invalid proxy number is %s,\n proxy total number is %s' % (len(self.invalid_proxy), start_num))

    def process_response(self, request, response, spider):
        # 如果返回的 response 状态不是 200 ，重新声称当前的 request 对象
        try:
            if str(response.status).startswith('4') or str(response.status).startswith('5'):
                print('状态码异常:', response.status)
                num = Proxy.get_status()
                # 当失效集合超过代理池ip数就清空集合
                if len(self.invalid_proxy) >= num:
                    self.invalid_proxy.clear()

                # 将失效代理ip添加到失效集合里
                self.invalid_proxy.add(request.meta['proxy'])
                # 重新获取代理ip
                self.proxy = Proxy.get_proxy()
                while True:
                    # 判断获取的代理ip是不是重复获取或者是失效代理集合里的
                    if self.proxy['https'] in self.invalid_proxy:
                        self.proxy = Proxy.get_proxy()
                        continue
                    else:
                        request.meta['proxy'] = self.proxy['https']
                        logging.debug('is the invalid ip, replace ip:' + self.proxy['https'])
                        # 对当前request 加上代理
                        break
                return request
        except:
            request.meta['proxy'] = self.proxy['https']
            logging.info('this is response ip:' + self.proxy['https'])
            # 对当前 request 加上代理
            return request

        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, TimeoutError):
            self.invalid_proxy.add(request.meta['proxy'])
            self.proxy = Proxy.get_proxy()
            return request

        self.invalid_proxy.add(request.meta['proxy'])
        self.proxy = Proxy.get_proxy()
        num = Proxy.get_status()
        # 当失效集合超过代理池ip数就清空集合
        if len(self.invalid_proxy) >= num:
            self.invalid_proxy.clear()
        while True:
            # 判断获取的代理ip是不是重复获取或者是失效代理集合里的
            if self.proxy['https'] in self.invalid_proxy:
                self.proxy = Proxy.get_proxy()
                continue
            else:
                request.meta['proxy'] = self.proxy['https']
                logging.debug('there is an error, replace ip:' + self.proxy['https'])
                # 对当前request 加上代理
                break
        return request
