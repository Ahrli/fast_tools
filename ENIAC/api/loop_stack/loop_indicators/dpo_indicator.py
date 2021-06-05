import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator


class iDpoCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #sma周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('dpo',)
    params = dict(rule=list())

    def __init__(self):
        super(iDpoCompare, self).__init__()
        self.dpo = btind.DetrendedPriceOscillator(self.data.close, period=self.args[0])

    def next(self):
        self.lines.dpo[0] = compare(self.dpo[0], self.logic)
        # print(self.dpo[0], self.data.close[0], '*', self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iDpoCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,"position": 0},  # 金叉情况比较大小， 短比长高多少 位置
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iDpoCrossGolden, self).__init__()
        self.dpo_short = btind.DetrendedPriceOscillator(self.data.close, period=self.args[0])
        self.dpo_long = btind.DetrendedPriceOscillator(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.dpo_short, self.dpo_long)

    def next(self):
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.dpo_short[0] - self.dpo_long[0], self.logic) and \
                                            self.dpo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.dpo_short[0] - self.dpo_long[0], self.logic) and \
                                            self.dpo_short[0] < 0
            else:
                self.lines.goldencross[0] = compare(self.dpo_short[0] - self.dpo_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.dpo_short[0],self.dpo_long[0], self.data.close[0], '*', self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iDpoCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,"position": 0},  # 金叉情况比较大小， 短比长高多少 位置
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iDpoCrossDie, self).__init__()
        self.dpo_short = btind.DetrendedPriceOscillator(self.data.close, period=self.args[0])
        self.dpo_long = btind.DetrendedPriceOscillator(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.dpo_short, self.dpo_long)

    def next(self):
        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.dpo_long[0] - self.dpo_short[0], self.logic) and self.dpo_short[
                    0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.diecross[0] = compare(self.dpo_long[0] - self.dpo_short[0], self.logic) and self.dpo_short[
                    0] < 0
            else:
                self.lines.diecross[0] = compare(self.dpo_long[0] - self.dpo_short[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iDpoLong(iBaseIndicator):
    '''
    因子：ma多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"position": 0},   #位置
            }
    '''
    # lines = ('dpolong', 'short', 'long')
    lines = ('dpolong',)
    params = dict(rule=list())

    def __init__(self):
        super(iDpoLong, self).__init__()
        self.logic = self.p.rule['logic']
        self.dpo_short = btind.DetrendedPriceOscillator(self.data.close, period=self.args[0])
        self.dpo_long = btind.DetrendedPriceOscillator(self.data.close, period=self.args[1])

    def next(self):
        dpolong = set([self.dpo_short[i] > self.dpo_long[i] for i in range(1 - self.args[2], 1)])

        if len(dpolong) == 1 and True in dpolong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.dpolong[0] = True and self.dpo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.dpolong[0] = True and self.dpo_short[0] < 0
            else:
                self.lines.dpolong[0] = True
        else:
            self.lines.dpolong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iDpoShort(iBaseIndicator):
    '''
    因子：ma空头
    传入参数：
         rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position": 0},   #位置
            }
    '''
    lines = ('dposhort',)
    params = dict(rule=list())

    def __init__(self):
        super(iDpoShort, self).__init__()
        self.dpo_short = btind.DetrendedPriceOscillator(self.data.close, period=self.args[0])
        self.dpo_long = btind.DetrendedPriceOscillator(self.data.close, period=self.args[1])

    def next(self):
        dposhort = set([self.dpo_short[i]< self.dpo_long[i] for i in range(1 - self.args[2], 1)])
        if len(dposhort) == 1 and True in dposhort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.dposhort[0] = True and self.dpo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.dposhort[0] = True and self.dpo_short[0] < 0
            else:
                self.lines.dposhort[0] = True
        else:
            self.lines.dposhort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iDpoTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                 "logic":{"position": 0},   #位置
                 }
    '''
    lines = ('dpotop',)
    params = dict(rule=list())

    def __init__(self):
        super(iDpoTop, self).__init__()
        self.dpo = btind.DetrendedPriceOscillator(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.dpo.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.dpotop[0] = True and self.dpo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.dpotop[0] = True and self.dpo_short[0] < 0
            else:
                self.lines.dpotop[0] = True
        else:
            self.lines.dpotop[0] = False


class iDpoBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"position": 0},   #位置
                }
    '''
    lines = ('dpobottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iDpoBottom, self).__init__()
        self.dpo = btind.DetrendedPriceOscillator(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.dpo.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.dpobottom[0] = True and self.dpo_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.dpobottom[0] = True and self.dpo_short[0] < 0
            else:
                self.lines.dpobottom[0] = True
        else:
            self.lines.dpobottom[0] = False
