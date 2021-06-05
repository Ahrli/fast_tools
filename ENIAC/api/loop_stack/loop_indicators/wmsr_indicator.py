import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iWMSRCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #wmsr周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('wmsr',)
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRCompare, self).__init__()
        self.wmsr = btind.WilliamsR( period=self.args[0])


    def next(self):
        self.lines.wmsr[0] = compare(abs(self.wmsr[0]), self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iWMSRCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
             "position":[1(up),-1(down),0(any)], # 1大于 -1 小于 0任何
            "positionValue": 80
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRCrossGolden, self).__init__()
        self.wmsr_short = btind.WilliamsR( period=self.args[0])
        self.wmsr_long = btind.WilliamsR( period=self.args[1])
        self.cross = btind.CrossOver(self.wmsr_short, self.wmsr_long)

    def next(self):
        # self.cross -1 是金叉
        if self.cross[0] == -1:
            if self.logic["position"] == 1: # 大于某个值
                self.lines.goldencross[0] = compare(abs(self.wmsr_short[0])-abs(self.wmsr_long[0]), self.logic)
            elif self.logic["position"] == -1:  # 小于某个值
                self.lines.goldencross[0] = compare(abs(self.wmsr_short[0]) - abs(self.wmsr_long[0]),self.logic)
            else:
                self.lines.goldencross[0] = compare(abs(self.wmsr_short[0]) - abs(self.wmsr_long[0]),self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iWMSRCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,  # 金叉情况比较大小， 短比长高多少
             "position":[1(up),-1(down),0(any)], # 1大于 -1 小于 0任何
            "positionValue": 80                  # [0-100] 区间包含0,100
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRCrossDie, self).__init__()
        self.wmsr_short = btind.WilliamsR( period=self.args[0])
        self.wmsr_long = btind.WilliamsR( period=self.args[1])
        self.cross = btind.CrossOver(self.wmsr_short, self.wmsr_long)

    def next(self):
        if self.cross[0] == 1:
            if self.logic["position"] == 1: # 大于某个值
                self.lines.goldencross[0] = compare(abs(self.wmsr_long[0])-abs(self.wmsr_short[0]), self.logic)
            elif self.logic["position"] == -1:  # 小于某个值
                self.lines.goldencross[0] = compare(abs(self.wmsr_long[0])-abs(self.wmsr_short[0]), self.logic)
            else:
                self.lines.goldencross[0] = compare(abs(self.wmsr_long[0])-abs(self.wmsr_short[0]), self.logic)

        else:
            self.lines.goldencross[0] = False
        # print(self.cross[0], abs(self.wmsr_short[0]), abs(self.wmsr_long[0]), self.data.datetime.datetime(),
        #       '=====' * 3)  # 打印当前的信号值

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iWMSRLong(iBaseIndicator):
    '''
    因子：wmsr多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('wmsrlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRLong, self).__init__()
        self.wmsr_short = btind.WilliamsR( period=self.args[0])
        self.wmsr_long = btind.WilliamsR( period=self.args[1])

    def next(self):
        wmsrlong = set([ self.wmsr_short[i] > self.wmsr_long[i] for i in range(1-self.args[2],1)])
        if len(wmsrlong) == 1 and True in wmsrlong:
            self.lines.wmsrlong[0] = True
        else:
            self.lines.wmsrlong[0] = False



    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iWMSRShort(iBaseIndicator):
    '''
    因子：wmsr空头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('wmsrshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRShort, self).__init__()
        self.wmsr_short = btind.WilliamsR( period=self.args[0])
        self.wmsr_long = btind.WilliamsR(period=self.args[1])

    def next(self):
        wmsrshort = set([ self.wmsr_short[i] < self.wmsr_long[i] for i in range(1-self.args[2],1)])
        if len(wmsrshort) == 1 and True in wmsrshort:
            self.lines.wmsrshort[0] = True
        else:
            self.lines.wmsrshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iWMSRTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [6,3] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('wmsrtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRTop, self).__init__()
        self.wmsr = btind.WilliamsR( period=self.args[0])

    def next(self):
        _list = list(self.wmsr.get(size=self.args[1]))
        if len(_list) == self.args[1]  and self.wmsr[0] == min(_list):
            self.lines.wmsrtop[0] = True
        else:
            self.lines.wmsrtop[0] = False




class iWMSRBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('wmsrbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRBottom, self).__init__()
        self.wmsr = btind.WilliamsR( period=self.args[0])

    def next(self):
        _list = list(self.wmsr.get(size=self.args[1]))
        if len(_list) == self.args[1] and self.wmsr[0] == max(_list):
            self.lines.wmsrbottom[0] = True
        else:
            self.lines.wmsrbottom[0] = False



class iWMSRHigh(iBaseIndicator):
    '''
    因子：连续 n 填高于
    传入参数：
        rule = {"args": [6,5,80] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('ehigh',)
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRHigh, self).__init__()
        self.wmsr = btind.WilliamsR( period=self.args[0])

    def next(self):

        _list = [abs(i) for i in list(self.wmsr.get(size=self.args[1]))]
        _list.sort()

        if len(_list) == self.args[1]:
            if _list[0] > self.args[2]:
                self.lines.ehigh[0] = True
            else:
                self.lines.ehigh[0] = False
        else:
            self.lines.ehigh[0] = False

          # 打印当前的信号值



class iWMSRBelow(iBaseIndicator):
    '''
    因子：连续 n 填低于
    传入参数：
        rule = {"args": [6,3,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('ebelow',)
    params = dict(rule=list())

    def __init__(self):
        super(iWMSRBelow, self).__init__()
        self.wmsr = btind.WilliamsR( period=self.args[0])

    def next(self):

        _list = [abs(i) for i in list(self.wmsr.get(size=self.args[1]))]
        _list.sort()

        if len(_list) == self.args[1]:
            if _list[-1] < self.args[2]:
                self.lines.ebelow[0] = True
            else:
                self.lines.ebelow[0] = False
        else:
            self.lines.ebelow[0] = False
        # print(_list, abs(self.wmsr[0]), self.data.datetime.datetime(),
        #       '=====' * 3)


