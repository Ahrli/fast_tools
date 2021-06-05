import pymysql
from dbutils.pooled_db import PooledDB
class SqlHelper(object):
    def __init__(self):
        self.pool = POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数 用才会有
    mincached=2,  # 初始化时，链接池中至少创建的链接，0表示不创建
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    ping=0, # ping MySQL服务端，检查是否服务可用。# 如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is created, 4 = when a query is executed, 7 = always

    host='192.168.249.154',
    port=3306,
    user='root',
    password='example',
    database='big_data',
    charset='utf8'
)

    def open(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn,cursor

    def close(self,cursor,conn):
        cursor.close()
        conn.close()

    def fetchallargs(self,sql, *args):
        """ 获取所有数据 """
        conn,cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchall()
        self.close(conn,cursor)
        return result
    def fetchall(self,sql):
        """ 获取所有数据 """
        conn,cursor = self.open()
        cursor.execute(sql)
        result = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        self.close(conn,cursor)
        return result,columns

    def fetchone(self,sql, *args):
        """ 获取所有数据 """
        conn, cursor = self.open()
        cursor.execute(sql, args)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result


