# -*- coding: utf-8 -*-
import scrapy, json


class CateFileSpider(scrapy.Spider):
    name = 'cate_file'
    # allowed_domains = ['gw.datayes.com']
    # start_urls = ['http://gw.datayes.com/']
    base_urls = 'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/'

    def start_requests(self):
        # 登陆
        url = 'https://gw.datayes.com/usermaster/authenticate/web.json'
        data = {
            'username': 'SJ9ewX/91/JpbPizq6p6ine07BwjSsK6d5gav20ZozVam3SfMXv/hNlNuJUKU0j2H7Llz/27NlqQDSWhzHiXFUSROTmG0hl3VItbEtdaFBVI8w/grde8CN5HTKE2OPcoGXagHdXWIiCAn/rEgkN073LnaVs9BseQOf9HTyqRazU=',
            'password': 'mt96Nqa/bxmP2QVFdDlev+IyTAUUY6cMApxU7Bi/Q7QmzCssDaN0VcfeqGHu2BfoGptcO0saZaBUySf+3Uouyqd0kIvlpUiy9uIkb+UVhcY5Vl2+7LydDqip9LCiELGLxRv1ymDi9gZ4I51Ky2C8DOc0C/tPMM+P3FcqGU7muAQ=',
            'rememberMe': 'false'
        }
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse_data, dont_filter=True)

    def parse_data(self, response):
        # url = 'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/26304'
        # 能源
        url = 'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/51702'
        req = scrapy.Request(url=url, callback=self.parse1, dont_filter=True)
        req.headers['referer'] = "https://robo.datayes.com"
        yield req

    def parse1(self, response):
        config_info = json.loads(response.text)
        ids = []
        i = 1
        num = []
        for info in config_info["data"]["childData"]:
            title = info['nameCn']

            if i < 10:
                num = f'400100{i}'
            elif (i >= 10) and (i < 100):
                num = f'40010{i}'
            elif i >= 100:
                num = f'4001{i}'

            cate = f'"{num}": "{title}",'
            print(cate)
            with open('cate_file.text', 'a') as file:
                file.write(cate + '\n')

            i += 1
            id = info['id']
            # ids.append(id)
            indicId = info['indicId']
            hasChildren = info['hasChildren']

            if hasChildren:
                url = self.base_urls + id
                yield scrapy.Request(url=url, callback=self.parse2, dont_filter=True, meta={'num': num})
            # else:
            #     url = 'https://gw.datayes.com/rrp_adventure/web/dataCenter/indic/{}?compare=false'.format(indicId)
            #     yield scrapy.Request(url=url, callback=self.parse_content, dont_filter=True)

    def parse2(self, response):

        config_info = json.loads(response.text)
        a = 1
        for info in config_info["data"]["childData"]:
            num = response.meta['num']
            title = info['nameCn']
            if a < 10:
                num = f'{num}00{a}'
            elif (a >= 10) and (a < 100):
                num = f'{num}0{a}'
            elif a >= 100:
                num = f'{num}{a}'

            cate = f'"{num}": "{title}",'
            print(cate)
            with open('cate_file.text', 'a') as file:
                file.write(cate + '\n')
            a += 1
            id = info['id']
            hasChildren = info['hasChildren']

            if hasChildren:
                url = self.base_urls + id
                yield scrapy.Request(url=url, callback=self.parse2, dont_filter=True, meta={'num': num})


    # def parse3(self, response):
    #
    #     config_info = json.loads(response.text)
    #     i = 1
    #
    #     for info in config_info["data"]["childData"]:
    #         num = response.meta['num']
    #
    #         title = info['nameCn']
    #         if i < 10:
    #             num = f'{num}00{i}'
    #         elif (i >= 10) and (i < 100):
    #             num = f'{num}0{i}'
    #         elif i >= 100:
    #             num = f'{num}{i}'
    #
    #         cate = f'"{num}": "{title}",'
    #         print(cate)
    #         with open('new_cate.text', 'a') as file:
    #             file.write(cate + '\n')
    #             file.close()
    #         i += 1
    #         id = info['id']
    #         hasChildren = info['hasChildren']
    #
    #         if hasChildren:
    #             url = self.base_urls + id
    #             yield scrapy.Request(url=url, callback=self.parse4, dont_filter=True, meta={'num': num})
    #
    # def parse4(self, response):
    #
    #     config_info = json.loads(response.text)
    #     i = 1
    #
    #     for info in config_info["data"]["childData"]:
    #         num = response.meta['num']
    #
    #         title = info['nameCn']
    #         if i < 10:
    #             num = f'{num}00{i}'
    #         elif (i >= 10) and (i < 100):
    #             num = f'{num}0{i}'
    #         elif i >= 100:
    #             num = f'{num}{i}'
    #
    #         cate = f'"{num}": "{title}",'
    #         print(cate)
    #         with open('new_cate.text', 'a') as file:
    #             file.write(cate + '\n')
    #             file.close()
    #         i += 1
    #         id = info['id']
    #         hasChildren = info['hasChildren']
    #
    #         if hasChildren:
    #             url = self.base_urls + id
    #             yield scrapy.Request(url=url, callback=self.parse5, dont_filter=True, meta={'num': num})
    #
    # def parse5(self, response):
    #
    #     config_info = json.loads(response.text)
    #     i = 1
    #
    #     for info in config_info["data"]["childData"]:
    #         num = response.meta['num']
    #
    #         title = info['nameCn']
    #         if i < 10:
    #             num = f'{num}00{i}'
    #         elif (i >= 10) and (i < 100):
    #             num = f'{num}0{i}'
    #         elif i >= 100:
    #             num = f'{num}{i}'
    #
    #         cate = f'"{num}": "{title}",'
    #         print(cate)
    #         with open('new_cate.text', 'a') as file:
    #             file.write(cate + '\n')
    #             file.close()
    #         i += 1
    #         id = info['id']
    #         hasChildren = info['hasChildren']
    #
    #         if hasChildren:
    #             url = self.base_urls + id
    #             yield scrapy.Request(url=url, callback=self.parse6, dont_filter=True, meta={'num': num})
    #
    # def parse6(self, response):
    #
    #     config_info = json.loads(response.text)
    #     i = 1
    #
    #     for info in config_info["data"]["childData"]:
    #         num = response.meta['num']
    #
    #         title = info['nameCn']
    #         if i < 10:
    #             num = f'{num}00{i}'
    #         elif (i >= 10) and (i < 100):
    #             num = f'{num}0{i}'
    #         elif i >= 100:
    #             num = f'{num}{i}'
    #
    #         cate = f'"{num}": "{title}",'
    #         print(cate)
    #         with open('new_cate.text', 'a') as file:
    #             file.write(cate + '\n')
    #             file.close()
    #         i += 1
    #         id = info['id']
    #         hasChildren = info['hasChildren']
    #
    #         if hasChildren:
    #             url = self.base_urls + id
    #             yield scrapy.Request(url=url, callback=self.parse6, dont_filter=True, meta={'num': num})


if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl cate_file".split()
    cmdline.execute(args)
