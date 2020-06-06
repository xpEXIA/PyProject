# encoding=utf8
# create_time:
# python 3.6.4



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

    :param length: int 列表长度
    :param type: int/float 指定连续数列数据类型
    :param begin: int 起始数字
    :param end: int 终点数字
    :return: list
    """
    return digitSeries(length=length,type=type,begin=begin,end=end)

