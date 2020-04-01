# -*- coding: utf-8 -*-
import scrapy, time, re, os, requests
from selenium import webdriver
from lxml import etree
from Scrapy_Ipoipo_V1_01.items import ScrapyIpoipoV101Item
from Scrapy_Ipoipo_V1_01.zip_rename import un_zip
from Scrapy_Ipoipo_V1_01.settings import CATES_DICT


class IpoipoV1Spider(scrapy.Spider):
    name = 'ipoipo_V1'
    allowed_domains = ['ipoipo.cn']
    start_urls = ['http://ipoipo.cn/tags-69_2.html']
    download_dir = 'E:\\报告\\report zip\\'

    # 实例化一个浏览器
    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.download_dir,
                 "profile.managed_default_content_settings.images": 2}
        options.add_experimental_option('prefs', prefs)

        self.d = webdriver.Chrome(chrome_options=options)
        super().__init__()

    # def start_requests(self):
    #     pass
        # for i in range(3, 15):
        #     url = f'http://ipoipo.cn/tags-69_{i}.html'
        #     time.sleep(2)
        #     yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        for i in range(1, 3):
            url = f'http://ipoipo.cn/tags-69_{i}.html'
            time.sleep(2)
            self.d.get(url)
            js = "window.scrollTo(0,document.body.scrollHeight)"
            self.d.execute_script(js)
            row_response = self.d.page_source
            html = etree.HTML(row_response)
            content = html.xpath('//div[@id="imgbox"]/div')
            #
            for con in content:
                item = ScrapyIpoipoV101Item()

                name = con.xpath('./h2/a/text()')[0]
                print(name)
                title = name[:-5].replace('（', '')
                download_link = con.xpath('./h2/a/@href')[0].replace('post', 'download')
                date = con.xpath('./div/span[2]/text()')[0]
                print(title, download_link)
                # yield scrapy.Request(url=download_link, callback=self.parse000)
                self.d.get(download_link)
                time.sleep(2)
                self.d.find_element_by_xpath('//div[@class="con main"]/p[2]/a').click()
                time.sleep(15)

                rename = un_zip(self.download_dir, 'E:\\报告\\文件', title + '.pdf', CATES_DICT)
                time.sleep(1)

                # 文章具体路径 id
                try:
                    # item['paper'] = rename['new_name']
                    item['paper'] = None
                    item['parent_id'] = None
                    # item['parent_id'] = rename['root_id']
                    item['abstract'] = None
                    item['title'] = title
                    item['paper_url'] = download_link
                    item['date'] = date
                    item['author'] = None
                    item['paper_from'] = '并购家'

                    # 清洗位
                    item['cleaning_status'] = 0
                    print(item)
                    yield item
                except:
                    print('文件无法保存！！！')

        time.sleep(3)
        self.d.quit()

    # def parse000(self, response):
    #     print(response)


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'ipoipo_V1'])
