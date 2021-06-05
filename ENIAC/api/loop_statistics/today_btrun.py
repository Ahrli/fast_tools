from __future__ import (absolute_import, division, print_function, unicode_literals)
from .loop_load_data import *
import backtrader as bt
from .today_strategy import iStrategy
from .loop_logic import TRADERATIONS
import arrow

def startRun(rule):
    engine = bt.Cerebro()
    # rule : {'startDay': 283968000, 'endDay': 2524579200, 'kline': 'kline_day', 'myStocks': ['SH.000054'], 'market': 'SH'}
    rule['tradeCondition'] = TRADERATIONS
    _ids = rule['myStocks']
    partical_get_es_group__stacks = functools.partial(get_es_group_stacks,
                                                      dim=rule["kline"],
                                                      # startTS=rule['startDay'],
                                                      # endTS=rule['endDay'],
                                                      startTS=arrow.get(arrow.now().replace(days=-int(180)).format('YYYY-MM-DD')).timestamp,
                                                      endTS=arrow.get(arrow.now().format('YYYY-MM-DD')).timestamp
                                                      )

    for i,d in enumerate(partical_get_es_group__stacks(_ids)):
        if len(d) > 30:
            data = bt.feeds.PandasData(dataname = d)
            engine.adddata(data,name=_ids[i])
    engine.addstrategy(iStrategy, rule=rule)

    run_result = engine.run()
    results = run_result[0].result_dict
    return results