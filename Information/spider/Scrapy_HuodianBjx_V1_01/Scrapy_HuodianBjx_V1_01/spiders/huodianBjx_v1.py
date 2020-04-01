# -*- coding: utf-8 -*-
import scrapy
from Scrapy_HuodianBjx_V1_01.items import ScrapyHuodianbjxV101Item
import time
from scrapy.utils import request
from Scrapy_HuodianBjx_V1_01.start_urls import urls


class HuodianbjxV1Spider(scrapy.Spider):
    name = 'huodianBjx_v1'
    allowed_domains = ['huodian.bjx.com.cn', 'news.bjx.com.cn']

    # 初始网址
    def start_requests(self):
        for url, cate in urls.items():
            yield scrapy.Request(url=url, callback=self.parse, meta={'cate': cate, 'url': url})

    def parse(self, response):
        cate = response.meta['cate']
        # 获取本页所有新闻链接
        node_list = response.xpath('//div[@class="list_left"]/ul/li')
        for node in node_list:
            link_list = node.xpath('./a/@href').extract_first()
            if link_list:
                item = ScrapyHuodianbjxV101Item()
                item['content_url'] = link_list
                item['issue_time'] = node.xpath('./span/text()').extract_first()
                req = scrapy.Request(url=link_list, callback=self.parse2, meta={'item': item, 'cate': cate})
                item["id"] = request.request_fingerprint(req)
                yield req
                # print(link_list)

        # 下一页新闻链接
        next_page1 = response.xpath('//div[@class="page"]/a[@title="下一页"]/@href').extract_first()
        next_page2 = response.xpath('//div[@class="tempa page btemp"]/a[@title="下一页"]/@href').extract_first()

        if next_page1:
            next_url = f'http://huodian.bjx.com.cn{next_page1}'
            # print(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'cate': cate})
        elif next_page2:
            next_url = f'http://huodian.bjx.com.cn{next_page2}'
            # print(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse, meta={'cate': cate})

    def parse2(self, response):
        # print(response.request.headers['User-Agent'])
        cate = response.meta['cate']
        item = response.meta['item']

        item['title'] = response.xpath('//div[@class="list_detail"]/h1/text()').extract_first()
        source1 = ''.join(response.xpath(
            '//div[@class="list_detail"]/div[@class="list_copy"]/b[1]//text()').extract())
        source2 = ''.join(response.xpath(
            '//div[@class="list_detail"]/div[@class="tempa list_copy btemp"]/b[1]//text()').extract())
        if source1:
            item['source'] = source1[3:]
        elif source2:
            item['source'] = source2[3:]
        else:
            item['source'] = None

        item['information_source'] = '北极星火力发电网'

        tags1 = ';'.join(response.xpath(
            '//div[@class="list_detail"]/div[@class="list_key"]/a/text()').extract())
        tags2 = ';'.join(response.xpath(
            '//div[@class="list_detail"]/div[@class="tempa list_key btemp"]/a/text()').extract())
        if tags1:
            item['tags'] = None if tags1 == ';' else tags1
        elif tags2:
            item['tags'] = None if tags2 == ';' else tags2
        else:
            item['tags'] = None

        content = response.xpath('//div[@class="list_detail"]/div[@id="content"]').extract_first()
        item['content'] = content if content else None

        next_page1 = response.xpath('//div[@class="page"]/a[@title="下一页"]/@href').extract_first()
        next_page2 = response.xpath('//div[@class="tempa page btemp"]/a[@title="下一页"]/@href').extract_first()
        if next_page1:
            content_url = item['content_url']
            next_content_url = content_url.replace(content_url[-6:], next_page1[-8:])
            print(next_content_url)
            yield scrapy.Request(url=next_content_url, callback=self.parse3, meta={'item': item})
        elif next_page2:
            content_url = item['content_url']
            next_content_url = content_url.replace(content_url[-6:], next_page2[-8:])
            print(next_content_url)
            yield scrapy.Request(url=next_content_url, callback=self.parse3, meta={'item': item})

        item['industry_categories'] = 'D'
        item['industry_Lcategories'] = '44'
        item['industry_Mcategories'] = '441'
        item['industry_Scategories'] = '4411'
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

        # 部分没有作者，解决报错
        try:
            author1 = response.xpath('//div[@class="list_copy"]/text()').extract()
            author2 = response.xpath('//div[@class="tempa list_copy btemp"]/text()').extract()
            if author1:
                author = author1[1].strip()
                item['author'] = author[3:] if author else None
            elif author2:
                author = author2[1].strip()
                item['author'] = author[3:] if author else None
            else:
                item['author'] = None
        except:
            item['author'] = None

        if not item['content']:
            self.logger.warning("注意：内容为空,地址为:{}".format(item['content_url']))

        # 如果内容有多页，则继续爬取content and images，没有就yield item
        next_page1 = response.xpath('//div[@class="page"]/a[@title="下一页"]/@href').extract_first()
        next_page2 = response.xpath('//div[@class="tempa page btemp"]/a[@title="下一页"]/@href').extract_first()
        if next_page1:
            content_url = item['content_url']
            next_content_url = content_url.replace(content_url[-6:], next_page1[-8:])
            # print(next_content_url)
            yield scrapy.Request(url=next_content_url, callback=self.parse3, meta={'item': item})
        elif next_page2:
            content_url = item['content_url']
            next_content_url = content_url.replace(content_url[-6:], next_page2[-8:])
            # print(next_content_url)
            yield scrapy.Request(url=next_content_url, callback=self.parse3, meta={'item': item})
        else:
            yield item
            self.logger.info("title:{},issue_time:{}".format(item['title'], item['issue_time']))
            self.logger.info('author:{},tags:{}'.format(item['author'], item['tags']))

    def parse3(self, response):
        item = response.meta['item']

        # 把之前的内容和下一页的内容拼接起来
        old_content = item['content']
        content = response.xpath('//div[@id="content"]').extract_first()
        if content:
            item['content'] = ('' if old_content is None else old_content) + content
        else:
            item['content'] = old_content

        # 把之前的images和下一页的images拼接起来
        old_images = '' if item['images'] is None else item['images']
        image_url = ';'.join(
            response.xpath('//div[@class="list_detail"]/div[@id="content"]//p//img/@data-echo').extract())
        new_images = old_images + ';' + ('' if image_url is None else image_url)
        new_images = '' if new_images == ';' else new_images
        item['images'] = new_images if new_images else None

        # 如果还有更多的内容，则获取下一页内容链接，没有就yield item
        next_page1 = response.xpath('//div[@class="page"]/a[@title="下一页"]/@href').extract_first()
        next_page2 = response.xpath('//div[@class="tempa page btemp"]/a[@title="下一页"]/@href').extract_first()
        if next_page1:
            content_url = item['content_url']
            next_content_url = content_url.replace(content_url[-6:], next_page1[-8:])
            print(next_content_url)
            yield scrapy.Request(url=next_content_url, callback=self.parse3, meta={'item': item})
        elif next_page2:
            content_url = item['content_url']
            next_content_url = content_url.replace(content_url[-6:], next_page2[-8:])
            # print(next_content_url)
            yield scrapy.Request(url=next_content_url, callback=self.parse3, meta={'item': item})
        else:
            yield item
            self.logger.info("title:{},issue_time:{}".format(item['title'], item['issue_time']))
            self.logger.info('author:{},tags:{}'.format(item['author'], item['tags']))


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'huodianBjx_v1'])
