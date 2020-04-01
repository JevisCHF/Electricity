import requests


# url = 'http://ipoipo.cn/post/6902.html'
# download = url.replace('post', 'download')
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
#     # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
#     # "Accept-Encoding": "gzip, deflate",
#     # "Accept-Language": "zh-CN,zh;q=0.9",
#     # "Cache-Control": "max-age=0",
#     # "Connection": "keep-alive",
#     # "Host": "ipoipo.cn",
#     # "Referer": "http://ipoipo.cn/tags-69.html",
#     # "Upgrade-Insecure-Requests": "1",
#     # 'Cookie': 'IISSafeDogLGSession=77E5DF483E88DE478D8DB84C25FE0B76; safedog-flow-item=77E5DF483E88DE478D8DB84C25FE0B76; pgv_pvi=4701479936; pgv_si=s9927538688; UM_distinctid=16f9db6f4e1614-020f7cea019c84-33365a06-240000-16f9db6f4e366f; CNZZDATA1261284055=2102031450-1578897314-http%253A%252F%252Fipoipo.cn%252F%7C1578897314; timezone=8',
# }
#
# get_prory = requests.get('http://192.168.0.11:5010/get/').json().get('proxy', False)
#
# proxies = {'http': get_prory,
#            }
#
# req = requests.get(url=download, headers=headers, proxies=proxies)
#
# print(req.text)


def download(url, file_name):
    # headers = {
    #     'Cookie': 'LoginKey=247EF7329DE24E3093ED65E525D44545'
    # }
    with requests.get(url=url, stream=True) as f:
        f.raise_for_status()
        print(f, '开始下载')

        with open(file_name, 'wb') as file:
            for chunk in f.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)


if __name__ == '__main__':
    download('http://ipoipo.cn/zb_users/upload/2019/11/201911121154255010859.zip', '111.zip')
