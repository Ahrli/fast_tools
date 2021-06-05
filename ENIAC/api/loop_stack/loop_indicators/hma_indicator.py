import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator

class iHmaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('hma', )
    params = dict(rule=list())

    def __init__(self):
        super(iHmaCompare, self).__init__()
        self.hma = btind.HullMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        self.lines.hma[0] = compare(self.hma[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iHmaCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iHmaCrossGolden, self).__init__()
        self.hma_short = btind.HullMovingAverage(self.data.close, period=self.args[0])
        self.hma_long = btind.HullMovingAverage(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.hma_short, self.hma_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.hma_short[0]-self.hma_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iHmaCrossDie(iBaseIndicator):
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
        super(iHmaCrossDie, self).__init__()
        self.hma_short = btind.HullMovingAverage(self.data.close, period=self.args[0])
        self.hma_long = btind.HullMovingAverage(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.hma_short, self.hma_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.diecross[0] = compare(self.hma_long[0]-self.hma_short[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iHmaLong(iBaseIndicator):
    '''
    因子：ma多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('hmalong',)
    params = dict(rule=list())

    def __init__(self):
        super(iHmaLong, self).__init__()
        self.logic = self.p.rule['logic']
        self.hma_short = btind.HullMovingAverage(self.data.close, period=self.args[0])
        self.hma_long = btind.HullMovingAverage(self.data.close, period=self.args[1])

    def next(self):
        hmalong = set([self.data.close[i] > self.hma_short[i] > self.hma_long[i] for i in range(1-self.args[2],1)])
        if len(hmalong) == 1 and True in hmalong:
            self.lines.hmalong[0] = True
        else:
            self.lines.hmalong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iHmaShort(iBaseIndicator):
    '''
    因子：ma空头
    传入参数：
        rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('hmashort',)
    params = dict(rule=list())

    def __init__(self):
        super(iHmaShort, self).__init__()
        self.hma_short = btind.HullMovingAverage(self.data.close, period=self.args[0])
        self.hma_long = btind.HullMovingAverage(self.data.close, period=self.args[1])

    def next(self):
        hmashort = set([self.data.close[i] < self.hma_short[i] < self.hma_long[i] for i in range(1 - self.args[2], 1)])
        if len(hmashort) == 1 and True in hmashort:
            self.lines.hmashort[0] = True
        else:
            self.lines.hmashort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iHmaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('hmatop',)
    params = dict(rule=list())

    def __init__(self):
        super(iHmaTop, self).__init__()
        self.hma = btind.HullMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.hma.get(size=self.args[1]))
        if len(_list) == self.args[1]  and _list[-1] == max(_list):
            self.lines.hmatop[0] = True
        else:
            self.lines.hmatop[0] = False




class iHmaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('hmabottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iHmaBottom, self).__init__()
        self.hma = btind.HullMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.hma.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            self.lines.hmabottom[0] = True
        else:
            self.lines.hmabottom[0] = False

