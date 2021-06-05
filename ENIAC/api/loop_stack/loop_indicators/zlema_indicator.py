import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iZlemaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #zlind周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('zlema',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlemaCompare, self).__init__()
        self.zlema = btind.ZLEMA(self.data.close, period=self.args[0])

    def next(self):
        self.lines.zlema[0] = compare(self.zlema[0], self.logic)
        # print(self.zlema[0],self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iZlemaCrossGolden(iBaseIndicator):
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
        super(iZlemaCrossGolden, self).__init__()
        self.zlema_short = btind.ZLEMA(self.data.close, period=self.args[0])
        self.zlema_long = btind.ZLEMA(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.zlema_short, self.zlema_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.zlema_short[0]-self.zlema_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.zlema_short[0], self.zlema_long[0], "===", self.data.datetime.datetime())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iZlemaCrossDie(iBaseIndicator):
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
        super(iZlemaCrossDie, self).__init__()
        self.zlema_short = btind.ZLEMA(self.data.close, period=self.args[0])
        self.zlema_long = btind.ZLEMA(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.zlema_short, self.zlema_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.zlema_long[0]-self.zlema_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iZlemaLong(iBaseIndicator):
    '''
    因子：zlind多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('zlindlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlemaLong, self).__init__()
        self.zlema_short = btind.ZLEMA(self.data.close, period=self.args[0])
        self.zlema_long = btind.ZLEMA(self.data.close, period=self.args[1])

    def next(self):
        zlindlong = set([self.data.close[i] > self.zlema_short[i] > self.zlema_long[i] for i in range(1-self.args[2],1)])
        if len(zlindlong) == 1 and True in zlindlong:
            self.lines.zlindlong[0] = True
        else:
            self.lines.zlindlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iZlemaShort(iBaseIndicator):
    '''
    因子：zlind空头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('zlindshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlemaShort, self).__init__()
        self.zlema_short = btind.ZLEMA(self.data.close, period=self.args[0])
        self.zlema_long = btind.ZLEMA(self.data.close, period=self.args[1])

    def next(self):
        zlindshort = set([self.data.close[i] < self.zlema_short[i] < self.zlema_long[i] for i in range(1-self.args[2],1)])
        if len(zlindshort) == 1 and True in zlindshort:
            self.lines.zlindshort[0] = True
        else:
            self.lines.zlindshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iZlemaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('zlematop',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlemaTop, self).__init__()
        self.zlema = btind.ZLEMA(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.zlema.get(size=self.args[1]))
        if len(_list) == self.args[1]  and self.zlema[0] == max(_list):
            self.lines.zlematop[0] = True
        else:
            self.lines.zlematop[0] = False




class iZlemaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('zlemabottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlemaBottom, self).__init__()
        self.zlema = btind.ZLEMA(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.zlema.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.zlema[0] == min(_list):
            self.lines.zlemabottom[0] = True
        else:
            self.lines.zlemabottom[0] = False