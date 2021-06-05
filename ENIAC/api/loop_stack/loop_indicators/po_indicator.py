import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator

class iPoCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": [12,26],      #sma周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    #lines = ('mc', 'ma')
    lines = ('mc', )
    params = dict(rule=list())

    def __init__(self):
        super(iPoCompare, self).__init__()
        self.po = btind.PriceOscillator(self.data.close, period1=self.args[0],period2=self.args[1])

    def next(self):
        self.lines.mc[0] = compare(self.po[0], self.logic)
        # print(self.po[0], self.data.close[0],'*',self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iPoCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    #lines = ('goldencross', 'short', 'long')
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iPoCrossGolden, self).__init__()
        self.po_short = btind.PriceOscillator(self.data.close, period1=self.args[0],period2=self.args[1])
        self.po_long = btind.PriceOscillator(self.data.close, period1=self.args[2],period2=self.args[3])
        self.cross = btind.CrossOver(self.po_short, self.po_long)

    def next(self):
        #self.lines.long[0] = self.po_long[0]
        #self.lines.short[0] = self.po_short[0]
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.po_short[0]-self.po_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iPoCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    # lines = ('dipoross', 'short', 'long')
    lines = ('dipoross', )
    params = dict(rule=list())

    def __init__(self):
        super(iPoCrossDie, self).__init__()
        self.po_short = btind.PriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1])
        self.po_long = btind.PriceOscillator(self.data.close, period1=self.args[2], period2=self.args[3])
        self.cross = btind.CrossOver(self.po_short, self.po_long)

    def next(self):
        #self.lines.long[0] = self.po_long[0]
        #self.lines.short[0] = self.po_short[0]
        if self.cross[0] == -1:
            self.lines.dipoross[0] = compare(self.po_long[0]-self.po_short[0], self.logic)
        else:
            self.lines.dipoross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iPoLong(iBaseIndicator):
    '''
    因子：ma多头
    传入参数：
    rule = {"args": [12,26, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    #lines = ('polong', 'short', 'long')
    lines = ('polong',)
    params = dict(rule=list())

    def __init__(self):
        super(iPoLong, self).__init__()
        self.logic = self.p.rule['logic']

        self.po_short = btind.PriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1])
        self.po_long = btind.PriceOscillator(self.data.close, period1=self.args[2], period2=self.args[3])
    def next(self):

        polong = set([self.po_short[i] > self.po_long[i] for i in range(1-self.args[4],1)])
        if len(polong) == 1 and True in polong:
            self.lines.polong[0] = True
        else:
            self.lines.polong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iPoShort(iBaseIndicator):
    '''
    因子：ma空头
    传入参数：
        rule = {"args": [12,26, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    #lines = ('poshort', 'short', 'long')
    lines = ('poshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iPoShort, self).__init__()
        self.po_short = btind.PriceOscillator(self.data.close, period1=self.args[0], period2=self.args[1])
        self.po_long = btind.PriceOscillator(self.data.close, period1=self.args[2], period2=self.args[3])
    def next(self):

        poshort = set([self.po_short[i] < self.po_long[i] for i in range(1 - self.args[4], 1)])
        if len(poshort) == 1 and True in poshort:
            self.lines.poshort[0] = True
        else:
            self.lines.poshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iPoTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        参数：
        rule = {"args": [12,26,3] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('potop',)
    params = dict(rule=list())

    def __init__(self):
        super(iPoTop, self).__init__()
        self.po = btind.PriceOscillator(self.data.close, period1=self.args[0],period2=self.args[1])

    def next(self):
        _list = list(self.po.get(size=self.args[2]))
        if len(_list) == self.args[2]  and _list[-1] == max(_list):
            self.lines.potop[0] = True
        else:
            self.lines.potop[0] = False




class iPoBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [12,26,3] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('pobottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iPoBottom, self).__init__()
        self.po = btind.PriceOscillator(self.data.close, period1=self.args[0],period2=self.args[1])

    def next(self):
        _list = list(self.po.get(size=self.args[2]))
        if len(_list) == self.args[2] and _list[-1] == min(_list):
            self.lines.pobottom[0] = True
        else:
            self.lines.pobottom[0] = False