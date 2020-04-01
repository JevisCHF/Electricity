# -*- coding: utf-8 -*-
import scrapy
from Scrapy_PowerIn_V1_01.items import ScrapyPowerinV101Item
import time
from scrapy.utils import request
from Scrapy_PowerIn_V1_01.urls import urls
from datetime import datetime


class PowerinV2Spider(scrapy.Spider):
    name = 'Powerin_V3'
    # allowed_domains = ['power.in-en.com']
    cookie = {
        "Hm_lvt_76395d13b9b91025737800738bf3cb55": "1579167406,1579167421,1579168839,1579251205",
        "Hm_lvt_084cd9740267c61cb6e361f94f60f798": "1579167421,1579168839,1579251227,1579319953",
        "Hm_lpvt_76395d13b9b91025737800738bf3cb55": "1579331771",
        "Hm_lpvt_084cd9740267c61cb6e361f94f60f798": "1579331771",
        "PHPSESSID": "tm05246vpd99ocujikt7nuko41",
    }

    # start_urls = ['http://power.in-en.com/']

    def start_requests(self):

        for url, cate in urls.items():
            information_categories = cate[:4]
            lastPage = cate[4:]

            self.logger.info("分类：{}, 页数：{}".format(information_categories, lastPage))
            # int(lastPage)
            for num in range(1, int(lastPage)):
                next_link = url[:-6] + f'{num}.html'
                yield scrapy.Request(url=next_link, callback=self.parse, meta={'cate': information_categories})
                # print(next_link)

    def parse(self, response):
        cate = response.meta['cate']

        new_urls = response.xpath('//div[@class="slideTxtBox fl"]/ul/li')
        for new_url in new_urls:

            item = ScrapyPowerinV101Item()

            try:
                title_images = new_url.xpath('./div[@class="imgBox"]/a/img/@src').extract_first()
                item['title_images'] = title_images if title_images else None
            except:
                item['title_images'] = None

            issue_time = new_url.xpath('.//div[@class="prompt"]/i[2]/text()').extract_first()
            if '天前' in issue_time:
                day = (int(issue_time[0])) * 24 * 60 * 60
                new_day = int(time.time()) - day
                issue_time = time.strftime('%Y-%m-%d', time.localtime(new_day))
                # print(issue_time)
            elif '小时' in issue_time:
                issue_time = datetime.now().date().strftime('%Y-%m-%d')
            else:
                pass

            source = new_url.xpath('.//div[@class="prompt"]/span[1]/text()').extract_first()[3:]
            tags = new_url.xpath('.//div[@class="prompt"]/span[2]/em/a/text()').extract()
            tags = '; '.join(tags)
            # print(issue_time, source, tags)

            item['content_url'] = new_url.xpath('.//h5/a/@href').extract_first()
            item['industry_categories'] = 'D'
            item['industry_Lcategories'] = '44'
            item['industry_Mcategories'] = None
            item['industry_Scategories'] = None
            item['information_categories'] = cate
            item['update_time'] = str(int(time.time() * 1000))
            item['issue_time'] = issue_time
            item['source'] = source
            item['tags'] = tags

            req = scrapy.Request(url=item['content_url'], callback=self.parse2, meta={'item': item})
            item["id"] = request.request_fingerprint(req)
            yield req

    def parse2(self, response):
        item = response.meta['item']

        item['sign'] = '19'
        item['information_source'] = '国际电力网'
        item['area'] = None
        item['address'] = None
        item['attachments'] = None
        item['content'] = response.xpath('//div[@id="article"]').extract_first()
        item['author'] = None

        title1 = response.xpath('//div[@class="leftBox fl"]/h1/text()').extract_first()
        title2 = response.xpath('//div[@class="c_content"]/h1/text()').extract_first()
        if title1:
            item['title'] = title1
        elif title2:
            item['title'] = title2
        else:
            item['title'] = None

        images = response.xpath('//div[@id="article"]//img/@src').extract()
        if images:
            images_urls = '; '.join(images)
            item['images'] = images_urls if images_urls else None
        else:
            item['images'] = None

        if not item['content']:
            self.logger.warning("注意：内容为空,地址为:{}".format(item['content_url']))
            # print("注意：内容为空,地址为:{}".format(item['content_url']))
        else:
            yield item
            # print(item)
            self.logger.info("title:{},issue_time:{}".format(item['title'], item['issue_time']))
            # self.logger.info('tags:{}'.format(item['tags']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'Powerin_V3'])
