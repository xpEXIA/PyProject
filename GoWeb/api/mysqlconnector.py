# encoding=utf8
# create_time:
# python 3.6.4


import pymysql
import pymysql.cursors
from GoWeb.settings import logSql



class MysqlExecute():

    '''
    用户连接mysql数据库，进行CURD操作
    '''

    def __init__(self, user_name='root',password='root',host='localhost',
                 port='3303',database='goweb',charset='utf8mb4'):

        self.con = pymysql.connect(host=host,user=user_name,password=password,
                                   port=port,database=database,charset=charset,cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.con.cursor()


    def get_table(self,sql,args):

        self.cursor.execute(sql,args)
        result = self.cursor.fetchall()
        return result

    def get_row(self,sql,args):

        self.cursor.execute(sql, args)
        result = self.cursor.fetchone()
        return result

    def modify(self,sql,args):

        self.cursor.execute(sql,args)
        self.con.commit()

