import pymysql
import pandas as pd

# todo 因子运算（loop_indicators）
def compare(x,condition):
    if condition["compare"]=="gt":
        return x > condition["byValue"]
    if condition["compare"]=="ge":
        return x >= condition["byValue"]
    if condition["compare"]=="lt":
        return x < condition["byValue"]
    if condition["compare"]=="le":
        return x <= condition["byValue"]
    if condition["compare"]=="eq":
        return x == condition["byValue"]
    if condition["compare"]=="in":
        return (x > condition["byValue"] and x <= condition["byMax"])
    return

# todo 因子运算（loop_indicators）
def compare_price(x,condition):
    byValue = condition["byValue"][0]
    byMax = condition["byMax"]
    cpe = condition["compare"]
    if cpe == "gt":
        return x > byValue
    if cpe == "ge":
        return x >= byValue
    if cpe == "lt":
        return x < byValue
    if cpe == "le":
        return x <= byValue
    if cpe == "eq":
        return x == byValue
    if cpe == "in":
        return (x > byValue and x <= byMax)
    return True


def search_code_block(country, startDay=1460764800, endDay=1555372800, kline='kline_day'):
    engine = pymysql.connect("192.168.82.172", "root", "LOOP2themoon", "iquant_stock")
    sql = f"select * from t_stock_spider WHERE exchange='{country}' and status=1"
    df = pd.read_sql(sql, engine)
    _records = eval(df[['code','exchange']].to_json(orient='records'))
    _l = [{'startDay': startDay, 'endDay': endDay, 'kline': kline, 'myStocks': [_r['code']], 'market': _r['exchange']} for _r in _records]
    return _l


DAYS = '5'

PATTERNS = ['CDL2CROWS','CDL3BLACKCROWS','CDL3INSIDE','CDL3LINESTRIKE','CDL3OUTSIDE','CDL3STARSINSOUTH','CDL3WHITESOLDIERS','CDLABANDONEDBABY','CDLADVANCEBLOCK','CDLBELTHOLD','CDLBREAKAWAY','CDLCLOSINGMARUBOZU','CDLCONCEALBABYSWALL','CDLCOUNTERATTACK','CDLDARKCLOUDCOVER','CDLDOJI','CDLDOJISTAR','CDLDRAGONFLYDOJI','CDLENGULFING','CDLEVENINGDOJISTAR','CDLEVENINGSTAR','CDLGAPSIDESIDEWHITE','CDLGRAVESTONEDOJI','CDLHAMMER','CDLHANGINGMAN','CDLHARAMI','CDLHARAMICROSS','CDLHIGHWAVE','CDLHIKKAKE','CDLHIKKAKEMOD','CDLHOMINGPIGEON','CDLIDENTICAL3CROWS','CDLINNECK','CDLINVERTEDHAMMER','CDLKICKING','CDLKICKINGBYLENGTH','CDLLADDERBOTTOM','CDLLONGLEGGEDDOJI','CDLLONGLINE','CDLMARUBOZU','CDLMATCHINGLOW','CDLMATHOLD','CDLMORNINGDOJISTAR','CDLMORNINGSTAR','CDLONNECK','CDLPIERCING','CDLRICKSHAWMAN','CDLRISEFALL3METHODS','CDLSEPARATINGLINES','CDLSHOOTINGSTAR','CDLSHORTLINE','CDLSPINNINGTOP','CDLSTALLEDPATTERN','CDLSTICKSANDWICH','CDLTAKURI','CDLTASUKIGAP','CDLTHRUSTING','CDLTRISTAR','CDLUNIQUE3RIVER','CDLUPSIDEGAP2CROWS','CDLXSIDEGAP3METHODS']



# ma, macd, kdj, rsi   ema, dma, vma   boll(long,short)
TRADERATIONS_CROSS = [{"clsName": "iMacdCrossGolden","modName": "macd_indicator",
                     "params": {"args": ["12", "26", "9"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iKdjCrossGolden","modName": "kdj_indicator",
                     "params": {"args": ["9", "3", "3"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iRsiCrossGolden","modName": "rsi_indicator",
                     "params": {"args": ["6", "12", "30"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iMaCrossGolden","modName": "ma_indicator",
                     "params": {"args": ["5", "10"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iMacdCrossDie","modName": "macd_indicator",
                     "params": {"args": ["12", "26", "9"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iKdjCrossDie","modName": "kdj_indicator",
                     "params": {"args": ["9", "3", "3"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iRsiCrossDie","modName": "rsi_indicator",
                     "params": {"args": ["6", "12", "30"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iMaCrossDie","modName": "ma_indicator",
                     "params": {"args": ["5", "10"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iVmaCrossGolden","modName": "vma_indicator",
                      "params": {"args": ["5", "10"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iVmaCrossDie","modName": "vma_indicator",
                      "params": {"args": ["5", "10"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iEmaCrossGolden","modName": "ema_indicator",
                      "params": {"args": ["5", "10"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iEmaCrossDie","modName": "ema_indicator",
                      "params": {"args": ["5", "10"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iDmaCrossGolden","modName": "dma_indicator",
                      "params": {"args": ["5", "10"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iDmaCrossDie","modName": "dma_indicator",
                      "params": {"args": ["5", "10"],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    ]

TRADERATIONS_HEAD = [{"clsName": "iBollLong","modName": "boll_indicator",
                     "params": {"args": ["20", "2", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iBollShort","modName": "boll_indicator",
                     "params": {"args": ["20", "2", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iMacdLong", "modName": "macd_indicator",
                      "params": {"args": ["12", "26", "9", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                     },
                     {"clsName": "iMacdShort", "modName": "macd_indicator",
                      "params": {"args": ["12", "26", "9", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                     },
                     {"clsName": "iMaLong","modName": "ma_indicator",
                      "params": {"args": ["5", "10", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iMaShort","modName": "ma_indicator",
                      "params": {"args": ["5", "10", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iRsiLong","modName": "rsi_indicator",
                     "params": {"args": ["6", "12", "30", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iRsiShort","modName": "rsi_indicator",
                     "params": {"args": ["6", "12", "30", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iVmaLong","modName": "vma_indicator",
                      "params": {"args": ["5", "10", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iVmaShort","modName": "vma_indicator",
                      "params": {"args": ["5", "10", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iEmaLong","modName": "ema_indicator",
                      "params": {"args": ["5", "10", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iEmaShort","modName": "ema_indicator",
                      "params": {"args": ["5", "10", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                    {"clsName": "iDmaCrossLong","modName": "dma_indicator",
                      "params": {"args": ["5", "10", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     {"clsName": "iDmaCrossShort","modName": "dma_indicator",
                      "params": {"args": ["5", "10", DAYS],"logic": {"byValue": 0,"compare": "ge"}}
                     },
                     ]

TRADERATIONS = TRADERATIONS_CROSS + TRADERATIONS_HEAD

TRADERATIONS+=[{"clsName": "iPatternUp","modName": "pattern_indicator",
                 "params": {"args": ["10"],"logic": {"byValue": 0,"compare": "ge"},'line': _l,}
                 } for _l in PATTERNS]

TRADERATIONS += [{"clsName": "iPatternDown","modName": "pattern_indicator",
                 "params": {"args": ["10"],"logic": {"byValue": 0,"compare": "ge"},'line': _l}
                 } for _l in PATTERNS]