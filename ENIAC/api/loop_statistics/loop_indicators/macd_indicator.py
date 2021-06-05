import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iMacdCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [12, 26, 9],      #快ema周期，慢ema周期，macd(dif)平均移动周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iMacdCrossGolden, self).__init__()
        self.macd = btind.MACD(self.data.close, period_me1=self.args[0], period_me2=self.args[1], period_signal= self.args[2])
        self.cross = btind.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        # print(self.data.datetime.date())
        # print(compare(self.macd.macd[0] - self.macd.signal[0], self.logic))
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.macd.macd[0] - self.macd.signal[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iMacdCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [12, 26, 9],      #快ema周期，慢ema周期，macd(dif)平均移动周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iMacdCrossDie, self).__init__()
        self.macd = btind.MACD(self.data.close, period_me1=self.args[0], period_me2=self.args[1], period_signal= self.args[2])
        self.cross = btind.CrossOver(self.macd.macd, self.macd.signal)

    def next(self):
        if self.cross[0] == -1:
            self.lines.diecross[0] = compare(self.macd.signal[0] - self.macd.macd[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iMacdLong(iBaseIndicator):
    '''
    因子：多头
    传入参数：
    rule = {"args": [12, 26, 9, 3],      #快ema周期，慢ema周期，macd(dif)平均移动周期, 连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('macdlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iMacdLong, self).__init__()
        self.macd = btind.MACD(self.data.close, period_me1=self.args[0], period_me2=self.args[1], period_signal= self.args[2])

    def next(self):
        difs = list(self.macd.macd.get(size=self.args[3])) # 短线
        deas = list(self.macd.signal.get(size=self.args[3])) # 长线
        if len(difs) == self.args[3]:
            macdlong = set(list(map(lambda d: d>0, difs + deas)))
        else:
            macdlong = []

        if len(macdlong) == 1 and True in macdlong:
            self.lines.macdlong[0] = True
        else:
            self.lines.macdlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])

class iMacdShort(iBaseIndicator):
    '''
    因子：空头
    传入参数：
    rule = {"args": [12, 26, 9, 3],      #快ema周期，慢ema周期，macd(dif)平均移动周期, 连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('macdshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iMacdShort, self).__init__()
        self.macd = btind.MACD(self.data.close, period_me1=self.args[0], period_me2=self.args[1], period_signal= self.args[2])

    def next(self):
        difs = list(self.macd.macd.get(size=self.args[3]))
        deas = list(self.macd.signal.get(size=self.args[3]))
        if len(difs) == self.args[3]:
            macdshort = set(list(map(lambda d: d<0, difs + deas)))
        else:
            macdshort = []

        if len(macdshort) == 1 and True in macdshort:
            self.lines.macdshort[0] = True
        else:
            self.lines.macdshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iMacdTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [12, 26, 9,  30，"difs"],      #快ema周期，慢ema周期，macd(dif)平均移动周期,  最近 n 天, 所选因子线，
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #
            }
    '''
    lines = ('macdtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iMacdTop, self).__init__()
        self.macd = btind.MACD(self.data.close, period_me1=self.args[0], period_me2=self.args[1], period_signal= self.args[2])

    def next(self):

        dif_list = list(self.macd.macd.get(size=self.args[3])) # 短线
        dea_list = list(self.macd.signal.get(size=self.args[3])) # 长线
        hist_list = [i-j for (i,j) in zip(dif_list,dea_list)]  # 柱线
        _list = eval(f"{self.sigline}_list") # 调用的因子线

        if len(_list) == self.args[3] and _list[-1] == max(_list):
            self.lines.macdtop[0] = True
        else:
            self.lines.macdtop[0] = False

        # if self.args[3] == 'difs':
        #     if len(difs_list) == self.args[4]  and difs_list[-1] == max(difs_list):
        #         self.lines.macdtop[0] = True
        #     else:
        #         self.lines.macdtop[0] = False
        #
        # elif self.args[3] == 'deas':
        #     if len(difs_list) == self.args[4]  and deas_list[-1] == max(deas_list):
        #         self.lines.macdtop[0] = True
        #     else:
        #         self.lines.macdtop[0] = False
        #     pass
        # elif self.args[3] == 'hist':
        #     if len(difs_list) == self.args[4]  and hist_list[-1] == max(hist_list):
        #         self.lines.macdtop[0] = True
        #     else:
        #         self.lines.macdtop[0] = False
        #     pass
        # else:
        #     print('input args.factor name error!')
        #     pass


class iMacdBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
    rule = {"args": [12, 26, 9,  30，"difs"],      #快ema周期，慢ema周期，macd(dif)平均移动周期, 所选因子线， 最近 n 天 极值
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #
            }
    '''
    lines = ('macdbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iMacdBottom, self).__init__()
        self.macd = btind.MACD(self.data.close, period_me1 = self.args[0], period_me2 = self.args[1], period_signal = self.args[2])

    def next(self):

        dif_list = list(self.macd.macd.get(size=self.args[3])) # 短线
        dea_list = list(self.macd.signal.get(size=self.args[3])) # 长线
        hist_list = [i-j for (i,j) in zip(dif_list,dea_list)]  # 柱线
        _list = eval(f"{self.sigline}_list") # 调用的因子线

        if len(_list) == self.args[3] and _list[-1] == min(_list):
            self.lines.macdbottom[0] = True
        else:
            self.lines.macdbottom[0] = False

