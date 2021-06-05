import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator

class iMaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #sma周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    #lines = ('mc', 'ma')
    lines = ('mc', )
    params = dict(rule=list())

    def __init__(self):
        super(iMaCompare, self).__init__()
        self.sma = btind.SimpleMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        self.lines.mc[0] = compare(self.sma[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iMaCrossGolden(iBaseIndicator):
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
        super(iMaCrossGolden, self).__init__()
        self.sma_short = btind.SimpleMovingAverage(self.data.close, period=self.args[0])
        self.sma_long = btind.SimpleMovingAverage(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.sma_short, self.sma_long)

    def next(self):
        #self.lines.long[0] = self.sma_long[0]
        #self.lines.short[0] = self.sma_short[0]
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.sma_short[0]-self.sma_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iMaCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    # lines = ('diecross', 'short', 'long')
    lines = ('diecross', )
    params = dict(rule=list())

    def __init__(self):
        super(iMaCrossDie, self).__init__()
        self.sma_short = btind.SimpleMovingAverage(self.data.close, period=self.args[0])
        self.sma_long = btind.SimpleMovingAverage(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.sma_short, self.sma_long)

    def next(self):
        #self.lines.long[0] = self.sma_long[0]
        #self.lines.short[0] = self.sma_short[0]
        if self.cross[0] == -1:
            self.lines.diecross[0] = compare(self.sma_long[0]-self.sma_short[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iMaLong(iBaseIndicator):
    '''
    因子：ma多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    #lines = ('malong', 'short', 'long')
    lines = ('malong',)
    params = dict(rule=list())

    def __init__(self):
        super(iMaLong, self).__init__()
        self.logic = self.p.rule['logic']
        self.sma_short = btind.SimpleMovingAverage(self.data.close, period=self.args[0])
        self.sma_long = btind.SimpleMovingAverage(self.data.close, period=self.args[1])

    def next(self):
        #self.lines.long[0] = self.sma_long[0]
        #self.lines.short[0] = self.sma_short[0]
        malong = set([self.data.close[i] > self.sma_short[i] > self.sma_long[i] for i in range(1-self.args[2],1)])
        if len(malong) == 1 and True in malong:
            self.lines.malong[0] = True
        else:
            self.lines.malong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iMaShort(iBaseIndicator):
    '''
    因子：ma空头
    传入参数：
        rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    #lines = ('mashort', 'short', 'long')
    lines = ('mashort',)
    params = dict(rule=list())

    def __init__(self):
        super(iMaShort, self).__init__()
        self.sma_short = btind.SimpleMovingAverage(self.data.close, period=self.args[0])
        self.sma_long = btind.SimpleMovingAverage(self.data.close, period=self.args[1])

    def next(self):
        #self.lines.long[0] = self.sma_long[0]
        #self.lines.short[0] = self.sma_short[0]
        mashort = set([self.data.close[i] < self.sma_short[i] < self.sma_long[i] for i in range(1 - self.args[2], 1)])
        if len(mashort) == 1 and True in mashort:
            self.lines.mashort[0] = True
        else:
            self.lines.mashort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iMaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('matop',)
    params = dict(rule=list())

    def __init__(self):
        super(iMaTop, self).__init__()
        self.sma = btind.SimpleMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.sma.get(size=self.args[1]))
        if len(_list) == self.args[1]  and _list[-1] == max(_list):
            self.lines.matop[0] = True
        else:
            self.lines.matop[0] = False




class iMaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('mabottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iMaBottom, self).__init__()
        self.sma = btind.SimpleMovingAverage(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.sma.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            self.lines.mabottom[0] = True
        else:
            self.lines.mabottom[0] = False