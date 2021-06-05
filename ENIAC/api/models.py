from sanic_openapi import doc

'''**********************************************************
                      >>> 策略model <<<
StrategyDto：入口，tradeCondition：交易条件，riskControl：风险控制
tradeCondition:{
                'params':{
                            'args':[], 
                            'logic':logic
                            }
                }
**********************************************************'''
class logic:
    compare = doc.String("比较方法", choices="le")
    byValue = doc.Float("比较值", choices=0.8)
    byMax = doc.Float("比较区间最大值", choices=5)

class params:
    args = doc.List(items=[doc.Integer("输入参数", choices=5)])
    logic = logic

class tradeCondition:
    modName = doc.String("模块名称", choices="ma_indicator")
    clsName = doc.String("类名称", choices="iMaCompare")
    params = params
    # params = doc.Dictionary(fileds = {"args":doc.List(items=[])})

class rule:
    tradeCondition = doc.List(tradeCondition, description="buy or sell rule")

class riskControl:
    maxRPS = doc.Float("单只股票最大资金占比", choices=0.35)
    maxAllPositionRate = doc.Float("每次交易现有资金的最大使用比例", choices=0.35)
    maxStocks = doc.Integer("最大持有股票数", choices=5)
    distribute = doc.Integer("?", choices=0)
    afterDaySell = doc.Integer("最长持有股票天数", choices=5)

class StrategyDto:
    strategyExecuteId = doc.Integer("策略job 唯一 ID 由 md5 生成", choices=1017)
    bullBear = doc.Integer("?", choices=0)
    startCash = doc.Integer("初始资金", choices=10000)
    commission = doc.Float("commission", choices=0.001)
    stampDuty = doc.Float("stampDuty", choices=0.001)
    startDay = doc.String("开始日期", choices="2018-01-01")
    endDay = doc.String("结束日期",choices="2018-11-01")
    kline = doc.String("k线类型", choices="kline_day")
    myStocks = doc.List(items=[doc.String("股票code", choices="SH.600000")])
    buyRule = rule
    sellRule = rule
    riskControl = riskControl


class APIVALIDATION:
    api_key=doc.String('api_key',choices= "e92d695f-90d1-4ca9-8adc-e54fb69841fc",)
    seceret_key=doc.String('seceret_key',choices= "5F6DDA0C9C825B360651EEF3013AA724",)
    passphrase=doc.String('passphrase 没有就传空字符串',choices= "qq2958635",)
    exchange=doc.String('交易所 OKEX HUOBI BINANCE',choices= "OKEX")

class YieldDto:
    user = doc.Integer("用户id", choices=1)
    api = doc.Integer("交易所apiID", choices=1)