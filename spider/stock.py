# coding=utf-8
# version:3.6.4
#

import tushare as ts
from datetime import datetime, timedelta
import pandas.io.sql as sql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from time import sleep
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s/%(filename)s[line:%(lineno)d]/%(levelname)s: %(message)s')


class StockSpider():


    def __init__(self,token='5ea96f455496951c2719b8b3a8daf621b9c8c2ea7ed9d30041a4c867'):

        self.token = token
        self.pro = ts.pro_api(self.token)
        self.fail_list = []


    def _toSql(self,data,table,if_exists):


        if len(data) == 0:
            logging.info('本次获取没有数据，跳过数据库写入')
        else:
            engine = create_engine("mysql+pymysql://root:root@localhost:3306/stock")
            Session = sessionmaker(bind=engine)
            session = Session()
            sql_id = 'select max(id) from ' + table
            cursor = session.execute(sql_id)
            start_id = cursor.fetchall()[0][0]
            session.close()
            if start_id is None:
                start_id = 0
            sql.to_sql(frame=data,name=table,con=engine,index=False,method='multi',if_exists=if_exists)
            session = Session()
            cursor = session.execute(sql_id)
            end_id = cursor.fetchall()[0][0]
            session.close()
            if end_id is None:
                end_id = 0
            rows = end_id - start_id
            if rows == len(data) and if_exists == 'append':
                logging.info('数据在数据库中保存成功且完整')
            elif end_id == len(data) and if_exists == 'replace':
                logging.info('数据在数据库中保存成功且完整')
            else:
                raise ValueError('数据在数据库中保存不完整，请手动验证')



    def data_save(self,data,table,save_type='sql',if_exists='append',path=''):


        if isinstance(data,str):
            logging.error('数据获取失败，失败股票代码为' + data)
            self.fail_list.append(data)
        else:
            if save_type == 'sql':
                self._toSql(data,table,if_exists)
                logging.info('数据保存完毕，保存的数据类型为' + save_type)
            elif save_type == 'csv':
                data.to_csv(path,index=False,encoding='GBK')
                logging.info('数据保存完毕，保存的数据类型为' + save_type + '保存路径：' + path)
            elif save_type == 'excel':
                data.to_csv(path)
                logging.info('数据保存完毕，保存的数据类型为' + save_type + '保存路径：' + path)



    def _stockRequest(self,data_type,ts_code,start_date,end_date,trade_date,fields):

        """

        :param data_type: {'stock_basic':'股票基本信息',
                            'daily':'股票日行情数据',
                            'daily_basic':'股票每日指标数据',
                            'fund_basic':'基金基本信息',
                            'fund_nav':'基金每日净值',
                            'fund_daily':'基金每日行情数据',
                            'fund_portfolio':'基金持仓'
        }
        :param ts_code:
        :param start_date:
        :param end_date:
        :param trade_date:
        :param fields:
        :return:
        """

        if data_type == 'stock_basic':
            data = self.pro.query(data_type, fields,exchange='', list_status='L')
        elif data_type == 'daily':
            data = self.pro.query(data_type, ts_code=ts_code,trade_date=trade_date,
                                  start_date=start_date, end_date=end_date)
        elif data_type == 'daily_basic':
            data = self.pro.query(data_type, ts_code=ts_code,trade_date=trade_date,
                                  start_date=start_date, end_date=end_date)
        elif data_type == 'fund_basic':
            data = self.pro.fund_basic(market='E')
        elif data_type == 'fund_nav':
            data = self.pro.fund_nav(end_date=end_date,market='E')
        elif data_type == 'fund_daily':
            data = self.pro.fund_daily(ts_code=ts_code, trade_date=trade_date,
                                       start_date=start_date, end_date=end_date)
        elif data_type == 'fund_portfolio':
            data = self.pro.fund_portfolio(ts_code=ts_code, trade_date=trade_date,
                                           start_date=start_date, end_date=end_date)
        else:
            raise ValueError('data_type未知，请使用正确的类型')

        return data


    def stockData(self,data_type,ts_code='',start_date='', end_date='',trade_date='',fields=''):


        a = 0
        while a < 3:
            try:
                sleep(0.14)
                data = self._stockRequest(data_type=data_type,ts_code=ts_code,
                                          start_date=start_date, end_date=end_date,
                                          trade_date=trade_date,fields=fields)
                logging.info(data_type + '数据获取成功')
                break
            except:
                a += 1
                if a <= 2:
                    logging.error(data_type + '数据获取失败,获取' + str(a) + '次，重新获取')
                elif a == 3:
                    logging.error(data_type + '数据获取失败,获取' + str(a) + '次，数据获取失败')
                data = ts_code

        return data


    def basicRun(self):

        # 获取所有上市公司股票列表
        data = self.stockData(data_type='stock_basic',
                              fields='ts_code,symbol,name,area,industry,market,list_status,list_date')
        self.data_save(data=data, table='stock_basic')

        # 获取所有开放基金列表
        data = self.stockData(data_type='fund_basic',
                              fields='ts_code,name,management,fund_type,found_date,'
                                     'due_date,list_date,issue_date,issue_amount,m_fee,type')
        self.data_save(data, table='fund_basic')
        logging.info('数据过程中失败的股票代码为' + str(self.fail_list))


    def dailyRun(self, date=datetime.now()):

        date_var = date.strftime('%Y%m%d')
        logging.info('开始获取股票每日行情')
        data = self.stockData(data_type='daily', trade_date=date_var)
        self.data_save(data, table='stock_daily')
        logging.info('开始获取股票每日指标')
        data = self.stockData(data_type='daily_basic', trade_date=date_var)
        self.data_save(data, table='stock_daily_basic')
        logging.info('开始获取基金每日净值')
        date_fund = (date - timedelta(days=1)).strftime('%Y%m%d')
        data = self.stockData(data_type='fund_nav', end_date=date_fund)
        self.data_save(data, table='fund_nav')

        # 获取基金每日行情
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/stock")
        Session = sessionmaker(bind=engine)
        session = Session()
        cursor = session.execute('select ts_code from fund_basic')
        fund_list = cursor.fetchall()
        session.close()
        list = []
        for i in fund_list:
            list.append(i[0])
        begin = 0
        logging.info('开始获取基金每日行情数据')
        while begin <= len(list):
            if len(list) - begin < 790:
                code_str = ','.join(list[begin:len(list)])
                data = self.stockData(data_type='fund_daily', ts_code=code_str, trade_date=date_fund)
                self.data_save(data, table='fund_daily')
                break
            else:
                end = begin + 790
                code_str = ','.join(list[begin:end])
                begin = end
                data = self.stockData(data_type='fund_daily', ts_code=code_str,trade_date=date_fund)
                self.data_save(data, table='fund_daily')
        logging.info('数据过程中失败的股票代码为' + str(self.fail_list))



    def daysRun(self, start_date='', end_date=''):


        # 获取股票每日行情
        engine = create_engine("mysql+pymysql://root:root@localhost:3306/stock")
        Session = sessionmaker(bind=engine)
        session = Session()
        cursor = session.execute('select ts_code from stock_basic')
        stock_list = cursor.fetchall()
        session.close()
        for i in stock_list:
            logging.info('开始获取ts代码为' + i[0] + '的股票每日数据')
            data = self.stockData(data_type='daily', ts_code=i[0], start_date=start_date, end_date=end_date)
            self.data_save(data, table='stock_daily')

        # 获取股票每日指标数据
        for i in stock_list:
            logging.info('开始获取ts代码为' + i[0] + '的股票每日指标数据')
            data = self.stockData(data_type='daily_basic', ts_code=i[0], start_date=start_date, end_date=end_date)
            self.data_save(data, table='stock_daily_basic')

        # 获取基金每日行情
        session = Session()
        cursor = session.execute('select ts_code from fund_basic')
        fund_list = cursor.fetchall()
        session.close()
        for i in fund_list:
            logging.info('开始获取ts代码为' + i[0] + '的基金每日数据')
            date_begin = start_date
            while date_begin <= end_date:
                if (datetime.strptime(end_date, '%Y%m%d') - datetime.strptime(date_begin, '%Y%m%d')).days < 790:
                    data = self.stockData(data_type='fund_daily', ts_code=i[0],
                                          start_date=date_begin, end_date=end_date)
                    self.data_save(data, table='fund_daily')
                    break
                else:
                    date_end = datetime.strptime(date_begin, '%Y%m%d')
                    date_end = date_end + timedelta(days=790)
                    date_var = date_end + timedelta(days=1)
                    date_end = date_end.strftime('%Y%m%d')
                    data = self.stockData(data_type='fund_daily', ts_code=i[0],
                                          start_date=date_begin, end_date=date_end)
                    date_begin = date_var.strftime('%Y%m%d')
                    self.data_save(data, table='fund_daily')

        # 获取基金净值
        days = (datetime.strptime(end_date, '%Y%m%d') - datetime.strptime(start_date, '%Y%m%d')).days
        date_var = datetime.strptime(start_date, '%Y%m%d')
        for i in list(range(days)):
            date_var2 = date_var + timedelta(days=i)
            date_var2 = date_var2.strftime('%Y%m%d')
            logging.info('开始获取基金每日净值日期为' + date_var2)
            data = self.stockData(data_type='fund_nav', end_date=date_var2)
            self.data_save(data, table='fund_nav')
        logging.info('数据过程中失败的股票代码为' + str(self.fail_list))


    def initRun(self,start_date='20100101', end_date='20200710'):

        self.basicRun()
        self.daysRun(start_date=start_date,end_date=end_date)


if __name__ == '__main__':

    stock = StockSpider()
    # stock.dailyRun()
    # stock.initRun(start_date='20200715', end_date='20200803')
    stock.daysRun(start_date='20200715', end_date='20200803')
    # 导入fund_basic数据
    # import pandas as pd
    # pro = ts.pro_api('5ea96f455496951c2719b8b3a8daf621b9c8c2ea7ed9d30041a4c867')
    # data = pro.fund_basic(market='E',fields='ts_code,name,management,fund_type,found_date,due_date,'
    #                                                      'list_date,issue_date,issue_amount,m_fee,type')
    # data.to_csv('C:/Users/Administrator/Desktop/test/asd.csv',index=False,encoding='GBK')
    # data2 = pd.read_csv('C:/Users/Administrator/Desktop/test/asd.csv',encoding='GBK')
    # engine = create_engine("mysql+pymysql://root:root@localhost:3306/stock")
    # sql.to_sql(frame=data,name='fund_basic',con=engine,index=False,method='multi',if_exists='append')
    # data = pro.fund_nav(end_date='20160101', market='E')

