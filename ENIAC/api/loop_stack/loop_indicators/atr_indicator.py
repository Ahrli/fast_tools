import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator


class iAtrCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #sma周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('atr',)
    params = dict(rule=list())

    def __init__(self):
        super(iAtrCompare, self).__init__()
        self.atr = btind.AverageTrueRange(period=self.args[0])

    def next(self):
        self.lines.atr[0] = compare(self.atr[0], self.logic)
        #print(self.atr[0], self.data.close[0], '*', self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iAtrCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iAtrCrossGolden, self).__init__()
        self.atr_short = btind.AverageTrueRange(period=self.args[0])
        self.atr_long = btind.AverageTrueRange(period=self.args[1])
        self.cross = btind.CrossOver(self.atr_short, self.atr_long)

    def next(self):

        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.atr_short[0] - self.atr_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.atr_short[0],self.atr_long[0], self.data.close[0], '*', self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iAtrCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''

    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iAtrCrossDie, self).__init__()
        self.atr_short = btind.AverageTrueRange(period=self.args[0])
        self.atr_long = btind.AverageTrueRange(period=self.args[1])
        self.cross = btind.CrossOver(self.atr_short, self.atr_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.diecross[0] = compare(self.atr_long[0] - self.atr_short[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iAtrLong(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('atrlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iAtrLong, self).__init__()
        self.logic = self.p.rule['logic']
        self.atr_short = btind.AverageTrueRange(period=self.args[0])
        self.atr_long = btind.AverageTrueRange(period=self.args[1])

    def next(self):
        atrlong = set([self.atr_short[i] > self.atr_long[i] for i in range(1 - self.args[2], 1)])
        if len(atrlong) == 1 and True in atrlong:
            self.lines.atrlong[0] = True
        else:
            self.lines.atrlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iAtrShort(iBaseIndicator):
    '''
    传入参数：
        rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('atrshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iAtrShort, self).__init__()
        self.atr_short = btind.AverageTrueRange(period=self.args[0])
        self.atr_long = btind.AverageTrueRange(period=self.args[1])

    def next(self):
        atrshort = set([ self.atr_short[i] < self.atr_long[i] for i in range(1 - self.args[2], 1)])
        if len(atrshort) == 1 and True in atrshort:
            self.lines.atrshort[0] = True
        else:
            self.lines.atrshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iAtrTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [5,3] ,#周期 连续天数
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('atrtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iAtrTop, self).__init__()
        self.atr = btind.AverageTrueRange(period=self.args[0])

    def next(self):
        _list = list(self.atr.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == max(_list):
            self.lines.atrtop[0] = True
        else:
            self.lines.atrtop[0] = False


class iAtrBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,3] ,#周期 连续天数
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('atrbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iAtrBottom, self).__init__()
        self.atr = btind.AverageTrueRange(period=self.args[0])

    def next(self):
        _list = list(self.atr.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            self.lines.atrbottom[0] = True
        else:
            self.lines.atrbottom[0] = False