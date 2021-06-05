import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator

class iStochasticSlowCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": [14, 3],      # 慢周期  快周期
            'line': 'percK',#  所选因子线，
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('stochastic',)
    params = dict(rule=list())

    def __init__(self):
        super(iStochasticSlowCompare, self).__init__()
        self.stochastic = btind.StochasticFull(period=self.args[0], period_dfast=self.args[1])

    def next(self):
        perck_lines = self.stochastic.percK  # 长线
        percd_lines = self.stochastic.percD  # 短线

        _lines = eval(f"{self.sigline}_lines")  # 调用的因子线

        self.lines.stochastic[0] = compare(_lines, self.logic)
        # print(self.stochastic.percK[0], self.stochastic.percD[0], self.stochastic.percDSlow[0], ",",
        #       self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iStochasticSlowCrossGolden(iBaseIndicator):
    '''
    因子：金叉
    传入参数：
    rule = {"args": [14, 3],       # 慢周期  快周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 无用
            "position":{1(up),-1(down),0(any)},
            }
    '''

    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iStochasticSlowCrossGolden, self).__init__()
        self.stochastic = btind.StochasticFull(period=self.args[0], period_dfast=self.args[1])
        self.cross = btind.CrossOver( self.stochastic.percD,self.stochastic.percK)

    def next(self):
        # print(compare(self.stochastic.macd[0] - self.stochastic.signal[0], self.logic))
        if self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.stochastic.percD[0] - self.stochastic.percK[0], self.logic) and \
                                            self.stochastic.percD[0] > 80
            elif self.logic["position"] == -1:  # 出现在下部 <0
                self.lines.goldencross[0] = compare(self.stochastic.percD[0] - self.stochastic.percK[0], self.logic) and \
                                            self.stochastic.percD[0] < 20
            else:  # 其他情况
                self.lines.goldencross[0] = compare(self.stochastic.percD[0] - self.stochastic.percK[0], self.logic)
        else:
            self.lines.goldencross[0] = False
        # print(self.stochastic.percK[0], self.stochastic.percD[0], self.stochastic.percDSlow[0], ",",
        #       self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iStochasticSlowCrossDie(iBaseIndicator):
    '''
    因子：死叉
    传入参数：
    rule = {"args": [14, 3],      # 慢周期  快周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 无用
            "position":{1(up),-1(down),0(any)},
            }
    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iStochasticSlowCrossDie, self).__init__()
        self.stochastic = btind.StochasticFull(period=self.args[0], period_dfast=self.args[1])
        self.cross = btind.CrossOver( self.stochastic.percD,self.stochastic.percK)

    def next(self):
        if self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.stochastic.percK[0] - self.stochastic.percD[0],
                                                 self.logic) and \
                                         self.stochastic.percD[0] > 80
            elif self.logic["position"] == -1:  # 出现在上部  <0
                self.lines.diecross[0] = compare(self.stochastic.percK[0] - self.stochastic.percD[0],
                                                 self.logic) and \
                                         self.stochastic.percD[0] < 20
            else:  # 其他情况
                self.lines.diecross[0] = compare(self.stochastic.percK[0] - self.stochastic.percD[0], self.logic)
        else:
            self.lines.diecross[0] = False
        # print(self.stochastic.percK[0], self.stochastic.percD[0], self.stochastic.percDSlow[0], ",",
        #       self.data.datetime.datetime())

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iStochasticSlowLong(iBaseIndicator):
    '''
    因子：多头
    传入参数：
    rule = {"args": [14, 3,3],      # 慢周期  快周期 连续n天多头
            "logic":{ "position":{1(up),-1(down),0(any)},
            }
    '''
    lines = ('stochasticlong',)
    params = dict(rule=list())

    def __init__(self):
        super(iStochasticSlowLong, self).__init__()
        self.stochastic = btind.StochasticFull(period=self.args[0], period_dfast=self.args[1])

    def next(self):
        stochasticlong = set([self.stochastic.percD[i] > self.stochastic.percK[i] for i in range(1 - self.args[2], 1)])

        if len(stochasticlong) == 1 and True in stochasticlong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.stochasticlong[0] = True and self.stochastic.percD[0] > 80
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.stochasticlong[0] = True and self.stochastic.percD[0] < 20
            else:  # 其他条件
                self.lines.stochasticlong[0] = True

        else:
            self.lines.stochasticlong[0] = False


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iStochasticSlowShort(iBaseIndicator):
    '''
    因子：空头
    传入参数：
     rule = {"args": [14, 3,3],       # 慢周期  快周期 连续n天多头
            "logic":{ "position":{1(up),-1(down),0(any)},
            }
    '''
    lines = ('stochastishort',)
    params = dict(rule=list())

    def __init__(self):
        super(iStochasticSlowShort, self).__init__()
        self.stochastic = btind.StochasticFull(period=self.args[0], period_dfast=self.args[1])

    def next(self):
        stochastishort = set([self.stochastic.percD[i] < self.stochastic.percK[i] for i in range(1 - self.args[2], 1)])
        if len(stochastishort) == 1 and True in stochastishort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.stochastishort[0] = True and self.stochastic.percD[0] > 80
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.stochastishort[0] = True and self.stochastic.percD[0] < 20
            else:  # 其他条件
                self.lines.stochastishort[0] = True
        else:
            self.lines.stochastishort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2]) + int(cond['args'][3])


class iStochasticSlowTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
    rule ={"args": [14, 3,3],       # 慢周期  快周期 连续n天
            'line': 'percK',#  所选因子线，
            "logic":{ "position":{1(up),-1(down),0(any)},}
            }
    '''
    lines = ('stochastictop',)
    params = dict(rule=list())

    def __init__(self):
        super(iStochasticSlowTop, self).__init__()
        self.stochastic = btind.StochasticFull(period=self.args[0], period_dfast=self.args[1])

    def next(self):

        perck_list = list(self.stochastic.percK.get(size=self.args[2]))  # 长线
        percd_list = list(self.stochastic.percD.get(size=self.args[2]))  # 短线
        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        if len(_list) == self.args[2] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.stochastictop[0] = True and _list[-1] > 80
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.stochastictop[0] = True and _list[-1] < 20
            else:
                self.lines.stochastictop[0] = True
        else:
            self.lines.stochastictop[0] = False

        # print(self.stochastic.percK[0], self.stochastic.percD[0], self.stochastic.percDSlow[0], ",",
        #       self.data.datetime.datetime())


class iStochasticSlowBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
    rule ={"args": [14, 3,3],       # 慢周期  快周期 连续n天
            'line': 'percK',#  所选因子线，
            "logic":{ "position":{1(up),-1(down),0(any)},}
            }
    '''
    lines = ('stochasticbottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iStochasticSlowBottom, self).__init__()
        self.stochastic = btind.StochasticFull(period=self.args[0], period_dfast=self.args[1])

    def next(self):
        perck_list = list(self.stochastic.percK.get(size=self.args[2]))  # 长线
        percd_list = list(self.stochastic.percD.get(size=self.args[2]))  # 短线
        _list = eval(f"{self.sigline}_list")  # 调用的因子线



        _list = eval(f"{self.sigline}_list")  # 调用的因子线

        if len(_list) == self.args[2] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.stochasticbottom[0] = True and _list[-1] > 0
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.stochasticbottom[0] = True and _list[-1] < 0
            else:
                self.lines.stochasticbottom[0] = True

        else:
            self.lines.stochasticbottom[0] = False
