import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iKamaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": [10,2,30],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('kama',)
    params = dict(rule=list())

    def __init__(self):
        super(iKamaCompare, self).__init__()
        self.kama = btind.AdaptiveMovingAverage(self.data.close, period=self.args[0],fast=self.args[1],slow=self.args[2])

    def next(self):
        self.lines.kama[0] = compare(self.kama[0], self.logic)
        # print(self.kama[0], self.data.close[0],'*',self.data.datetime.date())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iKamaCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
   rule = {"args": [10,2,30,30,10,10,10,15],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iKamaCrossGolden, self).__init__()
        self.kama_short =btind.AdaptiveMovingAverage(self.data.close, period=self.args[0],fast=self.args[1],slow=self.args[2])
        self.kama_long =btind.AdaptiveMovingAverage(self.data.close, period=self.args[3],fast=self.args[4],slow=self.args[5])
        self.cross = btind.CrossOver(self.kama_short, self.kama_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.kama_short[0]-self.kama_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iKamaCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [10,2,30,30,10,10,10,15],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iKamaCrossDie, self).__init__()
        self.kama_short = btind.AdaptiveMovingAverage(self.data.close, period=self.args[0], fast=self.args[1],
                                                      slow=self.args[2])
        self.kama_long = btind.AdaptiveMovingAverage(self.data.close, period=self.args[3], fast=self.args[4],
                                                     slow=self.args[5])
        self.cross = btind.CrossOver(self.kama_short, self.kama_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.kama_long[0]-self.kama_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iKamaLong(iBaseIndicator):
    '''
    因子：ema多头
    传入参数：
     rule = {"args": [10,2,30,30,10,10,10,15,3],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('kamalong',)
    params = dict(rule=list())

    def __init__(self):
        super(iKamaLong, self).__init__()
        self.kama_short = btind.AdaptiveMovingAverage(self.data.close, period=self.args[0], fast=self.args[1],
                                                      slow=self.args[2])
        self.kama_long = btind.AdaptiveMovingAverage(self.data.close, period=self.args[3], fast=self.args[4],
                                                     slow=self.args[5])

    def next(self):
        kamalong = set([self.data.close[i] > self.kama_short[i] > self.kama_long[i] for i in range(1-self.args[6],1)])
        if len(kamalong) == 1 and True in kamalong:
            self.lines.kamalong[0] = True
        else:
            self.lines.kamalong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iKamaShort(iBaseIndicator):
    '''
    因子：ema空头
    传入参数：
     rule = {"args": [10,2,30,30,10,10,10,15,3],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('kamashort',)
    params = dict(rule=list())

    def __init__(self):
        super(iKamaShort, self).__init__()
        self.kama_short = btind.AdaptiveMovingAverage(self.data.close, period=self.args[0], fast=self.args[1],
                                                      slow=self.args[2])
        self.kama_long = btind.AdaptiveMovingAverage(self.data.close, period=self.args[3], fast=self.args[4],
                                                     slow=self.args[5])

    def next(self):
        kamashort = set([self.data.close[i] < self.kama_short[i] < self.kama_long[i] for i in range(1-self.args[6],1)])
        if len(kamashort) == 1 and True in kamashort:
            self.lines.kamashort[0] = True
        else:
            self.lines.kamashort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iKamaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [10,2,30,3] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('kamatop',)
    params = dict(rule=list())

    def __init__(self):
        super(iKamaTop, self).__init__()
        self.kama = btind.AdaptiveMovingAverage(self.data.close, period=self.args[0], fast=self.args[1],
                                                      slow=self.args[2])

    def next(self):
        _list = list(self.kama.get(size=self.args[3]))
        if len(_list) == self.args[1]  and self.kama[0] == max(_list):
            self.lines.kamatop[0] = True
        else:
            self.lines.kamatop[0] = False




class iKamaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [10,2,30,3] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('kamabottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iKamaBottom, self).__init__()
        self.kama =  btind.AdaptiveMovingAverage(self.data.close, period=self.args[0], fast=self.args[1],
                                                      slow=self.args[2])

    def next(self):
        _list = list(self.kama.get(size=self.args[3]))
        if len(_list) == self.args[1] and self.kama[0] == min(_list):
            self.lines.kamabottom[0] = True
        else:
            self.lines.kamabottom[0] = False