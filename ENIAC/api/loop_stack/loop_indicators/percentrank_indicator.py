import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iPctRankCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #ema周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较 值选择范围[0-1]
            }
    '''
    lines = ('pctrank',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctRankCompare, self).__init__()
        self.pctrank = btind.PercentRank(self.data.close, period=self.args[0])

    def next(self):
        self.lines.pctrank[0] = compare(self.pctrank[0], self.logic)
        # print(self.pctrank[0], self.data.close[0], self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iPctRankCrossGolden(iBaseIndicator):
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
        super(iPctRankCrossGolden, self).__init__()
        self.pctrank_short = btind.PercentRank(self.data.close, period=self.args[0])
        self.pctrank_long = btind.PercentRank(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.pctrank_short, self.pctrank_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.pctrank_short[0]-self.pctrank_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.pgo_short[0], self.pgo_long[0], self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iPctRankCrossDie(iBaseIndicator):
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
        super(iPctRankCrossDie, self).__init__()
        self.pctrank_short = btind.PercentRank(self.data.close, period=self.args[0])
        self.pctrank_long = btind.PercentRank(self.data.close, period=self.args[1])
        self.cross = btind.CrossOver(self.pctrank_short, self.pctrank_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.pctrank_long[0]-self.pctrank_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iPctRankLong(iBaseIndicator):
    '''
    rule = {"args": [5,30] # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('pctranklong',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctRankLong, self).__init__()
        self.pctrank_short = btind.PercentRank(self.data.close, period=self.args[0])
        self.pctrank_long = btind.PercentRank(self.data.close, period=self.args[1])

    def next(self):
        pctranklong = set([ self.pctrank_short[i] > self.pctrank_long[i] for i in range(1-self.args[2],1)])
        if len(pctranklong) == 1 and True in pctranklong:
            self.lines.pctranklong[0] = True
        else:
            self.lines.pctranklong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iPctRankShort(iBaseIndicator):
    '''
     rule = {"args": [5,30] # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('pctrankshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctRankShort, self).__init__()
        self.pctrank_short = btind.PercentRank(self.data.close, period=self.args[0])
        self.pctrank_long = btind.PercentRank(self.data.close, period=self.args[1])

    def next(self):
        pctrankshort = set([self.pctrank_short[i] < self.pctrank_long[i] for i in range(1-self.args[2],1)])
        if len(pctrankshort) == 1 and True in pctrankshort:
            self.lines.pctrankshort[0] = True
        else:
            self.lines.pctrankshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iPctRankTop(iBaseIndicator):
    '''
     rule = {"args": [5,30] # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('pctranktop',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctRankTop, self).__init__()
        self.pctrank = btind.PercentRank(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.pctrank.get(size=self.args[1]))
        if len(_list) == self.args[1]  and self.pctrank[0] == max(_list):
            self.lines.pctranktop[0] = True
        else:
            self.lines.pctranktop[0] = False




class iPctRankBottom(iBaseIndicator):
    '''
    rule = {"args": [5,30] # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('pctrankbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iPctRankBottom, self).__init__()
        self.pctrank = btind.PercentRank(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.pctrank.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.pctrank[0] == min(_list):
            self.lines.pctrankbottom[0] = True
        else:
            self.lines.pctrankbottom[0] = False



class PctRankHigh(iBaseIndicator):
    '''
     rule = {"args": [5,30] # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('ehigh',)
    params = dict(rule=list())

    def __init__(self):
        super(PctRankHigh, self).__init__()
        self.pctrank = btind.PercentRank(self.data.close, period=self.args[0])

    def next(self):
        _list = [(i) for i in list(self.pctrank.get(size=self.args[1]))]
        _list.sort()

        if len(_list) == self.args[1]:
            _list = (list(map(lambda d: compare(d, self.logic), _list)))
            _list = [ i for i in _list if i is True ]

        else:
            _list = []
        if len(_list) == self.args[1]:
                self.lines.ehigh[0] = True
        else:
            self.lines.ehigh[0] = False
        # print(self.pctrank[0], self.data.close[0], self.data.datetime.date())
