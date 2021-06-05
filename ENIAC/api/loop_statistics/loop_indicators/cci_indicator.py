import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iCciCompare(iBaseIndicator):
    '''
    因子：相对强弱指数比较数值
    传入参数：
    # rule = {"args": ["5", "30", "50", "70", "100"],    #rsi周期,"极弱区", "弱区", "强区", "极强区"
    rule = {"args": ["5"],    #rsi周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('cc',)
    params = dict(rule=list())

    def __init__(self):
        super(iCciCompare, self).__init__()
        # self.rsi = btind.RSI(self.data.close, period=self.args[0], lowerband=self.args[1],
        #                      safelow=self.args[2], upperband=self.args[3], safehigh=self.args[4])
        self.cci = btind.CommodityChannelIndex(self.data.close, period=self.args[0])

    def next(self):
        self.lines.cc[0] = compare(self.cci[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iCciCrossGolden(iBaseIndicator):
    '''
    因子：短期RSI线在低位向上突破长期RSI线时，一般为RSI指标的“黄金交叉”
    传入参数：
    rule = {"args": ["5", "10", "30"],    #短均线周期, 长均线周期，低位点
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    lines = ('ccigoldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iCciCrossGolden, self).__init__()
        self.cci_short = btind.CommodityChannelIndex(self.data.close, period=self.args[0])
        self.cci_long = btind.CommodityChannelIndex(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.cci_short, self.cci_long)

    def next(self):
        if self.cci_short[0] < self.args[2] and self.cross[0] == 1:
            self.lines.ccigoldencross[0] = compare(self.cci_short[0]-self.cci_long[0], self.logic)
        else:
            self.lines.ccigoldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iCciCrossDie(iBaseIndicator):
    '''
    因子：死叉：短期RSI线在高位向下突破长期RSI线, 一般为RSI指标的“死亡交叉”
    传入参数：
    rule = {"args": ["5", "10", "70"],    #短均线周期, 长均线周期，高位点
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    lines = ('ccidiecross', )
    params = dict(rule=list())

    def __init__(self):
        super(iCciCrossDie, self).__init__()
        self.cci_short = btind.CommodityChannelIndex(self.data.close, period=self.args[0],)
        self.cci_long = btind.CommodityChannelIndex(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.cci_short, self.cci_long)

    def next(self):
        if self.cci_short[0] > self.args[2] and self.cross[0] == -1:
            self.lines.ccidiecross[0] = compare(self.cci_long[0]-self.cci_short[0], self.logic)
        else:
            self.lines.ccidiecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iCciLong(iBaseIndicator):
    '''
    因子：rsi多头,收盘价 > 短线rsi > 长线rsi
    传入参数：
    # rule = {"args": ["5", "10", "30", "50", "70", "100", "3"],    #短均线周期, 长均线周期，"极弱区", "弱区", "强区", "极强区", "连续多少天多头"
    rule = {"args": ["5", "10", "3"],    #短均线周期, 长均线周期, "连续多少天多头"
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('ccilong',)
    params = dict(rule=list())

    def __init__(self):
        super(iCciLong, self).__init__()
        self.cci_short = btind.CommodityChannelIndex(self.data.close, period=self.args[0])
        self.cci_long = btind.CommodityChannelIndex(self.data.close, period=self.args[1])

    def next(self):
        ccilong = set([self.data.close[i] > self.cci_short[i] > self.cci_long[i] for i in range(1-self.args[2],1)])
        if len(ccilong) == 1 and True in ccilong:
            self.lines.ccilong[0] = True
        else:
            self.lines.ccilong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iCciShort(iBaseIndicator):
    '''
    因子：rsi多头,收盘价 > 短线rsi > 长线rsi
    传入参数：
    # rule = {"args": ["5", "10", "30", "50", "70", "100", "3"],    #短均线周期, 长均线周期，"极弱区", "弱区", "强区", "极强区", "连续多少天多头"
    rule = {"args": ["5", "10", "3"],    #短均线周期, 长均线周期 "连续多少天空头"
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('ccishort',)
    params = dict(rule=list())

    def __init__(self):
        super(iCciShort, self).__init__()
        self.cci_short = btind.CommodityChannelIndex(self.data.close, period=self.args[0])
        self.cci_long = btind.CommodityChannelIndex(self.data.close, period=self.args[1])

    def next(self):
        ccishort = set([self.data.close[i] < self.cci_short[i] < self.cci_long[i] for i in range(1-self.args[2],1)])
        if len(ccishort) == 1 and True in ccishort:
            self.lines.ccishort[0] = True
        else:
            self.lines.ccishort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iCciTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('ctop',)
    params = dict(rule=list())

    def __init__(self):
        super(iCciTop, self).__init__()
        self.cci = btind.CommodityChannelIndex(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.cci.get(size=self.args[1]))

        if len(_list) == self.args[1] and self.cci[0] == max(_list):
            self.lines.ctop[0] = True
        else:
            self.lines.ctop[0] = False




class iCciBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('cbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iCciBottom, self).__init__()
        self.cci = btind.CommodityChannelIndex(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.cci.get(size=self.args[1]))

        if len(_list) == self.args[1] and self.cci[0] == min(_list):
            self.lines.cbottom[0] = True
        else:
            self.lines.cbottom[0] = False