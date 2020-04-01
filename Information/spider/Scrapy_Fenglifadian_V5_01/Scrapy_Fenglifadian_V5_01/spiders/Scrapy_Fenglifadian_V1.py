# -*- coding: utf-8 -*-
import scrapy
from Scrapy_Fenglifadian_V5_01.items import ScrapyFenglifadianV501Item
from Scrapy_Fenglifadian_V5_01.star_urls import urls
import time
from scrapy.utils import request


class ScrapyFenglifadianV1Spider(scrapy.Spider):
    name = 'Scrapy_Fenglifadian_v1'
    allowed_domains = ['fd.bjx.com.cn', 'news.bjx.com.cn']

    # start_urls = ['http://fd.bjx.com.cn/fdcy/']

    def start_requests(self):
        for url, cate in urls.items():
            yield scrapy.Request(url=url, callback=self.parse, meta={'cate': cate, 'url': url})

    def parse(self, response):
        cate = response.meta['cate']
        url = response.meta['url']
        for i in range(1, 100):
            self.start_urls = f'{url}?page={i}'
            yield scrapy.Request(url=self.start_urls, callback=self.parse2, meta={'cate': cate})
            print(self.start_urls)

    def parse2(self, response):
        cate = response.meta['cate']
        # over = response.xpath('//div[@class="noresult"]')
        # if over:
        #     return '------爬取完啦！！-------'

        node_list = response.xpath('//div[@class="list_left"]/ul/li')
        for node in node_list:
            link_list = node.xpath('./a/@href').extract_first()
            if link_list:
                item = ScrapyFenglifadianV501Item()
                item['content_url'] = link_list
                item['issue_time'] = node.xpath('./span/text()').extract_first()
                req = scrapy.Request(url=link_list, callback=self.parse3, meta={'item': item, 'cate': cate})
                item["id"] = request.request_fingerprint(req)
                yield req
                # print(link_list)

    def parse3(self, response):
        cate = response.meta['cate']
        item = response.meta['item']

        item['title'] = response.xpath('//div[@class="list_detail"]/h1/text()').extract_first()
        item['source'] = None
        source = ''.join(response.xpath(
            '//div[@class="list_detail"]/div[@class="tempa list_copy btemp"]/b[1]//text()').extract())
        item['source'] = source[3:] if source else None
        # print(source)
        item['information_source'] = '北极星风力发电网'

        tags = response.xpath(
            '//div[@class="list_detail"]/div[@class="tempa list_key btemp"]/a/text()').extract()
        item['tags'] = ';'.join(tags)
        content = response.xpath('//div[@class="list_detail"]/div[@id="content"]').extract_first()
        item['content'] = content if content else None

        item['industry_categories'] = 'D'
        item['industry_Lcategories'] = '44'
        item['industry_Mcategories'] = '441'
        item['industry_Scategories'] = '4415'
        item['information_categories'] = cate
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        image_url = ';'.join(
            response.xpath('//div[@class="list_detail"]/div[@id="content"]//p//img/@data-echo').extract())
        item["images"] = image_url if image_url else None
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['title_images'] = None
        author = response.xpath('//div[@class="list_copy"]/text()').extract()[1].strip()
        item['author'] = author[3:] if author else None

        if not item['content']:
            self.logger.warning("注意：内容为空,地址为:{}".format(item['content_url']))
        else:
            yield item
            self.logger.info("title:{},issue_time:{}".format(item['title'], item['issue_time']))
            self.logger.info('author:{},tags:{}'.format(item['author'], item['tags']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'Scrapy_Fenglifadian_v1'])
