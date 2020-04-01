# -*- coding: utf-8 -*-

import requests, time, json, re
from lxml import etree

url = 'https://data.iimedia.cn/front/search'
# url = 'https://data.iimedia.cn/front/getObjInfoByNodeId'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    # 'Host': 'wk.askci.com',
}
data = {
    # 关键字查询数据
    'key': '电力',
    'sourceType': '1',
    'nodeIdOfRoot': '0',
    'returnType': '0',

    # 子类数据
    # 'node_id': '13634413',
}

get_prory = requests.get('http://192.168.0.11:5010/get/').json().get('proxy', False)

proxies = {'http': get_prory,
           }

req = requests.post(url=url, headers=headers, data=data, proxies=proxies)

print(req.text)

# urls = {'data': {'objValue': {
#     'form': [['2017-09-30', '10.20'], ['2017-12-31', '11.00'], ['2018-03-31', '13.15'], ['2018-06-30', '8.06'],
#              ['2018-09-30', '2.98'], ['2018-12-31', '6.85'], ['2019-03-31', '16.46'], ['2019-06-30', '11.05'],
#              ['2019-09-30', '5.08']], 'maxColumnNum': 2, 'sourceData': None, 'dataModel': 1, 'isHorizontal': 1},
#                  'nodeInfo': {'nodeId': 27596902, 'name': '华通热力:主要指标:盈利能力指标-加权净资产收益率(%)(按报告期)', 'type': 0},
#                  'objInfo': {'createTime': None, 'dataModel': 1, 'isEnd': 0, 'introduce': '', 'pickTime': 1578153075000,
#                              'unit_id': None, 'endTime': 1569772800000, 'introduce_id': None,
#                              'startTime': 1498752000000, 'data_source_id': None, 'platName': '美国国土安全部', 'platId': 22,
#                              'sourceName': 'iiMedia Research (艾媒咨询)', 'frequenceName': None,
#                              'name': '华通热力:主要指标:盈利能力指标-加权净资产收益率(%)(按报告期)', 'objId': 13558426, 'note': '',
#                              'frequence': None, 'updateTime': 1572668125000, 'isStop': 0, 'isDeleted': 0,
#                              'frequenceMode': -1, 'name_id': None, 'stat': 4, 'unit': '%', 'note_id': None}},
#         'code': '1', 'msg': 'succ'}
# for u in urls['data']:
#     print(u)
