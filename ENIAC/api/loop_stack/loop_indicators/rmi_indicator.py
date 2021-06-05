import backtrader.indicators as btind
from . import compare_price as compare
from .base_indicator import iBaseIndicator


class iRmiCompare(iBaseIndicator):
    '''
    因子：相对强弱指数比较数值
    传入参数：
    rule = {"args": ["5"],    #rmi周期
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('rmi',)
    params = dict(rule=list())

    def __init__(self):
        super(iRmiCompare, self).__init__()
        self.rmi = btind.RMI(self.data.close, period=self.args[0], safediv=True)

    def next(self):
        self.lines.rmi[0] = compare(self.rmi[0], self.logic)
        # print(self.rmi.rmi[0])

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])


class iRmiCrossGolden(iBaseIndicator):
    '''

    传入参数：
    rule = {"args": [12,26],   # 连续N日短均线, 连续N日长均线
            "logic":{"position":0},
            }

    '''
    lines = ('goldencross',)
    params = dict(rule=list())

    def __init__(self):
        super(iRmiCrossGolden, self).__init__()
        self.rmi_short = btind.RMI(self.data.close, period=self.args[0], safediv=True)
        self.rmi_long = btind.RMI(self.data.close, period=self.args[1], safediv=True)
        self.cross = btind.CrossOver(self.rmi_short, self.rmi_long)

    def next(self):
        if  self.cross[0] == 1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.goldencross[0] = compare(self.rmi_short[0] - self.rmi_long[0], self.logic) and \
                                            self.rmi_short[0] > 70
            elif self.logic["position"] == -1:  # 出现部  < 0
                self.lines.goldencross[0] = compare(self.rmi_short[0] - self.rmi_long[0], self.logic) and \
                                            self.rmi_short[0] < 30
            else:
                self.lines.goldencross[0] = compare(self.rmi_short[0] - self.rmi_long[0], self.logic)
        else:
            self.lines.goldencross[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iRmiCrossDie(iBaseIndicator):
    '''
    因子：死叉：短期RMI线在高位向下突破长期RMI线, 一般为RMI指标的“死亡交叉”
    传入参数：
    rule = {"args": [12,26],   # 连续N日短均线, 连续N日长均线
            "logic":{"position":0},
            }

    '''
    lines = ('diecross',)
    params = dict(rule=list())

    def __init__(self):
        super(iRmiCrossDie, self).__init__()
        self.rmi_short = btind.RMI(self.data.close, period=self.args[0], safediv=True)
        self.rmi_long = btind.RMI(self.data.close, period=self.args[1], safediv=True)
        self.cross = btind.CrossOver(self.rmi_short, self.rmi_long)

    def next(self):
        if  self.cross[0] == -1:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.diecross[0] = compare(self.rmi_long[0] - self.rmi_short[0], self.logic) and self.rmi_short[
                    0] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.diecross[0] = compare(self.rmi_long[0] - self.rmi_short[0], self.logic) and self.rmi_short[
                    0] < 30
            else:
                self.lines.diecross[0] = compare(self.rmi_long[0] - self.rmi_short[0], self.logic)
        else:
            self.lines.diecross[0] = False
        # print( self.rmi_long[0] - self.rmi_short[0],self.data.datetime.datetime())  # 打印当前的信号值


    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1])


class iRmiLong(iBaseIndicator):
    '''
    因子：rmi多头,收盘价 > 短线rmi > 长线rmi
    传入参数：
    rule = {"args": [12,26,3],   # 连续N日短均线, 连续N日长均线
            "logic":{"position":0},
            }

    '''
    lines = ('rmilong',)
    params = dict(rule=list())

    def __init__(self):
        super(iRmiLong, self).__init__()
        self.rmi_short = btind.RMI(self.data.close, period=self.args[0], safediv=True)
        self.rmi_long = btind.RMI(self.data.close, period=self.args[1], safediv=True)

    def next(self):
        rmilong = set([ self.rmi_short[i] > self.rmi_long[i] for i in range(1 - self.args[2], 1)])
        if len(rmilong) == 1 and True in rmilong:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.rmilong[0] = True and self.rmi_short[0] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.rmilong[0] = True and self.rmi_short[0] < 30
            else:
                self.lines.rmilong[0] = True
        else:
            self.lines.rmilong[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iRmiShort(iBaseIndicator):
    '''
    因子：rmi多头,收盘价 > 短线rmi > 长线rmi
    传入参数：
   rule = {"args": [12,26,3],   # 连续N日短均线, 连续N日长均线
            "logic":{"position":0},
            }

    '''
    lines = ('rmishort',)
    params = dict(rule=list())

    def __init__(self):
        super(iRmiShort, self).__init__()
        self.rmi_short = btind.RMI(self.data.close, period=self.args[0], safediv=True)
        self.rmi_long = btind.RMI(self.data.close, period=self.args[1], safediv=True)

    def next(self):
        rmishort = set([self.rmi_short[i] < self.rmi_long[i] for i in range(1 - self.args[2], 1)])
        if len(rmishort) == 1 and True in rmishort:
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.rmishort[0] = True and self.rmi_short[0] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.rmishort[0] = True and self.rmi_short[0] < 30
            else:
                self.lines.rmishort[0] = True
        else:
            self.lines.rmishort[0] = False

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][1]) + int(cond['args'][2])


class iRmiTop(iBaseIndicator):
    '''
    因子：最近 n  天 最高点
    传入参数：
       rule = {"args": [5,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('rmitop',)
    params = dict(rule=list())

    def __init__(self):
        super(iRmiTop, self).__init__()
        self.rmi = btind.RMI(self.data.close, period=self.args[0], safediv=True)

    def next(self):
        _list = list(self.rmi.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == max(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.rmitop[0] = True and _list[-1] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.rmitop[0] = True and _list[-1] < 30
            else:
                self.lines.rmitop[0] = True
        else:
            self.lines.rmitop[0] = False


class iRmiBottom(iBaseIndicator):
    '''
    因子：最近 n  天 最低点
    传入参数：
        rule = {"args": [5,3],   # 连续N日短均线, 连续N日长均线, 连续N天
            "logic":{"position":0},
            }
    '''
    lines = ('rmibottom',)
    params = dict(rule=list())

    def __init__(self):
        super(iRmiBottom, self).__init__()
        self.rmi = btind.RMI(self.data.close, period=self.args[0], safediv=True)

    def next(self):
        _list = list(self.rmi.get(size=self.args[1]))
        if len(_list) == self.args[1] and _list[-1] == min(_list):
            if self.logic["position"] == 1:  # 出现在上部  > 0
                self.lines.rmibottom[0] = True and _list[-1] > 70
            elif self.logic["position"] == -1:  # 出现在下部  < 0
                self.lines.rmibottom[0] = True and _list[-1] < 30
            else:
                self.lines.rmibottom[0] = True
        else:
            self.lines.rmibottom[0] = False
