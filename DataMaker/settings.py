# encoding=utf8
# create_time:
# python 3.6.4


import numpy as np
import random
import pandas as pd
from pandas import DataFrame

ORDER_NO = DataFrame({'order_no':[random.randint(1000000000,9999999999) for x in list(range(1000))]})
PHONE_ORDER_NO = ORDER_NO['order_no'].map(lambda x: 'PH' + str(x)).to_list()

PHONE_SAMPLE = {
    'length': 1000,
    'columnO':{
        'name': ['订单号'],
        'operation': 'discreteSeries',
        'systematic': False,
        'data_list': PHONE_ORDER_NO
    },
    'columnA': {
        'name': ['品牌','型号'],
        'operation': 'relatedSeries',
        'systematic': False,
        'data_dict': {
            '小米':['小米6','小米7','小米8','小米9','小米10','小米CC','红米K30 pro','realme','小米mix4'],
            '华为':['nova8','nova7','华为mate20','华为mate30','华为P20','华为P30','华为P40'],
            'vivo':['U3x','Y70s','S6','Z5x','Z6','IQOO','Y70s','S6','NEX30S','X50'],
            'oppo':['Reno4','A92s','Ace2','FindX2','K5','Reno4 pro','A92s','Reno3'],
            '苹果':['iphoneX','iphoneXI','iphoneXII','iphoneSe','iphoneXI plus','iphoneXII plus']
        }
    },
    'columnB': {
        'name': ['销售日期'],
        'operation': 'dateSeries',
        'type': 'date',
        'continues': True,
        'begin': '2020/05/01',
        'end': '2020/06/30'
    },
    'columnC':{
        'name': ['走私11区价'],
        'operation': 'continuousSeries',
        'type': 'float',
        'distribution': 'lognormvariate',
        'mu': np.log(3500) - 0.5 * np.log(1 + 1700**2 / 3500**2),
        'sigma': (np.log(1 + 1700**2 / 3500**2))**0.5
    }
}

