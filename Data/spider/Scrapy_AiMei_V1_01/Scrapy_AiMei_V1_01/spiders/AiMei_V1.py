# -*- coding: utf-8 -*-
import scrapy, json, time, re, csv
from Scrapy_AiMei_V1_01.items import ScrapyAimeiV101Item
from Scrapy_AiMei_V1_01.isCountry import find_region
from Scrapy_AiMei_V1_01.settings import root_id


class AimeiV1Spider(scrapy.Spider):
    name = 'AiMei_V1'
    # allowed_domains = ['AiMeiData.com']
    # start_urls = ['http://AiMeiData.com/']
    base_url = 'https://data.iimedia.cn/front/childList'
    urls = {}

    # json数据接口, post请求
    def start_requests(self):
        # config_info = json.loads(response.text)
        # print(config_info)
        # 直接进入能源页面
        for c, r in root_id.items():
            data = {
                'key': c,
                'sourceType': '1',
                'nodeIdOfRoot': '0',
                'returnType': '0',
            }

            req = scrapy.FormRequest(url='https://data.iimedia.cn/front/search', formdata=data, callback=self.parse1,
                                     dont_filter=True, meta={'cate': c, 'root_id': r, 'data': data})
            req.headers["referer"] = "https://data.iimedia.cn"

            yield req

    # 建立二级目录
    def parse1(self, response):
        try:
            config_info = json.loads(response.text)['data']['index']
            # print(config_info)
            i = 5
            for info in config_info:
                num = response.meta['root_id']
                name = info['name']
                childIds = info['childIds']
                child = info['child']  # 判断是否还有子数据，若为空，则没有子数据

                if i < 10:
                    num = num + f'00{i}'
                elif (i >= 10) and (i < 100):
                    num = num + f'0{i}'
                elif i >= 100:
                    num = num + f'{i}'

                cate = f'"{num}": "{name}",'
                i += 1
                print(cate)
                with open('./new_cate_list5.txt', 'a') as f:
                    f.write(cate + '\n')

                yield from self.rec(num, child, childIds)

        except:
            with open('./retryt5.txt', 'a') as f:
                f.write(str(response.meta['data']) + '\n')

    # 解析数据结构
    def rec(self, root_id, child, childIds):
        if child:
            i = 1
            for childdata in child:
                num = root_id
                name = childdata['name']
                childIds = childdata['childIds']
                child = childdata['child']  # 判断是否还有子数据，若为空，则没有子数据

                if i < 10:
                    num = num + f'00{i}'
                elif (i >= 10) and (i < 100):
                    num = num + f'0{i}'
                elif i >= 100:
                    num = num + f'{i}'

                cate = f'"{num}": "{name}",'
                i += 1
                with open('./new_cate_list5.txt', 'a') as f:
                    f.write(cate + '\n')
                print(cate)
                yield from self.rec(num, child, childIds)
        else:
            i = 1
            # self.urls = {}
            for Ids in childIds:
                if i < 10:
                    num = root_id + f'00{i}'
                elif (i >= 10) and (i < 100):
                    num = root_id + f'0{i}'
                elif i >= 100:
                    num = root_id + f'{i}'

                self.urls[num] = Ids
                i += 1

            for r, Ids in self.urls.items():
                data = {
                    'node_id': str(Ids)
                }
                yield scrapy.FormRequest(url='https://data.iimedia.cn/front/getObjInfoByNodeId',
                                         callback=self.parse_detail,
                                         formdata=data, meta={'root_id': r, 'data': data})

            self.urls = {}

    # 爬取具体数据
    def parse_detail(self, response):
        # pass
        # print('来啦老弟！！！', response.meta['data'])
        try:
            num = response.meta['root_id']
            # print(num)
            config_info = json.loads(response.text)
            # print(config_info)
            data_info = config_info['data']
            try:
                source = data_info["objInfo"]["sourceName"]
            except:
                source = None
            name = data_info["objInfo"]["name"]
            unit = data_info["objInfo"]["unit"]
            frequency = data_info["objInfo"]["frequenceName"]

            # print(name)
            cate = f'"{num}": "{name}",'
            print(cate)
            with open('./new_cate_list5.txt', 'a') as f:
                f.write(cate + '\n')

            for value in data_info["objValue"]["form"]:

                item = ScrapyAimeiV101Item()
                # 父级目录
                item['parent_id'] = num
                # 名称
                item['indic_name'] = name
                # 根目录id
                n = len(num)
                item['root_id'] = num[:-(n - 1)]

                # 地区和国家
                country = find_region(name)
                item['region'] = country['region']
                item['country'] = country['country']
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

                # 年
                item['data_year'] = year if year else 0
                # 月
                item['data_month'] = month if month else 0
                # 日
                item['data_day'] = day if day else 0

                if frequency == '年':
                    # 频率
                    item['frequency'] = 5

                elif frequency == '季度':
                    # 频率
                    item['frequency'] = 5

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
                    # 频率
                    item['frequency'] = 6

                elif frequency == '周':
                    # 频率
                    item['frequency'] = 7

                elif frequency == '天':
                    # 频率
                    item['frequency'] = 8

                else:
                    # 频率
                    item['frequency'] = 0

                if unit:
                    item['unit'] = unit
                else:
                    item['unit'] = None

                # 数据来源
                item['data_source'] = source
                # 数据产生时间
                item['create_time'] = create_time
                # 数值
                item['data_value'] = float(data)
                # 个人编号
                item['sign'] = '19'
                # 0:无效  1: 有效
                item['status'] = 1
                # 0 : 未清洗  1 ： 清洗过
                item['cleaning_status'] = 0
                yield item
                # print(item)
        except:
            with open('./retryt5.txt', 'a') as f:
                f.write(str(response.meta['data']) + '\n')


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl AiMei_V1".split())
