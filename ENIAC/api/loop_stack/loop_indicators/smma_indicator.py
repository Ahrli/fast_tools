import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator

class iSMMACompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #sma周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    #lines = ('smma', 'ma')
    lines = ('smma', )
    params = dict(rule=list())

    def __init__(self):
        super(iSMMACompare, self).__init__()
        self.smma = btind.SmoothedMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        self.lines.smma[0] = compare(self.smma[0], self.logic)
        # print(self.smma[0], ",",self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iSMMACrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    #lines = ('goldencross', 'short', 'long')
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iSMMACrossGolden, self).__init__()
        self.smma_short = btind.SmoothedMovingAverage(self.data.close, period=self.args[0])
        self.smma_long = btind.SmoothedMovingAverage(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.smma_short, self.smma_long)

    def next(self):

        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.smma_short[0]-self.smma_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iSMMACrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    lines = ('diecross', )
    params = dict(rule=list())

    def __init__(self):
        super(iSMMACrossDie, self).__init__()
        self.smma_short = btind.SmoothedMovingAverage(self.data.close, period=self.args[0])
        self.smma_long = btind.SmoothedMovingAverage(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.smma_short, self.smma_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.diecross[0] = compare(self.smma_long[0]-self.smma_short[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iSMMALong(iBaseIndicator):
    '''
    因子：ma多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('smmalong',)
    params = dict(rule=list())

    def __init__(self):
        super(iSMMALong, self).__init__()
        self.logic = self.p.rule['logic']
        self.smma_short = btind.SmoothedMovingAverage(self.data.close, period=self.args[0])
        self.smma_long = btind.SmoothedMovingAverage(self.data.close, period=self.args[1])

    def next(self):

        smmalong = set([self.data.close[i] > self.smma_short[i] > self.smma_long[i] for i in range(1-self.args[2],1)])
        if len(smmalong) == 1 and True in smmalong:
            self.lines.smmalong[0] = True
        else:
            self.lines.smmalong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iSMMAShort(iBaseIndicator):
    '''
    因子：ma空头
    传入参数：
        rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('smmashort',)
    params = dict(rule=list())

    def __init__(self):
        super(iSMMAShort, self).__init__()
        self.smma_short = btind.SmoothedMovingAverage(self.data.close, period=self.args[0])
        self.smma_long = btind.SmoothedMovingAverage(self.data.close, period=self.args[1])

    def next(self):

        smmashort = set([self.data.close[i] < self.smma_short[i] < self.smma_long[i] for i in range(1 - self.args[2], 1)])
        if len(smmashort) == 1 and True in smmashort:
            self.lines.smmashort[0] = True
        else:
            self.lines.smmashort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iSMMATop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('smmatop',)
    params = dict(rule=list())

    def __init__(self):
        super(iSMMATop, self).__init__()
        self.smma = btind.SmoothedMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.smma.get(size=self.args[1]))
        if len(_list) == self.args[1]  and _list[-1] == max(_list):
            self.lines.smmatop[0] = True
        else:
            self.lines.smmatop[0] = False




class iSMMABottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('mabottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iSMMABottom, self).__init__()
        self.smma = btind.SmoothedMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.smma.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            self.lines.mabottom[0] = True
        else:
            self.lines.mabottom[0] = False