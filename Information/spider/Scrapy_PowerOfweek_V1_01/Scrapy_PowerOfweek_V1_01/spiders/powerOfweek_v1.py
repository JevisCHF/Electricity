# -*- coding: utf-8 -*-
import scrapy
from Scrapy_PowerOfweek_V1_01.items import ScrapyPowerofweekV101Item
import time
from scrapy.utils import request
# from Scrapy_PowerOfweek_V1_01.start_urls import urls


class PowerofweekV1Spider(scrapy.Spider):
    name = 'powerOfweek_v1'
    allowed_domains = ['power.ofweek.com']
    # start_urls = ['http://power.ofweek.com/']

    def start_requests(self):

        for i in range(1, 10):
            url = f'https://power.ofweek.com/CAT-35004-8100-News-{i}.html'
            cate = '新闻资讯'
            yield scrapy.Request(url=url, callback=self.parse, meta={'cate': cate})

    def parse(self, response):
        cate = response.meta['cate']
        print(response.status)
        new_urls = response.xpath('//div[@class="main_left"]/div')
        a = 0
        for new_url in new_urls:
            if a != 0 and a != 21:
                item = ScrapyPowerofweekV101Item()
                item['content_url'] = new_url.xpath('.//h3/a/@href').extract_first()
                item['tags'] = new_url.xpath('.//div[@class="tag"]/span[1]/a/text()').extract_first().strip()
                item['title_images'] = None
                item['industry_categories'] = 'D'
                item['industry_Lcategories'] = '44'
                item['industry_Mcategories'] = '441'
                item['industry_Scategories'] = None
                item['information_categories'] = cate
                req = scrapy.Request(url=item['content_url'], callback=self.parse2, meta={'item': item})
                item["id"] = request.request_fingerprint(req)
                yield req
            a += 1

    def parse2(self, response):
        item = response.meta['item']
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '电力网'
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        item['title'] = response.xpath('//div[@class="artical"]/p/text()').extract_first()
        item['content'] = response.xpath('//div[@class="artical-content"]').extract_first()
        item['issue_time'] = response.xpath('//div[@class="time fl"]/text()').extract_first().strip()[:10]

        source1 = response.xpath('//div[@class="source-name"]/text()').extract_first()
        source2 = response.xpath('//div[@class="artical-relative clearfix"]/a/span[2]/text()').extract_first()
        if source1:
            item['source'] = source1
        elif source2:
            item['source'] = source2
        else:
            item['source'] = None

        item['author'] = None
        images = ';'.join(response.xpath('//div[@class="artical-content"]//img/@src').extract())
        item['images'] = images if images else None

        if not item['content']:
            self.logger.warning("注意：内容为空,地址为:{}".format(item['content_url']))
        else:
            yield item
            self.logger.info("title:{},issue_time:{}".format(item['title'], item['issue_time']))
            self.logger.info('tags:{}, source:{}'.format(item['tags'], item['source']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'powerOfweek_v1'])
