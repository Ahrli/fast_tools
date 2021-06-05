from __future__ import (absolute_import, division, print_function, unicode_literals)
from .loop_load_data import *
import backtrader as bt
from . import FACTOR_strategy as fs
from . import loop_logic as ll #mport TRADERATIONS

def startRun(rule, count):
    engine = bt.Cerebro()
    # 判断是否有数据加入
    data_flag = False
    # rule : {'startDay': 283968000, 'endDay': 2524579200, 'kline': 'kline_day', 'myStocks': ['SH.000054'], 'market': 'SH'}
    rule['tradeCondition'] = ll.TRADERATIONS[rule['factor_type']]
    _ids = rule['myStocks']
    partical_get_es_group__stacks = functools.partial(get_es_group_stacks,
                                                      dim=rule["kline"],
                                                      startTS=rule['startDay'],
                                                      endTS=rule['endDay'])

    for i,d in enumerate(partical_get_es_group__stacks(_ids)):
        if len(d) > 30:
            data = bt.feeds.PandasData(dataname = d)
            engine.adddata(data,name=_ids[i])
            data_flag = True
    if not data_flag:
        raise Exception("400")

    engine.addstrategy(fs.iStrategy, rule=rule)



    run_result = engine.run()
    results = run_result[0].result_dict
    lt = [ int(i) for i in results['result'].keys()]

    # # 取最后一条
    # MAX = max(lt)
    # data = results['result'][str(MAX)]
    # base = {'date':data['date'],'close':data['close'],'high':data['high'],'open':data['open'],'low':data['low'],'volume':data['volume']}
    # for key in base:
    #     del data[key]

    all_count = len(lt)
    # 取最近几条
    lt.sort(reverse=True)
    lt = lt[0:int(count)]
    data_list = [results['result'][str(_l)] for _l in lt]
    # 基础信息
    data = results['result'][str(lt[0])]
    base = {'date':data['date'],'close':data['close'],'high':data['high'],'open':data['open'],'low':data['low'],'volume':data['volume'], 'countAll':all_count}

    return {'base':base,"data":data_list}


# r = {"startDay": 1421823053,  # 1979-2050
#          "endDay" : 2524579200,
#          "kline" : "kline_day",
#          "myStocks" : [
#              "SH.600570"
#              # "US.BABA"
#          ],
#          "market" : "SH",
#          "factor_type": 'all',
#          "mongo_col":"kline_day",
#     }
#
#
# c = startRun(r)
# # print(c)