import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iMomentumCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #ema周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('momentum',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumCompare, self).__init__()
        self.momentum = btind.Momentum(self.data.close, period=self.args[0])

    def next(self):
        self.lines.momentum[0] = compare(self.momentum[0], self.logic)


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iMomentumCrossGolden(iBaseIndicator):
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
        super(iMomentumCrossGolden, self).__init__()
        self.momentum_short = btind.Momentum(self.data.close, period=self.args[0])
        self.momentum_long = btind.Momentum(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.momentum_short, self.momentum_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.momentum_short[0]-self.momentum_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.momentum_short[0], self.momentum_long[0],'*',self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iMomentumCrossDie(iBaseIndicator):
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
        super(iMomentumCrossDie, self).__init__()
        self.momentum_short = btind.Momentum(self.data.close, period=self.args[0])
        self.momentum_long = btind.Momentum(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.momentum_short, self.momentum_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.momentum_long[0]-self.momentum_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iMomentumLong(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('momentumlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumLong, self).__init__()
        self.momentum_short = btind.Momentum(self.data.close, period=self.args[0])
        self.momentum_long = btind.Momentum(self.data.close, period=self.args[1])

    def next(self):
        momentumlong = set([ self.momentum_short[i] > self.momentum_long[i] for i in range(1-self.args[2],1)])
        if len(momentumlong) == 1 and True in momentumlong:
            self.lines.momentumlong[0] = True
        else:
            self.lines.momentumlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iMomentumShort(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('momentumshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumShort, self).__init__()
        self.momentum_short = btind.Momentum(self.data.close, period=self.args[0])
        self.momentum_long = btind.Momentum(self.data.close, period=self.args[1])

    def next(self):
        momentumshort = set([self.momentum_short[i] < self.momentum_long[i] for i in range(1-self.args[2],1)])
        if len(momentumshort) == 1 and True in momentumshort:
            self.lines.momentumshort[0] = True
        else:
            self.lines.momentumshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iMomentumTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('momentumtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumTop, self).__init__()
        self.momentum = btind.Momentum(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.momentum.get(size=self.args[1]))
        if len(_list) == self.args[1]  and self.momentum[0] == max(_list):
            self.lines.momentumtop[0] = True
        else:
            self.lines.momentumtop[0] = False




class iMomentumBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('momentumbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumBottom, self).__init__()
        self.momentum = btind.Momentum(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.momentum.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.momentum[0] == min(_list):
            self.lines.momentumbottom[0] = True
        else:
            self.lines.momentumbottom[0] = False