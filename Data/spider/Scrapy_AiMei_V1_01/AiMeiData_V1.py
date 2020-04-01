# -*- coding: utf-8 -*-
import json
import re
import time

import scrapy

# from ..items import ScrapyAimeidataV118Item
# from 行业数据.Scrapy_AiMeiData_V1_18.Scrapy_AiMeiData_V1_18.items import ScrapyAimeidataV118Item


class AimeidataV1Spider(scrapy.Spider):
    name = 'AiMeiData_V1'
    # allowed_domains = ['AiMeiData.com']
    # start_urls = ['http://AiMeiData.com/']
    base_url = "https://data.iimedia.cn/front/childList"

    def start_requests(self):
        url = "https://data.iimedia.cn/user/login"
        data = {
            'phoneNum': '13435522709',
            'password': 'Lx990814',
            'verifyCode': '',
            'countryCode': '86',
            'isSaveLogin': '1',
        }
        yield scrapy.FormRequest(url, formdata=data, callback=self.parse,
                                 dont_filter=True)

    def parse(self, response):
        config_info = json.loads(response.text)
        print(config_info)
        # 直接进入化工页面
        data = {"pid": "71146"}
        req = scrapy.FormRequest(url=self.base_url, formdata=data, callback=self.parse1, dont_filter=True)
        req.headers["referer"] = "https://data.iimedia.cn"
        yield req

    def parse1(self, response):
        config_info = json.loads(response.text)
        i = 28
        num = ''
        for info in config_info["data"]:
            title = info["name"]

            if i < 10:
                num = f'301400{i}'
            elif (i >= 10) and (i < 100):
                num = f'30140{i}'
            elif i >= 100:
                num = f'3014{i}'

            cate = '"{}": "{}",'.format(num, title)

            with open('cate_file1.text', 'a') as file:
                file.write(cate + '\n')

            i += 1
            id = info['id']
            is_end = info["is_end"]
            if is_end:
                data = {"node_id": "{}".format(id)}
                req = scrapy.FormRequest(url="https://data.iimedia.cn/front/getObjInfoByNodeId", formdata=data,
                                         callback=self.parse_detail, dont_filter=True, meta={'num': num})
                yield req
            else:
                data = {"pid": "{}".format(id)}
                req = scrapy.FormRequest(url=self.base_url, formdata=data, callback=self.parse2,
                                         dont_filter=True, meta={'num': num})
                yield req

    def parse2(self, response):
        config_info = json.loads(response.text)
        a = 1
        for info in config_info["data"]:
            num = response.meta['num']

            title = info["name"]
            if a < 10:
                num = f'{num}00{a}'
            elif (a >= 10) and (a < 100):
                num = f'{num}0{a}'
            elif a >= 100:
                num = f'{num}{a}'

            cate = f'"{num}": "{title}",'

            with open('cate_file1.text', 'a') as file:
                file.write(cate + '\n')
            a += 1
            id = info['id']
            is_end = info["is_end"]

            if is_end:
                data = {"node_id": "{}".format(id)}
                req = scrapy.FormRequest(url="https://data.iimedia.cn/front/getObjInfoByNodeId",
                                         formdata=data,
                                         callback=self.parse_detail, dont_filter=True, meta={'num': num})
                yield req
            else:
                data = {"pid": "{}".format(id)}
                req = scrapy.FormRequest(url=self.base_url, formdata=data, callback=self.parse2,
                                         dont_filter=True, meta={'num': num})
                yield req

    def parse_detail(self, response):
        parent_id = response.meta['num']
        config_info = json.loads(response.text)
        print(config_info)
        data_info = config_info['data']
        source = data_info["objInfo"]["sourceName"]
        name = data_info["objInfo"]["name"]
        unit = data_info["objInfo"]["unit"]
        frequency = data_info["objInfo"]["frequenceName"]
        # create_time = data_info["objInfo"]["createTime"][:-3]
        # timeArray = time.localtime(create_time)
        # createtime = time.strftime("%Y--%m--%d", timeArray)
        try:
            region = re.findall(r"\((.*?)\)", name)[0]
        except:
            region = "全国"

        for value in data_info["objValue"]["form"]:
            item = ScrapyAimeidataV118Item()
            # 父级目录
            item['parent_id'] = parent_id
            # 根目录id
            n = len(parent_id)
            item['root_id'] = parent_id[:-(n - 1)]

            # 地区和国家
            item['region'] = region
            item['country'] = "中国"
            create_time = value[0]
            data = value[1]
            data_time = create_time.split('-')
            year = int(data_time[0])
            try:
                month = int(data_time[1])
            except:
                month = None
            try:
                day = int(data_time[2])
            except:
                day = None

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
            if unit:
                item['unit'] = unit
            else:
                item['unit'] = None
            item['data_source'] = source
            # 数据产生时间
            item['create_time'] = create_time
            # 数值
            item['data_value'] = data
            # 个人编号
            item['sign'] = '18'
            # 0:无效  1: 有效
            item['status'] = 1
            # 0 : 未清洗  1 ： 清洗过
            item['cleaning_status'] = 0
            yield item


from scrapy import cmdline

cmdline.execute("scrapy crawl AiMeiData_V1".split())
