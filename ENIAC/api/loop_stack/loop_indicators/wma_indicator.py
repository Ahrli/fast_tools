import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iWmaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #ema周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('wma',)
    params = dict(rule=list())

    def __init__(self):
        super(iWmaCompare, self).__init__()
        self.wma = btind.WMA(self.data.close, period=self.args[0])

    def next(self):
        self.lines.wma[0] = compare(self.wma[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iWmaCrossGolden(iBaseIndicator):
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
        super(iWmaCrossGolden, self).__init__()
        self.wma_short = btind.WMA(self.data.close, period=self.args[0])
        self.wma_long = btind.WMA(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.wma_short, self.wma_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.wma_short[0]-self.wma_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iWmaCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iWmaCrossDie, self).__init__()
        self.wma_short = btind.WMA(self.data.close, period=self.args[0])
        self.wma_long = btind.WMA(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.wma_short, self.wma_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.wma_long[0]-self.wma_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iWmaLong(iBaseIndicator):
    '''
    因子：ema多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('wmalong',)
    params = dict(rule=list())

    def __init__(self):
        super(iWmaLong, self).__init__()
        self.wma_short = btind.WMA(self.data.close, period=self.args[0])
        self.wma_long = btind.WMA(self.data.close, period=self.args[1])

    def next(self):
        wmalong = set([ self.wma_short[i] > self.wma_long[i] for i in range(1-self.args[2],1)])
        if len(wmalong) == 1 and True in wmalong:
            self.lines.wmalong[0] = True
        else:
            self.lines.wmalong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iWmaShort(iBaseIndicator):
    '''
    因子：ema空头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('wmashort',)
    params = dict(rule=list())

    def __init__(self):
        super(iWmaShort, self).__init__()
        self.wma_short = btind.WMA(self.data.close, period=self.args[0])
        self.wma_long = btind.WMA(self.data.close, period=self.args[1])

    def next(self):
        wmashort = set([self.wma_short[i] < self.wma_long[i] for i in range(1-self.args[2],1)])
        if len(wmashort) == 1 and True in wmashort:
            self.lines.wmashort[0] = True
        else:
            self.lines.wmashort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iWmaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('wmatop',)
    params = dict(rule=list())

    def __init__(self):
        super(iWmaTop, self).__init__()
        self.wma = btind.WMA(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.wma.get(size=self.args[1]))
        if len(_list) == self.args[1]  and self.wma[0] == max(_list):
            self.lines.wmatop[0] = True
        else:
            self.lines.wmatop[0] = False




class iWmaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('wmabottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iWmaBottom, self).__init__()
        self.wma = btind.WMA(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.wma.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.wma[0] == min(_list):
            self.lines.wmabottom[0] = True
        else:
            self.lines.wmabottom[0] = False