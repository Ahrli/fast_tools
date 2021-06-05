import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iMomentumOscCompare(iBaseIndicator):
    '''

    传入参数：
    rule = {"args": ["5"],      #ema周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('momosc',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumOscCompare, self).__init__()
        self.momosc = btind.MomentumOsc(self.data.close, period=self.args[0])

    def next(self):
        self.lines.momosc[0] = compare(self.momosc[0], self.logic)
        # print(self.momosc[0], self.data.close[0],'*',self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iMomentumOscCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumOscCrossGolden, self).__init__()
        self.momosc_short = btind.MomentumOsc(self.data.close, period=self.args[0])
        self.momosc_long = btind.MomentumOsc(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.momosc_short, self.momosc_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.momosc_short[0]-self.momosc_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iMomentumOscCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumOscCrossDie, self).__init__()
        self.momosc_short = btind.MomentumOsc(self.data.close, period=self.args[0])
        self.momosc_long = btind.MomentumOsc(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.momosc_short, self.momosc_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.momosc_long[0]-self.momosc_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iMomentumOscLong(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('momosclong',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumOscLong, self).__init__()
        self.momosc_short = btind.MomentumOsc(self.data.close, period=self.args[0])
        self.momosc_long = btind.MomentumOsc(self.data.close, period=self.args[1])

    def next(self):
        momosclong = set([ self.momosc_short[i] > self.momosc_long[i] for i in range(1-self.args[2],1)])
        if len(momosclong) == 1 and True in momosclong:
            self.lines.momosclong[0] = True
        else:
            self.lines.momosclong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iMomentumOscShort(iBaseIndicator):
    '''
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('momoscshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumOscShort, self).__init__()
        self.momosc_short = btind.MomentumOsc(self.data.close, period=self.args[0])
        self.momosc_long = btind.MomentumOsc(self.data.close, period=self.args[1])

    def next(self):
        momoscshort = set([self.momosc_short[i] < self.momosc_long[i] for i in range(1-self.args[2],1)])
        if len(momoscshort) == 1 and True in momoscshort:
            self.lines.momoscshort[0] = True
        else:
            self.lines.momoscshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iMomentumOscTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('momosctop',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumOscTop, self).__init__()
        self.momosc = btind.MomentumOsc(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.momosc.get(size=self.args[1]))
        if len(_list) == self.args[1]  and self.momosc[0] == max(_list):
            self.lines.momosctop[0] = True
        else:
            self.lines.momosctop[0] = False




class iMomentumOscBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('momoscbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iMomentumOscBottom, self).__init__()
        self.momosc = btind.MomentumOsc(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.momosc.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.momosc[0] == min(_list):
            self.lines.momoscbottom[0] = True
        else:
            self.lines.momoscbottom[0] = False