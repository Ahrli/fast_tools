import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iPctChangeCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #ema周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('pctchange',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctChangeCompare, self).__init__()
        self.pctchange = btind.PercentChange(self.data.close, period=self.args[0])

    def next(self):
        self.lines.pctchange[0] = compare(self.pctchange[0], self.logic)
        # print(self.pctchange[0], self.data.close[0], self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iPctChangeCrossGolden(iBaseIndicator):
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
        super(iPctChangeCrossGolden, self).__init__()
        self.pctchange_short = btind.PercentChange(self.data.close, period=self.args[0])
        self.pctchange_long = btind.PercentChange(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.pctchange_short, self.pctchange_long)

    def next(self):
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.pctchange_short[0] - self.pctchange_long[0], self.logic) and \
                                            self.pctchange_short[0] > 0

            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.pctchange_short[0] - self.pctchange_long[0], self.logic) and \
                                            self.pctchange_short[0] < 0

            else:
                self.lines.goldencross[0] = compare(self.pctchange_short[0] - self.pctchange_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

        # print(self.cross[0],self.pctchange_short[0], self.pctchange_long[0], self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iPctChangeCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctChangeCrossDie, self).__init__()
        self.pctchange_short = btind.PercentChange(self.data.close, period=self.args[0])
        self.pctchange_long = btind.PercentChange(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.pctchange_short, self.pctchange_long)

    def next(self):
        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.pctchange_long[0] - self.pctchange_short[0], self.logic)  and self.pctchange_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.pctchange_long[0] - self.pctchange_short[0], self.logic) and  self.pctchange_short[0] < 0
            else:
                self.lines.goldencross[0] = compare(self.pctchange_long[0] - self.pctchange_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iPctChangeLong(iBaseIndicator):
    '''

    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('pctchangelong',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctChangeLong, self).__init__()
        self.pctchange_short = btind.PercentChange(self.data.close, period=self.args[0])
        self.pctchange_long = btind.PercentChange(self.data.close, period=self.args[1])

    def next(self):
        pctchangelong = set(
            [ self.pctchange_short[i] > self.pctchange_long[i] for i in range(1 - self.args[2], 1)])
        if len(pctchangelong) == 1 and True in pctchangelong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.pctchangelong[0] = True and self.pctchange_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.pctchangelong[0] = True and  self.pctchange_short[0] < 0
            else:
                self.lines.pctchangelong[0] = True
        else:
            self.lines.pctchangelong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iPctChangeShort(iBaseIndicator):
    '''
   传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('pctchangeshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctChangeShort, self).__init__()
        self.pctchange_short = btind.PercentChange(self.data.close, period=self.args[0])
        self.pctchange_long = btind.PercentChange(self.data.close, period=self.args[1])

    def next(self):
        pctchangeshort = set(
            [self.data.close[i] < self.pctchange_short[i] < self.pctchange_long[i] for i in range(1 - self.args[2], 1)])
        if len(pctchangeshort) == 1 and True in pctchangeshort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.pctchangeshort[0] = True and  self.pctchange_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.pctchangeshort[0] = True and  self.pctchange_short[0] < 0
            else:
                self.lines.pctchangeshort[0] = True
        else:
            self.lines.pctchangeshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iPctChangeTop(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": [5,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('pctchangetop',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctChangeTop, self).__init__()
        self.pctchange = btind.PercentChange(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.pctchange.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.pctchange[0] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.pctchangetop[0] = True  and  self.pctchange[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.pctchangetop[0] = True and  self.pctchange[0] < 0
            else:
                self.lines.pctchangetop[0] = True
        else:
            self.lines.pctchangetop[0] = False


class iPctChangeBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    rule = {"args": [5,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('pctchangebottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctChangeBottom, self).__init__()
        self.pctchange = btind.PercentChange(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.pctchange.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.pctchange[0] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.pctchangebottom[0] = True and  self.pctchange[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.pctchangebottom[0] = True and  self.pctchange[0] < 0
            else:
                self.lines.pctchangebottom[0] = True
        else:
            self.lines.pctchangebottom[0] = False
        # print(self.pctchange[0], self.data.close[0], self.data.datetime.date())


class iPctChangeHigh(iBaseIndicator):
    '''
    连续n天低于某个数值
    传入参数：
        rule = {"args": [6,2] # 周期 连续N天
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},
    '''
    lines = ('ehigh',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctChangeHigh, self).__init__()
        self.pctchange = btind.PercentChange(self.data.close, period=self.args[0])

    def next(self):
        _list = [(i) for i in list(self.pctchange.get(size=self.args[1]))]
        _list.sort()

        if len(_list) == self.args[1]:
            _list = (list(map(lambda d: compare(d, self.logic), _list)))
            _list = [ i for i in _list if i is True ]

        else:
            _list = []
        if len(_list) == self.args[1]:
                self.lines.ehigh[0] = True
        else:
            self.lines.ehigh[0] = False
        # print(self.pctchange[0], self.data.close[0], self.data.datetime.date())

