import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iBollPercentb(iBaseIndicator):
    '''
    因子：%b指标：（收盘价-布林线下轨价格）/（布林线上轨价格-布林线下轨价格）
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('percentb',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollPercentb, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.percentb = (self.data.close-self.boll.bot)/(self.boll.top-self.boll.bot)

    def next(self):
        self.lines.percentb[0] = compare(self.percentb[0], self.logic)

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iBollBandWidth(iBaseIndicator):
    '''
    因子：带宽（band width）：(布林线上轨价格-布林线下轨价格) / 布林线中轨价格
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 连续n天收紧，放大,盘整（>/</= 临界点）
            }
    '''
    lines = ('bandwith',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollBandWidth, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.bandwith = (self.boll.top-self.boll.bot)/self.boll.mid

    def next(self):
        wcs = set([compare(self.bandwith[i], self.logic) for i in range(1-self.args[2], 1)])
        if len(wcs) == 1 and True in wcs:
            self.lines.bandwith[0] = True
        else:
            self.lines.bandwith[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iBollLinesUp(iBaseIndicator):
    '''
    因子：向上：布林线的上、中、下轨线同时向上运行时，表明股价强势特征非常明显，股价短期内将继续上涨，投资者应坚决持股待涨或逢低买入。
    传入参数：
    rule = {"args": [20, 2.0, 3],      #boll周期, 几倍的标准差，默认为2, 连续多少天向上运行
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('linesup',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollLinesUp, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])

    def next(self):
        bots = self.boll.bot.get(size=self.args[2])
        mids = self.boll.mid.get(size=self.args[2])
        tops = self.boll.top.get(size=self.args[2])
        # 布林带连续上升
        ups = set(list(map(lambda s: sorted(s) == s, [bots, mids, tops])))
        if len(ups) == 1 and True in ups:
            self.lines.linesup[0] = True
        else:
            self.lines.linesup[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0]) + int(cond['args'][2])


class iBollLinesDown(iBaseIndicator):
    '''
    因子：向下：布林线的上、中、下轨线同时向下运行时，表明股价的弱势特征非常明显，股价短期内将继续下跌，投资者应坚决持币观望或逢高卖出。
    传入参数：
    rule = {"args": [20, 2.0, 3],      #boll周期, 几倍的标准差，默认为2, 连续多少天向上运行
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('linesdown',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollLinesDown, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])

    def next(self):
        bots = self.boll.bot.get(size=self.args[2])
        mids = self.boll.mid.get(size=self.args[2])
        tops = self.boll.top.get(size=self.args[2])
        # 布林带连续下跌
        downs = set(list(map(lambda s: sorted(s, reverse=True) == s, [bots, mids, tops])))
        if len(downs) == 1 and True in downs:
            self.lines.linesdown[0] = True
        else:
            self.lines.linesdown[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0]) + int(cond['args'][2])


class iBollLong(iBaseIndicator):
    '''
    因子：多头：价格在中间线与Up线之间波动运行时为多头市场
    传入参数：
    rule = {"args": [20, 2.0, 3],      #boll周期, 几倍的标准差，默认为2, 连续多少天多头
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('bolllong',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollLong, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])

    def next(self):
        # 价格在中间线与Up线
        bolllong = set([self.boll.top[i] > self.data.close[i] > self.boll.mid[i] for i in range(1-self.args[2], 1)])
        if len(bolllong) == 1 and True in bolllong:
            self.lines.bolllong[0] = True
        else:
            self.lines.bolllong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0]) + int(cond['args'][2])


class iBollShort(iBaseIndicator):
    '''
    因子：空头：价格在中间线与Down线之间向下波动运行时为空头市场
    传入参数：
    rule = {"args": [20, 2.0, 3],      #boll周期, 几倍的标准差，默认为2, 连续多少天多头
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('bollshort',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollShort, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])

    def next(self):
        bots = self.boll.bot.get(size=self.args[2])
        mids = self.boll.mid.get(size=self.args[2])
        tops = self.boll.top.get(size=self.args[2])
        # 价格在中间线与down线之间，并且向下波动
        bollshort = set(list(map(lambda s: sorted(s, reverse=True) == s, [bots, mids, tops])) +
                    [self.boll.mid[i] > self.data.close[i] > self.boll.bot[i] for i in range(1 - self.args[2], 1)])
        if len(bollshort) == 1 and True in bollshort:
            self.lines.bollshort[0] = True
        else:
            self.lines.bollshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0]) + int(cond['args'][2])


class iBollUpTop(iBaseIndicator):
    '''
    因子：收盘价上穿boll上轨
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2,
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('uptop',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollUpTop, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.cross = btind.CrossOver(self.data.close, self.boll.top)

    def next(self):
        if self.cross[0] == 1:
            # self.lines.uptop[0] = compare(self.data.close[0]-self.boll.top[0], self.logic)
            self.lines.uptop[0] = True
        else:
            self.lines.uptop[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iBollUpMid(iBaseIndicator):
    '''
    因子：收盘价上穿boll中轨
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2,
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('upmid',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollUpMid, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.cross = btind.CrossOver(self.data.close, self.boll.mid)

    def next(self):
        if self.cross[0] == 1:
            # self.lines.upmid[0] = compare(self.data.close[0]-self.boll.mid[0], self.logic)
            self.lines.upmid[0] = True
        else:
            self.lines.upmid[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iBollUpBot(iBaseIndicator):
    '''
    因子：收盘价上穿boll下轨
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('upbot',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollUpBot, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.cross = btind.CrossOver(self.data.close, self.boll.bot)

    def next(self):
        if self.cross[0] == 1:
            # self.lines.upbot[0] = compare(self.data.close[0]-self.boll.bot[0], self.logic)
            self.lines.upbot[0] = True
        else:
            self.lines.upbot[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iBollDownBot(iBaseIndicator):
    '''
    因子：收盘价下穿boll下轨
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('downbot',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollDownBot, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.cross = btind.CrossOver(self.data.close, self.boll.bot)

    def next(self):
        if self.cross[0] == -1:
            # self.lines.downbot[0] = compare(self.boll.bot[0]-self.data.close[0], self.logic)
            self.lines.downbot[0] = True
        else:
            self.lines.downbot[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iBollDownMid(iBaseIndicator):
    '''
    因子：收盘价下穿boll中轨
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('downmid',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollDownMid, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.cross = btind.CrossOver(self.data.close, self.boll.mid)

    def next(self):
        if self.cross[0] == -1:
            # self.lines.downmid[0] = compare(self.boll.mid[0]-self.data.close[0], self.logic)
            self.lines.downmid[0] = True
        else:
            self.lines.downmid[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iBollDownTop(iBaseIndicator):
    '''
    因子：收盘价下穿boll上轨
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('downtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollDownTop, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.cross = btind.CrossOver(self.data.close, self.boll.top)

    def next(self):
        if self.cross[0] == -1:
            self.lines.downtop[0] = True
            # self.lines.downtop[0] = compare(self.boll.top[0]-self.data.close[0], self.logic)
        else:
            self.lines.downtop[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iBollTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [20, 2.0, 30, top],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('btop',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollTop, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.bandwith = (self.boll.top - self.boll.bot) / self.boll.mid

    def next(self):
        _list = {
            'top': list(self.boll.top.get(size=self.args[2])),
            'mid': list(self.boll.mid.get(size=self.args[2])),
            'bot': list(self.boll.mid.get(size=self.args[2])),
            'bandwith': list(self.bandwith.get(size=self.args[2])),
        }

        _signal = {
            'top': self.boll.top[0],
            'mid': self.boll.mid[0],
            'bot': self.boll.bot[0],
            'bandwith': self.bandwith[0],
        }

        # kdj_line = self.args[3]
        # boll_line = self.logic['line']
        boll_line = self.sigline

        if len(_list[boll_line]) == self.args[2] and _signal[boll_line] == max(_list[boll_line]):
            self.lines.btop[0] = True
        else:
            self.lines.btop[0] = False


class iBollBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule = {"args": [20, 2.0, 30, top],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('bbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iBollBottom, self).__init__()
        self.boll = btind.BBands(self.data.close, period=self.args[0], devfactor=self.args[1])
        self.bandwith = (self.boll.top - self.boll.bot) / self.boll.mid

    def next(self):
        _list = {
            'top': list(self.boll.top.get(size=self.args[2])),
            'mid': list(self.boll.mid.get(size=self.args[2])),
            'bot': list(self.boll.mid.get(size=self.args[2])),
            'bandwith': list(self.bandwith.get(size=self.args[2])),
        }

        _signal = {
            'top': self.boll.top[0],
            'mid': self.boll.mid[0],
            'bot': self.boll.bot[0],
            'bandwith': self.bandwith[0],
        }

        # kdj_line = self.args[3]
        # boll_line = self.logic['line']
        boll_line = self.sigline


        if len(_list[boll_line]) == self.args[2] and _signal[boll_line] == min(_list[boll_line]):
            self.lines.bbottom[0] = True
        else:
            self.lines.bbottom[0] = False