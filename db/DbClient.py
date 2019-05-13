import pymysql
import uuid


class DBClient():
    def __init__(self):
        # 打开数据库连接
        self._conn = pymysql.connect("111.231.137.74", "root", "123456", "spider")
        self._cursor = self._conn.cursor()

    def _exeCute(self, sql):
        try:
            self._cursor.execute(sql)
            self._conn.commit()
        except:
            print('error')
