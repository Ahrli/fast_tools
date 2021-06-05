import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iZlindCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": [5,10],   # 周期, 增益
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('zlind',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlindCompare, self).__init__()
        self.zlind = btind.ZLIndicator(self.data.close, period=self.args[0],gainlimit=self.args[1])

    def next(self):
        self.lines.zlind[0] = compare(self.zlind[0], self.logic)


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iZlindCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [5,10, 10,50],   # 短周期, 短增益,长周期, 长增益
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iZlindCrossGolden, self).__init__()
        self.zlind_short = btind.ZLIndicator(self.data.close, period=self.args[0],gainlimit=self.args[1])
        self.zlind_long = btind.ZLIndicator(self.data.close, period=self.args[2],gainlimit=self.args[3])
        self.cross = btind.CrossOver(self.zlind_short, self.zlind_long)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.zlind_short[0]-self.zlind_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.zlind_short[0], self.zlind_long[0], "===", self.data.datetime.datetime())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iZlindCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args":[5,10, 10,50],   # 短周期, 短增益,长周期, 长增益
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iZlindCrossDie, self).__init__()
        self.zlind_short = btind.ZLIndicator(self.data.close, period=self.args[0], gainlimit=self.args[1])
        self.zlind_long = btind.ZLIndicator(self.data.close, period=self.args[2], gainlimit=self.args[3])
        self.cross = btind.CrossOver(self.zlind_short, self.zlind_long)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.zlind_long[0]-self.zlind_short[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iZlindLong(iBaseIndicator):
    '''
    因子：zlind多头
    传入参数：
    rule = {"args": [5,10, 10,50,3],   # 短周期, 短增益,长周期, 长增益, 连续N天
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('zlindlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlindLong, self).__init__()
        self.zlind_short = btind.ZLIndicator(self.data.close, period=self.args[0], gainlimit=self.args[1])
        self.zlind_long = btind.ZLIndicator(self.data.close, period=self.args[2], gainlimit=self.args[3])


    def next(self):
        zlindlong = set([self.data.close[i] > self.zlind_short[i] > self.zlind_long[i] for i in range(1-self.args[4],1)])
        if len(zlindlong) == 1 and True in zlindlong:
            self.lines.zlindlong[0] = True
        else:
            self.lines.zlindlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iZlindShort(iBaseIndicator):
    '''
    因子：zlind空头
    传入参数：
    rule = {"args": [5,10, 10,50,3],   # 短周期, 短增益,长周期, 长增益, 连续N天
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('zlindshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlindShort, self).__init__()
        self.zlind_short = btind.ZLIndicator(self.data.close, period=self.args[0], gainlimit=self.args[1])
        self.zlind_long = btind.ZLIndicator(self.data.close, period=self.args[2], gainlimit=self.args[3])


    def next(self):
        zlindshort = set([self.data.close[i] < self.zlind_short[i] < self.zlind_long[i] for i in range(1-self.args[4],1)])
        if len(zlindshort) == 1 and True in zlindshort:
            self.lines.zlindshort[0] = True
        else:
            self.lines.zlindshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iZlindTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
       rule = {"args": [5,10, 5],   # 周期, 增益, 连续N天
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('zlindtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlindTop, self).__init__()
        self.zlind = btind.ZLIndicator(self.data.close, period=self.args[0], gainlimit=self.args[1])

    def next(self):
        _list = list(self.zlind.get(size=self.args[2]))
        if len(_list) == self.args[1]  and self.zlind[0] == max(_list):
            self.lines.zlindtop[0] = True
        else:
            self.lines.zlindtop[0] = False




class iZlindBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
      rule = {"args": [5,10, 5],   # 周期, 增益, 连续N天
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('zlindbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iZlindBottom, self).__init__()
        self.zlind = btind.ZLIndicator(self.data.close, period=self.args[0],gainlimit=self.args[1])

    def next(self):
        _list = list(self.zlind.get(size=self.args[2]))
        if len(_list) == self.args[1] and self.zlind[0] == min(_list):
            self.lines.zlindbottom[0] = True
        else:
            self.lines.zlindbottom[0] = False