import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator

class iHaDeltaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('haD', )
    params = dict(rule=list())

    def __init__(self):
        super(iHaDeltaCompare, self).__init__()
        self.haD = btind.haDelta( period=self.args[0])


    def next(self):
        self.lines.haD[0] = compare(self.haD.smoothed[0], self.logic)
        #print(self.haD.smoothed[0],self.haD.haDelta[0], self.data.close[0],'*',self.data.datetime.date())


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iHaDeltaCrossGolden(iBaseIndicator):
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
        super(iHaDeltaCrossGolden, self).__init__()
        self.haD_short = btind.haDelta( period=self.args[0])
        self.haD_long = btind.haDelta( period=self.args[1])
        self.cross = btind.CrossOver(self.haD_short.smoothed, self.haD_long.smoothed)

    def next(self):
        #self.lines.long[0] = self.haD_long[0]
        #self.lines.short[0] = self.haD_short[0]
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.haD_short.smoothed[0] - self.haD_long.smoothed[0], self.logic) and self.haD_short.smoothed[0]>0

            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.haD_short.smoothed[0] - self.haD_long.smoothed[0], self.logic) and self.haD_short.smoothed[0]<0

            else:
                self.lines.goldencross[0] = compare(self.haD_short.smoothed[0]-self.haD_long.smoothed[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iHaDeltaCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    # lines = ('diecross', 'short', 'long')
    lines = ('diecross', )
    params = dict(rule=list())

    def __init__(self):
        super(iHaDeltaCrossDie, self).__init__()
        self.haD_short = btind.haDelta( period=self.args[0])
        self.haD_long = btind.haDelta( period=self.args[1])
        self.cross = btind.CrossOver(self.haD_short.smoothed, self.haD_long.smoothed)

    def next(self):

        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.haD_long.smoothed[0]-self.haD_short.smoothed[0], self.logic) and self.haD_short.smoothed[0]>0

            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.diecross[0] = compare(self.haD_long.smoothed[0]-self.haD_short.smoothed[0], self.logic) and self.haD_short.smoothed[0]<0

            else:

                self.lines.diecross[0] = compare(self.haD_long.smoothed[0]-self.haD_short.smoothed[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iHaDeltaLong(iBaseIndicator):
    '''
    因子：ma多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    #lines = ('haDlong', 'short', 'long')
    lines = ('haDlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iHaDeltaLong, self).__init__()
        self.logic = self.p.rule['logic']
        self.haD_short = btind.haDelta( period=self.args[0])
        self.haD_long = btind.haDelta( period=self.args[1])

    def next(self):
        print(list(self.haD_short.smoothed))
        haDlong = set([self.haD_short.smoothed[i] > self.haD_long.smoothed[i] for i in range(1-self.args[2],1)])
        if len(haDlong) == 1 and True in haDlong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.haDlong[0] = True and self.haD_short.smoothed[0]>0

            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.haDlong[0] = True and self.haD_short.smoothed[0]<0

            else:

                self.lines.haDlong[0] = True
        else:
            self.lines.haDlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iHaDeltaShort(iBaseIndicator):
    '''
    因子：ma空头
    传入参数：
        rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('haDshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iHaDeltaShort, self).__init__()
        self.haD_short = btind.haDelta( period=self.args[0])
        self.haD_long = btind.haDelta( period=self.args[1])

    def next(self):

        haDshort = set([ self.haD_short.smoothed[i] < self.haD_long.smoothed[i] for i in range(1 - self.args[2], 1)])
        if len(haDshort) == 1 and True in haDshort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.haDshort[0] = True and self.haD_short.smoothed[0]>0

            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.haDshort[0] = True and self.haD_short.smoothed[0]<0
            else:
                self.lines.haDshort[0] = True
        else:
            self.lines.haDshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iHaDeltaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('haDtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iHaDeltaTop, self).__init__()
        self.haD = btind.haDelta( period=self.args[0])

    def next(self):
        _list = list(self.haD.smoothed.get(size=self.args[1]))
        if len(_list) == self.args[1]  and _list[-1] == max(_list):
            self.lines.haDtop[0] = True
        else:
            self.lines.haDtop[0] = False




class iHaDeltaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
      rule = {"args": [30,10] ,  # 第一个参数是因子的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('haDbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iHaDeltaBottom, self).__init__()
        self.haD = btind.haDelta(self.data.close, period=self.args[0])

    def next(self):
        _list = list(self.haD.smoothed.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            self.lines.haDbottom[0] = True
        else:
            self.lines.haDbottom[0] = False