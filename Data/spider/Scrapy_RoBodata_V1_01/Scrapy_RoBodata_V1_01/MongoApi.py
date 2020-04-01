import requests
import re
import json
import datetime

# 查找
url = 'http://192.168.0.22:8025/chineseMacro/select'

# 查询所有
url1 = "http://192.168.0.22:8025/chineseMacro/selectAll"

# 插入
url2 = 'http://192.168.0.22:8025/chineseMacro/insert'

# 更新
url3 = 'http://192.168.0.22:8025/chineseMacro/update'

# 删除
url4 = 'http://192.168.0.22:8025/chineseMacro/delete'

insert_data = {
    "data_day": 31,
    "country": 5,
    "create_time": "2019-11-12",
    "sign": "wu",
    "data_year": 2019,
    "data_source": "www.baidu.com",
    "frequency": 0,
    "unit": "元",
    "parent_id": 1001001,
    "data_value": 3.16,
    "cleaning_status": 0,
    "data_month": 10,
    "indic_name": "test",
    "root_id": 10,
    "region": "test",
    "status": 1
}

update_data = {"query": {'data_value': 3.14}, 'updateParam': {"status": 1}}

select_data = {"query": {"indic_name": "test", "data_value": 3.16}, "limit": 5}

delete_data = {"query": {"status": 1, "data_value": 3.14}}


def operating(data):
    s = requests.Session()
    url = "http://192.168.0.22:8025/chineseMacro/selectAll"
    res = s.post(url=url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    return res.text


if __name__ == '__main__':
    pass
    # res = operating(url, select_data)
    # print(res)
