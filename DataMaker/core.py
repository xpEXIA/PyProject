# encoding=utf8
# create_time:
# python 3.6.4

from DataMaker.basic import *
from datetime import datetime, timedelta

def discreteSeries(length=0,systematic=False,data_list=[]):

    """
    以指定规则形成一个对应的数据列表
    :param length: int 列表长度
    :param systematic: boolean 是否指定单一数据形成量
    :param data_list: list 以列表形式传递数据
       systematic=True: [['a',2],['b',3]]
    :return: list
    """

    if systematic == True:
        return sysSeries(length=length,data_list=data_list)
    elif systematic == False:
        return oriSeries(length=length,data_list=data_list)
    else:
        return False


def continuousSeries(length=0,type='int',begin=0,end=100):

    """
    获得数字数据列表
    :param length: int 列表长度
    :param type: int/float 指定连续数列数据类型
    :param begin: int/float 起始数字
    :param end: int/float 终点数字
    :return: list
    """
    return digitSeries(length=length,type=type,begin=begin,end=end)


def dateSeries(length=0,type='date',continues=True,begin='',end=''):

    """
    获得日期数据列表
    :param length: int 列表长度
    :param type: date/datetime/timestamp 指定日期格式
        date: %Y/%m/%d
        datetime: %Y/%m/%d %H:%M:%S
    :param continues: boolean 日期是否连续
        :type: date 按天连续
        :type: datetime 按小时连续
    :param begin: str 起始日期
    :param end: str 结束日期
    :return: list
    """
    if begin == '':
        begin_time = datetime.strftime(datetime.now(),'%Y/%m/%d')
    else:
        begin_time = begin
    if end == '':
        end_time = datetime.strftime(datetime.now() + timedelta(days=9),'%Y/%m/%d')
    else:
        end_time = end
    return _dateSeries(length=length,type=type,continues=continues,begin=begin_time,end=end_time)


