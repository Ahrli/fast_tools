import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iTrixCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #ema周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('trix',)
    params = dict(rule=list())

    def __init__(self):
        super(iTrixCompare, self).__init__()
        self.trix = btind.Trix(self.data.close, period=self.args[0])

    def next(self):
        self.lines.trix[0] = compare(self.trix[0], self.logic)
        # print(self.trix[0], ",", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iTrixCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [12, 26],      #快周期，慢周期
            "logic":{
            "position":{1(up),-1(down),0(any)},# 周期结果比较

            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iTrixCrossGolden, self).__init__()
        self.trix_short = btind.Trix(self.data.close, period=self.args[0])
        self.trix_long = btind.Trix(self.data.close, period=self.args[1])

        self.cross = btind.CrossOver(self.trix_short, self.trix_long)

    def next(self):
        # print(self.data.datetime.date())
        # print(compare(self.trix.trix[0] - self.trix.signal[0], self.logic))
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.trix_short[0] - self.trix_long[0], self.logic) and \
                                            self.trix_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.trix_short[0] - self.trix_long[0], self.logic) and \
                                            self.trix_short[0] < 0
            else:  # 其他情况
                self.lines.goldencross[0] = compare(self.trix_short[0] - self.trix_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.trix_short[0], self.trix_long[0], ",", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iTrixCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [12, 26],      #快周期，慢周期
            "logic":{
            "position":{1(up),-1(down),0(any)},# 周期结果比较

            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iTrixCrossDie, self).__init__()
        self.trix_short = btind.Trix(self.data.close, period=self.args[0])
        self.trix_long = btind.Trix(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.trix_short, self.trix_long)

    def next(self):
        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.trix_long[0] - self.trix_short[0], self.logic) and \
                                         self.trix_long[0] > 0
            elif self.logic["position"] == -1:  # 出现在上部  <0
                self.lines.diecross[0] = compare(self.trix_long[0] - self.trix_short[0], self.logic) and \
                                         self.trix_long[0] < 0
            else:  # 其他情况
                self.lines.diecross[0] = compare(self.trix_long[0] - self.trix_short[0], self.logic)
        else:
            self.lines.diecross[0] = False
        # print(self.trix_short[0],self.trix_long[0], "*", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iTrixLong(iBaseIndicator):
    '''
    因子：多头
    传入参数：
    rule = {"args": [12,26,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('trixlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iTrixLong, self).__init__()
        self.trix_short = btind.Trix(self.data.close, period=self.args[0])
        self.trix_long = btind.Trix(self.data.close, period=self.args[1])

    def next(self):
        trixlong = set([self.trix_short[i] > self.trix_long[i] for i in range(1 - self.args[2], 1)])

        if len(trixlong) == 1 and True in trixlong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.trixlong[0] = True and self.trix_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.trixlong[0] = True and self.trix_short[0] < 0
            else:  # 其他条件
                self.lines.trixlong[0] = True

        else:
            self.lines.trixlong[0] = False
        # print(self.trix_short[0],self.trix_long[0], "*", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iTrixShort(iBaseIndicator):
    '''
    因子：空头
    传入参数：
   rule = {"args": [12,26,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('trixshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iTrixShort, self).__init__()
        self.trix_short = btind.Trix(self.data.close, period=self.args[0])
        self.trix_long = btind.Trix(self.data.close, period=self.args[1])

    def next(self):
        trixshort = set([self.trix_short[i] < self.trix_long[i] for i in range(1 - self.args[2], 1)])

        if len(trixshort) == 1 and True in trixshort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.trixshort[0] = True and self.trix_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.trixshort[0] = True and self.trix_short[0] < 0
            else:  # 其他条件
                self.lines.trixshort[0] = True
        else:
            self.lines.trixshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iTrixTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [5,3],   # 连续N日短均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('trixtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iTrixTop, self).__init__()
        self.trix = btind.Trix(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.trix.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.trix[0] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.trixtop[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.trixtop[0] = True and _list[-1] < 0
            else:
                self.lines.trixtop[0] = True
        else:
            self.lines.trixtop[0] = False


class iTrixBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
   rule = {"args": [5,3],   # 连续N日短均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('trixbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iTrixBottom, self).__init__()
        self.trix = btind.Trix(self.data.close, period=self.args[0])

    def next(self):

        _list = list(self.trix.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.trix[0] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.trixbottom[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.trixbottom[0] = True and _list[-1] < 0
            else:
                self.lines.trixbottom[0] = True

        else:
            self.lines.trixbottom[0] = False
