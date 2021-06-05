from __future__ import (absolute_import, division, print_function, unicode_literals)
import backtrader as bt
import importlib

class iStrategyBase(bt.Strategy):
    params = dict(rule=dict())

    def __init__(self):
        data = self.datas[0]
        self._inds = dict()
        self._code = data._name

        for cond in self.p.rule['tradeCondition']:
            if cond['modName'] == 'pattern_indicator':
                factor = f"{cond['clsName']}_{cond['params']['line']}"
            else:
                factor = cond['clsName']
            _moudle = getattr(importlib.import_module(f"api.loop_statistics.loop_indicators.{cond['modName']}"), cond['clsName'])
            self._inds[factor] = (_moudle(data, rule=cond['params']))

class iStrategy(iStrategyBase):

    def __init__(self):
        super(iStrategy, self).__init__()
        # self.result_dict = {'result': [], 'date': self._date, 'code': self._code, 'today': 0}
        self.result_dict = {}
        self.result_list = []
    # def next(self):
    #     stock = self.datas[0]
    #
    #     if str(stock.datetime.date()) == self._date:
    #         self.result_dict['today'] = 1
    #         self.result_dict['close'] = stock.close[0]
    #         for k in self._inds:
    #             if self._inds[k]:
    #                 self.result_dict['result'].append(k)

    def next(self):
        stock = self.datas[0]
        _m = []
        for k in self._inds:
            if self._inds[k]:
                _m.append(k)

        self.result_list.append({'code': stock._name, 'result': _m, 'close': stock.close[0], 'date': str(stock.datetime.date()),})
        self.result_dict = self.result_list[-1]