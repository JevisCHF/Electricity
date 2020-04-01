# import requests, time, json
# from lxml import etree
#
# url = 'http://www.gongyeyinxiang.com/bd/relateds?typeId=1243&cateId=12&limit=200'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
# }
# data = {
#     'typeId': '1383',
#     # 'cateId': '12',
#     # 'limit': '200',
# }
#
# get_prory = requests.get('http://192.168.0.11:5010/get/').json().get('proxy', False)
#
# proxies = {'https': get_prory,
#            }
#
# req = requests.get(url=url, headers=headers, proxies=proxies)
#
# print(req.text)

# detail = {{'code': 200, 'msg': 'success', 'data': {'list': [
#     {'id': '1055230', 'related_data_id': '20017', 'date': '2013', 'num': '189.00', 'create_time': '1517981193',
#      'status': '0', 'rate': '-'},
#     {'id': '1055240', 'related_data_id': '20017', 'date': '2014', 'num': '293.00', 'create_time': '1517981193',
#      'status': '0', 'rate': 55},
#     {'id': '1055250', 'related_data_id': '20017', 'date': '2015', 'num': '556.00', 'create_time': '1517981193',
#      'status': '0', 'rate': 90},
#     {'id': '1055260', 'related_data_id': '20017', 'date': '2016', 'num': '831.00', 'create_time': '1517981193',
#      'status': '0', 'rate': 49}], 'total_count': '4'}}}
# import time
#
# createValue = 1517980695 #以毫秒为单位的时间，自1970年开始到现今
#
# print(time.gmtime(createValue))
#
# a = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(createValue))
# print(a[:10])
import time

task_time = int(input('你觉得自己至少可以专注这个任务多少分钟？输入 N 分钟'))

time_start = time.strftime('%Y/%m/%d %H:%M:%S')
print('自动记录开始时间为{}'.format(time_start))

task_time_s = task_time * 60
while task_time_s:
    print('离结束还剩{}秒'.format(task_time_s))
    time.sleep(1)
    task_time_s -= 1
print('任务时间到！')