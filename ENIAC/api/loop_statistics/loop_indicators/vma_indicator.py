import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iVmaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["5"],      #sma周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('vmc', )
    params = dict(rule=list())

    def __init__(self):
        super(iVmaCompare, self).__init__()
        self.vma = btind.SimpleMovingAverage(self.data.volume, period=self.args[0])

    def next(self):
        self.lines.vmc[0] = compare(self.vma[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iVmaCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('vgoldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iVmaCrossGolden, self).__init__()
        self.vma_short = btind.SimpleMovingAverage(self.data.volume, period=self.args[0])
        self.vma_long = btind.SimpleMovingAverage(self.data.volume, period=self.args[1])
        self.vcross = btind.CrossOver(self.vma_short, self.vma_long)

    def next(self):
        if self.vcross[0] == 1:
            self.lines.vgoldencross[0] = compare(self.vma_short[0]-self.vma_long[0], self.logic)
        else:
            self.lines.vgoldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iVmaCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 死叉情况比较大小,长比短高多少
            }
    '''
    lines = ('vdiecross', )
    params = dict(rule=list())

    def __init__(self):
        super(iVmaCrossDie, self).__init__()
        self.vma_short = btind.SimpleMovingAverage(self.data.volume, period=self.args[0])
        self.vma_long = btind.SimpleMovingAverage(self.data.volume, period=self.args[1])
        self.vcross = btind.CrossOver(self.vma_short, self.vma_long)

    def next(self):
        if self.vcross[0] == -1:
            self.lines.vdiecross[0] = compare(self.vma_long[0]-self.vma_short[0], self.logic)
        else:
            self.lines.vdiecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iVmaLong(iBaseIndicator):
    '''
    因子：ma多头
    传入参数：
    rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},   #无用
            }
    '''
    lines = ('vmalong',)
    params = dict(rule=list())

    def __init__(self):
        super(iVmaLong, self).__init__()
        self.logic = self.p.rule['logic']
        self.vma_short = btind.SimpleMovingAverage(self.data.volume, period=self.args[0])
        self.vma_long = btind.SimpleMovingAverage(self.data.volume, period=self.args[1])

    def next(self):
        malong = set([self.data.volume[i] > self.vma_short[i] > self.vma_long[i] for i in range(1-self.args[2],1)])
        if len(malong) == 1 and True in malong:
            self.lines.vmalong[0] = True
        else:
            self.lines.vmalong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iVmaShort(iBaseIndicator):
    '''
    因子：ma空头
    传入参数：
        rule = {"args": [5,10, 5],   # 连续N日短均线, 连续N日长均线, 连续N天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
            }
    '''
    lines = ('vmashort',)
    params = dict(rule=list())

    def __init__(self):
        super(iVmaShort, self).__init__()
        self.vma_short = btind.SimpleMovingAverage(self.data.volume, period=self.args[0])
        self.vma_long = btind.SimpleMovingAverage(self.data.volume, period=self.args[1])

    def next(self):
        mashort = set([self.data.volume[i] < self.vma_short[i] < self.vma_long[i] for i in range(1 - self.args[2], 1)])
        if len(mashort) == 1 and True in mashort:
            self.lines.vmashort[0] = True
        else:
            self.lines.vmashort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iVmaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [30,10] ,  # 第一个参数是ma的周期，第二个参数是最近 n  天 极值
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('vtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iVmaTop, self).__init__()
        self.vma = btind.SimpleMovingAverage(self.data.volume, period=self.args[0])

    def next(self):

        # if self.vma[0] == max([self.vam[0-num] for num in range(self.args[0])]):
        # print(self.args[0])
        # print(self.vma.get(size=self.args[1]))
        # print(len(list(self.vma.get(size=self.args[1]))))
        _list = list(self.vma.get(size=self.args[1]))
        if len(_list) == self.args[1]  and _list[-1] == max(_list):
            self.lines.vtop[0] = True
        else:
            self.lines.vtop[0] = False




class iVmaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,30] ,
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    lines = ('vbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iVmaBottom, self).__init__()
        self.vma = btind.SimpleMovingAverage(self.data.volume, period=self.args[0])

    def next(self):
        # print(self.args[0])
        # # if self.vma[0] == max([self.vam[0-num] for num in range(self.args[0])]):
        # print(list(self.vma.get(size=self.args[1])))
        _list = list(self.vma.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            self.lines.vbottom[0] = True
        else:
            self.lines.vbottom[0] = False




