import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iViCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [12],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            "position":{1(up),-1(down),0(any)},无意义

            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iViCrossGolden, self).__init__()
        self.vi = btind.Vortex(period=self.args[0])
        self.cross = btind.CrossOver(self.vi.vi_plus, self.vi.vi_minus)

    def next(self):
        # print(self.data.datetime.date())
        # print(compare(self.vi.vi_plus[0] - self.vi.vi_minus[0], self.logic))
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.vi.vi_plus[0] - self.vi.vi_minus[0], self.logic)

        else:
            self.lines.goldencross[0] = False

        # print(self.vi.vi_plus[0], ",", self.vi.vi_minus[0], ",", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iViCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [12],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            "position":{1(up),-1(down),0(any)},无意义
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iViCrossDie, self).__init__()
        self.vi = btind.Vortex(period=self.args[0])
        self.cross = btind.CrossOver(self.vi.vi_plus, self.vi.vi_minus)

    def next(self):
        if self.cross[0] == -1:
            self.lines.diecross[0] = compare(self.vi.vi_minus[0] - self.vi.vi_plus[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iViLong(iBaseIndicator):
    '''
    因子：多头
    传入参数：
    rule = {"args": [12,  3],      #周期 连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
             "position":{1(up),-1(down),0(any)}, # 无意义
            }
    '''
    lines = ('vi_pluslong',)
    params = dict(rule=list())

    def __init__(self):
        super(iViLong, self).__init__()
        self.vi = btind.Vortex(period=self.args[0])

    def next(self):
        vi_plus = list(self.vi.vi_plus.get(size=self.args[1]))
        vi_minus = list(self.vi.vi_minus.get(size=self.args[1]))

        if len(vi_plus) == self.args[1]:
            vi_pluslong = set([vi_plus[i] > vi_minus[i] for i in range(0, self.args[1])])

        else:
            vi_pluslong = []

        if len(vi_pluslong) == 1 and True in vi_pluslong:

            self.lines.vi_pluslong[0] = True

        else:
            self.lines.vi_pluslong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iViShort(iBaseIndicator):
    '''
    因子：空头
    传入参数：
    rule = {"args": [12,  3],      #周期 连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
             "position":{1(up),-1(down),0(any)}, #无意义
            }
    '''
    lines = ('vi_plusshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iViShort, self).__init__()
        self.vi = btind.Vortex(period=self.args[0])

    def next(self):
        vi_plus = list(self.vi.vi_plus.get(size=self.args[1]))
        vi_minus = list(self.vi.vi_minus.get(size=self.args[1]))
        if len(vi_plus) == self.args[1]:
            vi_plusshort = set([vi_plus[i] < vi_minus[i] for i in range(0, self.args[1])])

        else:
            vi_plusshort = []

        if len(vi_plusshort) == 1 and True in vi_plusshort:

            self.lines.vi_plusshort[0] = True
        else:
            self.lines.vi_plusshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iViTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [12,3],      #周期，  最近 n 天,
            'line': 'vi_plus',   所选因子线，
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''

    lines = ('vi_plustop',)
    params = dict(rule=list())

    def __init__(self):
        super(iViTop, self).__init__()
        self.vi = btind.Vortex(period=self.args[0])

    def next(self):

        vi_plus = list(self.vi.vi_plus.get(size=self.args[1]))
        vi_minus = list(self.vi.vi_minus.get(size=self.args[1]))
        _list = eval(f"{self.sigline}")  # 调用的因子线

        if len(_list) == self.args[1] and _list[-1] == max(_list):

            self.lines.vi_plustop[0] = True
        else:
            self.lines.vi_plustop[0] = False


class iViBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
    rule =  "params": {"args": ["13", 3, ],  #周期，  最近 n 天,
                         'line': 'vi_plus',  所选因子线，
                         "logic": {"compare": "ge", "byValue": 0, "byMax": 5,  #无意义
                         }
    '''
    lines = ('vi_plusbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iViBottom, self).__init__()
        self.vi = btind.Vortex(period=self.args[0])

    def next(self):

        vi_plus = list(self.vi.vi_plus.get(size=self.args[1]))
        vi_minus = list(self.vi.vi_minus.get(size=self.args[1]))
        _list = eval(f"{self.sigline}")  # 调用的因子线

        if len(_list) == self.args[1] and _list[-1] == min(_list):
            self.lines.vi_plusbottom[0] = True

        else:
            self.lines.vi_plusbottom[0] = False


class iViDistance(iBaseIndicator):
    '''
    因子：最近 n  天 最点
    传入参数：
    rule =  "params": {"args": ["13", 3, ],  #周期，  最近 n 天,
                         'line': 'vi_plus',  所选因子线，
                         "logic": {"compare": "ge", "byValue": 0, "byMax": 5,  #无意义
                         }
    '''
    lines = ('vi_distance',)
    params = dict(rule=list())

    def __init__(self):
        super(iViDistance, self).__init__()
        self.vi = btind.Vortex(period=self.args[0])

    def next(self):
        print(self.vi.vi_plus[0] ,self.vi.vi_minus[0])
        print( self.vi.vi_plus[0] - self.vi.vi_minus[0])
        self.lines.vi_distance[0] = self.vi.vi_plus[0] - self.vi.vi_minus[0]
