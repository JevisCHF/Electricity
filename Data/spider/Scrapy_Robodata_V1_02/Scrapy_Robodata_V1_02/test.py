# -*- coding: utf-8 -*-

import requests, time, json, re
from lxml import etree

url = 'http://wk.askci.com/details/46cfdb37d2c9483683bd62afdf4e60cc/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
    # 'Host': 'wk.askci.com',
}
data = {
    # "ThePhone": "18819492919",
    # "ThePassword": "2a810c88e3cb947e85bbab2728102f0d",
    # "TheCode": "8",
    # 'id': '04926ffd3ea849d69411681e7f5bb672',
}

get_prory = requests.get('http://192.168.0.11:5010/get/').json().get('proxy', False)

proxies = {'http': get_prory,
           }

req = requests.get(url=url, headers=headers, proxies=proxies, allow_redirects=False)

Coo = req.headers['Set-Cookie']
link = re.search(r'wkpdfpath=(.+); domain=', Coo).group(1).replace('%253a', ':').replace('%252f', '/')
print(link)

# http://wkpdf.askci.com/19-12-03/2019123101123306.pdf

# headers = {
#     "user-agent": "mozilla/5.0 (windowS NT 6.1; win64; x64) appLewEbkit/537.36 (KHTML, likE gecko) chrome/78.0.3904.108 safari/537.36",
#     # "Cookie": "LoginKey=71403CB7E7A74FFAA98DF6A801A14EF0",
# }
# with requests.get('http://user.askci.com/ReportDownload/09c685d8ecea4fcba43124254ec317f3',
#                   stream=True, headers=headers) as r:
#     r.raise_for_status()
#
#     print(('请求状态码为{},开始下载'.format(r.status_code)))
#     with open('111.pdf', 'wb') as f:
#         for chunk in r.iter_content(chunk_size=1024):
#             if chunk:  # filter out keep-alive new chunks
#                 f.write(chunk)


