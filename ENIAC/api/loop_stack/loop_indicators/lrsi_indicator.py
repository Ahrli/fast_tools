import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iLrsiCompare(iBaseIndicator):
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
        super(iLrsiCompare, self).__init__()
        self.lrsi = btind.LaguerreFilter(self.data.close,period=self.args[0],gamma = self.logic['gamma'][0])


    def next(self):
        self.lines.rc[0] = compare(self.lrsi[0], self.logic)
        # print(self.lrsi[0], self.data.close[0],'*',self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iLrsiCrossGolden(iBaseIndicator):
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
        super(iLrsiCrossGolden, self).__init__()

        self.lrsi_short = btind.LaguerreRSI(self.data.close, period=self.args[0], gamma = self.logic['gamma'][0])
        self.lrsi_long = btind.LaguerreRSI(self.data.close, period=self.args[1], gamma = self.logic['gamma'][0])
        self.cross = btind.CrossOver(self.lrsi_short, self.lrsi_long)

    def next(self):
        if self.cross[0] == 1:
                self.lines.goldencross[0] = compare(self.lrsi_short[0] - self.lrsi_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iLrsiCrossDie(iBaseIndicator):
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
        super(iLrsiCrossDie, self).__init__()
        self.lrsi_short = btind.LaguerreRSI(self.data.close, period=self.args[0], gamma = self.logic['gamma'][0])
        self.lrsi_long = btind.LaguerreRSI(self.data.close, period=self.args[1], gamma = self.logic['gamma'][0])
        self.cross = btind.CrossOver(self.lrsi_short, self.lrsi_long)

    def next(self):
        if  self.cross[0] == -1:

                self.lines.diecross[0] = compare(self.lrsi_long[0] - self.lrsi_short[0], self.logic)
        else:
            self.lines.diecross[0] = False


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iLrsiLong(iBaseIndicator):
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
        super(iLrsiLong, self).__init__()
        self.lrsi_short = btind.LaguerreRSI(self.data.close, period=self.args[0], gamma = self.logic['gamma'][0])
        self.lrsi_long = btind.LaguerreRSI(self.data.close, period=self.args[1], gamma = self.logic['gamma'][0])

    def next(self):
        rsilong = set([self.data.close[i] > self.lrsi_short[i] > self.lrsi_long[i] for i in range(1 - self.args[2], 1)])
        if len(rsilong) == 1 and True in rsilong:

                self.lines.rsilong[0] = True
        else:
            self.lines.rsilong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iLrsiShort(iBaseIndicator):
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
        super(iLrsiShort, self).__init__()
        self.lrsi_short = btind.LaguerreRSI(self.data.close, period=self.args[0], gamma = self.logic['gamma'][0])
        self.lrsi_long = btind.LaguerreRSI(self.data.close, period=self.args[1], gamma = self.logic['gamma'][0])

    def next(self):
        rsishort = set([self.data.close[i] < self.lrsi_short[i] < self.lrsi_long[i] for i in range(1 - self.args[2], 1)])
        if len(rsishort) == 1 and True in rsishort:

                self.lines.rsishort[0] = True
        else:
            self.lines.rsishort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iLrsiTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [5,3] ,
                "logic":{'gamma':[0.5]}}
    '''
    lines = ('rsitop',)
    params = dict(rule=list())

    def __init__(self):
        super(iLrsiTop, self).__init__()
        self.lrsi = btind.LaguerreRSI(self.data.close, period=self.args[0], gamma = self.logic['gamma'][0])

    def next(self):
        _list = list(self.lrsi.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == max(_list):

                self.lines.rsitop[0] = True
        else:
            self.lines.rsitop[0] = False


class iLrsiBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,3] ,
                "logic":{'gamma':[0.5]}}
    '''
    lines = ('rsibottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iLrsiBottom, self).__init__()
        self.lrsi = btind.LaguerreRSI(self.data.close, period=self.args[0], gamma = self.logic['gamma'][0])

    def next(self):
        _list = list(self.lrsi.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
                self.lines.rsibottom[0] = True
        else:
            self.lines.rsibottom[0] = False
