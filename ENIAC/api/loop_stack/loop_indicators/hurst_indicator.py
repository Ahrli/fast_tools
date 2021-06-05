import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iHurstCompare(iBaseIndicator):
    '''
    因子：相对强弱指数比较数值
    传入参数：
    rule = {"args": ["5"],    #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('hurst',)
    params = dict(rule=list())

    def __init__(self):
        super(iHurstCompare, self).__init__()
        self.hurst = btind.HurstExponent(self.data.close, period=self.args[0] )

    def next(self):
        self.lines.hurst[0] = compare(self.hurst[0], self.logic)
        # print(self.hurst[0], self.data.close[0], '*', self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iHurstCrossGolden(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": ["5", "10", ],    #短均线周期, 长均线周期，低位点
                       "logic":{"compare": "eq","byValue": 1,"byMax": 5,"position": 0},  # 金叉情况比较大小， 短比长高多少 位置
                    }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iHurstCrossGolden, self).__init__()
        self.hurst_short = btind.HurstExponent(self.data.close, period=self.args[0] )
        self.hurst_long = btind.HurstExponent(self.data.close, period=self.args[1] )
        self.cross = btind.CrossOver(self.hurst_short, self.hurst_long)

    def next(self):
        if  self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.hurst_short[0] - self.hurst_long[0], self.logic) and \
                                            self.hurst_short[0] > 0
            elif self.logic["position"] == -1:  # 出现部  < 0
                self.lines.goldencross[0] = compare(self.hurst_short[0] - self.hurst_long[0], self.logic) and \
                                            self.hurst_short[0] < 0
            else:
                self.lines.goldencross[0] = compare(self.hurst_short[0] - self.hurst_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iHurstCrossDie(iBaseIndicator):
    '''
    因子：死叉：短期RSI线在高位向下突破长期RSI线, 一般为RSI指标的“死亡交叉”
    传入参数：
     rule = {"args": ["5", "10", ],    #短均线周期, 长均线周期，低位点
                       "logic":{"compare": "eq","byValue": 1,"byMax": 5,"position": 0},  # 金叉情况比较大小， 短比长高多少 位置
                    }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iHurstCrossDie, self).__init__()
        self.hurst_short = btind.HurstExponent(self.data.close, period=self.args[0] )
        self.hurst_long = btind.HurstExponent(self.data.close, period=self.args[1] )
        self.cross = btind.CrossOver(self.hurst_short, self.hurst_long)

    def next(self):
        if  self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.hurst_long[0] - self.hurst_short[0], self.logic) and self.hurst_short[
                    0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.diecross[0] = compare(self.hurst_long[0] - self.hurst_short[0], self.logic) and self.hurst_short[
                    0] < 0
            else:
                self.lines.diecross[0] = compare(self.hurst_long[0] - self.hurst_short[0], self.logic)
        else:
            self.lines.diecross[0] = False


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iHurstLong(iBaseIndicator):
    '''
    因子：rsi多头,收盘价 > 短线rsi > 长线rsi
    传入参数：
    # rule = {"args": ["5", "10", "30", "50", "70", "100", "3"],    #短均线周期, 长均线周期，"极弱区", "弱区", "强区", "极强区", "连续多少天多头"
    rule = {"args": ["5", "10", "3"],    #短均线周期, 长均线周期, "连续多少天多头"
            "logic":{"position": 0},  ]
            }
    '''
    lines = ('hurstlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iHurstLong, self).__init__()
        self.hurst_short = btind.HurstExponent(self.data.close, period=self.args[0] )
        self.hurst_long = btind.HurstExponent(self.data.close, period=self.args[1] )

    def next(self):
        hurstlong = set([ self.hurst_short[i] > self.hurst_long[i] for i in range(1 - self.args[2], 1)])
        if len(hurstlong) == 1 and True in hurstlong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.hurstlong[0] = True and self.hurst_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.hurstlong[0] = True and self.hurst_short[0] < 0
            else:
                self.lines.hurstlong[0] = True
        else:
            self.lines.hurstlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iHurstShort(iBaseIndicator):
    '''
    因子：rsi多头,收盘价 > 短线rsi > 长线rsi
    传入参数：
    rule = {"args": ["5", "10", "3"],    #短均线周期, 长均线周期 "连续多少天空头"
            "logic":{"position": 0}
            }
    '''
    lines = ('hurstshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iHurstShort, self).__init__()
        self.hurst_short = btind.HurstExponent(self.data.close, period=self.args[0] )
        self.hurst_long = btind.HurstExponent(self.data.close, period=self.args[1] )

    def next(self):
        hurstshort = set([self.hurst_short[i] < self.hurst_long[i] for i in range(1 - self.args[2], 1)])
        if len(hurstshort) == 1 and True in hurstshort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.hurstshort[0] = True and self.hurst_short[0] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.hurstshort[0] = True and self.hurst_short[0] < 0
            else:
                self.lines.hurstshort[0] = True
        else:
            self.lines.hurstshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iHurstTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"position": 0}
    '''
    lines = ('hursttop',)
    params = dict(rule=list())

    def __init__(self):
        super(iHurstTop, self).__init__()
        self.hurst = btind.HurstExponent(self.data.close, period=self.args[0] )

    def next(self):
        _list = list(self.hurst.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.hursttop[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.hursttop[0] = True and _list[-1] < 0
            else:
                self.lines.hursttop[0] = True
        else:
            self.lines.hursttop[0] = False


class iHurstBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"position": 0}
    '''
    lines = ('hurstbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iHurstBottom, self).__init__()
        self.hurst = btind.HurstExponent(self.data.close, period=self.args[0] )

    def next(self):
        _list = list(self.hurst.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.hurstbottom[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.hurstbottom[0] = True and _list[-1] < 0
            else:
                self.lines.hurstbottom[0] = True
        else:
            self.lines.hurstbottom[0] = False
