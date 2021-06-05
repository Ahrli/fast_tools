'''
支持ai因子，只能做多，不支持多颗粒度时间混合
'''
import backtrader as bt
from .import sizerutil as su
import importlib
# import time
# import backtrader.indicators as btind

class iStrategyBase(bt.Strategy):
    params = dict(rule=dict(), sct=0, htrade=dict())

    def __init__(self):
        # # todo 传进来的数据分成，{'datas':[], 'middle':[], 'bigger':[]}
        # self.data_dict  ={'datas':[],}
        # for _data in self.datas:
        #     _ds = _data._name.split('_')
        #     if len(_ds) == 1:
        #         self.data_dict['datas'].append(_data)
        #     else:
        #         try:
        #             self.data_dict[_ds[-1]].append(_data)
        #         except:
        #             self.data_dict[_ds[-1]] = [_data]
        # '''
        #     根据股票池构造买卖的因子：
        #     例：buy_sigs = {
        #         "SH.600000":[sma, macross],
        #         "SH.600006":[sma, macross]
        #     }
        # '''
        # 循环股票池，构造因子数据结构
        self.buy_sigs, self.sell_sigs = dict(), dict()
        for data in self.datas:
            buy_rules = list()
            for rul in self.p.rule['buyRule']:
                buy_inds = list()
                for cond in rul['tradeCondition']:
                    # 动态引入自定义因子
                    buy_moudle = getattr(importlib.import_module(f"api.loop_stack.loop_indicators.{cond['modName']}"),cond['clsName'])
                    # 生成因子，并放入list
                    buy_inds.append(buy_moudle(data, rule=cond['params']))
                # 根据股票code，建立因子列表字典
                buy_rules.append(buy_inds)
            self.buy_sigs[data._name] = buy_rules

            sell_rules = list()
            for rul in self.p.rule['sellRule']:
                sell_inds = list()
                for cond in rul['tradeCondition']:
                    sell_moudle = getattr(importlib.import_module(f"api.loop_stack.loop_indicators.{cond['modName']}"),cond['clsName'])
                    sell_inds.append(sell_moudle(data, rule=cond['params']))
                sell_rules.append(sell_inds)
            self.sell_sigs[data._name] = sell_rules


class iStrategy(iStrategyBase):

    # params = dict(rule=dict())

    def __init__(self):
        '''
        继承因子生成基类iStrategyBase，构造买卖信号池，无因子，则返回空list
        列：sell_sigs = {
            "SH.600000":[],
            "SH.600006":[]
        }

        '''
        self.can_buy = dict()
        self.can_sell = dict()
        self.must_buy_price = dict()
        self.must_sell_price = dict()
        super(iStrategy, self).__init__()
        # print(self.buy_sigs)            # {'US.CMS': [[<loop_indicators.ai_indicator.iAiBuy object at 0x11b4192e8>]]}

    def canBuy(self, code):
        if self.buy_sigs[code]:
            buy_rs = list()
            for br in self.buy_sigs[code]:  # 'US.CMS': [[<loop_indicators.ai_indicator.iAiBuy object at 0x11b4192e8>]]
                buy_time_buffer = list()
                for indc in br:             # [<loop_indicators.ai_indicator.iAiBuy object at 0x11b4192e8>]
                    time_buffer = list(indc.get(size=self.p.rule['riskControl'].get("maxTimeBuffer", 1)))   # <loop_indicators.ai_indicator.iAiBuy object at 0x11b4192e8>
                    buy_time_buffer.append(any(time_buffer))        #[9.1, 9.2 ,9.3]
                buy_rs.append(all(buy_time_buffer))                 # [macd, ma, kdj]
            if (any(buy_rs)):                                       # [[macd, ma, kdj], [macd, rsi]]
                # print("可以买====")
                return True

        return False

    def canSell(self, code):
        if self.sell_sigs[code]:
            sell_rs = list()
            for sr in self.sell_sigs[code]:
                sell_time_buffer = list()
                for indc in sr:
                    time_buffer = list(indc.get(size=self.p.rule['riskControl'].get("maxTimeBuffer", 1)))
                    sell_time_buffer.append(any(time_buffer))
                sell_rs.append(all(sell_time_buffer))
            if (any(sell_rs)):
                # print("可以卖====")
                return True

        return False

    def next(self):
        # print('新的一天')
        # print(self.data0.datetime.datetime())

        buy_pool = []  # 平仓买购买池
        sell_pool = []  # 平仓卖股票池,（做空）
        bullBear = self.p.rule.get('bullBear', 0)  # 是否作空,0:作多
        # print("============================")
        curPosSize = 0
        # todo 循环股票池，判断买卖，买：放入购买池，卖：立即卖掉
        for i, stock in enumerate(self.datas):
            pos = self.getposition(stock)

            if (pos.size != 0):
                curPosSize += 1

            if (bullBear == 0):  # 作多
                # if self.canSell(stock._name):
                    # print("卖出信号")
                    # print(pos.size)
                    # print(self.can_sell)
                # 判断是否卖出
                if (self.canSell(stock._name) and pos.size > 0 and stock._name not in self.can_sell):
                    self.sell(data=stock, size=su.getsellsize(self, stock))  # 全卖？
                    # print("卖出")
                    # print(su.getsellsize(self, stock))
                    self.can_sell[stock._name] = 1
                    # sell_pool.append(stock._name)
                    curPosSize -= 1

                # 判断是否买入
                if (self.canBuy(stock._name) and pos.size == 0 and stock._name not in self.can_buy):
                    buy_pool.append(stock)
                    self.can_buy[stock._name] = 1
            else:#作空
                # 判断是否卖
                if (self.canSell(stock._name) and pos.size==0 and stock._name not in self.can_sell):
                    sell_pool.append(stock)
                    curPosSize -= 1
                    self.can_sell[stock._name]=1
                # 判断是否买：现在是买点，并且持仓量为负（之前卖空过），股票不在可买池子里（有些股票可能买了几天没买到）
                if (self.canBuy(stock._name) and pos.size < 0 and stock._name not in self.can_buy):
                    # 判断是否止损买(上涨的部分超过你的保证金的百分比)，ai没有止损
                    # if(stock._name in self.must_buy_price.keys() and self.must_buy_price.get(stock._name,0) <= stock.close[0]):
                    #     self.sell(data=stock, size=su.getsellsize(self, stock))
                    #     self.can_buy[stock._name]=1
                    #     del self.must_buy_price[stock._name]
                    self.buy(data=stock, size=pos.size*-1)
                    self.can_buy[stock._name]=1
                    # print("买入")
                    # print(stock._name)
                    # buy_pool.append(stock._name)

        # 最大持仓树-已经持仓数=还可以买的股票数量
        canPosSize = self.p.rule['riskControl']['maxStocks'] - curPosSize
        # todo 做多：买股票池决策，做空：卖股票池决策
        if (bullBear == 0):  # 作多
            real_buy_pool = sorted(buy_pool, key=lambda d: d.volume[0], reverse=True)[:canPosSize]
            cursize = len(real_buy_pool)
            # 可能存在问题，暴力方式：根据cash，定死每只股票的价钱
            # 需要买的股票>0
            if (cursize > 0):
                # if (self.p.rule['riskControl']['distribute'] == 0):   # 平权买入
                com_adj_max_risk = su.getAdjMaxPrice(self, cursize, 1 / cursize)  # 单只股票最高可用现金
                # com_adj_max_risk = self.broker.cash
                # com_adj_max_risk = 1000000
                for stock in real_buy_pool:
                    # print("买入")
                    # print(com_adj_max_risk)
                    # print(stock.close[0])
                    # print(su.getbuysize(self, stock, cursize, com_adj_max_risk))
                    self.buy(data=stock, size=su.getbuysize(self, stock, cursize, com_adj_max_risk))
        else:#做空

            real_sell_pool = sorted(sell_pool, key=lambda d: d.volume[0], reverse=True)[:canPosSize]
            # print("需要卖出")
            # print(real_sell_pool)
            cursize = len(real_sell_pool)
            stopLoseRate=self.p.rule['riskControl'].get('stopLossRate',0)
            if (cursize > 0):
                # if(self.p.rule['riskControl']['distribute']==0):#平权卖出
                com_adj_max_risk = su.getShortAdjMaxPrice(self, cursize,1/cursize)  # 单只股票最高可用现金
                for stock in real_sell_pool:
                    # print("start buy:", stock[0], "date:", stock.datetime.date(), "volume:", stock.volume[0], "acc:", self.broker.getvalue())
                    self.sell(data=stock, size=su.getShortSellsize(self, stock, cursize, com_adj_max_risk))
                    #止损价格
                    if(stopLoseRate > 0):
                        stopPrice=round(stock.close[0]*(1+stopLoseRate),2)
                        self.must_buy_price[stock._name]=stopPrice


    def prenext(self):
        self.next()

    def notify_order(self, order):

        if order.status in [order.Canceled, order.Margin, order.Rejected, order.Completed]:
            if (order.isbuy and order.data._name in self.can_buy):
                del self.can_buy[order.data._name]
            elif (order.issell and order.data._name in self.can_sell):
                del self.can_sell[order.data._name]

    def notify_trade(self, trade):
        self.p.htrade[trade.data._name] = trade.baropen
        if not trade.isclosed:
            return