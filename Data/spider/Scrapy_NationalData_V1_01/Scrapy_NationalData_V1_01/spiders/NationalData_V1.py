# -*- coding: utf-8 -*-
import scrapy, json, time, requests, re
from Scrapy_NationalData_V1_01.items import ScrapyNationaldataV101Item
from scrapy.http.cookies import CookieJar


class NationaldataV1Spider(scrapy.Spider):
    name = 'NationalData_V1'
    # allowed_domains = ['data.stas.gov.cn']
    # start_urls = ['http://data.stas.gov.cn/']

    # 国家统计局爬取的数据网站
    url = 'http://data.stats.gov.cn/easyquery.htm'

    def start_requests(self):
        key_data = {
            "id": "A07",  # 能源编码：A07
            "dbcode": "hgnd",
            "wdcode": "zb",
            "m": "getTree",
        }
        req = scrapy.FormRequest(url=self.url, callback=self.parse, dont_filter=True, formdata=key_data)
        yield req

    def parse(self, response):
        cookie = {
            'JSESSIONID': '57BF3B3016A6F723BA163F97D74F5A75',
            '_trs_uv': 'k4zanh0s_6_17bx',
            'u': 2,
            "experience": "show",
        }
        # print(cookie)
        get_info = json.loads(response.text)
        print(get_info)
        a = 1
        for info in get_info:
            # print(info)
            Cid = info['id']
            isParent = info['isParent']
            name = info['name']
            pid = info['pid']
            # print(Cid, isParent, name, pid)

            # 建立一级目录
            if a < 10:
                num = f'400100{a}'
            elif (a >= 10) and (a < 100):
                num = f'40010{a}'
            else:
                num = f'4001{a}'

            cate = f'"{num}": "{name}",'
            # print(cate)
            # with open('../cate.text', 'a') as f:
            #     f.write(cate + '\n')
            a += 1

            keyvalue = {}
            # 参数填充
            keyvalue['m'] = 'QueryData'
            keyvalue['dbcode'] = 'hgnd'
            keyvalue['rowcode'] = 'zb'
            keyvalue['colcode'] = 'sj'
            keyvalue['wds'] = '[]'
            keyvalue['k1'] = str(int(round(time.time() * 1000)))

            df = f'["wdcode": "zb", "valuecode": "{Cid}"]'
            keyvalue['dfwds'] = df.replace('[', '[{').replace(']', '}]')
            # print(keyvalue['dfwds'])

            # 第一次请求
            req = scrapy.FormRequest(url=self.url, formdata=keyvalue, cookies=cookie, callback=self.make_cate,
                                     dont_filter=True, meta={'num': num, 'cate': cate, 'Cid': Cid})

            # # # 更改参数，再次请求
            # keyvalue['dfwds'] = '[{"wdcode": "sj", "valuecode": "LAST20"}]'
            # req_again = scrapy.FormRequest(url=self.url, callback=self.make_cate, formdata=keyvalue, cookies=cookie,
            #                                dont_filter=True,
            #                                meta={'num': num, 'cate': cate})

            yield req

    def make_cate(self, response):
        headers = {
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Cookie': '_trs_uv=k4zanh0s_6_17bx; u=2; JSESSIONID=57BF3B3016A6F723BA163F97D74F5A75; experience=show',
        }

        keyvalue = {}
        # 参数填充
        keyvalue['m'] = 'QueryData'
        keyvalue['dbcode'] = 'hgnd'
        keyvalue['rowcode'] = 'zb'
        keyvalue['colcode'] = 'sj'
        keyvalue['wds'] = '[]'
        Cid = response.meta['Cid']
        df = f'["wdcode": "zb", "valuecode": "{Cid}"]'
        keyvalue['dfwds'] = df.replace('[', '[{').replace(']', '}]')
        # keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A070N"}]'
        # print(keyvalue['dfwds'])
        # print(type(keyvalue['dfwds']))
        keyvalue['k1'] = str(int(round(time.time() * 1000)))
        keyvalue['h'] = "1"

        # 第一次请求
        req = requests.post(self.url, headers=headers, data=keyvalue)

        keyvalue['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST20"}]'

        # 再次请求
        req_again = requests.post(self.url, headers=headers, data=keyvalue)

        get_detail = json.loads(req_again.text)

        cate = response.meta['cate']

        print(get_detail)

        print(cate)
        with open('../cate.text', 'a') as f:
            f.write(cate + '\n')

        # 获取目录
        b = 1
        wdnodes = get_detail['returndata']['wdnodes'][0]['nodes']
        for wd in wdnodes:
            c_name = wd['cname']
            code_id = wd['code']
            unit = wd['unit']

            num = response.meta['num']
            if b < 10:
                num = f'{num}00{b}'
            elif (b >= 10) and (b < 100):
                num = f'{num}0{b}'
            else:
                num = f'{num}{b}'

            cate1 = f'"{num}": "{c_name}",'
            print(cate1)
            with open('../cate.text', 'a') as f:
                f.write(cate1 + '\n')
            b += 1

            # 获取数据
            datanodes = get_detail['returndata']['datanodes']
            for co in datanodes:
                valuecode = co['wds'][0]['valuecode']
                # print(valuecode)

                if code_id == valuecode:
                    # print(valuecode)
                    data_value = co['data']['data']
                    year = co['wds'][1]['valuecode']

                    item = ScrapyNationaldataV101Item()
                    # 数据名称
                    item['indic_name'] = c_name
                    # 单位
                    item['unit'] = unit
                    # 数据目录
                    item['parent_id'] = num
                    # 根目录id
                    item['root_id'] = num[:1]
                    # 年、月、日     数据类型：int
                    item['data_year'] = int(year)
                    item['data_month'] = None
                    item['data_day'] = None
                    # 数据产生时间    数据类型：date
                    item['create_time'] = f'{year}-12-31'
                    # 数值
                    item['data_value'] = data_value
                    # 频率(0：季度， 1234： 季度 ，5678：年月周日 )    数据类型：int
                    item['frequency'] = 5
                    # 数据来源(网站名)
                    item['data_source'] = '国家统计局'
                    # 地区
                    item['region'] = '全国'
                    # 国家
                    item['country'] = '中国'
                    # 个人编号  string
                    item['sign'] = '19'
                    # 0:无效  1: 有效       int
                    item['status'] = 1
                    # 0 : 未清洗  1 ： 清洗过      int
                    item['cleaning_status'] = 0
                    # print(item)
                    print(item)
                    yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute(['scrapy', 'crawl', 'NationalData_V1'])
