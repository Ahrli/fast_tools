# factor 计算
from binance.exceptions import BinanceAPIException
from huobi import RequestClient
from binance.client import Client
from huobi.exception.huobiapiexception import HuobiApiException
import talib
import pandas as pd
from elasticsearch import Elasticsearch
import re
from functools import reduce
from itertools import chain
import numpy as np


from . import talib_inds as tainds
from . import config
from .config import *
from pandasql import sqldf
import os
from datetime import datetime
from enum import Enum
import time
import sys
# print(sys.path)
import api.okex.account_api as account
import api.okex as okex
systemSignal = os.system('ls /.dockerenv')
print("signal",systemSignal)

KLINE_ES_SIZE = 100000

def query_es(index, code, times, autotype='qfq'):
    global df, fdf

    starttime, endtime = times.split(",")
    sql = {
        "query":
            {"bool": {"must": [{"bool": {"must": [{"term": {"code": {"value": code,"boost": 1}}},
            {"range": {"time_key": {"from": int(starttime),"to": None,"include_lower": False,"include_upper": False,"boost": 1}}}],"adjust_pure_negative": True,"boost": 1}},
            {"range": {"time_key": {"from": None,"to": int(endtime),"include_lower": False,"include_upper": False,"boost": 1}}}],"adjust_pure_negative": True,"boost": 1}},
        "_source": False,
        "stored_fields": "_none_",
        "docvalue_fields": ["close","code","create_time","high","low","open","pe","spider_time","time_key","turnover","turnover_rate","volume"],
        "sort": [{"_doc": {"order": "asc"}}]}

    adjfactor_sql = {
        "query": {"term": {"code": {"value": code,"boost": 1}}},
        "_source": False,
        "stored_fields": "_none_",
        "docvalue_fields": ["ex_div_date", "qfq_x", "qfq_y", "hfq_x", "hfq_y" ],
        "sort": [{"_doc": {"order": "asc"}}]
        }



    def serialize(hit):
        fields = hit["fields"]
        for k in fields:
            fields[k] = fields[k][0]
        return fields
    es = Elasticsearch([dbHost], http_auth=(dbUser, dbPass), port=dbPort)
    res = es.search(index=index, doc_type=index, body=sql, size=KLINE_ES_SIZE)
    hits = res["hits"]["hits"]
    df = pd.DataFrame(list(map(serialize, hits)))
    # 没有数据
    if len(df) == 0:
        return pd.DataFrame()

    # 除权数据
    df = df.sort_values(by='time_key', ascending=True)
    if autotype == 'cq':
        return df

    # 前复权，后复权数据
    # if autotype in ['qfq', 'hfq']:
    if autotype == 'qfq':
        if systemSignal == 0:
            join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date desc) group by create_time order by create_time ;"
        else:
            join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date asc) group by create_time order by create_time ;"
    elif autotype == 'hfq':
        if systemSignal == 0:
            join_sql = "select * from (select * from df left join fdf where df.create_time > fdf.ex_div_date order by fdf.ex_div_date asc) group by create_time order by create_time ;"
        else:
            join_sql = "select * from (select * from df left join fdf where df.create_time > fdf.ex_div_date order by fdf.ex_div_date desc) group by create_time order by create_time ;"
    else:
        # 不穿参数，默认除权数据
        return df

    res_adj = es.search(index='adjustments', doc_type='adjustments', body=adjfactor_sql, size=KLINE_ES_SIZE)
    hits_adj = res_adj["hits"]["hits"]
    # 查询不到复权因子，返回原始数据
    if len(hits_adj)==0:
        return df

    fdf = pd.DataFrame(list(map(serialize, hits_adj))).sort_values(by='ex_div_date', ascending=True)
    pysqldf = lambda q: sqldf(q, globals())

    qfq_df = pysqldf(join_sql)
    for i in ['close', 'open', 'low', 'high']:
        # qfq_df[f'abj_{i}'] = qfq_df[f'{i}'] * qfq_df['x'] + qfq_df['y']
        # qfq_df[f'{i}'] = qfq_df[f'{i}'] * qfq_df['x'] + qfq_df['y']
        qfq_df[f'{i}'] = qfq_df[f'{i}'] * qfq_df[f'{autotype}_x'] + qfq_df[f'{autotype}_y']
    return qfq_df

# print(query_es("adjustments_a", "HK.00023", "1546845620,1546932020")["create_time"])


def query_es_signal(index, code, interval=3600):
    sql = {
        "query": {"term": {"code": {"value": code,"boost": 1}}},
        "_source": False,
        "stored_fields": "_none_",
        "docvalue_fields": ["close","code","create_time","high","low","open","pe","spider_time","time_key","turnover","turnover_rate","volume"],
        "sort": [{"time_key": {"order": "desc"}}]
    }

    def serialize(hit):
        fields = hit["fields"]
        for k in fields:
            fields[k] = fields[k][0]
        return fields
    es = Elasticsearch([dbHost], http_auth=(dbUser, dbPass), port=dbPort)
    res = es.search(index=index, doc_type=index, body=sql, size=1)
    hits = res["hits"]["hits"]
    df = pd.DataFrame(list(map(serialize, hits))).sort_values(by='time_key', ascending=True)
    # df = pd.DataFrame(list(map(serialize, res["hits"]["hits"]))).sort_values(by='time_key', ascending=True)
    print(df)
    data = eval(df.to_json(orient='records'))
    if abs(data[0]["time_key"]-time.time()) < int(interval):
        return {"signal": int(data[0]["volume"]),"state":1, "price":data[0]["close"]}
    else:
        return {"signal": None, "state":0}


def query_es_profit_loss(stype, index, code):
    sql = {
        "query": {"term": {"code": {"value": code,"boost": 1}}},
        "_source": False,
        "stored_fields": "_none_",
        "docvalue_fields": ["close","code","create_time","high","low","open","pe","spider_time","time_key","turnover","turnover_rate","volume"],
        "sort": [{"time_key": {"order": "desc"}}]
    }

    def serialize(hit):
        fields = hit["fields"]
        for k in fields:
            fields[k] = fields[k][0]
        return fields
    es = Elasticsearch([dbHost], http_auth=(dbUser, dbPass), port=dbPort)
    res = es.search(index=index, doc_type=index, body=sql, size=100000)
    hits = res["hits"]["hits"]
    df = pd.DataFrame(list(map(serialize, hits))).sort_values(by='time_key', ascending=True)
    # df = pd.DataFrame(list(map(serialize, res["hits"]["hits"]))).sort_values(by='time_key', ascending=True)
    # print(df)
    data = eval(df.to_json(orient='records'))
    if stype=="long":
        flag = [1, -1]
    else:
        flag = [-1, 1]

    short = False
    close_price = []
    high_price = []
    low_price = []
    result_list = []
    for i in range(2,len(data)):
    # for _d in data:
        _d = data[i]
        # print(_d)
        if short == True:
            close_price.append(_d["close"])
            high_price.append(_d["high"])
            low_price.append(_d["low"])
            # if _d["volume"] == flag[1] and data[i-1] == flag[1] and data[i-2] == flag[1] :
            if _d["volume"] == flag[1]:
                # result_list.append({"开盘价":close_price[0], "平仓价":close_price[-1], "持仓天数":len(close_price),
                #                     "最低价":min(close_price), "几天后最低价":close_price.index(min(close_price)),
                #                     "最大跌幅":(min(close_price)-close_price[0])/close_price[0],"最大涨幅":(max(close_price)-close_price[0])/close_price[0],
                #                     "最终收益":(close_price[-1]-close_price[0])/close_price[0]})
                try:
                    close_price.append(data[i+1]["close"])
                    close_price.append(data[i+2]["close"])

                    high_price.append(data[i + 1]["high"])
                    high_price.append(data[i + 2]["high"])

                    low_price.append(data[i + 1]["low"])
                    low_price.append(data[i + 2]["low"])
                except:
                    pass
                result_list.append({"开盘价": close_price[2], "平仓价": close_price[-1], "持仓天数": len(close_price[2:]),
                                    # "最低价": min(close_price[2:]), "几天后最低价": close_price[2:].index(min(close_price[2:])),
                                    # "最大跌幅": (min(close_price[2:]) - close_price[2]) / close_price[2],
                                    # "最大涨幅": (max(close_price[2:]) - close_price[2]) / close_price[2],
                                    "最低价": min(low_price[2:]), "几天后最低价": low_price[2:].index(min(low_price[2:])),
                                    "最大跌幅": (min(low_price[2:]) - close_price[2]) / close_price[2],
                                    "最大涨幅": (max(high_price[2:]) - close_price[2]) / close_price[2],
                                    "最终收益": (close_price[-1] - close_price[2]) / close_price[2]})
                short = False
        else:
            # if _d["volume"] == flag[0] and data[i-1] == flag[0] and data[i-2] == flag[0]:
            if _d["volume"] == flag[0]:
                short = True
                close_price = [_d["close"]]
                high_price = [_d["high"]]
                low_price = [_d["low"]]
    return result_list




from talib import *

def EMA(df, base, target, period, alpha=False):
    """
    Function to compute Exponential Moving Average (EMA)
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        base : String indicating the column name from which the EMA needs to be computed from
        target : String indicates the column name to which the computed data needs to be stored
        period : Integer indicates the period of computation in terms of number of candles
        alpha : Boolean if True indicates to use the formula for computing EMA using alpha (default is False)
    Returns :
        df : Pandas DataFrame with new column added with name 'target'
    """

    con = pd.concat([df[:period][base].rolling(window=period).mean(), df[period:][base]])

    if (alpha == True):
        # (1 - alpha) * previous_val + alpha * current_val where alpha = 1 / period
        df[target] = con.ewm(alpha=1 / period, adjust=False).mean()
    else:
        # ((current_val - previous_val) * coeff) + previous_val where coeff = 2 / (period + 1)
        df[target] = con.ewm(span=period, adjust=False).mean()

    df[target].fillna(0, inplace=True)
    return df

def ATR(df, period, ohlc=['Open', 'High', 'Low', 'Close']):
    """
    Function to compute Average True Range (ATR)
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR)
            ATR (ATR_$period)
    """
    atr = 'ATR_' + str(period)

    # Compute true range only if it is not computed and stored earlier in the df
    if not 'TR' in df.columns:
        df['h-l'] = df[ohlc[1]] - df[ohlc[2]]
        df['h-yc'] = abs(df[ohlc[1]] - df[ohlc[3]].shift())
        df['l-yc'] = abs(df[ohlc[2]] - df[ohlc[3]].shift())

        df['TR'] = df[['h-l', 'h-yc', 'l-yc']].max(axis=1)

        df.drop(['h-l', 'h-yc', 'l-yc'], inplace=True, axis=1)

    # Compute EMA of true range using ATR formula after ignoring first row
    EMA(df,'TR', atr, period, alpha=True)
    print(ohlc[3])
    return df

def SuperTrend(df, period, multiplier, ohlc=['open', 'high', 'low', 'close']):
    """
    Function to compute SuperTrend
    Args :
        df : Pandas DataFrame which contains ['date', 'open', 'high', 'low', 'close', 'volume'] columns
        period : Integer indicates the period of computation in terms of number of candles
        multiplier : Integer indicates value to multiply the ATR
        ohlc: List defining OHLC Column names (default ['Open', 'High', 'Low', 'Close'])
    Returns :
        df : Pandas DataFrame with new columns added for
            True Range (TR), ATR (ATR_$period)
            SuperTrend (ST_$period_$multiplier)
            SuperTrend Direction (STX_$period_$multiplier)
    """

    ATR(df, period, ohlc=ohlc)
    atr = 'ATR_' + str(period)
    st = 'ST_' + str(period) + '_' + str(multiplier)
    stx = 'STX_' + str(period) + '_' + str(multiplier)

    """
    SuperTrend Algorithm :
        BASIC UPPERBAND = (HIGH + LOW) / 2 + Multiplier * ATR
        BASIC LOWERBAND = (HIGH + LOW) / 2 - Multiplier * ATR
        FINAL UPPERBAND = IF( (Current BASICUPPERBAND < Previous FINAL UPPERBAND) or (Previous Close > Previous FINAL UPPERBAND))
                            THEN (Current BASIC UPPERBAND) ELSE Previous FINALUPPERBAND)
        FINAL LOWERBAND = IF( (Current BASIC LOWERBAND > Previous FINAL LOWERBAND) or (Previous Close < Previous FINAL LOWERBAND)) 
                            THEN (Current BASIC LOWERBAND) ELSE Previous FINAL LOWERBAND)
        SUPERTREND = IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close <= Current FINAL UPPERBAND)) THEN
                        Current FINAL UPPERBAND
                    ELSE
                        IF((Previous SUPERTREND = Previous FINAL UPPERBAND) and (Current Close > Current FINAL UPPERBAND)) THEN
                            Current FINAL LOWERBAND
                        ELSE
                            IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close >= Current FINAL LOWERBAND)) THEN
                                Current FINAL LOWERBAND
                            ELSE
                                IF((Previous SUPERTREND = Previous FINAL LOWERBAND) and (Current Close < Current FINAL LOWERBAND)) THEN
                                    Current FINAL UPPERBAND
    """

    # Compute basic upper and lower bands
    df['basic_ub'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 + multiplier * df[atr]
    df['basic_lb'] = (df[ohlc[1]] + df[ohlc[2]]) / 2 - multiplier * df[atr]

    # Compute final upper and lower bands
    df['final_ub'] = 0.00
    df['final_lb'] = 0.00
    for i in range(period, len(df)):
        df['final_ub'].iat[i] = df['basic_ub'].iat[i] if df['basic_ub'].iat[i] < df['final_ub'].iat[i - 1] or \
                                                         df[ohlc[3]].iat[i - 1] > df['final_ub'].iat[i - 1] else \
        df['final_ub'].iat[i - 1]
        df['final_lb'].iat[i] = df['basic_lb'].iat[i] if df['basic_lb'].iat[i] > df['final_lb'].iat[i - 1] or \
                                                         df[ohlc[3]].iat[i - 1] < df['final_lb'].iat[i - 1] else \
        df['final_lb'].iat[i - 1]

    # Set the Supertrend value
    df[st] = 0.00
    for i in range(period, len(df)):
        df[st].iat[i] = df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[
            i] <= df['final_ub'].iat[i] else \
            df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_ub'].iat[i - 1] and df[ohlc[3]].iat[i] > \
                                     df['final_ub'].iat[i] else \
                df['final_lb'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] >= \
                                         df['final_lb'].iat[i] else \
                    df['final_ub'].iat[i] if df[st].iat[i - 1] == df['final_lb'].iat[i - 1] and df[ohlc[3]].iat[i] < \
                                             df['final_lb'].iat[i] else 0.00

        # Mark the trend direction up/down
    df[stx] = np.where((df[st] > 0.00), np.where((df[ohlc[3]] < df[st]), 'down', 'up'), np.NaN)
    df
    # Remove basic and final bands from the columns
    df.drop(['basic_ub', 'basic_lb', 'final_ub', 'final_lb'], inplace=True, axis=1)

    df.fillna(0, inplace=True)

    return df


def cq_sign(df):
    df['ma128_close'] = talib.MA(df['close'], timeperiod=128, matype=0)
    df['ma128_high'] = talib.MA(df['high'], timeperiod=128, matype=0)
    df['ma128_low'] = talib.MA(df['low'], timeperiod=128, matype=0)
    mp = 0
    lt = []
    for i in df.to_dict('records')[128:]:

        if mp == 0 and i['close'] > i['ma128_high']:  # 如果没有持仓,价格大于上轨,买入
            i['updownMatrixArray'] = 1
            mp = 1
        elif mp == 0 and i['close'] < i['ma128_low']:  # 如果没有持仓,价格小于于上轨,卖出
            i['updownMatrixArray'] = -1
            mp = -1
        else:
            i['updownMatrixArray'] = 0

        if mp == -1 and i['close'] > i['ma128_high']:  # 如果持仓 价格大于上轨,平空买入
            i['updownMatrixArray'] = 1
            mp = 1
        elif mp == 1 and i['close'] < i['ma128_low']:  # 如果持仓 价格小于下轨,平多做空
            i['updownMatrixArray'] = -1
            mp = -1
        else:
            i['updownMatrixArray'] = 0
        lt.append(i)
    df = pd.DataFrame(lt)
    df =df.drop(['ma128_low','ma128_high','ma128_close'],axis=1)

    return df

def df2factor(df,close,high,low,Open,volume):
    """
    ### 因子数量274个
    # ## 1. Overlap Studies Functions 重叠研究指标

# ```zsh
# *BBANDS               Bollinger Bands #布林带
# *DEMA                 Double Exponential Moving Average #双指数移动平均线
# *EMA                  Exponential Moving Average #指数滑动平均
# *HT_TRENDLINE         Hilbert Transform - Instantaneous Trendline #希尔伯特变换瞬时趋势
# *KAMA                 Kaufman Adaptive Moving Average #卡玛考夫曼自适应移动平均
# *MA                   Moving average #均线
# *MAMA                 MESA Adaptive Moving Average #自适应移动平均
# MAVP                 Moving average with variable period #变周期移动平均
# *MIDPOINT             MidPoint over period #在周期的中点
# *MIDPRICE             Midpoint Price over period #中间时段价格
# *SAR                  Parabolic SAR #抛物线转向指标
# *SAREXT               Parabolic SAR - Extended #抛物线转向指标 - 扩展
# *SMA                  Simple Moving Average# 简单移动平均线
# *T3                   Triple Exponential Moving Average (T3)
# *TEMA                 Triple Exponential Moving Average
# *TRIMA                Triangular Moving Average
# *WMA                  Weighted Moving Average#加权移动平均线
# ```

# ## 2. Momentum Indicators 动量指标
# all in

# ```zsh
# ADX                  Average Directional Movement Index # 平均趋向指数
# ADXR                 Average Directional Movement Index Rating # 平均趋向指数的趋向指数
# APO                  Absolute Price Oscillator #
# AROON                Aroon # 平均趋向指数的趋向指数
# AROONOSC             Aroon Oscillator # 阿隆振荡
# BOP                  Balance Of Power # 均势指标
# CCI                  Commodity Channel Index # 顺势指标
# CMO                  Chande Momentum Oscillator # 钱德动量摆动指标
# DX                   Directional Movement Index # 动向指标或趋向指标
# MACD                 Moving Average Convergence/Divergence # 平滑异同移动平均线
# MACDEXT              MACD with controllable MA type
# MACDFIX              Moving Average Convergence/Divergence Fix 12/26
# MFI                  Money Flow Index # 资金流量指标
# MINUS_DI             Minus Directional Indicator # 下升动向值
# MINUS_DM             Minus Directional Movement # 上升动向值 DMI中的DM代表正趋向变动值即上升动向值
# MOM                  Momentum # 上升动向值
# PLUS_DI              Plus Directional Indicator #
# PLUS_DM              Plus Directional Movement
# PPO                  Percentage Price Oscillator # 价格震荡百分比指标（PPO）是一个和MACD指标非常接近的指标。
# ROC                  Rate of change : ((price/prevPrice)-1)*100 # 变动率指标
# ROCP                 Rate of change Percentage: (price-prevPrice)/prevPrice #
# ROCR                 Rate of change ratio: (price/prevPrice)
# ROCR100              Rate of change ratio 100 scale: (price/prevPrice)*100
# RSI                  Relative Strength Index # 相对强弱指数
# STOCH                Stochastic # 随机指标,俗称KD
# STOCHF               Stochastic Fast
# STOCHRSI             Stochastic Relative Strength Index
# TRIX                 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
# ULTOSC               Ultimate Oscillator # 终极波动指标
# WILLR                Williams' %R # 威廉指标
# ```

# ## Pattern Recognition 形态识别
# all in

# ```zsh
# CDL2CROWS            Two Crows # 两只乌鸦
# CDL3BLACKCROWS       Three Black Crows # 三只乌鸦
# CDL3INSIDE           Three Inside Up/Down # 三内部上涨和下跌
# CDL3LINESTRIKE       Three-Line Strike # 三线打击
# CDL3OUTSIDE          Three Outside Up/Down # 三外部上涨和下跌
# CDL3STARSINSOUTH     Three Stars In The South # 南方三星
# CDL3WHITESOLDIERS    Three Advancing White Soldiers # 三个白兵
# CDLABANDONEDBABY     Abandoned Baby # 弃婴
# CDLADVANCEBLOCK      Advance Block # 大敌当前
# CDLBELTHOLD          Belt-hold # 捉腰带线
# CDLBREAKAWAY         Breakaway # 脱离
# CDLCLOSINGMARUBOZU   Closing Marubozu # 收盘缺影线
# CDLCONCEALBABYSWALL  Concealing Baby Swallow # 藏婴吞没
# CDLCOUNTERATTACK     Counterattack # 反击线
# CDLDARKCLOUDCOVER    Dark Cloud Cover # 乌云压顶
# CDLDOJI              Doji # 十字
# CDLDOJISTAR          Doji Star # 十字星
# CDLDRAGONFLYDOJI     Dragonfly Doji # 蜻蜓十字/T形十字
# CDLENGULFING         Engulfing Pattern # 吞噬模式
# CDLEVENINGDOJISTAR   Evening Doji Star # 十字暮星
# CDLEVENINGSTAR       Evening Star # 暮星
# CDLGAPSIDESIDEWHITE  Up/Down-gap side-by-side white lines # 向上/下跳空并列阳线
# CDLGRAVESTONEDOJI    Gravestone Doji # 墓碑十字/倒T十字
# CDLHAMMER            Hammer # 锤头
# CDLHANGINGMAN        Hanging Man # 上吊线
# CDLHARAMI            Harami Pattern # 母子线
# CDLHARAMICROSS       Harami Cross Pattern # 十字孕线
# CDLHIGHWAVE          High-Wave Candle # 风高浪大线
# CDLHIKKAKE           Hikkake Pattern # 陷阱
# CDLHIKKAKEMOD        Modified Hikkake Pattern # 修正陷阱
# CDLHOMINGPIGEON      Homing Pigeon # 家鸽
# CDLIDENTICAL3CROWS   Identical Three Crows # 三胞胎乌鸦
# CDLINNECK            In-Neck Pattern #  颈内线
# CDLINVERTEDHAMMER    Inverted Hammer #  颈内线
# CDLKICKING           Kicking # 反冲形态
# CDLKICKINGBYLENGTH   Kicking - bull/bear determined by the longer marubozu # 由较长缺影线决定的反冲形态
# CDLLADDERBOTTOM      Ladder Bottom # 梯底
# CDLLONGLEGGEDDOJI    Long Legged Doji # 长脚十字
# CDLLONGLINE          Long Line Candle # 长蜡烛
# CDLMARUBOZU          Marubozu # 光头光脚/缺影线
# CDLMATCHINGLOW       Matching Low # 相同低价
# CDLMATHOLD           Mat Hold # 铺垫
# CDLMORNINGDOJISTAR   Morning Doji Star # 十字晨星
# CDLMORNINGSTAR       Morning Star # 晨星
# CDLONNECK            On-Neck Pattern # 颈上线
# CDLPIERCING          Piercing Pattern # 刺透形态
# CDLRICKSHAWMAN       Rickshaw Man # 黄包车夫
# CDLRISEFALL3METHODS  Rising/Falling Three Methods # 上升/下降三法
# CDLSEPARATINGLINES   Separating Lines #  分离线
# CDLSHOOTINGSTAR      Shooting Star # 射击之星
# CDLSHORTLINE         Short Line Candle # 短蜡烛
# CDLSPINNINGTOP       Spinning Top # 纺锤
# CDLSTALLEDPATTERN    Stalled Pattern # 停顿形态
# CDLSTICKSANDWICH     Stick Sandwich # 条形三明治
# CDLTAKURI            Takuri (Dragonfly Doji with very long lower shadow) # 探水竿
# CDLTASUKIGAP         Tasuki Gap # 跳空并列阴阳线
# CDLTHRUSTING         Thrusting Pattern # 插入
# CDLTRISTAR           Tristar Pattern # 三星
# CDLUNIQUE3RIVER      Unique 3 River # 奇特三河床
# CDLUPSIDEGAP2CROWS   Upside Gap Two Crows # 向上跳空的两只乌鸦
# CDLXSIDEGAP3METHODS  Upside/Downside Gap Three Methods # 上升/下降跳空三法
# ```


#Volume_Indicators  成交量指标
AD            累积/派发线
ADOSC         震荡指标
OBV           能量潮
#Volatility_Indicator  波动性指标
ATR                  真实波动幅度均值
NATR                 归一化波动幅度均值
TRANGE               真正的范围

#Price_Transform 价格指标
AVGPRICE             平均价格函数
MEDPRICE             中位数价格
TYPPRICE             代表性价格
WCLPRICE             加权收盘价

#Cycle_Indicators 周期指标

HT_DCPERIOD          希尔伯特变换-主导周期
HT_DCPHASE           希尔伯特变换-主导循环阶段
HT_PHASOR            希尔伯特变换-希尔伯特变换相量分量
HT_SINE              希尔伯特变换-正弦波
HT_TRENDMODE         希尔伯特变换-趋势与周期模式

#Statistic_Functions 统计学指标
BETA                 β系数也称为贝塔系数
CORREL               皮尔逊相关系数
LINEARREG            线性回归
LINEARREG_ANGLE      线性回归的角度
LINEARREG_INTERCEPT  线性回归截距
LINEARREG_SLOPE      线性回归斜率指标
STDDEV               标准偏差
TSF                  时间序列预测
VAR                  方差
# Math_Transform 数学变换
ACOS                 acos函数是反余弦函数，三角函数
ASIN                 反正弦函数，三角函数
ATAN                 数字的反正切值，三角函数
CEIL                 向上取整数
COS                  余弦函数，三角函数
COSH(去掉)            双曲正弦函数，三角函数
EXP(去掉)             指数曲线，三角函数
FLOOR                向下取整数
LN                   自然对数
LOG10                对数函数log
SIN                  正弦函数，三角函数
SINH(去掉)            双曲正弦函数，三角函数
SQRT                 非负实数的平方根
TAN                  正切函数，三角函数
TANH                 双曲正切函数，三角函数

#Math_Operators 数学运算符
ADD                  向量加法运算
DIV                  向量除法运算
MAX                  周期内最大值（未满足周期返回nan）
MAXINDEX             周期内最大值的索引
MIN                  周期内最小值 （未满足周期返回nan）
MININDEX             周期内最小值的索引
MINMAX               周期内最小值和最大值
MINMAXINDEX          周期内最小值和最大值索引
MULT                 向量乘法运算
SUB                  向量减法运算
SUM                  周期内求和


    """

    '----------------------------------------------base-------------------------------------------------------'
    # 基础数据
    base = list(df.columns)

    for i in [5, 10,20,30,50,100,200]:
        for func in ['DEMA','EMA','KAMA','MA','SMA','TEMA','TRIMA','WMA']:
            df[f'{func}{i}'] = eval(f'talib.{func}')(close, i)

    for func in ['HT_TRENDLINE','MIDPOINT','T3','APO','CMO','MOM','PPO','ROC','ROCP','ROCR','ROCR100','RSI','TRIX']:
        df[f'{func}'] = eval(f'talib.{func}')(close)

    for func in ['SAR','SAREXT','MIDPRICE','AROONOSC','MINUS_DM','PLUS_DM']:
        df[f'{func}'] = eval(f'talib.{func}')(high, low)

    for func in ['ADX','ADXR','CCI','DX','MINUS_DI','PLUS_DI','ULTOSC','WILLR']:
        df[f'{func}'] = eval(f'talib.{func}')(high, low, close)

    for func in ['BOP',
                 'CDL2CROWS',
                'CDL3BLACKCROWS',
                'CDL3INSIDE',
                'CDL3LINESTRIKE',
                'CDL3OUTSIDE',
                'CDL3STARSINSOUTH',
                'CDL3WHITESOLDIERS',
                'CDLABANDONEDBABY',
                'CDLADVANCEBLOCK',
                'CDLBELTHOLD',
                'CDLBREAKAWAY',
                'CDLCLOSINGMARUBOZU',
                'CDLCONCEALBABYSWALL',
                'CDLCOUNTERATTACK',
                'CDLDARKCLOUDCOVER',
                'CDLDOJI',
                'CDLDOJISTAR',
                'CDLDRAGONFLYDOJI',
                'CDLENGULFING',
                'CDLEVENINGDOJISTAR',
                'CDLEVENINGSTAR',
                'CDLGAPSIDESIDEWHITE',
                'CDLGRAVESTONEDOJI',
                'CDLHAMMER',
                'CDLHANGINGMAN',
                'CDLHARAMI',
                'CDLHARAMICROSS',
                'CDLHIGHWAVE',
                'CDLHIKKAKE',
                'CDLHIKKAKEMOD',
                'CDLHOMINGPIGEON',
                'CDLIDENTICAL3CROWS',
                'CDLINNECK',
                'CDLINVERTEDHAMMER',
                'CDLKICKING',
                'CDLKICKINGBYLENGTH',
                'CDLLADDERBOTTOM',
                'CDLLONGLEGGEDDOJI',
                'CDLLONGLINE',
                'CDLMARUBOZU',
                'CDLMATCHINGLOW',
                'CDLMATHOLD',
                'CDLMORNINGDOJISTAR',
                'CDLMORNINGSTAR',
                'CDLONNECK',
                'CDLPIERCING',
                'CDLRICKSHAWMAN',
                'CDLRISEFALL3METHODS',
                'CDLSEPARATINGLINES',
                'CDLSHOOTINGSTAR',
                'CDLSHORTLINE',
                'CDLSPINNINGTOP',
                'CDLSTALLEDPATTERN',
                'CDLSTICKSANDWICH',
                'CDLTAKURI',
                'CDLTASUKIGAP',
                'CDLTHRUSTING',
                'CDLTRISTAR',
                'CDLUNIQUE3RIVER',
                'CDLUPSIDEGAP2CROWS',
                'CDLXSIDEGAP3METHODS',]:
        df[f'{func}'] = eval(f'talib.{func}')(Open, high, low, close)
    df['BBANDS_upperband'], df['BBANDS_middleband'], df['BBANDS_lowerband'] = talib.BBANDS(close)
    df['MAMA_mama'], df['MAMA_fama'] = talib.MAMA(close)
    df['MACD_macd'], df['MACD_macdsignal'], df['MACD_macdhist'] = talib.MACD(close)
    df['MACDEXT_macd'], df['MACDEXT_macdsignal'], df['MACDEXT_macdhist'] = talib.MACDEXT(close)
    df['MACDFIX_macd'], df['MACDFIX_macdsignal'], df['MACDFIX_macdhist'] = talib.MACDFIX(close)
    df['STOCH_slowk'], df['STOCH_slowd'] = talib.STOCH(high, low, close)
    df['STOCHF_fastk'], df['STOCHF_fastd'] = talib.STOCHF(high, low, close)
    df['STOCHRSI_fastk'], df['STOCHRSI_fastd'] = talib.STOCHRSI(close)
    df['AROON_aroondown'], df['AROON_aroonup'] = talib.AROON(high, low)
    #df['MFI'] = talib.MFI(high, low, close, volume)
    df['KDJ_k'], df['KDJ_d'], df['KDJ_j'] = tainds.talib_KDJ(high, low, close)
    for i in [5, 10,20,30,50,100,200]:
        df[f'VOLUMEMA{i}'] = talib.SMA(volume, i)
    try:
        df['DMA_dma'], df['DMA_ama'] = tainds.talib_DMA(close)
    except:
        df['DMA_dma'], df['DMA_ama'] =0, 0




    '----------------------------------------------Volume_Indicators  成交量指标-------------------------------------------------------'

    for func in ['AD','ADOSC']:
        df[f'{func}'] = eval(f'talib.{func}')(high, low, close, volume)

    for func in ['OBV']:
            df[f'{func}'] = eval(f'talib.{func}')( close, volume)

    '----------------------------------------------Volatility_Indicator  波动性指标-------------------------------------------------------'

    for func in ['ATR','NATR','TRANGE']:
        df[f'{func}'] = eval(f'talib.{func}')(high, low, close)


    '----------------------------------------------Price_Transform 价格指标-------------------------------------------------------'

    for func in ['AVGPRICE']:
        df[f'{func}'] = eval(f'talib.{func}')(Open, high, low, close)

    for func in ['MEDPRICE']:
        df[f'{func}'] = eval(f'talib.{func}')(high, low)

    for func in ['TYPPRICE','WCLPRICE']:
        df[f'{func}'] = eval(f'talib.{func}')(high, low, close)

    '----------------------------------------------Cycle_Indicators 周期指标-------------------------------------------------------'

    for func in ['HT_DCPERIOD','HT_DCPHASE','HT_TRENDMODE',]:
        df[f'{func}'] = eval(f'talib.{func}')(close)

    df['HT_PHASOR_inphase'], df['HT_PHASOR_quadrature'] = talib.HT_PHASOR(close)
    df['HT_SINE_sine'], df['HT_SINE_leadsine'] = talib.HT_SINE(close)

    '----------------------------------------------Statistic_Functions 统计学指标 -------------------------------------------------------'

    for func in ['BETA','CORREL']:
        df[f'{func}'] = eval(f'talib.{func}')(high, low)

    for func in ['LINEARREG','LINEARREG_ANGLE','LINEARREG_INTERCEPT','LINEARREG_SLOPE','STDDEV','TSF','VAR',]:
        df[f'{func}'] = eval(f'talib.{func}')(close)

    '----------------------------------------------Math_Transform 数学变换 -------------------------------------------------------'

    for func in ['ACOS', 'ASIN', 'ATAN', 'CEIL','COS', 'FLOOR','LN', 'LOG10', 'SIN','SQRT', 'TAN', 'TANH']:
        df[f'{func}'] = eval(f'talib.{func}')(close)


    '----------------------------------------------Math_Operators 数学运算符-------------------------------------------------------'

    for func in ['ADD', 'DIV', 'MULT', 'SUB']:
        df[f'{func}'] = eval(f'talib.{func}')(high, low)

    for func in [ 'MAX', 'MAXINDEX', 'MIN', 'MININDEX', 'SUM']:
        df[f'{func}'] = eval(f'talib.{func}')(close)

    df['MINMAXINDEX_minidx'], df['MINMAXINDEX_maxidx'] = talib.MINMAXINDEX(close)
    df['MINMAX_min'], df['MINMAX_max'] = talib.MINMAX(close)


    # 计算完成之后
    ndf = df.tail(1)
    ndf = ndf.fillna(0)


    '----------------------------------------------Volume_Indicators  成交量指标------------------------------------------------------------------'
    Volume_Indicators = ['AD','ADOSC','OBV']
    '----------------------------------------------Volatility_Indicator  波动性指标---------------------------------------------------------------'
    Volatility_Indicator = ['ATR','NATR','TRANGE']

    '----------------------------------------------Price_Transform 价格指标----------------------------------------------------------------------'
    Price_Transform =  ['AVGPRICE','MEDPRICE','TYPPRICE','WCLPRICE']

    '----------------------------------------------Cycle_Indicators 周期指标---------------------------------------------------------------------'
    Cycle_Indicators =  ['HT_DCPERIOD','HT_DCPHASE','HT_TRENDMODE','HT_PHASOR_inphase','HT_PHASOR_quadrature','HT_SINE_sine','HT_SINE_leadsine']


    '----------------------------------------------Statistic_Functions 统计学指标 ---------------------------------------------------------------'
    Statistic_Functions =  ['BETA','CORREL','LINEARREG','LINEARREG_ANGLE','LINEARREG_INTERCEPT','LINEARREG_SLOPE','STDDEV','TSF','VAR']

    '----------------------------------------------Math_Transform 数学变换 ----------------------------------------------------------------------'

    Math_Transform = ['ACOS', 'ASIN', 'ATAN', 'CEIL', 'COS',  'FLOOR', 'LN', 'LOG10', 'SIN',  'SQRT',
                 'TAN', 'TANH']
    '----------------------------------------------Math_Operators 数学运算符---------------------------------------------------------------------'
    Math_Operators = ['ADD', 'DIV', 'MULT', 'SUB','MAX', 'MAXINDEX', 'MIN', 'MININDEX', 'SUM','MINMAXINDEX_minidx','MINMAXINDEX_maxidx','MINMAX_min','MINMAX_max']



    '----------------------------------------------Pattern_Recognition-------------------------------------------------------'
    # 形态学指标
    pattern_recognition = list(ndf[[i for i in list(df.columns) if i[:3] == "CDL"]])

    '----------------------------------------------Momentum_Indicators-------------------------------------------------------'
    # 动量类指标
    momentum_indicators =  ['ADX',
                            'ADXR',
                            'APO',
                            'AROON_aroondown',
                            'AROON_aroonup',
                            'AROONOSC',
                            'BOP',
                            'CCI',
                            'CMO',
                            'DX',
                            'MACD_macd',
                            'MACD_macdsignal',
                            'MACD_macdhist',
                            'MACDEXT_macd',
                            'MACDEXT_macdsignal',
                            'MACDEXT_macdhist',
                            'MACDFIX_macd',
                            'MACDFIX_macdsignal',
                            'MACDFIX_macdhist',
                            #'MFI',
                            'MINUS_DI',
                            'MINUS_DM',
                            'MOM',
                            'PLUS_DI',
                            'PLUS_DM',
                            'PPO',
                            'ROC',
                            'ROCR',
                            'ROCR100',
                            'RSI',
                            'STOCH_slowk',
                            'STOCH_slowd',
                            'STOCHF_fastk',
                            'STOCHF_fastd',
                            'STOCHRSI_fastk',
                            'STOCHRSI_fastd',
                            'TRIX',
                            'ULTOSC',
                            'WILLR',
                            # 'KDJ',
                            # 'DMA',
                            # 'VOLUMEMA',
                            ]

    '----------------------------------------------Overlap_Studies_Functions-------------------------------------------------------'
    # 重叠指标
    overlap_studies_functions = ['DEMA5', 'EMA5', 'KAMA5', 'MA5', 'SMA5', 'TEMA5', 'TRIMA5', 'WMA5', 'DEMA10', 'EMA10', 'KAMA10', 'MA10', 'SMA10', 'TEMA10', 'TRIMA10', 'WMA10', 'DEMA20', 'EMA20', 'KAMA20', 'MA20', 'SMA20', 'TEMA20', 'TRIMA20', 'WMA20', 'DEMA30', 'EMA30', 'KAMA30', 'MA30', 'SMA30', 'TEMA30', 'TRIMA30', 'WMA30', 'DEMA50', 'EMA50', 'KAMA50', 'MA50', 'SMA50', 'TEMA50', 'TRIMA50', 'WMA50', 'DEMA100', 'EMA100', 'KAMA100', 'MA100', 'SMA100', 'TEMA100', 'TRIMA100', 'WMA100', 'DEMA200', 'EMA200', 'KAMA200', 'MA200', 'SMA200', 'TEMA200', 'TRIMA200', 'WMA200', 'HT_TRENDLINE', 'MIDPOINT', 'T3', 'ROCP', 'SAR', 'SAREXT', 'MIDPRICE', 'BBANDS_upperband', 'BBANDS_middleband', 'BBANDS_lowerband', 'MAMA_mama', 'MAMA_fama', 'KDJ_k', 'KDJ_d', 'KDJ_j', 'VOLUMEMA5', 'VOLUMEMA10', 'VOLUMEMA20', 'VOLUMEMA30', 'VOLUMEMA50', 'VOLUMEMA100', 'VOLUMEMA200', 'DMA_dma', 'DMA_ama']
    #
    # overlap_studies_functions = [i for i in list(df.columns) if
    #                              i not in base + pattern_recognition + momentum_indicators+Volume_Indicators+ Volatility_Indicator+Price_Transform+Cycle_Indicators+Statistic_Functions
    #                              +Math_Transform+Math_Operators]

    '----------------------------------------------Loop_MA-------------------------------------------------------'
    # iQuant指标
    iquant_indicators  =   {'CLOSECHANGE': 0,    # 股价连续变化N天
                            'MA5CHANGE': 0,      # 5日均线连续变化N天
                            'MA10CHANGE': 0,     # 10日均线连续变化N天
                            'MA20CHANGE': 0,     # 20日均线连续变化N天
                            'LMA5': 0,           # 股价低于5日均线
                            'LMA10': 0,          # 股价低于10日均线
                            'LMA20': 0,          # 股价低于20日均线
                            'HMA5': 0,           # 股价高于5日均线
                            'HMA10': 0,          # 股价高于10日均线
                            'HMA20': 0,          # 股价高于20日均线
                            'LONGPOSITION5': 0,  # 多头排列连续5天
                            'SHORTPOSITION5': 0, # 空头排列连续5天
                            'MA5HMA10': 0,       # 5日均线高于10日均线
                            'MA5HMA20': 0,       # 5日均线高于20日均线
                            'MA5LMA10': 0,       # 5日均线低于10日均线
                            'MA5LMA20': 0,       # 5日均线低于20日均线
                            # VOLUME
                            'VOLUMEMA5CHANGE': 0,      # 5日均线连续变化N天
                            'VOLUMEMA10CHANGE': 0,  # 10日均线连续变化N天
                            'VOLUMEMA20CHANGE': 0,  # 20日均线连续变化N天
                            'LVOLUMEMA5': 0,  # 股价低于5日均线
                            'LVOLUMEMA10': 0,  # 股价低于10日均线
                            'LVOLUMEMA20': 0,  # 股价低于20日均线
                            'HVOLUMEMA5': 0,  # 股价高于5日均线
                            'HVOLUMEMA10': 0,  # 股价高于10日均线
                            'HVOLUMEMA20': 0,  # 股价高于20日均线
                            'VOLUMEMALONG5': 0,  # 多头排列连续5天
                            'VOLUMEMASHORT5': 0,  # 空头排列连续5天
                            'VOLUMEMA5HVOLUMEMA10': 0,  # 5日均线高于10日均线
                            'VOLUMEMA5HVOLUMEMA20': 0,  # 5日均线高于20日均线
                            'VOLUMEMA5LVOLUMEMA10': 0,  # 5日均线低于10日均线
                            'VOLUMEMA5LVOLUMEMA20': 0,  # 5日均线低于20日均线
                            # DMA, KDJ, MACD
                            'DMALONG5': 0,       # 5日DMA多头
                            'DMASHORT5': 0,      # 5日DMA空头
                            'KDJLONG5': 0,       # 5日DMA空头
                            'KDJSHORT5': 0,      # 5日DMA空头
                            'MACDLONG5': 0,      # 5日DMA空头
                            'MACDSHORT5': 0,      # 5日DMA空头
                            }

    # MA/VMA均线大小比较
    for i in ['MA5','MA10','MA20']:
        if float(ndf['close']) > float(ndf[i]):
            iquant_indicators[f'H{i}'] = 1
        if float(ndf['close']) < float(ndf[i]):
            iquant_indicators[f'L{i}'] = 1
    for i in ['MA10','MA20']:
        if float(ndf['MA5']) > float(ndf[i]):
            iquant_indicators[f'MA5H{i}'] = 1
        if float(ndf['MA5']) < float(ndf[i]):
            iquant_indicators[f'MA5L{i}'] = 1
    for i in ['VOLUMEMA5', 'VOLUMEMA10', 'VOLUMEMA20']:
        if float(ndf['volume']) > float(ndf[i]):
            iquant_indicators[f'H{i}'] = 1
        if float(ndf['volume']) < float(ndf[i]):
            iquant_indicators[f'L{i}'] = 1
    for i in ['VOLUMEMA10', 'VOLUMEMA20']:
        if float(ndf['VOLUMEMA5']) > float(ndf[i]):
            iquant_indicators[f'VOLUMEMA5H{i}'] = 1
        if float(ndf['VOLUMEMA5']) < float(ndf[i]):
            iquant_indicators[f'VOLUMEMA5L{i}'] = 1

    #连续变化N天
    def continuous_change(_array):
        # 后项减前项 / 后项减前项的模  = 后项相对于前项的涨跌 （涨 1 跌 -1 为 nan 不涨不跌）
        seq = np.diff(_array) / np.abs(np.diff(_array))
        nseq = [1]
        for i, value in enumerate(seq):
            #判断 nan
            if value == value:
                nseq.append(value)
            else:
                nseq.append(nseq[-1])
        symbol = nseq[-1]
        for i, value in enumerate(nseq[::-1]):
            if value != nseq[-1]:
                return int(symbol * i + symbol)
        return 0

    iquant_indicators['CLOSECHANGE'] = continuous_change(_array = list(df['close']))
    iquant_indicators['MA5CHANGE'] = continuous_change(_array = list(df['MA5']))
    iquant_indicators['MA10CHANGE'] = continuous_change(_array = list(df['MA10']))
    iquant_indicators['MA20CHANGE'] = continuous_change(_array = list(df['MA20']))
    # volumema 连续变化N天
    iquant_indicators['VOLUMEMA5CHANGE'] = continuous_change(_array=list(df['VOLUMEMA5']))
    iquant_indicators['VOLUMEMA10CHANGE'] = continuous_change(_array=list(df['VOLUMEMA10']))
    iquant_indicators['VOLUMEMA20CHANGE'] = continuous_change(_array=list(df['VOLUMEMA20']))

    # SMA(ma, volumema, ...)连续5天多、空头
    idf = df.tail(5)
    def long_short_five(sma_columns):
        ss5 = set(reduce(chain, [list(idf[sma_columns[i]] > idf[sma_columns[i + 1]]) for i in range(len(sma_columns) - 1)]))
        if len(ss5) == 2:
            lp5 = 0
            sp5 = 0
        elif True in ss5:
            lp5 = 1
            sp5 = 0
        else:
            lp5 = 0
            sp5 = 1
        return lp5, sp5

    iquant_indicators['LONGPOSITION5'], iquant_indicators['SHORTPOSITION5'] = long_short_five(["close", "MA5", "MA10", "MA20"])
    iquant_indicators['VOLUMEMALONG5'], iquant_indicators['VOLUMEMASHORT5'] = long_short_five(["close", "VOLUMEMA5", "VOLUMEMA10", "VOLUMEMA20"])

    # DMA 连续5天多、空头
    dmas = list(idf['DMA_dma'])
    amas = list(idf['DMA_ama'])
    dmalong = set(list(map(lambda d: d > 0, dmas + amas)) + list(map(lambda s: sorted(s) == s, [dmas, amas])))
    dmashort = set(list(map(lambda d: d < 0, dmas + amas)) + list(map(lambda s: sorted(s, reverse=True) == s, [dmas, amas])))
    if len(dmalong) == 1 and True in dmalong:
        iquant_indicators['DMALONG5'] = 1
    if len(dmashort) == 1 and True in dmashort:
        iquant_indicators['DMASHORT5'] = 1

    # KDJ 连续5天多、空头
    ks = list(idf['KDJ_k'])
    ds = list(idf['KDJ_d'])
    js = list(idf['KDJ_j'])
    kdjlong = set(list(map(lambda d: d > 50, ks + ds + js)) + [sorted(s, reverse=True) == s for s in zip(js, ds, ks)])
    if len(kdjlong) == 1 and True in kdjlong:
        iquant_indicators['KDJLONG5'] = 1
    kdjshort = set(list(map(lambda d: d > 50, ks + ds + js)) + [sorted(s) == s for s in zip(js, ds, ks)])
    if len(kdjshort) == 1 and True in kdjshort:
        iquant_indicators['KDJSHORT5'] = 1

    # MACD 连续5天多，空头
    difs = list(idf['MACD_macd'])
    deas = list(idf['MACD_macdsignal'])
    macdlong = set(list(map(lambda d: d > 0, difs + deas)))
    if len(macdlong) == 1 and True in macdlong:
        iquant_indicators['MACDLONG5'] = 1
    macdshort = set(list(map(lambda d: d < 0, difs + deas)))
    if len(macdshort) == 1 and True in macdshort:
        iquant_indicators['MACDSHORT5'] = 1

    # BOLL 上穿上轨， 下轨、 中规、  下穿上、中、下  连续5天
    def BOLL_cross(band):
        up_flag, down_flag = 0, 0
        close_band = np.array(idf.close.values)
        r = list(map(lambda d: 1 if d > 0 else 0, close_band - band))
        cross_result = [r[i + 1] - r[i] for i in range(len(r) - 1)]
        if 1 in cross_result:
            up_flag = 1
        if -1 in cross_result:
            down_flag = 1
        return up_flag, down_flag

    ups, mids, lows = map(np.array, [idf.BBANDS_upperband.values, idf.BBANDS_middleband.values, idf.BBANDS_lowerband.values])
    iquant_indicators['BOLLUPTOP'], iquant_indicators['BOLLDOWNTOP'] = BOLL_cross(ups)
    iquant_indicators['BOLLUPMID'], iquant_indicators['BOLLDOWNMID'] = BOLL_cross(mids)
    iquant_indicators['BOLLUPLOW'], iquant_indicators['BOLLDOWNLOW'] = BOLL_cross(lows)

    # BOLL 开口宽带窄 连续5天  WIDTH=（布林上限值－布林下限值）/布林股价平均值 < 0.10  宽带窄
    widths = (ups - lows) / mids
    if 0 in [1 if w < 0.1 else 0 for w in widths]:
        iquant_indicators['BOLLWIDTHSMALL5'] = 0
    else:
        iquant_indicators['BOLLWIDTHSMALL5'] = 1

    '----------------------------------------------tradingview-------------------------------------------------------'
    t_df = SuperTrend(df,7,3)
    t_df_data = (t_df.tail(1).to_dict('recoders'))[0]



    '----------------------------------------------result-------------------------------------------------------'
    result = {
        #"create_time":1540952558,
        #"use_time":13,
        "base":eval(ndf[base].to_json(orient='records'))[0],
        "Overlap_Studies_Functions":eval(ndf[overlap_studies_functions].to_json(orient='records'))[0],
        "Momentum_Indicators":eval(ndf[momentum_indicators].to_json(orient='records'))[0],
        "Pattern_Recognition":eval(ndf[pattern_recognition].to_json(orient='records'))[0],
        "Volume_Indicators":eval(ndf[Volume_Indicators ].to_json(orient='records'))[0],
        "Volatility_Indicator":eval(ndf[Volatility_Indicator ].to_json(orient='records'))[0],
        "Price_Transform":eval(ndf[Price_Transform ].to_json(orient='records'))[0],
        "Cycle_Indicators":eval(ndf[Cycle_Indicators ].to_json(orient='records'))[0],
        "Statistic_Functions":eval(ndf[Statistic_Functions ].to_json(orient='records'))[0],
        "Math_Transform":eval(ndf[Math_Transform ].to_json(orient='records'))[0],
        "Math_Operators":eval(ndf[Math_Operators ].to_json(orient='records'))[0],
        "Loop_MA": iquant_indicators,
        "tradingview":{'supertrend':t_df_data['ST_7_3']}
        }
    return result


def loop_cls_re(result):
    '''

    :param result: put数据流
    :return: 模块名称
    '''
    name = re.findall('filename="(.*?)"', result)[0]
    content = re.sub('(.*?\r\n.*?\r\n.*?\r\n\r\n)', '', result)
    content = re.sub('(\r\n----------------------------.*)', '', content)
    with open(f'api/btscript/{name}', 'w') as w:
        w.write(content)
    name = name.replace('.py', '')
    return name


class SecondsConvert(Enum):
    kline_min1 = 60
    kline_min5 = 300
    kline_min15 = 900
    kline_min30 = 1800
    kline_min60 = 3600
    kline_min120 = 7200
    kline_min240 = 14400
    kline_min720 = 43200
    kline_day = 86400

def query_es_kline_series(index, code):

    sql = {
        "query": {
            "term": {"code": {"value": code,"boost": 1}}
            },
        "_source": False,
        "stored_fields": "_none_",
        "aggregations": {"groupby":
                             {"composite":
                                  { "size": 1,"sources": [{"54548300": {"terms": {"field": "code","order": "asc"}}}]},
                                    "aggregations": {"54548317": {"stats": {"field": "time_key"}}}
                            }
                         }
        }

    es = Elasticsearch([dbHost], http_auth=(dbUser, dbPass), port=dbPort)
    res = es.search(index=index, doc_type=index, body=sql, size=1)
    gorupby_result = res["aggregations"]["groupby"]["buckets"][0]["54548317"]
    # 计算实际bar
    # dt1 = datetime.utcfromtimestamp(int(gorupby_result["min"]))
    # dt2 = datetime.utcfromtimestamp(int(gorupby_result["max"]))
    gorupby_result["calculate_bar"] = (int(gorupby_result["max"])-int(gorupby_result["min"])+86400)/eval(f"SecondsConvert.{index}.value")

    # df = query_es(index, code, f"{int(gorupby_result['min'])},{int(gorupby_result['max'])}", "cq")

    query_all = {
        "query": {"term": {"code": {"value": code,"boost": 1}}},
        "_source": False,
        "stored_fields": "_none_",
        "docvalue_fields": [
            "close",
            "code",
            "create_time",
            "high",
            "low",
            "open",
            "pe",
            "spider_time",
            "time_key",
            "turnover",
            "turnover_rate",
            "volume"
        ],
        "sort": [{"time_key": {"order": "asc"}} ]
    }

    res_all = es.search(index=index, doc_type=index, body=query_all, size=KLINE_ES_SIZE)

    def serialize(hit):
        fields = hit["fields"]
        for k in fields:
            fields[k] = fields[k][0]
        return fields

    hits = res_all["hits"]["hits"]
    df = pd.DataFrame(list(map(serialize, hits)))
    # 除权数据
    df = df.sort_values(by='time_key', ascending=True)

    time_key_diff = list(np.diff(list(df["time_key"])))
    diffdata = {}
    for i in set(time_key_diff):
        diffdata[str(i)] = time_key_diff.count(i)
    gorupby_result["data"] = diffdata
    gorupby_result["period"] = eval(f"SecondsConvert.{index}.value")

    return gorupby_result



def ApiValidation(dc):
    '''
    添加三个交易所验证
    :param dc:
    :return:
    '''
    if dc is None:
        return False,'参数缺少'
    dc_keys=list(dc.keys())
    for i in dc_keys:
        if i not in ['exchange','api_key','seceret_key','passphrase']:
            return False,'参数名称错误'
    globals().update(dc)

    if dc.get('exchange',"") == "OKEX":
        accountAPI = account.AccountAPI(api_key, seceret_key, passphrase, False)
        try:
            data = accountAPI.get_wallet()
            return True, 1, 'API正确'
        except okex.exceptions.OkexAPIException as e:
            if e.code == 30006:
                return False, -1, "Api Key 错误"     #api_key 错误
            if e.code == 30013:
                return False, -2, "Secret Key 错误"  #seceret_key 错误
            if e.code == 30015:
                return False, -3, "PassPharse 错误"  #passphrase 错误
        return False, 0, "未知错误，稍后重试" # 未知错误，稍后重试

    elif dc.get('exchange',"") == "BINANCE":
        proxies = {
            'https': 'https://192.168.80.196:18181',
            'http': 'http://192.168.80.196:18181'
        }
        try:
            client = Client(api_key, seceret_key, {"verify": False, "timeout": 20, 'proxies': proxies})
            client.get_account()
            return True, 1, 'API正确'
        except BinanceAPIException as e:
            if e.code == -2014:
                return False, -1, "Api Key 错误"  #api_key 错误
            if e.code == -1022:
                return False, -2, "Secret Key 错误"  #seceret_key 错误
        return False, 0, "未知错误，稍后重试"  # 未知错误，稍后重试

    elif dc.get('exchange',"")== "HUOBI":
        try:
            request_client = RequestClient(api_key=api_key, secret_key=seceret_key)
            account_balance_list = request_client.get_account_balance()
            return True, 1, 'API正确'
        except HuobiApiException as e:
            # if e.args[0]=='ExecuteError':
            if "Access key错误" in e.args[1]:
                return False, -1, "Api Key 错误"   #api_key 错误
            if "校验失败" in e.args[1]:
                return False, -2, "Secret Key 错误" # seceret_key 错误
        return False, 0, "未知错误，稍后重试"  # 未知错误，稍后重试
    else:
        return False, -4, f'exchange error'

