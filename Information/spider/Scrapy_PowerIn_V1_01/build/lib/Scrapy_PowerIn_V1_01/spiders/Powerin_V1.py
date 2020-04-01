# -*- coding: utf-8 -*-
import scrapy
from Scrapy_PowerIn_V1_01.items import ScrapyPowerinV101Item
import time
from scrapy.utils import request
from Scrapy_PowerIn_V1_01.start_urls import urls


class PowerinV1Spider(scrapy.Spider):
    name = 'Powerin_V1'
    allowed_domains = ['power.in-en.com']

    def start_requests(self):

        # for url, cate in urls.items():
        #     yield scrapy.Request(url=url, callback=self.parse, meta={'cate': cate})
        #     self.logger.info("cat({})".format(cate))

        for num in range(1, 30):
            next_link = f'https://power.in-en.com/news/china/list83-{num}.html'
            cate = '国内动态'
            yield scrapy.Request(url=next_link, callback=self.parse, meta={'cate': cate})
            print(next_link)

    def parse(self, response):
        cate = response.meta['cate']

        new_urls = response.xpath('//div[@class="slideTxtBox fl"]/ul/li')
        for new_url in new_urls:
            item = ScrapyPowerinV101Item()
            item['content_url'] = new_url.xpath('.//h5/a/@href').extract_first()
            title_images = new_url.xpath('./div[@class="imgBox"]/a/img/@src').extract_first()
            item['title_images'] = title_images if title_images else None
            item['industry_categories'] = 'D'
            item['industry_Lcategories'] = '44'
            item['industry_Mcategories'] = '441'
            item['industry_Scategories'] = str(cate[5:]) if cate[5:] else None
            item['information_categories'] = cate[:4]
            req = scrapy.Request(url=item['content_url'], callback=self.parse2, meta={'item': item})
            item["id"] = request.request_fingerprint(req)
            yield req

        # 下一页链接
        # next_link = response.xpath('//div[@class="pages"]/a[last()]/@href').extract_first()
        # if next_link:
        #     print(next_link)
        #     yield scrapy.Request(url=next_link, callback=self.parse, meta={'cate': cate})

    def parse2(self, response):
        item = response.meta['item']
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '国际电力网'
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        item['title'] = response.xpath('//div[@class="leftBox fl"]/h1/text()').extract_first()
        item['content'] = response.xpath('//div[@class="content"]').extract_first()
        item['issue_time'] = response.xpath('//p[@class="source"]/b[1]/text()').extract_first()[3:]
        item['source'] = response.xpath('//p[@class="source"]/b[2]/text()').extract_first()[5:]
        author = response.xpath('//p[@class="source"]/text()').extract_first()[5:]
        item['author'] = author if author else None
        item['tags'] = ';'.join(response.xpath('//p[@class="keyWords"]/a//text()').extract())
        images = ';'.join(response.xpath('//div[@class="content"]//img/@src').extract())
        item['images'] = images if images else None

        if not item['content']:
            self.logger.warning("注意：内容为空,地址为:{}".format(item['content_url']))
            print("注意：内容为空,地址为:{}".format(item['content_url']))
        else:
            yield item
            # self.logger.info("title:{},issue_time:{}".format(item['title'], item['issue_time']))
            # self.logger.info('tags:{}'.format(item['tags']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'Powerin_V1'])
