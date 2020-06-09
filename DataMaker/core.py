# encoding=utf8
# create_time:
# python 3.6.4

from DataMaker.basic import *
from DataMaker.basic import _dateSeries



def discreteSeries(length=0,systematic=False,data_list=[]):

    """
    以指定规则形成一个对应的数据列表
    :param length: int 列表长度
    :param data_list: list 以列表形式传递数据
       systematic=True: [['a',2],['b',3]] 根据为每个字符串指定的数字比例形成数据
       systematic=False: ['a','b']
    :return: list
    """

    assert isinstance(data_list, list), 'data_list must be list'

    if systematic == True:
        return sysSeries(length,data_list)
    else:
        return oriSeries(length,data_list)


def continuousSeries(length=0,type='int',distribution='uniform',begin=0,end=100,
                     low=0,high=1,mode=None,mu=0,sigma=2,lambd=1,kappa=1,alpha=1,beta=1):

    """
    获得数字数据列表
    :param length: int 列表长度
    :param type: int/float 指定连续数列数据类型
    :param distribution: 指定数据分布，只有float能指定分布
        None为随机分布，
        distribution_dict = {
        'None': random.uniform(begin,end), 随机分布
        'triangular': random.triangular(low=low, high=high, mode=mode), 三角分布
        'normalvariate': random.normalvariate(mu, sigma), 正态分布
        'lognormvariate': random.lognormvariate(mu, sigma), 对数正态分布
        'expovariate': random.expovariate(lambd), 指数分布
        'vonmisesvariate': random.vonmisesvariate(mu, kappa), 卡帕分布
        'gammavariate': random.gammavariate(alpha, beta), 伽马分布
        'gauss': random.gauss(mu, sigma), 高斯分布
        'betavariate': random.betavariate(alpha,beta), beta分布
        'paretovariate': random.paretovariate(alpha), 帕累托分布
        'weibullvariate': random.weibullvariate(alpha,beta) 威尔分布
        }
    :param begin: int/float 起始数字
    :param end: int/float 终点数字
    :return: list
    """
    return digitSeries(length=length,type=type,distribution=distribution,begin=begin,end=end,
                       low=low,high=high,mode=mode,mu=mu,sigma=sigma,
                       lambd=lambd,kappa=kappa,alpha=alpha,beta=beta)


def dateSeries(length=0,type='date',continues=True,begin='',end=''):

    """
    获得日期数据列表
    :param length: int 列表长度
    :param type: date/datetime/timestamp 指定日期格式
        date: %Y/%m/%d
        datetime: %Y/%m/%d %H:%M:%S
    :param continues: boolean 日期是否连续
        type: date 按天连续
        type: datetime 按小时连续
    :param begin: str 起始日期
    :param end: str 结束日期
    :return: list
    """

    from datetime import datetime, timedelta

    if begin == '':
        begin_time = datetime.strftime(datetime.now(),'%Y/%m/%d')
    else:
        begin_time = begin
    if end == '':
        end_time = datetime.strftime(datetime.now() + timedelta(days=9),'%Y/%m/%d')
    else:
        end_time = end
    return _dateSeries(length=length,type=type,continues=continues,begin=begin_time,end=end_time)


def relatedSeries(length=0,systematic=False,data_dict={}):


    """
    获取具有对应关系的两列数组
    :param length: int 列表长度
    :param systematic: boolean 是否指定单一数据形成量
    :param data_dict: dict 以字典形式传递
        systematic: True {'a':[['q',3],['w',5]], 'b':[['e',5],['t',8]]} 根据为每个字符串指定的数字比例形成数据
        systematic: False {'a':['q','w'], 'b':['e','t']}
    :return: list
    """

    assert isinstance(data_dict, dict), 'data_dict must be dict'

    if systematic == True:
        return sysRelatedSeries(length,data_dict)
    else:
        return oriRelatedSeries(length,data_dict)




