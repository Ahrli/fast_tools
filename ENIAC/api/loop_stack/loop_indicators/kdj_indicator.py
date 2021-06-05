import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator, iKdj

class iKdjCompare(iBaseIndicator):
    '''
        因子：kdj比较
        传入参数：
        rule = {"args": [20],      #n日KDj
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
                }
    '''
    lines = ('kdjc',)
    params = dict(rule=list())

    def __init__(self):
        super(iKdjCompare, self).__init__()
        self.kdj = iKdj(self.data, period=self.args[0], a=self.args[1], b=self.args[2])

    def next(self):
        kc = compare(self.kdj.k[0], self.logic)
        dc = compare(self.kdj.d[0], self.logic)
        jc = compare(self.kdj.j[0], self.logic)
        self.lines.kdjc[0] = kc and dc and jc

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iKdjCrossGolden(iBaseIndicator):
    '''
        因子：金叉：K线向上突破D线时，俗称金叉
        传入参数：
        rule = {"args": [20],      #n日KDj
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
                }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iKdjCrossGolden, self).__init__()
        self.kdj = iKdj(self.data, period=self.args[0], a=self.args[1], b=self.args[2])
        self.cross = btind.CrossOver(self.kdj.k, self.kdj.d)

    def next(self):
        if self.cross[0] == 1:
            self.lines.goldencross[0] = compare(self.kdj.k[0] - self.kdj.d[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])

class iKdjCrossDie(iBaseIndicator):
    '''
        因子：死叉：K线向下突破D线时，俗称死叉
        传入参数：
        rule = {"args": [20,3,3],      #n日KDj, a,b
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
                }
    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iKdjCrossDie, self).__init__()
        self.kdj = iKdj(self.data, period=self.args[0], a=self.args[1], b=self.args[2])
        self.cross = btind.CrossOver(self.kdj.k, self.kdj.d)

    def next(self):
        if self.cross[0] == -1:
            self.lines.goldencross[0] = compare(self.kdj.d[0] - self.kdj.k[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iKdjLong(iBaseIndicator):
    '''
        因子：多头， 当J大于K、K大于D时 默认大于50
        传入参数：
        rule = {"args": [20, a,b,3, 50],      #n日KDj, 连续n天多头
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
                }
    '''
    lines = ('kdjlong', )
    params = dict(rule=list())

    def __init__(self):
        super(iKdjLong, self).__init__()
        self.kdj = iKdj(self.data, period = self.args[0], a=self.args[1], b=self.args[2])

    def next(self):
        ds = list(self.kdj.d.get(size=self.args[3]))
        ks = list(self.kdj.k.get(size=self.args[3]))
        js = list(self.kdj.j.get(size=self.args[3]))
        # d<k<j, 且都大于50为多头
        if len(ks) == self.args[3]:
            kdjlong = set(list(map(lambda d: d > self.args[4], ks + ds + js)) + [sorted(s, reverse=True)==s for s in zip(js, ds, ks)])
        else:
            kdjlong = []

        if len(kdjlong) == 1 and True in kdjlong:
            self.lines.kdjlong[0] = True
        else:
            self.lines.kdjlong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0]) + int(cond['args'][1])


class iKdjShort(iBaseIndicator):
    '''
        因子：空头
        传入参数：
        rule = {"args": [20, a,b,3, 50],      #n日KDj, 连续n天多头
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
                }
    '''
    lines = ('kdjshort', )
    params = dict(rule=list())

    def __init__(self):
        super(iKdjShort, self).__init__()
        self.kdj = iKdj(self.data, period = self.args[0], a=self.args[1], b=self.args[2])

    def next(self):
        ks = list(self.kdj.k.get(size=self.args[3]))
        ds = list(self.kdj.d.get(size=self.args[3]))
        js = list(self.kdj.j.get(size=self.args[3]))
        if len(ks) == self.args[3]:
            kdjshort = set(list(map(lambda d: d > self.args[4], ks + ds + js)) + [sorted(s) == s for s in zip(js, ds, ks)])
        else:
            kdjshort = []

        if len(kdjshort) == 1 and True in kdjshort:
            self.lines.kdjshort[0] = True
        else:
            self.lines.kdjshort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0]) + int(cond['args'][1])


class iKdjTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [20, 3, 3, 30, k] , n日， a, b m日最高, k线
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''
    # lines = ('ktop', 'dtop', 'jtop',)
    lines = ('kdjtop',)
    params = dict(rule=list())

    def __init__(self):
        super(iKdjTop, self).__init__()
        self.kdj = iKdj(self.data, period=self.args[0], a=self.args[1], b=self.args[2])

    def next(self):
        _list = {
            'k': list(self.kdj.k.get(size=self.args[3])),
            'd': list(self.kdj.d.get(size=self.args[3])),
            'j': list(self.kdj.j.get(size=self.args[3])),
        }

        _signal = {
            'k': self.kdj.k[0],
            'd': self.kdj.d[0],
            'j': self.kdj.j[0],
        }

        # kdj_line = self.args[4]
        # kdj_line = self.logic['line']
        kdj_line = self.sigline

        if len(_list[kdj_line]) == self.args[3]  and _signal[kdj_line] == max(_list[kdj_line]):
            self.lines.kdjtop[0] = True
        else:
            self.lines.kdjtop[0] = False


class iKdjBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
        rule = {"args": [20, 3, 3, 30, k] , n日， a, b m日最高, k线
                "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  #无意义
    '''



    lines = ('kdjbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iKdjBottom, self).__init__()
        self.kdj = iKdj(self.data, period=self.args[0], a=self.args[1], b=self.args[2])

    def next(self):
        _list = {
            'k': list(self.kdj.k.get(size=self.args[3])),
            'd': list(self.kdj.d.get(size=self.args[3])),
            'j': list(self.kdj.j.get(size=self.args[3])),
        }

        _signal = {
            'k': self.kdj.k[0],
            'd': self.kdj.d[0],
            'j': self.kdj.j[0],
        }

        # kdj_line = self.args[4]
        # kdj_line = self.logic['line']
        kdj_line = self.sigline

        if len(_list[kdj_line]) == self.args[3] and _signal[kdj_line] == min(_list[kdj_line]):
            self.lines.kdjbottom[0] = True
        else:
            self.lines.kdjbottom[0] = False