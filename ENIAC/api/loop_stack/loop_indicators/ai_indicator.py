from .base_indicator import iBaseIndicator




ptop_model = {'US.GOOGL':'gogogl.pkl'
              }


'''
indicator
'''

class iAiBuy(iBaseIndicator):
    '''
    因子：tpot模型
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('aibuy',)
    params = dict(rule=list())

    def __init__(self):
        super(iAiBuy, self).__init__()

    def next(self):
        if self.data.volume[0]==1:
            self.lines.aibuy[0] = True
        else:
            self.lines.aibuy[0] = False

class iAiSell(iBaseIndicator):
    '''
    因子：tpot模型
    传入参数：
    rule = {"args": [20, 2.0],      #boll周期, 几倍的标准差，默认为2
            "logic":{"compare": "gt","byValue": 1,"byMax": 5,},  # 周期结果比较
            }
    '''
    lines = ('aisell',)
    params = dict(rule=list())

    def __init__(self):
        super(iAiSell, self).__init__()

    def next(self):
        if self.data.volume[0] == -1:
            self.lines.aisell[0] = True
        else:
            self.lines.aisell[0] = False