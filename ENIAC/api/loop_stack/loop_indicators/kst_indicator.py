import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iKstCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [10,15,20,30,10,10,10,15,9]      #
            "logic":{"compare": "eq","byValue": 1,"byMax": 5  # 周期结果比较
            "position":1,}

            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iKstCrossGolden, self).__init__()
        self.kst = btind.KnowSureThing(self.data.close, rp1=self.args[0], rp2=self.args[1], rp3=self.args[2],
                                       rp4=self.args[3],
                                       rma1=self.args[4], rma2=self.args[5], rma3=self.args[6], rma4=self.args[7],
                                       rsignal=self.args[8]
                                       )
        self.cross = btind.CrossOver(self.kst.kst, self.kst.signal)

    def next(self):
        # print(self.data.datetime.date())
        # print(compare(self.kst.kst[0] - self.kst.signal[0], self.logic))
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.kst.kst[0] - self.kst.signal[0], self.logic) and \
                                            self.kst.kst[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.kst.kst[0] - self.kst.signal[0], self.logic) and \
                                            self.kst.kst[0] < 0
            else:  # 其他情况
                self.lines.goldencross[0] = compare(self.kst.kst[0] - self.kst.signal[0], self.logic)

        else:
            self.lines.goldencross[0] = False
        # print(self.kst.kst[0], self.kst.signal[0], self.data.close[0], '*', self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iKstCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [10,15,20,30,10,10,10,15,9]      #
            "logic":{"compare": "eq","byValue": 1,"byMax": 5  # 周期结果比较
            "position":1,}

            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iKstCrossDie, self).__init__()
        self.kst = btind.KnowSureThing(self.data.close, rp1=self.args[0], rp2=self.args[1], rp3=self.args[2],
                                       rp4=self.args[3],
                                       rma1=self.args[4], rma2=self.args[5], rma3=self.args[6], rma4=self.args[7],
                                       rsignal=self.args[8]
                                       )

        self.cross = btind.CrossOver(self.kst.kst, self.kst.signal)

    def next(self):
        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.kst.signal[0] - self.kst.kst[0], self.logic) and \
                                         self.kst.kst[0] > 0
            elif self.logic["position"] == -1:  # 出现在上部  <0
                self.lines.diecross[0] = compare(self.kst.signal[0] - self.kst.kst[0], self.logic) and \
                                         self.kst.kst[0] < 0
            else:  # 其他情况
                self.lines.diecross[0] = compare(self.kst.signal[0] - self.kst.kst[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iKstLong(iBaseIndicator):
    '''
    因子：多头
    传入参数：
     rule = {"args": [10,15,20,30,10,10,10,15,9]      #
            "logic":{"position":1,}

            }
    '''
    lines = ('kstlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iKstLong, self).__init__()
        self.kst = btind.KnowSureThing(self.data.close, rp1=self.args[0], rp2=self.args[1], rp3=self.args[2],
                                       rp4=self.args[3],
                                       rma1=self.args[4], rma2=self.args[5], rma3=self.args[6], rma4=self.args[7],
                                       rsignal=self.args[8]
                                       )

    def next(self):
        ksts = list(self.kst.kst.get(size=self.args[9]))  # 短线
        signals = list(self.kst.signal.get(size=self.args[9]))  # 长线
        if len(ksts) == self.args[9]:
            kstlong = set(list(map(lambda d: d > 0, ksts + signals)))
        else:
            kstlong = []

        if len(kstlong) == 1 and True in kstlong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.kstlong[0] = True and self.kst.kst[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.kstlong[0] = True and self.kst.kst[0] < 0
            else:  # 其他条件
                self.lines.kstlong[0] = True

        else:
            self.lines.kstlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iKstShort(iBaseIndicator):
    '''
    因子：空头
    传入参数：
     rule = {"args": [10,15,20,30,10,10,10,15,9]      #
            "logic":{"position":1,}

            }
    '''
    lines = ('kstshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iKstShort, self).__init__()
        self.kst = btind.KnowSureThing(self.data.close, rp1=self.args[0], rp2=self.args[1], rp3=self.args[2],
                                       rp4=self.args[3],
                                       rma1=self.args[4], rma2=self.args[5], rma3=self.args[6], rma4=self.args[7],
                                       rsignal=self.args[8]
                                       )

    def next(self):
        ksts = list(self.kst.kst.get(size=self.args[9]))
        signals = list(self.kst.signal.get(size=self.args[9]))
        if len(ksts) == self.args[9]:
            kstshort = set(list(map(lambda d: d < 0, ksts + signals)))
        else:
            kstshort = []

        if len(kstshort) == 1 and True in kstshort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.kstshort[0] = True and self.kst.kst[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.kstshort[0] = True and self.kst.kst[0] < 0
            else:  # 其他条件
                self.lines.kstshort[0] = True
        else:
            self.lines.kstshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iKstTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [10,15,20,30,10,10,10,15,9]      #
            "logic":{"position":1,}

            }
    '''
    lines = ('ksttop',)
    params = dict(rule=list())

    def __init__(self):
        super(iKstTop, self).__init__()
        self.kst = btind.KnowSureThing(self.data.close, rp1=self.args[0], rp2=self.args[1], rp3=self.args[2],
                                       rp4=self.args[3],
                                       rma1=self.args[4], rma2=self.args[5], rma3=self.args[6], rma4=self.args[7],
                                       rsignal=self.args[8]
                                       )

    def next(self):

        kst_list = list(self.kst.kst.get(size=self.args[9]))  # 短线
        signal_list = list(self.kst.signal.get(size=self.args[9]))  # 长线
        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        if len(_list) == self.args[9] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.ksttop[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.ksttop[0] = True and _list[-1] < 0
            else:
                self.lines.ksttop[0] = True
        else:
            self.lines.ksttop[0] = False


class iKstBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
    rule = {"args": [12, 26, 9,  30，"ksts"],      #快ema周期，慢ema周期，kst(kst)平均移动周期, 所选因子线， 最近 n 天 极值
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #
            }
    '''
    lines = ('kstbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iKstBottom, self).__init__()
        self.kst = btind.KnowSureThing(self.data.close, rp1=self.args[0], rp2=self.args[1], rp3=self.args[2],
                                       rp4=self.args[3],
                                       rma1=self.args[4], rma2=self.args[5], rma3=self.args[6], rma4=self.args[7],
                                       rsignal=self.args[8]
                                       )

    def next(self):

        kst_list = list(self.kst.kst.get(size=self.args[9]))  # 短线
        signal_list = list(self.kst.signal.get(size=self.args[9]))  # 长线
        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        if len(_list) == self.args[3] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.kstbottom[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.kstbottom[0] = True and _list[-1] < 0
            else:
                self.lines.kstbottom[0] = True

        else:
            self.lines.kstbottom[0] = False
