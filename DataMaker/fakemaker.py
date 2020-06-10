# encoding=utf8
# create_time:
# python 3.6.4


from DataMaker.core import *
from DataMaker.basic import paramterString
import pandas as pd
from pandas import DataFrame


def dataMaker(data_format):

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
                'data_dict': {'a':['q','w'], 'b':['e','t']}
            },
            'columnC':{
                'name': ['columnC'],
                'operation': 'continuousSeries',
                'type': 'int',
                'distribution': 'None',
                'begin': 0,
                'end': 100,
            },
            'columnD':{
                'name': ['columnD'],
                'operation': 'dateSeries',
                'type': 'date',
                'continues': True,
                'begin': '2020/06/10',
                'end': '2020/06/30'
            }
        }
    :return DataFrame
    """

    assert isinstance(data_format, dict), 'data_format must be dict'

    length = data_format.pop('length')
    result = DataFrame(list(range(1,length+1)),columns=['id'])
    for i in data_format:
        name = data_format[i].pop('name')
        operation = data_format[i].pop('operation')
        parameter = paramterString(data_format[i])
        exec(i + '=' + operation + '(length=' + str(length) + ',' + parameter + ')')
        exec(i + '=DataFrame(' + i + ',columns=' + str(name) + ')')

        # 在使用exec执行代码时，字符串代码中的内部变量无法在函数中被调用，
        # 想要调用需要使用locals()方法找到exec中的内部变量
        result = pd.merge(result, locals()[i],how='left',left_index=True,right_index=True)
    return result

def dataMerge(origin,merge_data):

    """
    向已有数据集合并指定规则的数据集
    :param origin:  DataFrame 原数据集
    :param merge_data:  dict 指定数据格式
        merge_data = {
            'columnA':{
                'index': 'columnA_name', 指定origin中合并的列
                'name': 'nameA',
                'operation': 'discreteSeries',
                'param': {
                    'a':{
                        'systematic': False,
                        'data': ['a','b','c']
                    },
                    'b':{
                        'systematic': True,
                        'data': [['q',6],['w',7],['e',3]]
                    }
                }
            },
            'columnB':{
                'index': 'columnB_name',
                'name': 'nameB',
                'operation': 'continuousSeries',
                'param': {
                    'type': 'int',
                    'begin': 0,
                    'end': 100
                }
            },
            'columnC':{
                'index': 'columnC_name',
                'name': 'nameC',
                'operation': 'dateSeries',
                'param': {
                    'type': 'date',
                    'continues': True,
                    'begin': '2020/06/10',
                    'end': '2020/06/30'
                }
            }
        }
    :return:  DataFrame
    """

    assert isinstance(merge_data, dict), 'data_format must be dict'

    result = origin.copy()
    for i in merge_data:
        merge_dict = {}
        data_length = result.groupby(merge_data[i]['index'])[merge_data[i]['index']].count()
        for x in list(data_length.index):
            parameter = paramterString(merge_data[i]['param'])
            exec(x + '=' + merge_data[i]['operation'] + '(length=' + str(data_length[x]) + ',' + parameter + ')')
            merge_dict[x] = locals()[x]
        result[merge_data[i]['name']] = result[merge_data[i]['index']].map(lambda x: merge_dict[x].pop())
    return result









if __name__ == '__main__':


    from DataMaker.settings import PHONE_SAMPLE
    phone_sample = dataMaker(PHONE_SAMPLE)










