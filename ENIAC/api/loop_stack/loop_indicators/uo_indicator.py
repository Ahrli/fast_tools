import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iUoCompare(iBaseIndicator):
    '''
    因子：相对强弱指数比较数值
    传入参数：
    rule = {"args": [7,14,28],
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('uo',)
    params = dict(rule=list())

    def __init__(self):
        super(iUoCompare, self).__init__()
        self.uo = btind.UltimateOscillator(p1=self.args[0], p2=self.args[1], p3=self.args[2])

    def next(self):
        self.lines.uo[0] = compare(self.uo[0], self.logic)
        # print(self.uo[0], ",", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iUoCrossGolden(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": ["5", "10", "30"],    #短均线周期, 长均线周期，低位点
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,
                    "position":1
                         },  # 死叉情况比较大小,长比短高多少
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iUoCrossGolden, self).__init__()
        self.uo_short = btind.UltimateOscillator(p1=self.args[0], p2=self.args[1], p3=self.args[2])
        self.uo_long = btind.UltimateOscillator(p1=self.args[3], p2=self.args[4], p3=self.args[5])
        self.cross = btind.CrossOver(self.uo_short, self.uo_long)

    def next(self):
        if self.uo_short[0] < self.args[2] and self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.uo_short[0] - self.uo_long[0], self.logic) and \
                                            self.uo_short[0] > 50
            elif self.logic["position"] == -1:  # 出现部  < 0
                self.lines.goldencross[0] = compare(self.uo_short[0] - self.uo_long[0], self.logic) and \
                                            self.uo_short[0] < 50
            else:
                self.lines.goldencross[0] = compare(self.uo_short[0] - self.uo_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.uo_short[0], self.uo_long[0],",", self.data.datetime.datetime())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iUoCrossDie(iBaseIndicator):
    '''
    因子：死叉：短期RSI线在高位向下突破长期RSI线, 一般为RSI指标的“死亡交叉”
    传入参数：
    rule = {"args": ["5", "10", "70"],    #短均线周期, 长均线周期，高位点
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,
            "position":1
            },  # 死叉情况比较大小,长比短高多少
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iUoCrossDie, self).__init__()
        self.uo_short = btind.UltimateOscillator(p1=self.args[0], p2=self.args[1], p3=self.args[2])
        self.uo_long = btind.UltimateOscillator(p1=self.args[3], p2=self.args[4], p3=self.args[5])
        self.cross = btind.CrossOver(self.uo_short, self.uo_long)

    def next(self):
        if self.uo_short[0] > self.args[2] and self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.uo_long[0] - self.uo_short[0], self.logic) and self.uo_short[
                    0] > 50
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.diecross[0] = compare(self.uo_long[0] - self.uo_short[0], self.logic) and self.uo_short[
                    0] < 50
            else:
                self.lines.diecross[0] = compare(self.uo_long[0] - self.uo_short[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iUoLong(iBaseIndicator):
    '''

    传入参数：
    rule = {"args": ["5", "10", "3"],    #短均线周期, 长均线周期, "连续多少天多头"
            "logic":{"position":1  },  #位置
            }
    '''
    lines = ('uolong',)
    params = dict(rule=list())

    def __init__(self):
        super(iUoLong, self).__init__()
        self.uo_short = btind.UltimateOscillator(p1=self.args[0], p2=self.args[1], p3=self.args[2])
        self.uo_long = btind.UltimateOscillator(p1=self.args[3], p2=self.args[4], p3=self.args[5])

    def next(self):
        uolong = set([self.uo_short[i] > self.uo_long[i] for i in range(1 - self.args[6], 1)])
        if len(uolong) == 1 and True in uolong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.uolong[0] = True and self.uo_short[0] > 50
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.uolong[0] = True and self.uo_short[0] < 50
            else:
                self.lines.uolong[0] = True
        else:
            self.lines.uolong[0] = False
        # print(self.uo_short[0], ",", self.uo_long[0], ",", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iUoShort(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": ["5", "10", "3"],    #短均线周期, 长均线周期 "连续多少天空头"
            "logic":{"position":1  },  #位置
            }
    '''
    lines = ('uoshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iUoShort, self).__init__()
        self.uo_short = btind.UltimateOscillator(p1=self.args[0], p2=self.args[1], p3=self.args[2])
        self.uo_long = btind.UltimateOscillator(p1=self.args[3], p2=self.args[4], p3=self.args[5])

    def next(self):
        uoshort = set([ self.uo_short[i] < self.uo_long[i] for i in range(1 - self.args[6], 1)])
        if len(uoshort) == 1 and True in uoshort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.uoshort[0] = True and self.uo_short[0] > 50
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.uoshort[0] = True and self.uo_short[0] < 50
            else:
                self.lines.uoshort[0] = True
        else:
            self.lines.uoshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iUoTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] , # 周期 连续天数
               "logic":{"position":1
               },  #位置
                },
    '''
    lines = ('uotop',)
    params = dict(rule=list())

    def __init__(self):
        super(iUoTop, self).__init__()
        self.uo = btind.UltimateOscillator(p1=self.args[0], p2=self.args[1], p3=self.args[2])

    def next(self):
        _list = list(self.uo.get(size=self.args[3]))
        if len(_list) == self.args[3] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.uotop[0] = True and _list[-1] > 50
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.uotop[0] = True and _list[-1] < 50
            else:
                self.lines.uotop[0] = True
        else:
            self.lines.uotop[0] = False


class iUoBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [12,26,9,3],   # 连续N日短, 连续N中,连续N长, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('uobottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iUoBottom, self).__init__()
        self.uo = btind.UltimateOscillator(p1=self.args[0], p2=self.args[1], p3=self.args[2])

    def next(self):
        _list = list(self.uo.get(size=self.args[3]))
        if len(_list) == self.args[3] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.uobottom[0] = True and _list[-1] > 50
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.uobottom[0] = True and _list[-1] < 50
            else:
                self.lines.uobottom[0] = True
        else:
            self.lines.uobottom[0] = False

