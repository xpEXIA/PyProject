# encoding=utf8
# create_time:
# python 3.6.4

import random



def sysSeries(length,data_list):

    """
    根据分配的比例形成随机列表
    :param length: int 列表长度
    :param data_list: list 数据列表
        [['a',2],['b',3]]
    :return: list
    """

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

    ori_list =[]
    for i in data_list:
        random_var = random.randint(1,100)
        inter_var = [i,random_var]
        ori_list.append(inter_var)
    return sysList(length=length,data_list=ori_list)


def digitSeries(length,type,begin,end):


    result=[]
    if type == 'int':
        for i in list(range(length)):
           result.append(random.randint(begin,end))
    elif type == 'float':
        for i in list(range(length)):
            result.append(random.uniform(begin,end))
    return result

