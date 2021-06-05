import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iPriceoscillatorCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [12, 26, 9],      #快周期，慢周期，ppo(dif)平均移动周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,  # 周期结果比较
            "position":0}

            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iPriceoscillatorCrossGolden, self).__init__()
        self.ppo = btind.PercentagePriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1],period_signal=self.args[2])
        self.cross = btind.CrossOver(self.ppo.ppo, self.ppo.signal)

    def next(self):
        # print(self.data.datetime.date())
        # print(compare(self.ppo.ppo[0] - self.ppo.signal[0], self.logic))
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.ppo.ppo[0] - self.ppo.signal[0], self.logic) and \
                                            self.ppo.ppo[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.ppo.ppo[0] - self.ppo.signal[0], self.logic) and \
                                            self.ppo.ppo[0] < 0
            else:  # 其他情况
                self.lines.goldencross[0] = compare(self.ppo.ppo[0] - self.ppo.signal[0], self.logic)

        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iPriceoscillatorCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [12, 26, 9],      #快ema周期，慢ema周期，ppo(dif)平均移动周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,"position":0},  # 周期结果比较
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iPriceoscillatorCrossDie, self).__init__()
        self.ppo = btind.PercentagePriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1],period_signal=self.args[2])
        self.cross = btind.CrossOver(self.ppo.ppo, self.ppo.signal)

    def next(self):
        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.ppo.signal[0] - self.ppo.ppo[0], self.logic) and \
                                         self.ppo.ppo[0] > 0
            elif self.logic["position"] == -1:  # 出现在上部  <0
                self.lines.diecross[0] = compare(self.ppo.signal[0] - self.ppo.ppo[0], self.logic) and \
                                         self.ppo.ppo[0] < 0
            else:  # 其他情况
                self.lines.diecross[0] = compare(self.ppo.signal[0] - self.ppo.ppo[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iPriceoscillatorLong(iBaseIndicator):
    '''
    因子：多头
    传入参数：
   rule = {"args": [12,26,9,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('ppolong',)
    params = dict(rule=list())

    def __init__(self):
        super(iPriceoscillatorLong, self).__init__()
        self.ppo = btind.PercentagePriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1],period_signal=self.args[2])

    def next(self):
        difs = list(self.ppo.ppo.get(size=self.args[3]))  # 短线
        deas = list(self.ppo.signal.get(size=self.args[3]))  # 长线
        if len(difs) == self.args[3]:
            ppolong = set(list(map(lambda d: d > 0, difs + deas)))
        else:
            ppolong = []

        if len(ppolong) == 1 and True in ppolong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.ppolong[0] = True and self.ppo.ppo[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.ppolong[0] = True and self.ppo.ppo[0] < 0
            else:  # 其他条件
                self.lines.ppolong[0] = True

        else:
            self.lines.ppolong[0] = False
        # print(self.ppo.ppo[0], self.ppo.signal[0],self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iPriceoscillatorShort(iBaseIndicator):
    '''
    因子：空头
    传入参数：
    rule = {"args": [12,26,9,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('pposhort',)
    params = dict(rule=list())

    def __init__(self):
        super(iPriceoscillatorShort, self).__init__()
        self.ppo = btind.PercentagePriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1],period_signal=self.args[2])

    def next(self):
        difs = list(self.ppo.ppo.get(size=self.args[3]))
        deas = list(self.ppo.signal.get(size=self.args[3]))
        if len(difs) == self.args[3]:
            pposhort = set(list(map(lambda d: d < 0, difs + deas)))
        else:
            pposhort = []

        if len(pposhort) == 1 and True in pposhort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.pposhort[0] = True and self.ppo.ppo[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.pposhort[0] = True and self.ppo.ppo[0] < 0
            else:  # 其他条件
                self.lines.pposhort[0] = True
        else:
            self.lines.pposhort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iPriceoscillatorTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [12,26,9,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('ppotop',)
    params = dict(rule=list())

    def __init__(self):
        super(iPriceoscillatorTop, self).__init__()
        self.ppo = btind.PercentagePriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1],
                                                   period_signal=self.args[2])

    def next(self):

        ppo_list = list(self.ppo.ppo.get(size=self.args[3]))  # 短线
        signal_list = list(self.ppo.signal.get(size=self.args[3]))  # 长线
        histo_list = list(self.ppo.signal.get(size=self.args[3]))  # 柱线
        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        if len(_list) == self.args[3] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.ppotop[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.ppotop[0] = True and _list[-1] < 0
            else:
                self.lines.ppotop[0] = True
        else:
            self.lines.ppotop[0] = False


class iPriceoscillatorBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
    rule = {"args": [12,26,9,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('ppobottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iPriceoscillatorBottom, self).__init__()
        self.ppo = btind.PercentagePriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1],
                                                   period_signal=self.args[2])

    def next(self):

        ppo_list = list(self.ppo.ppo.get(size=self.args[3]))  # 短线
        signal_list = list(self.ppo.signal.get(size=self.args[3]))  # 长线
        histo_list = list(self.ppo.signal.get(size=self.args[3]))  # 柱线
        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        if len(_list) == self.args[3] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.ppobottom[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.ppobottom[0] = True and _list[-1] < 0
            else:
                self.lines.ppobottom[0] = True

        else:
            self.lines.ppobottom[0] = False
