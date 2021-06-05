import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iRsiCompare(iBaseIndicator):
    '''
    因子：相对强弱指数比较数值
    传入参数：
    # rule = {"args": ["5", "30", "50", "70", "100"],    #rsi周期,"极弱区", "弱区", "强区", "极强区"
    rule = {"args": ["5"],    #rsi周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('rc',)
    params = dict(rule=list())

    def __init__(self):
        super(iRsiCompare, self).__init__()
        # self.rsi = btind.RSI(self.data.close, period=self.args[0], lowerband=self.args[1],
        #                      safelow=self.args[2], upperband=self.args[3], safehigh=self.args[4])
        self.rsi = btind.RSI(self.data.close, period=self.args[0], safediv=True)

    def next(self):
        self.lines.rc[0] = compare(self.rsi[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iRsiCrossGolden(iBaseIndicator):
    '''
    因子：短期RSI线在低位向上突破长期RSI线时，一般为RSI指标的“黄金交叉”
    传入参数：
    rule = {"args": ["5", "10", "30"],    #短均线周期, 长均线周期，低位点
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iRsiCrossGolden, self).__init__()
        self.rsi_short = btind.RSI(self.data.close, period=self.args[0], safediv=True)
        self.rsi_long = btind.RSI(self.data.close, period=self.args[1], safediv=True)
        self.cross = btind.CrossOver(self.rsi_short, self.rsi_long)

    def next(self):
        if self.rsi_short[0] < self.args[2] and self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.rsi_short[0] - self.rsi_long[0], self.logic) and \
                                            self.rsi_short[0] > 70
            elif self.logic["position"] == -1:  # 出现部  < 0
                self.lines.goldencross[0] = compare(self.rsi_short[0] - self.rsi_long[0], self.logic) and \
                                            self.rsi_short[0] < 30
            else:
                self.lines.goldencross[0] = compare(self.rsi_short[0] - self.rsi_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iRsiCrossDie(iBaseIndicator):
    '''
    因子：死叉：短期RSI线在高位向下突破长期RSI线, 一般为RSI指标的“死亡交叉”
    传入参数：
    rule = {"args": ["5", "10", "70"],    #短均线周期, 长均线周期，高位点
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iRsiCrossDie, self).__init__()
        self.rsi_short = btind.RSI(self.data.close, period=self.args[0], safediv=True)
        self.rsi_long = btind.RSI(self.data.close, period=self.args[1], safediv=True)
        self.cross = btind.CrossOver(self.rsi_short, self.rsi_long)

    def next(self):
        if self.rsi_short[0] > self.args[2] and self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.rsi_long[0] - self.rsi_short[0], self.logic) and self.rsi_short[
                    0] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.diecross[0] = compare(self.rsi_long[0] - self.rsi_short[0], self.logic) and self.rsi_short[
                    0] < 30
            else:
                self.lines.diecross[0] = compare(self.rsi_long[0] - self.rsi_short[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iRsiLong(iBaseIndicator):
    '''
    因子：rsi多头,收盘价 > 短线rsi > 长线rsi
    传入参数：
    # rule = {"args": ["5", "10", "30", "50", "70", "100", "3"],    #短均线周期, 长均线周期，"极弱区", "弱区", "强区", "极强区", "连续多少天多头"
    rule = {"args": ["5", "10", "3"],    #短均线周期, 长均线周期, "连续多少天多头"
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('rsilong',)
    params = dict(rule=list())

    def __init__(self):
        super(iRsiLong, self).__init__()
        self.rsi_short = btind.RSI(self.data.close, period=self.args[0], safediv=True)
        self.rsi_long = btind.RSI(self.data.close, period=self.args[1], safediv=True)

    def next(self):
        rsilong = set([self.rsi_short[i] > self.rsi_long[i] for i in range(1 - self.args[2], 1)])
        if len(rsilong) == 1 and True in rsilong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.rsilong[0] = True and self.rsi_short[0] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.rsilong[0] = True and self.rsi_short[0] < 30
            else:
                self.lines.rsilong[0] = True
        else:
            self.lines.rsilong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iRsiShort(iBaseIndicator):
    '''
    因子：rsi多头,收盘价 > 短线rsi > 长线rsi
    传入参数：
    # rule = {"args": ["5", "10", "30", "50", "70", "100", "3"],    #短均线周期, 长均线周期，"极弱区", "弱区", "强区", "极强区", "连续多少天多头"
    rule = {"args": ["5", "10", "3"],    #短均线周期, 长均线周期 "连续多少天空头"
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('rsishort',)
    params = dict(rule=list())

    def __init__(self):
        super(iRsiShort, self).__init__()
        self.rsi_short = btind.RSI(self.data.close, period=self.args[0], safediv=True)
        self.rsi_long = btind.RSI(self.data.close, period=self.args[1], safediv=True)

    def next(self):
        rsishort = set([self.rsi_short[i] < self.rsi_long[i] for i in range(1 - self.args[2], 1)])
        if len(rsishort) == 1 and True in rsishort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.rsishort[0] = True and self.rsi_short[0] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.rsishort[0] = True and self.rsi_short[0] < 30
            else:
                self.lines.rsishort[0] = True
        else:
            self.lines.rsishort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iRsiTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('rsitop',)
    params = dict(rule=list())

    def __init__(self):
        super(iRsiTop, self).__init__()
        self.rsi = btind.RSI(self.data.close, period=self.args[0], safediv=True)

    def next(self):
        _list = list(self.rsi.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.rsitop[0] = True and _list[-1] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.rsitop[0] = True and _list[-1] < 30
            else:
                self.lines.rsitop[0] = True
        else:
            self.lines.rsitop[0] = False


class iRsiBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('rsibottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iRsiBottom, self).__init__()
        self.rsi = btind.RSI(self.data.close, period=self.args[0], safediv=True)

    def next(self):
        _list = list(self.rsi.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.rsibottom[0] = True and _list[-1] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.rsibottom[0] = True and _list[-1] < 30
            else:
                self.lines.rsibottom[0] = True
        else:
            self.lines.rsibottom[0] = False
