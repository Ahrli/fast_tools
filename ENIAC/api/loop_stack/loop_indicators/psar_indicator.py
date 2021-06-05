import backtrader.indicators as btind
from . import compare_price as compare
# import backtrader.talib as btalib
from .base_indicator import iBaseIndicator

class iPsarCompare(iBaseIndicator):
    '''
    因子：平均移动线比较数值
    传入参数：
    rule = {"args": ["2",2,20],      #周期 步长 最大步长
            "logic":{"compare": "eq","byValue": 1,"byMax": 5,

            },  # 周期结果比较
            }
    '''
    lines = ('psar',)
    params = dict(rule=list())

    def __init__(self):
        super(iPsarCompare, self).__init__()
        self.psar = btind.ParabolicSAR( period=self.args[0], af=self.args[1]/100, afmax=self.args[2]/100,)

    def next(self):
        self.lines.psar[0] = compare(self.psar[0], self.logic)
        # print(self.psar[0], ",", self.data.datetime.datetime())
        pass

    @classmethod
    def judge(cls, cond):
        return int(cond['args'][0])





