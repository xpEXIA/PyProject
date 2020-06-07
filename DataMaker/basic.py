# encoding=utf8
# create_time:
# python 3.6.4

import random
from datetime import datetime, timedelta


def sysSeries(length,data_list):

    """
    根据分配的比例形成随机列表
    :param length: int 列表长度
    :param data_list: list 数据列表
        [['a',2],['b',3]] 根据为每个字符串指定的数字比例形成数据
    :return: list
    """

    assert length == int(length), 'length must be int'

    sum_num = 0
    for i in data_list:
        sum_num += i[1]
    result=[]
    for i in data_list:
        result.extend([i[0]] * round(length * i[1] / sum_num))
    random.shuffle(result)
    while len(result) > length:
        result.pop()
    return result


def oriSeries(length,data_list):

    """
    随机分配比例形成随机列表
    :param length: int 列表长度
    :param data_list: list 数据列表
        ['a','b','c']
    :return: list
    """

    ori_list=[]
    for i in data_list:
        random_var = random.randint(1,100)
        inter_var = [i,random_var]
        ori_list.append(inter_var)
    return sysSeries(length=length,data_list=ori_list)


def digitSeries(length,type,begin,end):

    """
    形成数字数据列表
    :param length: int 列表长度
    :param type: int/float 指定连续数列数据类型
    :param begin: int/float 起始数字
    :param end: int/float 终点数字
    :return: list
    """

    assert type in ['int','float'], 'type must be int or float'

    result=[]
    if type == 'int':
        for i in list(range(length)):
           result.append(random.randint(begin,end))
    elif type == 'float':
        for i in list(range(length)):
            result.append(random.uniform(begin,end))
    return result


def _dateSeries(length,type,continues,begin,end):

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

    assert type in ['date','datetime','timestamp'], 'type must be date/datetime/timestamp'

    date_list = []
    if type == 'date':
        date_interval = datetime.strptime(end,'%Y/%m/%d') - datetime.strptime(begin,'%Y/%m/%d')
        for i in list(range(date_interval.days + 1)):
            date = datetime.strptime(begin, '%Y/%m/%d') + timedelta(days=i)
            date_list.append(datetime.strftime(date, '%Y/%m/%d'))
        if continues is False:
            date_list = random.sample(date_list, random.randint(int(len(date_list) / 2),date_interval.days)).sort()
        return oriSeries(length=length,data_list=date_list)
    elif type == 'datetime':
        date_interval = datetime.strptime(end, '%Y/%m/%d %H:%M:%S') - datetime.strptime(begin, '%Y/%m/%d %H:%M:%S')
        hour_interval = date_interval.days * 24 + int(date_interval.seconds / 3600)
        second_interval = date_interval.seconds % 3600
        for i in list(range(hour_interval + 1)):
            date = datetime.strptime(begin, '%Y/%m/%d %H:%M:%S') + timedelta(hours=i)
            date_list.append(datetime.strftime(date, '%Y/%m/%d %H:%M:%S'))
        if continues is False:
            date_list = random.sample(date_list, random.randint(int(len(date_list) / 2), date_interval.days)).sort()
        result = oriSeries(length=length, data_list=date_list)
        a = [datetime.strptime(x, '%Y/%m/%d %H:%M:%S') + timedelta(seconds=random.randint(0,3600))
             for i in result if x != date_list[-1]]
        b = [datetime.strptime(x, '%Y/%m/%d %H:%M:%S') + timedelta(seconds=random.randint(0,second_interval))
             for i in result if x == date_list[-1]]
        result = a.extend(b)
        return result.sort()
    elif type == 'timestamp':
        return digitSeries(length=length,type='float',begin=begin,end=end)


def sysRelatedSeries(length,data_dict):

    """
    获取具有对应关系的两列数组
    :param length: int 列表长度
    :param data_dict: dict 以字典形式传递
         {'a':[['q',3],['w',5]], 'b':[['e',5],['t',8]]} 根据为每个字符串指定的数字比例形成数据
    :return: list
    """

    assert length == int(length), 'length must be int'

    sum_num = 0
    for i in data_dict:
        for x in data_dict[i]:
            sum_num += x[1]
    result=[]
    for i in data_dict:
        inter_num = 0
        inter_result=[]
        for x in data_dict[i]:
            inter_num += x[1]
        inter_list = sysSeries(length=round(inter_num * length / sum_num), data_list=data_dict[i])
        for y in inter_list:
            inter_result.append([[i,y]])
        result.extend(inter_result)
    random.shuffle(result)
    while len(result) > length:
        result.pop()
    return result


def oriRelatedSeries(length,data_dict):

    """
    获取具有对应关系的两列数组
    :param length: int 列表长度
    :param data_dict: dict 以字典形式传递
        {'a':['q','w'], 'b':['e','t']}
    :return: list
    """

    random_length=[]
    random_length_sum = 0
    for i in data_dict:
        random_var = random.randint(1,100)
        random_length.append(random_var)
        random_length_sum += random_var

    result=[]
    for i in data_dict:
        inter_list = oriSeries(length=round(random_length.pop() / random_length_sum * length),
                               data_list=data_dict[i])
        inter_result=[]
        for x in inter_list:
            inter_result.append([i,x])
        result.extend(inter_result)
    random.shuffle(result)
    while len(result) > length:
        result.pop()
    return result