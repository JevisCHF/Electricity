# -*- coding: utf-8 -*-
import scrapy, json, os, re
from Scrapy_RoBodata_V1_01.items import ScrapyRobodataV101Item
from Scrapy_RoBodata_V1_01.proxy import get_proxy
from Scrapy_RoBodata_V1_01.cos_similarity import similarity
from Scrapy_RoBodata_V1_01.settings import COUNTRY, PROVINCES


class ScrapyRobodata01Spider(scrapy.Spider):
    name = 'scrapy_RoboData_01'
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
        # 爬取行业类型：能源
        url = 'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/757383'
        req = scrapy.Request(url, callback=self.parse, dont_filter=True)
        # req.headers['referer'] = "https://robo.datayes.com"
        yield req

    def parse(self, response):
        config_info = json.loads(response.text)
        print(config_info)
        for info in config_info["data"]["childData"]:
            name = info["nameCn"]
            id = info["id"]
            indicId = info['indicId']
            hasChildren = info['hasChildren']
            # yield scrapy.Request(url=url, callback=self.parse_page, dont_filter=True, meta={'name': name})
            if hasChildren:
                url = self.base_urls + id
                yield scrapy.Request(url, callback=self.parse, dont_filter=True)
            else:
                url = 'https://gw.datayes.com/rrp_adventure/web/dataCenter/indic/{}?compare=false'.format(indicId)
                yield scrapy.Request(url, callback=self.parse_content, dont_filter=True)

    def parse_content(self, response):
        config_info = json.loads(response.text)
        data_info = config_info['data']['indic']
        s = similarity()
        name = data_info['indicName']
        region = data_info['region']
        country = data_info['country']
        print(name)
        # 根据指标名称相似度进行分类处理
        result = s.calcSimilarity(name)
        if result:
            for info in config_info['data']['data']:
                item = ScrapyRobodataV101Item()
                # 父级目录
                item['parent_id'] = result
                # 根目录id
                n = len(result)
                item['root_id'] = result[:-(n - 1)]

                # 地区和国家
                item['region'] = region
                item['country'] = country

                # 数值
                data = info['dataValue']
                # 名称
                item['indic_name'] = name

                data_time = info['periodDate'].replace('-', '')
                frequency = data_info['frequency']
                # 频率
                year = int(data_time[0:4])
                month = int(data_time[4:6])

                day = int(data_time[6:8])
                if frequency == '年':
                    # 年
                    item['data_year'] = year
                    # 月
                    item['data_month'] = None
                    # 日
                    item['data_day'] = None
                    # 频率
                    item['frequency'] = 5

                elif frequency == '季':
                    # 年
                    item['data_year'] = year
                    # 月
                    item['data_month'] = month
                    # 日
                    item['data_day'] = None

                    # 频率
                    if month == 3:
                        item['frequency'] = 1
                    elif month == 6:
                        item['frequency'] = 2
                    elif month == 9:
                        item['frequency'] = 3
                    elif month == 12:
                        item['frequency'] = 4

                elif frequency == '月':
                    # 年
                    item['data_year'] = year
                    # 月
                    item['data_month'] = month
                    # 日
                    item['data_day'] = None
                    # 频率
                    item['frequency'] = 6

                elif frequency == '周':
                    # 年
                    item['data_year'] = year
                    # 月
                    item['data_month'] = month
                    # 日
                    item['data_day'] = day
                    # 频率
                    item['frequency'] = 7

                elif frequency == '日':
                    # 年
                    item['data_year'] = year
                    # 月
                    item['data_month'] = month
                    # 日
                    item['data_day'] = day
                    # 频率
                    item['frequency'] = 8
                else:
                    # 年
                    item['data_year'] = None
                    # 月
                    item['data_month'] = None
                    # 日
                    item['data_day'] = None
                    # 频率
                    item['frequency'] = None

                # 单位
                unit = data_info['unit']
                if unit:
                    item['unit'] = unit
                else:
                    suffix = re.findall(r'\((.*?)\)', name)
                    num = len(suffix)
                    if suffix:
                        item['unit'] = suffix[num - 1]
                    else:
                        item['unit'] = None

                # 数据来源(网站名)
                item['data_source'] = data_info['dataSource']

                # 判断国别地区
                # t = re.findall(r':(.\D)', name)
                # if t:
                #     for region in t:
                #         region = region.replace('省', '').replace('市', '')
                #         if any(tag in region for tag in COUNTRY):
                #             # 国家
                #             item['country'] = region
                #             # 地区
                #             item['region'] = '全国'
                #         else:
                #             if any(tag in region for tag in PROVINCES['all']):
                #                 # 地区
                #                 item['region'] = region
                #                 item['country'] = '中国'
                #             elif any(tag in region + '市' for tag in PROVINCES['city']):
                #                 # 地区
                #                 item['region'] = region
                #                 item['country'] = '中国'
                #             else:
                #                 item['country'] = '中国'
                #                 # 地区
                #                 item['region'] = '全国'
                # else:
                #     item['country'] = '中国'
                #     # 地区
                #     item['region'] = '全国'

                # regin = self.find_region(name)
                # item['country'] = regin['country']
                # # 地区
                # item['region'] = regin['region']

                # 数据产生时间
                item['create_time'] = info['periodDate']
                # 数值
                item['data_value'] = data
                # 个人编号
                item['sign'] = '19'
                # 0:无效  1: 有效
                item['status'] = 1
                # 0 : 未清洗  1 ： 清洗过
                item['cleaning_status'] = 0
                yield item
                # 调用 mongo api 插入数据到数据库
                # mongoapi = operating(dict(item))
                # print(mongoapi)
                # print(item)

    def find_region(self, name):
        item = {}
        # 国家
        for c in COUNTRY:
            if c in name:
                if c != '中国':
                    item['country'] = c
                    item['region'] = '全球'
        # 地区
        for p in PROVINCES['all']:
            if p in name:
                item['country'] = '中国'
                item['region'] = p
                break
        for city in PROVINCES['city']:
            key = city.replace('市', '')
            if key in name:
                item['country'] = '中国'
                item['region'] = city
                break
        if len(item) <= 0:
            # 国家
            item['country'] = '中国'
            # 地区
            item['region'] = '全国'
        return item


if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl scrapy_RoboData_01".split()
    cmdline.execute(args)


