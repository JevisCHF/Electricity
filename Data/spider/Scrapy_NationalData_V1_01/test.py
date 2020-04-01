import requests, time, json
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
    'Cookie': '_trs_uv=k4zanh0s_6_17bx; u=2; JSESSIONID=57BF3B3016A6F723BA163F97D74F5A75; experience=show',
}

# headers = {
#     'Server': 'nginx',
#     'Date': 'Wed, 08 Jan 2020 07:18:33 GMT',
#     'X-Powered-y': 'anyu.qianxin.com',
#     'X-Frame-Options': 'SAMEORIGIN',
#     # 'Cookie': 'JSESSIONID=A1D973C8603D684CD3D7F6874980DEE6; Path=/; HttpOnly',
#     # 'u': '1',
#     'Wzws-Ray': '1120-1578496713.413-w-waf04tjgt'
# }

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
Cid = "A0702"
df = f'["wdcode": "zb", "valuecode": "{Cid}"]'
keyvalue['dfwds'] = df.replace('[', '[{').replace(']', '}]')
# keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A070N"}]'
# print(keyvalue['dfwds'])
# print(type(keyvalue['dfwds']))
keyvalue['k1'] = str(int(round(time.time() * 1000)))
keyvalue['h'] = "1"

# 第一次请求
req = requests.post(url, headers=headers, data=keyvalue, proxies=proxies)

keyvalue['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST20"}]'

# 再次请求
req_again = requests.post(url=url, headers=headers, data=keyvalue, proxies=proxies)
# print(req_again.text)

returndata = json.loads(req_again.text)
# print(returndata)

code = returndata['returndata']['datanodes']

for co in code:
    print(co)

wdnodes = returndata['returndata']['wdnodes'][0]['nodes']

for wd in wdnodes:
    print(wd)

# req_text = requests.get(url=url, headers=headers, data=keyvalue, proxies=proxies)
#
# print(req.text)
