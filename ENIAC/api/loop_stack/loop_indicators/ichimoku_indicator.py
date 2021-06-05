import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iIchimokuCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": [9,26,52,26,26],
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('ichi',)
    params = dict(rule=list())

    def __init__(self):
        super(iIchimokuCompare, self).__init__()
        self.ichi = btind.Ichimoku(tenkan=self.args[0], kijun=self.args[1], senkou=self.args[2],
                                   senkou_lead=self.args[3], chikou=self.args[4])

    def next(self):
        tenkan_list = self.ichi.tenkan_sen
        kijun_list = self.ichi.kijun_sen
        senkou_span_a_list = self.ichi.senkou_span_a
        senkou_span_b_list = self.ichi.senkou_span_b
        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        self.lines.ichi[0] = compare(_list[0], self.logic)
        # print(self.ichi.tenkan_sen[0],self.ichi.kijun_sen[0],self.ichi.senkou_span_a[0],self.ichi.senkou_span_a[0],self.ichi.chikou_span[0],self.data.close[0],'*',self.data.datetime.date())


class iIchimokuCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [9,26,52,26,26]
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            },

            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iIchimokuCrossGolden, self).__init__()
        self.ichi = btind.Ichimoku(tenkan=self.args[0], kijun=self.args[1], senkou=self.args[2],
                                   senkou_lead=self.args[3], chikou=self.args[4])
        cross_sen = btind.CrossOver(self.ichi.tenkan_sen, self.ichi.kijun_sen)
        cross_span = btind.CrossOver(self.ichi.senkou_span_a, self.ichi.senkou_span_b)

    def next(self):

        self.cross = eval(f"{self.sigline}")  # 调用的cross线
        if self.cross[0] == 1:
            if self.sigline == 'cross_sen':
                self.lines.goldencross[0] = compare(self.ichi.tenkan_sen[0] - self.ichi.kijun_sen[0], self.logic)
            else:
                self.lines.goldencross[0] = compare(self.ichi.senkou_span_a[0] - self.ichi.senkou_span_b[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iIchimokuCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [9,26,52,26,26]
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iIchimokuCrossDie, self).__init__()
        self.ichi = btind.Ichimoku(tenkan=self.args[0], kijun=self.args[1], senkou=self.args[2],
                                   senkou_lead=self.args[3], chikou=self.args[4])
        cross_sen = btind.CrossOver(self.ichi.tenkan_sen, self.ichi.kijun_sen)
        cross_span = btind.CrossOver(self.ichi.senkou_span_a, self.ichi.senkou_span_b)

    def next(self):
        self.cross = eval(f"{self.sigline}")  # 调用的cross线
        if self.cross[0] == -1:
            if self.sigline == 'cross_sen':
                self.lines.diecross[0] = compare(self.ichi.kijun_sen[0] - self.ichi.tenkan_sen[0], self.logic)
            else:
                self.lines.goldencross[0] = compare(self.ichi.senkou_span_b[0] - self.ichi.senkou_span_a[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iIchimokuLong(iBaseIndicator):
    '''
    因子：多头
    传入参数：
    rule = {"args": [9,26,52,26,26]
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('ichilong',)
    params = dict(rule=list())

    def __init__(self):
        super(iIchimokuLong, self).__init__()
        self.ichi = btind.Ichimoku(tenkan=self.args[0], kijun=self.args[1], senkou=self.args[2],
                                   senkou_lead=self.args[3], chikou=self.args[4])

    def next(self):
        _long = eval(f"{self.sigline}")  # 调用的cross线
        if _long=='sen':
            ichilong = set([self.ichi.tenkan_sen[i] > self.ichi.kijun_sen[i] for i in range(1 - self.args[5], 1)])
        else:
            ichilong = set([self.ichi.senkou_span_a[i] > self.ichi.senkou_span_b[i] for i in range(1 - self.args[5], 1)])
        if len(ichilong) == 1 and True in ichilong:

            self.lines.ichilong[0] = True

        else:
            self.lines.ichilong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iIchimokuShort(iBaseIndicator):
    '''
    因子：空头
    传入参数：
    rule = {"args": [9,26,52,26,26]
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('ichishort',)
    params = dict(rule=list())

    def __init__(self):
        super(iIchimokuShort, self).__init__()
        self.ichi = btind.Ichimoku(tenkan=self.args[0], kijun=self.args[1], senkou=self.args[2],
                                   senkou_lead=self.args[3], chikou=self.args[4])

    def next(self):
        _short = eval(f"{self.sigline}")  # 调用的cross线
        if _short == 'sen':
            ichishort = set([self.ichi.tenkan_sen[i] < self.ichi.kijun_sen[i] for i in range(1 - self.args[5], 1)])
        else:
            ichishort = set([self.ichi.senkou_span_a[i] < self.ichi.senkou_span_b[i] for i in range(1 - self.args[5], 1)])

        if len(ichishort) == 1 and True in ichishort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.ichishort[0] = True and self.ichi.tenkan_sen[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.ichishort[0] = True and self.ichi.tenkan_sen[0] < 0
            else:  # 其他条件
                self.lines.ichishort[0] = True
        else:
            self.lines.ichishort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iIchimokuTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [9,26,52,26,26]
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #
            }
    '''
    lines = ('ichitop',)
    params = dict(rule=list())

    def __init__(self):
        super(iIchimokuTop, self).__init__()
        self.ichi = btind.Ichimoku(tenkan=self.args[0], kijun=self.args[1], senkou=self.args[2],
                                   senkou_lead=self.args[3], chikou=self.args[4])

    def next(self):

        tenkan_list = list(self.ichi.tenkan_sen.get(size=self.args[5]))  # 短线
        kijun_list = list(self.ichi.kijun_sen.get(size=self.args[5]))  # 长线
        senkou_span_a_list = list(self.ichi.senkou_span_a.get(size=self.args[5]))
        senkou_span_b_list = list(self.ichi.senkou_span_b.get(size=self.args[5]))
        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        if len(_list) == self.args[3] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.ichitop[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.ichitop[0] = True and _list[-1] < 0
            else:
                self.lines.ichitop[0] = True
        else:
            self.lines.ichitop[0] = False


class iIchimokuBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
    rule = {"args": [9,26,52,26,26],
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #
            }
    '''
    lines = ('ichibottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iIchimokuBottom, self).__init__()
        self.ichi = btind.Ichimoku(tenkan=self.args[0], kijun=self.args[1], senkou=self.args[2],
                                   senkou_lead=self.args[3], chikou=self.args[4])

    def next(self):
        tenkan_list = list(self.ichi.tenkan_sen.get(size=self.args[5]))  # 短线
        kijun_list = list(self.ichi.kijun_sen.get(size=self.args[5]))  # 长线
        senkou_span_a_list = list(self.ichi.senkou_span_a.get(size=self.args[5]))
        senkou_span_b_list = list(self.ichi.senkou_span_b.get(size=self.args[5]))
        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        if len(_list) == self.args[3] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.ichibottom[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.ichibottom[0] = True and _list[-1] < 0
            else:
                self.lines.ichibottom[0] = True

        else:
            self.lines.ichibottom[0] = False
