# -*- coding: utf-8 -*-
import scrapy
from Scrapy_ChinaPower_V1_01.items import ScrapyChinapowerV101Item
import time
from scrapy.utils import request
from Scrapy_ChinaPower_V1_01.start_urls import urls
import re


class ChinapowerV1Spider(scrapy.Spider):
    name = 'chinaPower_V1'
    allowed_domains = ['www.chinapower.com.cn']

    def start_requests(self):
        for url, cate in urls.items():
            yield scrapy.Request(url=url, callback=self.parse, meta={'cate': cate})
            self.logger.info("cat({})".format(cate))

        # http://www.chinapower.com.cn/shuidian/index_50.html
        # 下一页链接
        for i in range(2, 19):
            cate = '风云人物'
            next_url = f'http://www.chinapower.com.cn/guandian/index_{i}.html'
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'cate': cate})
            print(next_url)

    def parse(self, response):
        cate = response.meta['cate']

        new_urls = response.xpath('//div[@class="ns_nr"]/ul[@class="list00"]/li')
        for url in new_urls:
            issue_time = url.xpath('./span[1]/text()').extract_first()
            link = url.xpath('.//a/@href').extract_first()
            title = url.xpath('.//a/text()').extract_first()

            item = ScrapyChinapowerV101Item()
            item['content_url'] = f'http://www.chinapower.com.cn{link}'
            item['title_images'] = None
            item['industry_categories'] = 'D'
            item['industry_Lcategories'] = '44'
            item['industry_Mcategories'] = '441'
            item['industry_Scategories'] = None
            item['information_categories'] = '风云人物'
            item['issue_time'] = issue_time
            item['title'] = title

            req = scrapy.Request(url=item['content_url'], callback=self.parse2, meta={'item': item})
            item['id'] = request.request_fingerprint(req)
            yield req

    def parse2(self, response):
        item = response.meta['item']
        item['sign'] = '19'
        item['update_time'] = str(int(time.time() * 1000))
        item['information_source'] = '中国电力网'
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        # item['title'] = response.xpath('//div[@class="subleft"]//h1/text()').extract_first()
        # item['issue_time'] = response.xpath('//div[@class="subleft"]//h3/text()')
        item['content'] = ''.join(response.xpath('//div[@class="subleft"]/p').extract())
        center = response.xpath('//div[@class="subleft"]//h3/text()').extract_first()
        source = re.search(r'来源：(\S+)', center).group(1)
        item['source'] = source if source else None

        try:
            author = re.search(r'作者：(\S+( \S+)*)', center).group(1).strip()
            item['author'] = author if author else None
        except:
            item['author'] = None

        item['tags'] = None
        item['images'] = None

        images = response.xpath('//div[@class="subleft"]/p//img/@src').extract()
        if images:
            images_url = []
            for img in images:
                if 'http' in img:
                    images_url.append(img)
                else:
                    image = f'http://www.chinapower.com.cn{img}'
                    images_url.append(image)
            images_urls = ';'.join(images_url)
            item['images'] = images_urls if images_urls else None
            # print(item['images'])
        else:
            item['images'] = None
            # print(item['images'])

        if not item['content']:
            self.logger.warning("注意：内容为空,地址为:{}".format(item['content_url']))
        else:
            yield item
            self.logger.info("title:{},issue_time:{}".format(item['title'], item['issue_time']))
            self.logger.info('tags:{}'.format(item['tags']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'chinaPower_V1'])
