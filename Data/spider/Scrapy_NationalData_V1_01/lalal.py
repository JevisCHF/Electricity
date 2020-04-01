import requests, time
from lxml import etree

url = 'http://data.stats.gov.cn/easyquery.htm'
# url = 'http://data.stats.gov.cn/adv.htm'

data = {
    "id": "A07",
    "dbcode": "hgnd",
    "wdcode": "zb",
    "m": "getTree",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
}

get_prory = requests.get('http://192.168.0.11:5010/get/').json().get('proxy', False)

proxies = {'http': get_prory,
           }

keyvalue = {}
# 参数填充
keyvalue['m'] = 'QueryData'
keyvalue['dbcode'] = 'hgnd'
keyvalue['rowcode'] = 'zb'
keyvalue['colcode'] = 'sj'
keyvalue['wds'] = '[]'
keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A070N"}]'
keyvalue['k1'] = str(int(round(time.time() * 1000)))

req = requests.get(url, headers=headers, params=keyvalue, proxies=proxies)

print(req.text)
