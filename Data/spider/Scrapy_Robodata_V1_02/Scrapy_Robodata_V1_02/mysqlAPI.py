# -*- coding: utf-8 -*-
import pymysql
from Scrapy_Robodata_V1_02.power_new import cate
# from Scrapy_Robodata_V1_02.sql import cate


def connect():
    conn = pymysql.connect(host="localhost",
                           port=3306,
                           user="root",
                           password="root",
                           database="power_dir",
                           charset="utf8")
    db = conn.cursor()
    return db, conn


def insert(sql):
    db, conn = connect()
    try:

        info = db.execute(sql)
        print(info)
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()


def main():
    for key, value in cate.items():

        if len(key) <= 4:
            parent_menu_id = key[0]
            id = key
            menu_name = value
            sql = "insert into building_dir(id, menu_name, parent_menu_id) values('%s','%s','%s');" % (id, menu_name, parent_menu_id)
            # print(sql)
            insert(sql)
        else:
            parent_menu_id = key[:-3]
            id = key
            menu_name = value
            sql = "insert into building_dir(id, menu_name, parent_menu_id) values('%s','%s','%s');" % (id, menu_name, parent_menu_id)
            # print(sql)
            insert(sql)


if __name__ == '__main__':
    main()
