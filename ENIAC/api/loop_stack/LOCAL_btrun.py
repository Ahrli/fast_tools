from . import user_commission as bcomm
from .  import BTC_strategy as bstrategy
from .loop_load_data import *
import toolkit
if toolkit.__version__=="1.7.20":
    from toolkit.managers import Timer
else:
    from toolkit.tools.managers import Timer
# from ENIAC import Timer
from .funcutil import *

def startRun(rule):

    engine = bt.Cerebro()
    startcash = rule['startCash']
    _ids = rule['myStocks']
    if not _ids:
        raise Exception("401")

    # 动态加载数据，判断最大至少天数
    minimum_days = list()
    for rul in rule['buyRule'] + rule['sellRule']:
        for cond in rul['tradeCondition']:
            minimum_days.append(sum(list(map(int, cond['params']['args']))))  # 取和最大


    max_arg = max(minimum_days)
    # 判断是否有数据加入
    data_flag = False

    # todo 加载数据/耗时计算
    with Timer() as timer_es:

        df = list(get_es_group_stacks_p(startTS=rule['startDay'],
                                        endTS=rule['endDay'],
                                        codes=rule["myStocks"],
                                        dim=rule["kline"],
                                        autotype="cq")
                  )[0]
        df["volume"] = df["updownMatrixArray"].astype(np.float64)
        # df["volume"] = df["volume"].astype(np.float64)
        # df = df[['close', 'code', 'high', 'low', 'open', 'pe','spider_time', 'time_key', 'volume']]
        df = df[['close', 'code', 'high', 'low', 'open', 'time_key', 'volume']]
        data = bt.feeds.PandasData(dataname=df)
        engine.adddata(data, name=rule["myStocks"][0])
        # print(df)

        # if "okex.btc" in [_s.lower() for _s in _ids]:
        #     df = list(get_es_group_stacks_p(startTS=rule['startDay'],endTS=rule['endDay'],codes=rule["myStocks"], dim=rule["kline"]))[0]
        #     df["volume"] = df["updownMatrixArray"].astype(np.float64)
        #     # df["volume"] = df["volume"].astype(np.float64)
        #     # df = df[['close', 'code', 'high', 'low', 'open', 'pe','spider_time', 'time_key', 'volume']]
        #     df = df[['close', 'code', 'high', 'low', 'open', 'time_key', 'volume']]
        #     data = bt.feeds.PandasData(dataname=df)
        #     engine.adddata(data, name="OKEX.BTC")
        #     print(df)
        # # ai因子数据
        # else:
        #     partical_get_es_group__stacks = functools.partial(get_all_factor_df,
        #                                                       startTS=rule['startDay'],
        #                                                       endTS=rule['endDay'],
        #                                                       topN=rule['topN'],
        #                                                       barNum=rule['barNum'],
        #                                                       minP=rule['minP'],
        #                                                       bottomV=rule['bottomV'],
        #                                                       topV=rule['topV'],
        #                                                       longshort=rule['longshort'],
        #                                                       dim=rule["kline"]
        #                                                       )
        #     for i, d in enumerate(partical_get_es_group__stacks(_ids)):
        #         # print(d)
        #         if len(d) > max_arg:
        #             data_flag = True
        #             # print(data_flag)
        #             data = bt.feeds.PandasData(dataname=d)
        #             engine.adddata(data, name=_ids[i])

    # todo 策略计算/耗时计算
    with Timer() as timer_loop:
        ht=dict() #记录持仓天数
        bullBear=rule.get('bullBear',0) #是否作空
        engine.addstrategy(bstrategy.iStrategy, rule=rule,htrade=ht)

        # 设置启动资金
        engine.broker.setcash(startcash)
        # 定义手续费
        cs = bcomm.myCommission()
        cs.params.rule = rule
        engine.broker.addcommissioninfo(cs)
        # 定义风险控制,使用sizeutil控制
        # engine.addsizer(sizer.mySizer,rule=rule)

        # 指标监控
        # 每个数据发生的交易
        engine.addanalyzer(bt.analyzers.Transactions, _name="trs")
        # 系统质量编号
        engine.addanalyzer(bt.analyzers.SQN, _name="sqn")
        # 累计收益
        engine.addanalyzer(bt.analyzers.TimeReturn, _name="tr")
        # 年化（年收益）
        engine.addanalyzer(bt.analyzers.AnnualReturn, _name="anr")
        #engine.addanalyzer(bt.analyzers.PositionsValue, _name="pv")
        bt.analyzers.OrderedDict
        # 夏普比率
        engine.addanalyzer(bt.analyzers.SharpeRatio, _name="sr")
        # 最大回撤率
        engine.addanalyzer(bt.analyzers.DrawDown, _name="dd")
        # 提供有关已结束交易的统计信息（同时保留未结交易的计数）
        engine.addanalyzer(bt.analyzers.TradeAnalyzer, _name="ta")
        strategies = engine.run()
    # 返回结果
    portvalue = round(engine.broker.getvalue(), 2)
    pnl = round(portvalue - startcash, 2)

    # print('Final Portfolio Value: ${}'.format(portvalue))
    # print('P/L: ${}'.format(pnl))
    azs = strategies[0].analyzers
    xdd = dict()
    # print(azs.trs.get_analysis().items())
    addRecordsRs("records", xdd, azs.trs,bullBear)

    addRs("sqn", xdd, azs.sqn)
    addTrRs("timeReturn", xdd, azs.tr)
    addRs("annualReturn", xdd, azs.anr)
    #addRs("positionsValue", xdd, azs.pv)
    addRs("sharpeRatio", xdd, azs.sr)
    addRs("drawDown", xdd, azs.dd)

    addRs("tradeAnalyzer", xdd, azs.ta)

    xdd["cashvalue"] = round(engine.broker.getcash(),2)
    xdd["portvalue"] = portvalue
    xdd["pnl"] = pnl
    xdd["yield"]= round (pnl*100/startcash,2)
    xdd["use_time_es"] = f"{timer_es.cost:.2f}"
    xdd["use_time_loop"] = f"{timer_loop.cost:.2f}"
    xdd["create_time"] = f"{pendulum.now()}"
    # saveRedis(rule["strategyExecuteId"], xdd)
    del engine
    del data
    # try:
    #     xdd["startDay"] = str(list(df.index)[0])[:10]
    #     xdd["endDay"] = str(list(df.index)[-1])[:10]
    # except:
    #     pass
    xdd["sid"] = rule["sid"]
    xdd = loopresult(xdd, rule)
    return xdd