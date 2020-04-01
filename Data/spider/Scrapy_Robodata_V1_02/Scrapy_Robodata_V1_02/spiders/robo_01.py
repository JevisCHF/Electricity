# -*- coding: utf-8 -*-
import scrapy, json, os, re
from Scrapy_Robodata_V1_02.items import ScrapyRobodataV102Item


class Robo01Spider(scrapy.Spider):
    name = 'robo_01'
    # allowed_domains = ['gw']
    # start_urls = ['http://gw/']
    base_urls = 'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/'

    def start_requests(self):
        # 登陆
        url = 'https://gw.datayes.com/usermaster/authenticate/web.json'
        data = {
            # me
            'username': 'WQm6aETMyuCLhUCCs+FTybZwma3yzqOUcC4pIvO7mNWrv0fUkcJ8OxyW/ktvnnTcUSokr++Myr+uWk41aLmZoMP6WkHP15/WMHjbMPlTV9YDrB1ionWahfW8kX9zWcwuazxTdi/YXa5v4mMfWTCky01Qrg5BvusQt3T9sZG67wg=',
            'password': 'CFO9q2KtbX8+df8h64wc/66yrmu6XyGv5IsO0/CYo1aKyUtss/lt/+WZkpQYOpcpHNjVo895hePWpkObEC4cBueP5+HKfVLRAXvXt7KJSu6CXZf81FxDM4TbHo4prYe69r9HV5unPS7Q7Ig8H+BPz4y+O3w6WMLRFQzYtJRkEBI=',
            'rememberMe': 'false'
        }
        yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse_data, dont_filter=True)

    # 起始网站
    def parse_data(self, response):
        # 行业分类：能源
        url = 'https://gw.datayes.com/rrp_adventure/web/supervisor/macro/51702'
        req = scrapy.Request(url, callback=self.parse1, dont_filter=True)
        req.headers['referer'] = "https://robo.datayes.com"
        yield req

    # 一级目录
    def parse1(self, response):
        config_info = json.loads(response.text)
        i = 1
        num = ''
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
            with open('cate_file1.text', 'a') as file:
                file.write(cate + '\n')

            i += 1
            id = info['id']
            hasChildren = info['hasChildren']
            indicId = info['indicId']

            if hasChildren:
                url = self.base_urls + id
                yield scrapy.Request(url=url, callback=self.parse2, dont_filter=True, meta={'num': num})
            else:
                url = 'https://gw.datayes.com/rrp_adventure/web/dataCenter/indic/{}?compare=false'.format(indicId)
                yield scrapy.Request(url, callback=self.parse_content, dont_filter=True, meta={'num': num})

    # 继承根目录,判断是否还有子数据，没有则开始爬取数据
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
            with open('cate_file1.text', 'a') as file:
                file.write(cate + '\n')
            a += 1
            id = info['id']
            hasChildren = info['hasChildren']
            indicId = info['indicId']

            if hasChildren:
                url = self.base_urls + id
                yield scrapy.Request(url=url, callback=self.parse2, dont_filter=True, meta={'num': num})
            else:
                url = 'https://gw.datayes.com/rrp_adventure/web/dataCenter/indic/{}?compare=false'.format(indicId)
                yield scrapy.Request(url, callback=self.parse_content, dont_filter=True, meta={'num': num})

    # 开始爬取数据
    def parse_content(self, response):
        parent_id = response.meta['num']
        config_info = json.loads(response.text)
        data_info = config_info['data']['indic']

        name = data_info['indicName']
        region = data_info['region']
        country = data_info['country']

        for info in config_info['data']['data']:
            item = ScrapyRobodataV102Item()
            # 父级目录
            item['parent_id'] = parent_id
            # 根目录id
            n = len(parent_id)
            item['root_id'] = parent_id[:-(n - 1)]

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

            print(item)
            # 调用 mongo api 插入数据到数据库
            # mongoapi = operating(dict(item))
            # print(mongoapi)
            # print(item)


if __name__ == '__main__':
    from scrapy import cmdline

    args = "scrapy crawl robo_01".split()
    cmdline.execute(args)
