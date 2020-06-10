# encoding=utf8
# create_time:
# python 3.6.4

import random
from datetime import datetime, timedelta
from functools import wraps



# 数据集取整函数
# bug，由于列表复制采用round()方法，当出现0.5时会出现大量多于数据，暂时没想出好的方法避免
def roundSeries(a_func):

    @wraps(a_func)
    def wrapper(length, data):

        result = a_func(length,data)
        if len(result) - length > 100:
            result = result[0:-(len(result) - length)]
        else:
            while len(result) > length:
                a = result.pop()
                if a not in result:
                    result.insert(a, 0)

        if len(result) < length:
            result.extend(result[0:(length - len(result))])
            random.shuffle(result)
        return result
    return wrapper


@roundSeries
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

    result = []
    for i in data_list:
        result.extend([i[0]] * round(length * i[1] / sum_num))
    random.shuffle(result)
    return result


def oriSeries(length,data_list):

    """
    随机分配比例形成随机列表
    :param length: int 列表长度
    :param data_list: list 数据列表
        ['a','b','c']
    :return: list
    """

    assert isinstance(data_list, list), 'data must be list'


    if length > len(data_list):
        ori_list = []
        random_end = length / len(data_list)
        for i in data_list:
            random_var = random.uniform(1, random_end)
            inter_var = [i, random_var]
            ori_list.append(inter_var)
        return sysSeries(length, ori_list)
    else:
        return random.sample(data_list,length)



def digitSeries(length,type,distribution,begin,end,
                low,high,mode,mu,sigma,lambd,kappa,alpha,beta):

    """
    形成数字数据列表
    :param length: int 列表长度
    :param type: int/float 指定连续数列数据类型
    :param  distribution: 指定数据分布
    :param begin: int/float 起始数字
    :param end: int/float 终点数字
    :return: list
    """
    """
    采用字典获取对应函数，将分布函数字典形成配置的方法似乎代码量更多
    而且还需要采用exec来执行，效率也会更低，就是写出来的东西，看起来好蠢……想想还有没有办法改进
    distribution_dict = {
        'uniform': {
            'expr': '''
                import random
                value = ramdom.lognormvariate(mu,sigma)
                ''',
            'para':{'begin':begin,'end':end}
        },
        'triangular': random.triangular(low, high, mode),
        'normalvariate': random.normalvariate(mu, sigma),
        'lognormvariate': random.lognormvariate(mu, sigma),
        'expovariate': random.expovariate(lambd),
        'vonmisesvariate': random.vonmisesvariate(mu, kappa),
        'gammavariate': random.gammavariate(alpha, beta),
        'gauss': random.gauss(mu, sigma),
        'betavariate': random.betavariate(alpha,beta),
        'paretovariate': random.paretovariate(alpha),
        'weibullvariate': random.weibullvariate(alpha,beta)
    }
    """

    distribution_list = ['uniform','normalvariate','lognormvariate','expovariate',
        'vonmisesvariate','gammavariate','gauss','betavariate','paretovariate','weibullvariate']
    assert type in ['int','float'], 'type must be int or float'
    if type == 'int' and type != 'None':
        raise ValueError('distribution not attribute type int')
    assert distribution in list(distribution_list), 'The distribution is not supported'

    result = []
    if type == 'int':
        for i in list(range(length)):
           result.append(random.randint(begin,end))
    elif type == 'float':
        if distribution == 'uniform':
            for i in list(range(length)):
                result.append(random.uniform(begin,end))
        elif distribution == 'triangular':
            for i in list(range(length)):
                result.append(random.triangular(low, high, mode))
        elif distribution == 'normalvariate':
            for i in list(range(length)):
                result.append(random.normalvariate(mu, sigma))
        elif distribution == 'lognormvariate':
            for i in list(range(length)):
                result.append(random.lognormvariate(mu, sigma))
        elif distribution == 'expovariate':
            for i in list(range(length)):
                result.append(random.expovariate(lambd))
        elif distribution == 'vonmisesvariate':
            for i in list(range(length)):
                result.append(random.vonmisesvariate(mu, kappa))
        elif distribution == 'gammavariate':
            for i in list(range(length)):
                result.append(random.gammavariate(alpha, beta))
        elif distribution == 'gauss':
            for i in list(range(length)):
                result.append(random.gauss(mu, sigma))
        elif distribution == 'betavariate':
            for i in list(range(length)):
                result.append(random.betavariate(alpha,beta))
        elif distribution == 'paretovariate':
            for i in list(range(length)):
                result.append(random.paretovariate(alpha))
        elif distribution == 'weibullvariate':
            for i in list(range(length)):
                result.append(random.weibullvariate(alpha,beta))
    return result


def dateSeriesMaker(length,type,continues,begin,end):

    # 调用日期数据集获取类获取日期数据集

    date = _dateSeries(length,type,continues,begin,end)
    return date.getResult()


class _dateSeries():

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

    def __index__(self,length,type,continues,begin,end):

        self.length = length
        self.type = type
        self.continues = continues
        self.begin = begin
        self.end = end

    def dateSeries(self):

        date_list = []
        date_interval = datetime.strptime(self.end, '%Y/%m/%d') - datetime.strptime(self.begin, '%Y/%m/%d')
        for i in list(range(date_interval.days + 1)):
            date = datetime.strptime(self.begin, '%Y/%m/%d') + timedelta(days=i)
            date_list.append(datetime.strftime(date, '%Y/%m/%d'))
        if self.continues is False:
            date_list = random.sample(date_list, random.randint(int(len(date_list) / 2), date_interval.days)).sort()
        return oriSeries(length=self.length, data_list=date_list)

    def datetimeSeries(self):

        date_list = []
        date_interval = datetime.strptime(self.end, '%Y/%m/%d %H:%M:%S') - datetime.strptime(self.begin, '%Y/%m/%d %H:%M:%S')
        hour_interval = date_interval.days * 24 + int(date_interval.seconds / 3600)
        second_interval = date_interval.seconds % 3600
        for i in list(range(hour_interval + 1)):
            date = datetime.strptime(self.begin, '%Y/%m/%d %H:%M:%S') + timedelta(hours=i)
            date_list.append(datetime.strftime(date, '%Y/%m/%d %H:%M:%S'))
        if self.continues is False:
            date_list = random.sample(date_list, random.randint(int(len(date_list) / 2), date_interval.days)).sort()
        result = oriSeries(length=self.length, data_list=date_list)
        a = [datetime.strptime(x, '%Y/%m/%d %H:%M:%S') + timedelta(seconds=random.randint(0, 3600))
             for i in result if x != date_list[-1]]
        b = [datetime.strptime(x, '%Y/%m/%d %H:%M:%S') + timedelta(seconds=random.randint(0, second_interval))
             for i in result if x == date_list[-1]]
        result = a.extend(b)
        return result.sort()

    def timestampSeries(self):

        return digitSeries(length=self.length, type='float', distribution='uniform', begin=self.begin, end=self.end)

    def getResult(self):
        if self.type == 'date':
            result = self.dateSeries()
        elif self.type == 'datetime':
            result = self.datetimeSeries()
        elif self.type == 'timestamp':
            result = self.timestampSeries()
        return result


@roundSeries
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
        assert isinstance(i, list), 'data must be list'
        for x in data_dict[i]:
            sum_num += x[1]

    result = []
    for i in data_dict:
        inter_num = 0
        inter_result = []
        for x in data_dict[i]:
            inter_num += x[1]
        inter_list = sysSeries(round(inter_num * length / sum_num), data_dict[i])
        for y in inter_list:
            inter_result.append([[i,y]])
        result.extend(inter_result)
    random.shuffle(result)
    return result


@roundSeries
def oriRelatedSeries(length,data_dict):

    """
    获取具有对应关系的两列数组
    :param length: int 列表长度
    :param data_dict: dict 以字典形式传递
        {'a':['q','w'], 'b':['e','t']}
    :return: list
    """

    assert length == int(length), 'length must be int'

    random_length = []
    random_length_sum = 0
    for i in data_dict:
        random_var = random.randint(1,100)
        random_length.append(random_var)
        random_length_sum += random_var

    result=[]
    for i in data_dict:
        inter_list = oriSeries(round(random_length.pop() / random_length_sum * length),
                               data_dict[i])
        inter_result=[]
        for x in inter_list:
            inter_result.append([i,x])
        result.extend(inter_result)
    random.shuffle(result)
    return result


def paramterString(param_dict):

    """
    将参数字典转换为字符串，用户exec执行
    :param param_dict: dict 参数字典
    :return: str
    """

    parameter = ''
    for x in param_dict:
        if isinstance(param_dict[x], str):
            parameter = parameter + x + '="' + str(param_dict[x]) + '",'
        else:
            parameter = parameter + x + '=' + str(param_dict[x]) + ','
    return parameter