import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator


class iDv2Compare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    # lines = ('dv2', 'ma')
    lines = ('dv2',)
    params = dict(rule=list())

    def __init__(self):
        super(iDv2Compare, self).__init__()
        self.dv2 = btind.DV2(period=self.args[0])

    def next(self):
        self.lines.dv2[0] = compare(self.dv2[0], self.logic)
        print(self.dv2[0], self.data.close[0], '*', self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iDv2CrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    # lines = ('goldencross', 'short', 'long')
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iDv2CrossGolden, self).__init__()
        self.dv2_short = btind.DV2(period=self.args[0])
        self.dv2_long = btind.DV2(period=self.args[1])
        self.cross = btind.CrossOver(self.dv2_short, self.dv2_long)

    def next(self):

        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.dv2_short[0] - self.dv2_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iDv2CrossDie(iBaseIndicator):
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
        super(iDv2CrossDie, self).__init__()
        self.dv2_short = btind.DV2(period=self.args[0])
        self.dv2_long = btind.DV2(period=self.args[1])
        self.cross = btind.CrossOver(self.dv2_short, self.dv2_long)

    def next(self):

        if self.cross[0] == -1:
            self.lines.diecross[0] = compare(self.dv2_long[0] - self.dv2_short[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iDv2Long(iBaseIndicator):
    '''
    因子：ma多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    # lines = ('dv2long', 'short', 'long')
    lines = ('dv2long',)
    params = dict(rule=list())

    def __init__(self):
        super(iDv2Long, self).__init__()
        self.logic = self.p.rule['logic']
        self.dv2_short = btind.DV2(period=self.args[0])
        self.dv2_long = btind.DV2(period=self.args[1])

    def next(self):

        dv2long = set([self.dv2_short[i] > self.dv2_long[i] for i in range(1 - self.args[2], 1)])
        if len(dv2long) == 1 and True in dv2long:
            self.lines.dv2long[0] = True
        else:
            self.lines.dv2long[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iDv2Short(iBaseIndicator):
    '''
    因子：ma空头
    传入参数：
        rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    # lines = ('dv2short', 'short', 'long')
    lines = ('dv2short',)
    params = dict(rule=list())

    def __init__(self):
        super(iDv2Short, self).__init__()
        self.dv2_short = btind.DV2(period=self.args[0])
        self.dv2_long = btind.DV2(period=self.args[1])

    def next(self):
        dv2short = set([self.dv2_short[i] < self.dv2_long[i] for i in range(1 - self.args[2], 1)])
        if len(dv2short) == 1 and True in dv2short:
            self.lines.dv2short[0] = True
        else:
            self.lines.dv2short[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iDv2Top(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('dv2top',)
    params = dict(rule=list())

    def __init__(self):
        super(iDv2Top, self).__init__()
        self.dv2 = btind.DV2(period=self.args[0])

    def next(self):
        _list = list(self.dv2.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == max(_list):
            self.lines.dv2top[0] = True
        else:
            self.lines.dv2top[0] = False


class iDv2Bottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('dv2bottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iDv2Bottom, self).__init__()
        self.dv2 = btind.DV2(period=self.args[0])

    def next(self):
        _list = list(self.dv2.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            self.lines.dv2bottom[0] = True
        else:
            self.lines.dv2bottom[0] = False