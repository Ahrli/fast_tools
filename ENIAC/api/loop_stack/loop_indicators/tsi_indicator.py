import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iTSICompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["25",'13',1],      #长周期,短周期,价格回看周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('tsi',)
    params = dict(rule=list())

    def __init__(self):
        super(iTSICompare, self).__init__()
        self.tsi = btind.TrueStrengthIndicator(self.data.close, period1=self.args[0], period2=self.args[1],
                                               pchange=self.args[2])

    def next(self):
        self.lines.tsi[0] = compare(self.tsi[0], self.logic)
        # print(self.tsi[0], ",", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iTSICrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["26",'13',1,"40",'20',1],   #长周期,短周期,价格回看周期  , 长周期,短周期,价格回看周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,  # 金叉情况比较大小， 短比长高多少
            "position":{1(up),-1(down),0(any)},             # 1 0轴以上金叉  -1 0轴以下金叉 0 无
             }
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iTSICrossGolden, self).__init__()
        self.tsi_short = btind.TrueStrengthIndicator(self.data.close, period1=self.args[0], period2=self.args[1],
                                                     pchange=self.args[2])
        self.tsi_long = btind.TrueStrengthIndicator(self.data.close, period1=self.args[3], period2=self.args[4],
                                                    pchange=self.args[5])
        self.cross = btind.CrossOver(self.tsi_short, self.tsi_long)

    def next(self):
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.tsi_short[0] - self.tsi_long[0], self.logic) and \
                                            self.tsi_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.tsi_short[0] - self.tsi_long[0], self.logic) and \
                                            self.tsi_short[0] < 0
            else:  # 其他情况
                self.lines.goldencross[0] = compare(self.tsi_short[0] - self.tsi_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iTSICrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["26",'13',1,"40",'20',1],   #长周期,短周期,价格回看周期  , 长周期,短周期,价格回看周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,  # 金叉情况比较大小， 短比长高多少
            "position":{1(up),-1(down),0(any)},             # 1 0轴以上死叉  -1 0轴以下死叉 0 无
             }
            }

    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iTSICrossDie, self).__init__()
        self.tsi_short = btind.TrueStrengthIndicator(self.data.close, period1=self.args[0], period2=self.args[1],
                                                     pchange=self.args[2])
        self.tsi_long = btind.TrueStrengthIndicator(self.data.close, period1=self.args[3], period2=self.args[4],
                                                    pchange=self.args[5])
        self.cross = btind.CrossOver(self.tsi_short, self.tsi_long)

    def next(self):
        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.tsi_long[0] - self.tsi_short[0], self.logic) and self.tsi_long[
                    0] > 0
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.tsi_long[0] - self.tsi_short[0], self.logic) and self.tsi_long[
                    0] < 0
            else:  # 其他情况
                self.lines.goldencross[0] = compare(self.tsi_long[0] - self.tsi_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iTSILong(iBaseIndicator):
    '''
    因子：tsi多头
    传入参数：
    rule = {"args": ["26",'13',1,"40",'20',1,3],   #长周期,短周期,价格回看周期  , 长周期,短周期,价格回看周期 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,
            "position":{1(up),-1(down),0(any)},             # 1 0轴以上  -1 0轴以下 0 无
             }
            }
    '''
    lines = ('tsilong',)
    params = dict(rule=list())

    def __init__(self):
        super(iTSILong, self).__init__()
        self.tsi_short = btind.TrueStrengthIndicator(self.data.close, period1=self.args[0], period2=self.args[1],
                                                     pchange=self.args[2])
        self.tsi_long = btind.TrueStrengthIndicator(self.data.close, period1=self.args[3], period2=self.args[4],
                                                    pchange=self.args[5])

    def next(self):
        tsi_short = list(self.tsi_short.get(size=self.args[6]))  # 短线
        tsi_long = list(self.tsi_long.get(size=self.args[6]))  # 长线
        if len(tsi_short) == self.args[6]:
            tsilong = set(list(map(lambda d: d > 0, tsi_short + tsi_long)))
        else:
            tsilong = []
        if len(tsilong) == 1 and True in tsilong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.tsilong[0] = True and self.tsi_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.tsilong[0] = True and self.tsi_short[0] < 0
            else:  # 其他条件
                self.lines.tsilong[0] = True
        else:
            self.lines.tsilong[0] = False
        # print(self.tsi_short[0], self.tsi_long[0], ",", self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iTSIShort(iBaseIndicator):
    '''
    因子：tsi空头
    传入参数：
    rule = {"args": ["26",'13',1,"40",'20',1,3],   #长周期,短周期,价格回看周期  , 长周期,短周期,价格回看周期 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('tsishort',)
    params = dict(rule=list())

    def __init__(self):
        super(iTSIShort, self).__init__()
        self.tsi_short = btind.TrueStrengthIndicator(self.data.close, period1=self.args[0], period2=self.args[1],
                                                     pchange=self.args[2])
        self.tsi_long = btind.TrueStrengthIndicator(self.data.close, period1=self.args[3], period2=self.args[4],
                                                    pchange=self.args[5])

    def next(self):
        tsi_short = list(self.tsi_short.get(size=self.args[6]))  # 短线
        tsi_long = list(self.tsi_long.get(size=self.args[6]))  # 长线
        if len(tsi_short) == self.args[6]:
            tsishort = set(list(map(lambda d: d < 0, tsi_short + tsi_long)))
        else:
            tsishort = []
        if len(tsishort) == 1 and True in tsishort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.tsishort[0] = True and self.tsi_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.tsishort[0] = True and self.tsi_short[0] < 0
            else:  # 其他条件
                self.lines.tsishort[0] = True
        else:
            self.lines.tsishort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iTSITop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": ["26",'13',1,3],   #长周期,短周期,价格回看周期   连续N天
            "logic":{"position":{1(up),-1(down),0(any)},             # 1 0轴以上  -1 0轴以下 0 无
             }
            }
    '''
    lines = ('tsitop',)
    params = dict(rule=list())

    def __init__(self):
        super(iTSITop, self).__init__()
        self.tsi = btind.TrueStrengthIndicator(self.data.close, period1=self.args[0], period2=self.args[1],
                                               pchange=self.args[2])

    def next(self):
        _list = list(self.tsi.get(size=self.args[3]))
        if len(_list) == self.args[3] and self.tsi[0] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.tsitop[0] = True and self.tsi[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.tsitop[0] = True and self.tsi[0] < 0
            else:  # 其他条件
                self.lines.tsitop[0] = True
        else:
            self.lines.tsitop[0] = False
        # print(self.tsi[0], ",", self.data.datetime.datetime())


class iTSIBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
    rule = {"args": ["26",'13',1,3],   #长周期,短周期,价格回看周期   连续N天
            "logic":{"position":{1(up),-1(down),0(any)},             # 1 0轴以上  -1 0轴以下 0 无
             }
            }
    '''
    lines = ('tsibottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iTSIBottom, self).__init__()
        self.tsi = btind.TrueStrengthIndicator(self.data.close, period1=self.args[0], period2=self.args[1],
                                               pchange=self.args[2])

    def next(self):
        _list = list(self.tsi.get(size=self.args[3]))
        if len(_list) == self.args[3] and self.tsi[0] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.tsibottom[0] = True and self.tsi[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.tsibottom[0] = True and self.tsi[0] < 0
            else:  # 其他条件
                self.lines.tsibottom[0] = True
        else:
            self.lines.tsibottom[0] = False
        # print(self.tsi[0], ",", self.data.datetime.datetime())

