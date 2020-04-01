# -*- coding: utf-8 -*-
import scrapy, time, os, requests, json, re
from Scrapy_WkAskci_V1_01.items import ScrapyWkaskciV101Item
from Scrapy_WkAskci_V1_01.settings import FILES_STORE, CATES_DICT


class WkaskciV1Spider(scrapy.Spider):
    name = 'WkAskci_V1'
    # allowed_domains = ['wk.askci.com/']
    # base_urls = 'http://wk.askci.com/Search/'
    cookie = {
        'LoginKey': '5D55891D41FF4DA5A32C010E478E3F09',
    }

    # 报告列表接口
    def start_requests(self):

        for cate, num in CATES_DICT.items():
            url = f'http://user.askci.com/booklist/?tagname={cate}&isfree=0&pagenum=1'
            print(url)
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookie, meta={'cate': cate, 'num': num},
                                 dont_filter=True)

            if num == "4001001":
                for pagenum in range(2, 7):
                    url = f'http://user.askci.com/booklist/?tagname={cate}&isfree=0&pagenum={pagenum}'
                    print(url)
                    yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookie,
                                         meta={'cate': cate, 'num': num},
                                         dont_filter=True)

    # 获取详情页面链接并返回response
    def parse(self, response):
        # print(response)
        num = response.meta['num']
        cate = response.meta['cate']
        lis = response.xpath('//table[@id="variable_table_width"]/tr')
        n = 1
        for li in lis:
            if n != 1:
                title = li.xpath('./td[1]/a/text()').extract_first()
                date_time = li.xpath('./td[5]/text()').extract_first()
                source = li.xpath('./td[7]/a/text()').extract_first()
                detail_url = li.xpath('./td[1]/a/@href').extract_first()
                # print(title, date_time, source, detail_url)
                yield scrapy.Request(url=detail_url, callback=self.parse2,
                                     meta={'title': title, 'source': source, 'date_time': date_time, 'num': num,
                                           'cate': cate})
            n += 1

        # # 如果有下一页，递归
        # next_link = response.xpath('//a[@title="下一页"]').extract_first()
        # print(next_link)
        # if next_link:
        #     next_url = f'http://user.askci.com{next_link}'
        #     print(next_url)
        #     link = scrapy.Request(url=next_url, callback=self.parse, cookies=self.cookie,
        #                           meta={'cate': cate, 'num': num})
        #     yield link

    # 详情页面获取download_url
    def parse2(self, response):
        cate = response.meta['cate']
        Coo = response.headers['Set-Cookie']
        link = re.search(r'wkpdfpath=(.+); domain=', str(Coo)).group(1).replace('%253a', ':').replace('%252f', '/')
        item = ScrapyWkaskciV101Item()
        item['abstract'] = None
        item['title'] = response.meta['title']
        item['paper_url'] = link
        item['date'] = response.meta['date_time']
        item['author'] = None
        item['paper_from'] = response.meta['source']
        item['parent_id'] = response.meta['num']
        item['cleaning_status'] = 0

        if not os.path.exists(FILES_STORE):
            os.mkdir(FILES_STORE)
        file_path = os.path.join(FILES_STORE, cate)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = os.path.join(file_path, item['title'] + '.pdf')

        item['paper'] = file_name
        self.download(item['paper_url'], file_name)
        # print(item)
        yield item
        self.logger.info("item:{}".format(item))

    # 下载文件
    def download(self, url, file_name):
        # headers = {
        #     'Cookie': 'LoginKey=247EF7329DE24E3093ED65E525D44545'
        # }
        with requests.get(url=url, stream=True) as f:
            f.raise_for_status()
            self.logger.info('请求状态码为{},开始下载'.format(f.status_code))

            with open(file_name, 'wb') as file:
                for chunk in f.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
        return


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'WkAskci_V1'])
