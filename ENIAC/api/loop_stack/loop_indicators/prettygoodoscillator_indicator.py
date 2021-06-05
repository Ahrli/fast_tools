import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iPGOCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #pgo周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('pgo',)
    params = dict(rule=list())

    def __init__(self):
        super(iPGOCompare, self).__init__()
        self.pgo = btind.PrettyGoodOscillator(period=self.args[0])

    def next(self):
        self.lines.pgo[0] = compare(self.pgo[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iPGOCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [12,26],   # 连续N日短均线, 连续N日长均线
            "logic":{"position":0},
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iPGOCrossGolden, self).__init__()
        self.pgo_short = btind.PrettyGoodOscillator(self.data, period=self.args[0])
        self.pgo_long = btind.PrettyGoodOscillator(self.data, period=self.args[1])
        self.cross = btind.CrossOver(self.pgo_short, self.pgo_long)

    def next(self):
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.pgo_short[0] - self.pgo_long[0], self.logic) and \
                                            self.pgo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0

                self.lines.goldencross[0] = compare(self.pgo_short[0] - self.pgo_long[0], self.logic) and \
                                            self.pgo_short[0] < 0
            else:
                self.lines.goldencross[0] = compare(self.pgo_short[0] - self.pgo_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.pgo_short[0], self.pgo_long[0], self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iPGOCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [12,26],   # 连续N日短均线, 连续N日长均线
            "logic":{"position":0},
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iPGOCrossDie, self).__init__()
        self.pgo_short = btind.PrettyGoodOscillator(self.data, period=self.args[0])
        self.pgo_long = btind.PrettyGoodOscillator(self.data, period=self.args[1])
        self.cross = btind.CrossOver(self.pgo_short, self.pgo_long)

    def next(self):
        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0

                self.lines.goldencross[0] = compare(self.pgo_long[0] - self.pgo_short[0], self.logic) and self.pgo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0

                self.lines.goldencross[0] = compare(self.pgo_long[0] - self.pgo_short[0], self.logic)  and self.pgo_short[0] < 0
            else:

                self.lines.goldencross[0] = compare(self.pgo_long[0] - self.pgo_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.pgo_short[0], self.pgo_long[0], self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iPGOLong(iBaseIndicator):
    '''
    因子：pgo多头
    传入参数：
   rule = {"args": [12,26,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('pgolong',)
    params = dict(rule=list())

    def __init__(self):
        super(iPGOLong, self).__init__()
        self.pgo_short = btind.PrettyGoodOscillator(self.data, period=self.args[0])
        self.pgo_long = btind.PrettyGoodOscillator(self.data, period=self.args[1])

    def next(self):
        pgolong = set([ self.pgo_short[i] > self.pgo_long[i] for i in range(1 - self.args[2], 1)])
        if len(pgolong) == 1 and True in pgolong:
            if self.logic["position"] == 1:  # 出现在上部  > 0

                self.lines.pgolong[0] = True  and self.pgo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0

                self.lines.pgolong[0] = True  and self.pgo_short[0] < 0
            else:
                self.lines.pgolong[0] = True
        else:
            self.lines.pgolong[0] = False
        # print(self.pgo_short[0], self.pgo_long[0], self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iPGOShort(iBaseIndicator):
    '''
    因子：pgo空头
    传入参数：
    rule = {"args": [12,26,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('pgoshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iPGOShort, self).__init__()
        self.pgo_short = btind.PrettyGoodOscillator(self.data, period=self.args[0])
        self.pgo_long = btind.PrettyGoodOscillator(self.data, period=self.args[1])

    def next(self):
        pgoshort = set([ self.pgo_short[i] < self.pgo_long[i] for i in range(1 - self.args[2], 1)])
        if len(pgoshort) == 1 and True in pgoshort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.pgoshort[0] = True and self.pgo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0

                self.lines.pgoshort[0] = True and self.pgo_short[0] < 0
            else:
                self.lines.pgoshort[0] = True
        else:
            self.lines.pgoshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iPGOTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
       rule = {"args": [5,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }

    '''
    lines = ('pgotop',)
    params = dict(rule=list())

    def __init__(self):
        super(iPGOTop, self).__init__()
        self.pgo = btind.PrettyGoodOscillator(self.data, period=self.args[0])

    def next(self):
        _list = list(self.pgo.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.pgo[0] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.pgotop[0] = True and self.pgo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.pgotop[0] = True and self.pgo_short[0] < 0
            else:
                self.lines.pgotop[0] = True
        else:
            self.lines.pgotop[0] = False
        # print(self.pgo[0], self.data.datetime.date())



class iPGOBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rurule = {"args": [5,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }

    '''
    lines = ('pgobottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iPGOBottom, self).__init__()
        self.pgo = btind.PrettyGoodOscillator(self.data, period=self.args[0])

    def next(self):
        _list = list(self.pgo.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.pgo[0] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.pgobottom[0] = True and self.pgo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0

                self.lines.pgobottom[0] = True and self.pgo_short[0] < 0
            else:
                self.lines.pgobottom[0] = True
        else:
            self.lines.pgobottom[0] = False
