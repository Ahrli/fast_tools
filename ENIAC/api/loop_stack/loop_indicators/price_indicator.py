import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator

class iPriceCompare(iBaseIndicator):
    '''
    因子：当前价格与昨日收盘价比较
    传入参数：
    '''
    lines = ('pc', )
    params = dict(rule=list())

    def __init__(self):
        super(iPriceCompare, self).__init__()

    def next(self):
        openprice = list(self.data.close)[0]
        # if openprice > self.data.close[0]:
        #     self.lines.pc[0] = 1
        self.logic["byValue"] = openprice
        self.lines.pc[0] = compare(self.data.close[0], self.logic)