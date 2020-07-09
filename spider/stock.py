# coding=utf-8
# version:3.6.4
#

import tushare as ts
from pandas import DataFrame
import pandas as pd
import pymysql
import pandas.io.sql as sql
from sqlalchemy import create_engine
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s/%(filename)s[line:%(lineno)d]/%(levelname)s: %(message)s')


class StockSpider():


    def __init__(self,token='5ea96f455496951c2719b8b3a8daf621b9c8c2ea7ed9d30041a4c867'):

        self.token = token
        self.pro = ts.pro_api(self.token)


    def _toSql(self,data,table):

        con = create_engine()


    def _data_save(self,data,save_type,table,path=''):

        if save_type == 'sql':
            self._toSql(data,table)
            logging.info('数据保存完毕，保存类型为' + save_type)
        elif save_type == 'csv':
            data.to_csv(path,index=False,encoding='GBK')
            logging.info('数据保存完毕，保存类型为' + save_type + '保存路径：' + path)
        elif save_type == 'excel':
            data.to_csv(path)
            logging.info('数据保存完毕，保存类型为' + save_type + '保存路径：' + path)


    def _stockRequest(self,data_type,ts_code,start_date,end_date,trade_date,fields):

        if data_type == 'stock_basic':
            data = self.pro.query(data_type, exchange='', list_status='L')
        elif data_type == 'daily':
            data = self.pro.query(data_type, ts_code=ts_code, start_date=start_date, end_date=end_date)
        elif data_type == 'daily_basic':
            data = self.pro.query(data_type, trade_date=trade_date,fields=fields)
        else:
            raise ValueError('data_type未知，请使用正确的类型')

        return data


    def stockData(self,data_type,save_type='sql',path='',ts_code='',
                  start_date='20140701', end_date='20140718',trade_date='',fields=''):

        a = 0
        while a < 3:
            try:
                data = self._stockRequest(data_type=data_type,ts_code=ts_code,
                                          start_date=start_date, end_date=end_date,
                                          trade_date=trade_date,fields=fields)
                logging.info(data_type + '数据获取成功')
                self._data_save(data=data, save_type=save_type, path=path)
                logging.info(data_type + '数据保存成功')
                break
            except:
                a += 1
                if a <= 2:
                    logging.error(data_type + '数据获取失败,获取' + str(a) + '次，重新获取')
                elif a == 3:
                    logging.error(data_type + '数据获取失败,获取' + str(a) + '次，数据获取失败')


if __name__ == '__main__':

    stock = StockSpider()



