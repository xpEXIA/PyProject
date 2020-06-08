# encoding=utf8
# create_time:
# python 3.6.4


from DataMaker.core import *
import pandas as pd
from pandas import DataFrame


def dataMaker(data_format,output_type='DataFrame',path=None):

    """
    获取数据DataFrame或Series
    :param data_format: dict 指定数据格式
        data_formate = {
            'length': 10, 指定行数
            'columnA':{
                'name': ['columnA'], 指定列名称
                'operation': 'discreteSeries', 指定数据处理方式 discrete/continuous/date/related
                'systematic': False, 是否指定占比规则
                'data_list': ['a','b','c'] 指定的样例数据
            },
            'columnB':{
                'name': ['columnB_a','columnB_b'],
                'operation': 'relatedSeries',
                'systematic': False,
                'data_list': {'a':['q','w'], 'b':['e','t']}
            },
            'columnC':{
                'name': ['columnC'],
                'operation': 'continuousSeries',
                'type': 'int',
                'distribution': 'None',
                'begin': 0,
                'end'= 100,
            },
            'columnD':{
                'name': ['columnD'],
                'operation': 'dateSeries',
                'type': 'date',
                'continues': True
                'begin': '2020/06/10',
                'end'= '2020/06/30'
            }
        }
    :return: DataFrame Series
    """

    assert isinstance(data_format, dict), 'data_format must be dict'

    length = data_format.pop('length')
    result = DataFrame(list(range(1,length+1)),columns=['id'])
    for i in data_format:
        name = data_format[i].pop('name')
        operation = data_format[i].pop('operation')
        parameter = ''
        for x in data_format[i]:
            parameter = parameter + x + '=' + data_format[i][x]
        exec(i + '=' + operation + '(' + parameter + ')')
        exec(i + '=DataFrame(' + i + ',columns=' + name + ')')
        exec('result = pd.merge(result,' + i + ',how="left",left_index=True,right_index=True)')

    if output_type == 'excel':
        result.to_excel(path, index=False)
        return result
    elif output_type == 'csv':
        result.to_csv(path, index=False, encoding='GBK')
        return result
    else:
        return result












