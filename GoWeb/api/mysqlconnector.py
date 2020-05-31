# encoding=utf8
# create_time:
# python 3.6.4


import pymysql
import pymysql.cursors
from GoWeb.settings import MYSQL_CONFING
import logging

logSql = logging.getLogger('sql')



class MysqlExecute():

    '''
    用户连接mysql数据库，进行CURD操作
    '''

    def __init__(self, set=MYSQL_CONFING):


        self.con = pymysql.connect(host=set['host'],user=set['user_name'],password=set['password'],
                                   port=set['port'],database=set['database'],charset=set['charset'],
                                   cursorclass=set['pymysql.cursors.DictCursor'])
        self.cursor = self.con.cursor()

    def success(self,type):

        self.cursor.execute('select last_insert_id()')

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

    def multiple_modify(self,sql,args):

        self.cursor.executemany(sql,args)
        self.con.commit()

    def create(self,sql,args):

        self.cursor.execute(sql,args)
        self.con.commit()
        return self.cursor.lastrowid

    def close(self):

        self.cursor.close()
        self.con.close()

mysqlExe = MysqlExecute()