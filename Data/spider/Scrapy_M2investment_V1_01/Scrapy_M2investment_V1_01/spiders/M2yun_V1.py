# -*- coding: utf-8 -*-
import scrapy, json, time
from Scrapy_M2investment_V1_01.items import ScrapyM2InvestmentV101Item
from Scrapy_M2investment_V1_01.cate_id import cate_id


class M2yunV1Spider(scrapy.Spider):
    name = 'M2yun_V1'
    # allowed_domains = ['1234']
    # start_urls = ['http://1234/']
    # 链接：http://www.gongyeyinxiang.com/bd/relateds?typeId=1243&cateId=12&limit=200
    # base_url = 'http://www.gongyeyinxiang.com/bd/relateds'
    # 链接：http://www.gongyeyinxiang.com/bd/datas?dataId=20047&flag=list
    # data_url = 'http://www.gongyeyinxiang.com/bd/datas'

    # 初次请求，获取分类ID，并建立一级目录
    def start_requests(self):
        i = 18
        for name, id in cate_id.items():
            url = f'http://www.gongyeyinxiang.com/bd/relateds?typeId={id}&cateId=12&limit=200'

            if i < 100:
                num = f'40010{ i}'
            else:
                num = f'4001{i}'

            cate = f'"{num}": "{name}", '
            # print(cate)
            # with open('../cate_list.txt', 'a') as file:
            #     file.write(cate + '\n')
            i += 1
            req = scrapy.Request(url=url, callback=self.parse, meta={'num': num, 'cate': cate})

            yield req

    # 继承上级目录
    def parse(self, response):
        config_info = json.loads(response.text)
        cate = response.meta['cate']
        # print(config_info)
        print(cate)
        with open('../cate_list.txt', 'a') as file:
            file.write(cate + '\n')

        a = 1
        for info in config_info['data']['list']:
            title = info['name'].strip()
            Cid = info['id']

            num = response.meta['num']
            if a < 10:
                num = f'{num}00{a}'
            elif (a >= 10) and (a < 100):
                num = f'{num}0{a}'
            elif a >= 100:
                num = f'{num}{a}'

            cate = f'"{num}": "{title}",'
            print(cate)
            a += 1
            with open('../cate_list.txt', 'a') as file:
                file.write(cate + '\n')

            req = scrapy.Request(url=f'http://www.gongyeyinxiang.com/bd/datas?dataId={Cid}&flag=list', callback=self.parse2, meta={'num': num, 'title': title})
            yield req

    # 爬取具体数据
    def parse2(self, response):
        config_info = json.loads(response.text)
        title = response.meta['title']
        parent_id = response.meta['num']
        # print(config_info)

        for info in config_info['data']['list']:
            # print(info)
            date = info['date']
            data_value = info['num']
            create_time = int(info['create_time'])   # 数据产生时间
            a = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(create_time))
            # print(a[:10])
            # print(date, data_value, create_time)

            item = ScrapyM2InvestmentV101Item()
            # 名称
            item['indic_name'] = title
            # 数据目录
            item['parent_id'] = parent_id
            # 根目录id
            n = len(parent_id)
            item['root_id'] = parent_id[:-(n - 1)]
            # 年
            item['data_year'] = int(date[:4])
            # 月
            item['data_month'] = int(date[5:7]) if date[5:7] else None
            # 日
            item['data_day'] = None
            # 频率    频率(0：季度， 1234： 季度 ，5678：年月周日  )

            if '季' in title:
                if item['data_month'] == 3:
                    item['frequency'] = 1
                elif item['data_month'] == 6:
                    item['frequency'] = 2
                elif item['data_month'] == 9:
                    item['frequency'] = 3
                elif item['data_month'] == 12:
                    item['frequency'] = 4
            elif item['data_month']:
                item['frequency'] = 6
            else:
                item['frequency'] = 5

            # 单位
            item['unit'] = None
            # 数据来源(网站名)
            item['data_source'] = '觅途云'
            # 地区
            item['region'] = '全国'
            # 国家
            item['country'] = '中国'
            # 数据产生时间
            item['create_time'] = date
            # # 数据插入时间（爬取时间）
            # item['update_time'] = scrapy.Field()
            # 数值
            item['data_value'] = float(data_value)
            # 个人编号
            item['sign'] = '19'
            # 0:无效  1: 有效
            item['status'] = 1
            # 0 : 未清洗  1 ： 清洗过
            item['cleaning_status'] = 0
            print(item)
            yield item


if __name__ == '__main__':
    from scrapy import cmdline

    cmdline.execute("scrapy crawl M2yun_V1".split())
