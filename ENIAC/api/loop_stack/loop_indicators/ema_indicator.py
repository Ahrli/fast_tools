import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iEmaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #ema周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('ec',)
    params = dict(rule=list())

    def __init__(self):
        super(iEmaCompare, self).__init__()
        self.ema = btind.MovingAverageExponential(self.data.close, period=self.args[0])

    def next(self):
        self.lines.ec[0] = compare(self.ema[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iEmaCrossGolden(iBaseIndicator):
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
        super(iEmaCrossGolden, self).__init__()
        self.ema_short = btind.MovingAverageExponential(self.data.close, period=self.args[0])
        self.ema_long = btind.MovingAverageExponential(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.ema_short, self.ema_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.ema_short[0]-self.ema_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iEmaCrossDie(iBaseIndicator):
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
        super(iEmaCrossDie, self).__init__()
        self.ema_short = btind.MovingAverageExponential(self.data.close, period=self.args[0])
        self.ema_long = btind.MovingAverageExponential(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.ema_short, self.ema_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.ema_long[0]-self.ema_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iEmaLong(iBaseIndicator):
    '''
    因子：ema多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('emalong',)
    params = dict(rule=list())

    def __init__(self):
        super(iEmaLong, self).__init__()
        self.ema_short = btind.MovingAverageExponential(self.data.close, period=self.args[0])
        self.ema_long = btind.MovingAverageExponential(self.data.close, period=self.args[1])

    def next(self):
        emalong = set([self.data.close[i] > self.ema_short[i] > self.ema_long[i] for i in range(1-self.args[2],1)])
        if len(emalong) == 1 and True in emalong:
            self.lines.emalong[0] = True
        else:
            self.lines.emalong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iEmaShort(iBaseIndicator):
    '''
    因子：ema空头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('emashort',)
    params = dict(rule=list())

    def __init__(self):
        super(iEmaShort, self).__init__()
        self.ema_short = btind.MovingAverageExponential(self.data.close, period=self.args[0])
        self.ema_long = btind.MovingAverageExponential(self.data.close, period=self.args[1])

    def next(self):
        emashort = set([self.data.close[i] < self.ema_short[i] < self.ema_long[i] for i in range(1-self.args[2],1)])
        if len(emashort) == 1 and True in emashort:
            self.lines.emashort[0] = True
        else:
            self.lines.emashort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iEmaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('etop',)
    params = dict(rule=list())

    def __init__(self):
        super(iEmaTop, self).__init__()
        self.ema = btind.MovingAverageExponential(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.ema.get(size=self.args[1]))
        if len(_list) == self.args[1]  and self.ema[0] == max(_list):
            self.lines.etop[0] = True
        else:
            self.lines.etop[0] = False




class iEmaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('ebottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iEmaBottom, self).__init__()
        self.ema = btind.MovingAverageExponential(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.ema.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.ema[0] == min(_list):
            self.lines.ebottom[0] = True
        else:
            self.lines.ebottom[0] = False