import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iAroonUpDownCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [12,],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较

            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iAroonUpDownCrossGolden, self).__init__()
        self.aroon = btind.AroonUpDown(period=self.args[0])
        self.cross = btind.CrossOver(self.aroon.aroonup, self.aroon.aroondown)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.aroon.aroonup[0] - self.aroon.aroondown[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.aroon.aroonup[0], self.aroon.aroondown[0], self.data.close[0], '*', self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iAroonUpDownCrossDie(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [12,],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较

            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iAroonUpDownCrossDie, self).__init__()
        self.aroon = btind.AroonUpDown(period=self.args[0])

        self.cross = btind.CrossOver(self.aroon.aroonup, self.aroon.aroondown)

    def next(self):
        if self.cross[0] == -1:

            self.lines.diecross[0] = compare(self.aroon.aroondown[0] - self.aroon.aroonup[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iAroonUpDownLong(iBaseIndicator):
    '''
    因子：多头
    传入参数：
    rule = {"args": [12,  3],      #周期,连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 无意义
            }
    '''
    lines = ('aroonlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iAroonUpDownLong, self).__init__()
        self.aroon = btind.AroonUpDown(period=self.args[0])

    def next(self):
        aroonlong = set([self.aroon.aroonup[i] >50> self.aroon.aroondown[i] for i in range(1 - self.args[1], 1)])

        if len(aroonlong) == 1 and True in aroonlong:
            self.lines.aroonlong[0] = True
        else:
            self.lines.aroonlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iAroonUpDownShort(iBaseIndicator):
    '''
    因子：空头
    传入参数：
    rule = {"args": [12,  3],      #周期,连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 无意义
            }

    '''
    lines = ('aroonshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iAroonUpDownShort, self).__init__()
        self.aroon = btind.AroonUpDown(period=self.args[0])

    def next(self):

        aroonshort = set([self.aroon.aroonup[i]<50 < self.aroon.aroondown[i] for i in range(1 - self.args[1], 1)])

        if len(aroonshort) == 1 and True in aroonshort:

            self.lines.aroonshort[0] = True
        else:
            self.lines.aroonshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iAroonUpDownTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [12, 3],      #周期，  最近 n 天, 所选因子线，
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
             'line': 'aroonup',
            }
    '''
    lines = ('aroontop',)
    params = dict(rule=list())

    def __init__(self):
        super(iAroonUpDownTop, self).__init__()
        self.aroon = btind.AroonUpDown(period=self.args[0])

    def next(self):
        aroonup_list = list(self.aroon.aroonup.get(size=self.args[1]))  # 短线
        aroondown_list = list(self.aroon.aroondown.get(size=self.args[1]))  # 长线
        _list = eval(f"{self.sigline}_list")  # 调用的因子线
        if len(_list) == self.args[1] and _list[-1] == max(_list):

            self.lines.aroontop[0] = True
        else:
            self.lines.aroontop[0] = False


class iAroonUpDownBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
   rule = {"args": [12, 3],      #周期，  最近 n 天, 所选因子线，
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
             'line': 'aroonup',
            }
    '''
    lines = ('aroonbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iAroonUpDownBottom, self).__init__()
        self.aroon = btind.AroonUpDown(period=self.args[0])

    def next(self):
        aroonup_list = list(self.aroon.aroonup.get(size=self.args[1]))  # 短线
        aroondown_list = list(self.aroon.aroondown.get(size=self.args[1]))  # 长线
        _list = eval(f"{self.sigline}_list")  # 调用的因子线
        if len(_list) == self.args[1] and _list[-1] == min(_list):

            self.lines.aroonbottom[0] = True
        else:
            self.lines.aroonbottom[0] = False
