import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator, iDma

class iDmaCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": [10, 50],      #dma短周期， dma长周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('dc',)
    params = dict(rule=list())

    def __init__(self):
        super(iDmaCompare, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])

    def next(self):
        dmac = compare(self.dma.dma[0], self.logic)
        amac = compare(self.dma.ama[0], self.logic)
        self.lines.dc[0] = dmac and amac

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iDmaCrossGolden(iBaseIndicator):
    '''
    因子：金叉：DMA线向上交叉AMA线，买进
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('goldencross', )
    params = dict(rule=list())

    def __init__(self):
        super(iDmaCrossGolden, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])
        self.cross = btind.CrossOver(self.dma.dma, self.dma.ama)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.dma.dma[0] - self.dma.ama[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iDmaCrossDie(iBaseIndicator):
    '''
    因子：死叉：DMA线向下交叉AMA线，卖出。
    传入参数：
    rule = {"args": ["5","10"],    #短均线周期, 长均线周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iDmaCrossDie, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])
        self.cross = btind.CrossOver(self.dma.dma, self.dma.ama)

    def next(self):
        if self.cross[0] == -1:
            self.lines.diecross[0] = compare(self.dma.ama[0] - self.dma.dma[0], self.logic)
        else:
            self.lines.diecross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])

class iDmaCrossLong(iBaseIndicator):
    '''
    因子：多头：当DMA和AMA均>0（即在图形上表示为它们处于零线以上）并向上移动时，一般表示为股市处于多头行情中。
    传入参数：
    rule = {"args": ["5","10","3"],    #短均线周期, 长均线周期, 连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('dmalong',)
    params = dict(rule=list())

    def __init__(self):
        super(iDmaCrossLong, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])

    def next(self):
        # 最新的价格在list末尾，上升趋势：dma[-3] < dma[-2] < dma[-1] < 最新， 全都大于0
        dmas = list(self.dma.dma.get(size=self.args[2]))
        amas = list(self.dma.ama.get(size=self.args[2]))
        if len(dmas) == self.args[2]:
            dmalong = set(list(map(lambda d: d > 0, dmas + amas)) + [dmas[i] > amas[i] for i in range(len(dmas))] + list(map(lambda s: sorted(s) == s, [dmas, amas])))
        else:
            dmalong = []

        if len(dmalong)==1 and True in dmalong:
            self.lines.dmalong[0] = True
        else:
            self.lines.dmalong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iDmaCrossShort(iBaseIndicator):
    '''
    因子：空头：当DMA和AMA均 < 0（即在图形上表示为它们处于零线以上）并向下移动时，一般表示为股市处于空头行情中。
    AMA 长周期， 短> 长 多头 短< 长空头
    传入参数：
    rule = {"args": ["5","10","3"],    #短均线周期, 长均线周期, 连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('dmashort',)
    params = dict(rule=list())

    def __init__(self):
        super(iDmaCrossShort, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])

    def next(self):
        # 最新的价格在list末尾，上升趋势：dma[-3] < dma[-2] < dma[-1] < 最新， 全都小于0
        dmas = list(self.dma.dma.get(size=self.args[2]))
        amas = list(self.dma.ama.get(size=self.args[2]))
        if len(dmas) == self.args[2]:
            dmashort = set(list(map(lambda d: d < 0, dmas + amas)) + [dmas[i] < amas[i] for i in range(len(dmas))] + list(map(lambda s: sorted(s, reverse=True) == s, [dmas, amas])))
        else:
            dmashort = []

        if len(dmas) != 0 and len(dmashort)==1 and True in dmashort:
            self.lines.dmashort[0] = True
        else:
            self.lines.dmashort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iDmaRise(iBaseIndicator):
    '''
    因子：多头：当DMA和AMA均>0（即在图形上表示为它们处于零线以上）并向上移动时，一般表示为股市处于多头行情中。
    传入参数：
    rule = {"args": ["5","10","3"],    #短均线周期, 长均线周期, 连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('dmarise',)
    params = dict(rule=list())

    def __init__(self):
        super(iDmaRise, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])

    def next(self):
        # 最新的价格在list末尾，上升趋势：dma[-3] < dma[-2] < dma[-1] < 最新， 全都大于0
        dmas = list(self.dma.dma.get(size=self.args[2]))
        amas = list(self.dma.ama.get(size=self.args[2]))
        dmarise = set([dmas[i] > amas[i] for i in range(len(dmas))] + list(map(lambda s: sorted(s) == s, [dmas, amas])))

        if len(dmarise)==1 and True in dmarise:
            self.lines.dmarise[0] = True
        else:
            self.lines.dmarise[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])

class iDmaFall(iBaseIndicator):
    '''
    因子：空头：当DMA和AMA均 < 0（即在图形上表示为它们处于零线以上）并向下移动时，一般表示为股市处于空头行情中。
    AMA 长周期， 短> 长 多头 短< 长空头
    传入参数：
    rule = {"args": ["5","10","3"],    #短均线周期, 长均线周期, 连续n天多头
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 金叉情况比较大小， 短比长高多少
            }
    '''
    lines = ('dmafall',)
    params = dict(rule=list())

    def __init__(self):
        super(iDmaFall, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])

    def next(self):
        # 最新的价格在list末尾，上升趋势：dma[-3] < dma[-2] < dma[-1] < 最新， 全都小于0
        dmas = list(self.dma.dma.get(size=self.args[2]))
        amas = list(self.dma.ama.get(size=self.args[2]))
        dmafall = set([dmas[i] < amas[i] for i in range(len(dmas))] + list(map(lambda s: sorted(s, reverse=True) == s, [dmas, amas])))

        if len(dmafall)==1 and True in dmafall:
            self.lines.dmafall[0] = True
        else:
            self.lines.dmafall[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iDmaTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [10, 50, 30],      #dma短周期， dma长周期, n日最高
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('dtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iDmaTop, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])

    def next(self):
        _list = {
            'dma' : list(self.dma.dma.get(size=self.args[2])),
            'ama' : list(self.dma.ama.get(size=self.args[2])),
        }

        _signal = {
            'dma': self.dma.dma[0],
            'ama': self.dma.ama[0],
        }

        # dma_line = self.logic['line']
        dma_line = self.sigline


        if len(_list[dma_line]) == self.args[2] and _signal[dma_line] == max(_list[dma_line]):
            self.lines.dtop[0] = True
        else:
            self.lines.dtop[0] = False


class iDmaBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [10, 50, 30],      #dma短周期， dma长周期, n日最高
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('dbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iDmaBottom, self).__init__()
        self.dma = iDma(self.data.close, short=self.args[0], long=self.args[1])

    def next(self):
        _list = {
            'dma' : list(self.dma.dma.get(size=self.args[2])),
            'ama' : list(self.dma.ama.get(size=self.args[2])),
        }

        _signal = {
            'dma': self.dma.dma[0],
            'ama': self.dma.ama[0],
        }

        # dma_line = self.logic['line']
        dma_line = self.sigline


        if len(_list[dma_line]) == self.args[2] and _signal[dma_line] == min(_list[dma_line]):
            self.lines.dbottom[0] = True
        else:
            self.lines.dbottom[0] = False