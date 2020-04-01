import pymysql


class DB():
    def __init__(self):
        # 连接database
        # self.db = pymysql.connect(host="192.168.0.11", user="root", password="123456",
        #                        database="lab_test",charset="utf8")
        self.db = pymysql.connect(host="localhost", user="root", password="root",
                                  database="python", charset="utf8")
        # 得到一个可以执行SQL语句的光标对象
        self.cursor = self.db.cursor()

    # 定义要执行的SQL语句
    def update(self, sql, data):
        try:
            self.cursor.execute(sql, data)
            self.db.commit()
        except:
            print("操作失败，请检查sql语句")

    def query(self, sql):
        try:
            self.cursor.execute(sql)
            data = self.cursor.fetchall()
            return data
        except:
            print("查询失败，请检查sql语句")

    def __del__(self):
        # 关闭光标对象
        self.cursor.close()
        # 关闭数据库连接
        self.db.close()


if __name__ == '__main__':
    # 测试这个代码好使不好使
    db = DB()
    sql = 'SELECT * FROM students'
    data = db.query(sql)
    print(data)
