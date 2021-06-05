import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iRocCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #ema周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('roc',)
    params = dict(rule=list())

    def __init__(self):
        super(iRocCompare, self).__init__()
        self.roc = btind.RateOfChange100(self.data.close, period=self.args[0])

    def next(self):
        self.lines.roc[0] = compare(self.roc[0], self.logic)
        # print(self.roc[0],self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iRocCrossGolden(iBaseIndicator):
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
        super(iRocCrossGolden, self).__init__()
        self.roc_short = btind.RateOfChange100(self.data.close, period=self.args[0])
        self.roc_long = btind.RateOfChange100(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.roc_short, self.roc_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.roc_short[0]-self.roc_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iRocCrossDie(iBaseIndicator):
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
        super(iRocCrossDie, self).__init__()
        self.roc_short = btind.RateOfChange100(self.data.close, period=self.args[0])
        self.roc_long = btind.RateOfChange100(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.roc_short, self.roc_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.roc_long[0]-self.roc_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iRocLong(iBaseIndicator):
    '''
    因子：ema多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('roclong',)
    params = dict(rule=list())

    def __init__(self):
        super(iRocLong, self).__init__()
        self.roc_short = btind.RateOfChange100(self.data.close, period=self.args[0])
        self.roc_long = btind.RateOfChange100(self.data.close, period=self.args[1])

    def next(self):
        roclong = set([self.data.close[i] > self.roc_short[i] > self.roc_long[i] for i in range(1-self.args[2],1)])
        if len(roclong) == 1 and True in roclong:
            self.lines.roclong[0] = True
        else:
            self.lines.roclong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iRocShort(iBaseIndicator):
    '''
    因子：ema空头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('rocshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iRocShort, self).__init__()
        self.roc_short = btind.RateOfChange100(self.data.close, period=self.args[0])
        self.roc_long = btind.RateOfChange100(self.data.close, period=self.args[1])

    def next(self):
        rocshort = set([self.data.close[i] < self.roc_short[i] < self.roc_long[i] for i in range(1-self.args[2],1)])
        if len(rocshort) == 1 and True in rocshort:
            self.lines.rocshort[0] = True
        else:
            self.lines.rocshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iRocTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('roctop',)
    params = dict(rule=list())

    def __init__(self):
        super(iRocTop, self).__init__()
        self.roc = btind.RateOfChange100(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.roc.get(size=self.args[1]))
        if len(_list) == self.args[1]  and self.roc[0] == max(_list):
            self.lines.roctop[0] = True
        else:
            self.lines.roctop[0] = False




class iRocBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('rocbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iRocBottom, self).__init__()
        self.roc = btind.RateOfChange100(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.roc.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.roc[0] == min(_list):
            self.lines.rocbottom[0] = True
        else:
            self.lines.rocbottom[0] = False