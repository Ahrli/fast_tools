# factor 计算
import talib
import numpy as np
from . import talib_inds as tainds
import pandas as pd



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


def Overlap_Sign(inds_dict, close):
    rds = []
    for _k in inds_dict:
        if inds_dict[_k]>close:
            rds.append([str(_k), inds_dict[_k], -1])
        elif inds_dict[_k]<close:
            rds.append([str(_k), inds_dict[_k], 1])
        else:
            rds.append([str(_k), inds_dict[_k], 0])
    return rds

def Momentum_Sign(inds_list, close):
    # rsi、cci、TRIX、macd、Williams、MFI、Slow Stochastic、Fast Stochastic、Chaikin Osc、ADX、ADXR、APO、Aroon、
    # Aroon Oscillitor、ATR、Beta、Chande Momentum、CORREL、DEMA、Directional Movement、Momentum、NATR、OBV、
    # Rate of Change、ROCP、ROCR、STOCHRSI 5K(5)D(3)、TSF、Ultimate Oscillator(7、14、28)

    inds_dict = inds_list[-1]
    inds_dict_0 = inds_list[0]
    rds = []
    # RSI buy: <30，sell：> 70
    if inds_dict["RSI"]<30:
        rds.append(["RSI", inds_dict["RSI"], 1])
    elif inds_dict["RSI"]>70:
        rds.append(["RSI", inds_dict["RSI"], -1])
    else:
        rds.append(["RSI", inds_dict["RSI"], 0])

    # CCI buy: <-100，sell：> 100
    if inds_dict["CCI"] < -100:
        rds.append(["CCI", inds_dict["CCI"], 1])
    elif inds_dict["RSI"] > 100:
        rds.append(["CCI", inds_dict["CCI"], -1])
    else:
        rds.append(["CCI", inds_dict["CCI"], 0])

    # TRIX 上穿0线买入信号：
    if inds_dict["TRIX"] > 0:
        rds.append(["TRIX", inds_dict["TRIX"], 1])
    elif inds_dict["TRIX"] < 0:
        rds.append(["TRIX", inds_dict["TRIX"], -1])
    else:
        rds.append(["TRIX", inds_dict["TRIX"], 0])

    # MACD 0线以上买入信号：
    if inds_dict["MACD_macd"] > 0:
        rds.append(["MACD_macd", inds_dict["MACD_macd"], 1])
    elif inds_dict["MACD_macd"] < 0:
        rds.append(["MACD_macd", inds_dict["MACD_macd"], -1])
    else:
        rds.append(["MACD_macd", inds_dict["MACD_macd"], 0])

    # WILLR W&R指标线全部低于-80, 超卖; 高于-20，超买状态
    if inds_dict["WILLR"] < -80:
        rds.append(["WILLR", inds_dict["WILLR"], 1])
    elif inds_dict["WILLR"] > -20:
        rds.append(["WILLR", inds_dict["WILLR"], -1])
    else:
        rds.append(["WILLR", inds_dict["WILLR"], 0])

    # # MFI 低于20, 超卖; 高于80，超买状态 -1  # talib没有mfi  1、典型价格(TP)=当日最高价、最低价与收盘价的算术平均值 2、货币流量（MF）=典型价格（TYP）×N日内成交金额 3、MFI=100-［100/（1+PMF/NMF）］
    # if inds_dict["MFI"] < 30:
    #     rds["MFI"] = [inds_dict["MFI"], 1]
    # elif inds_dict["MFI"] > 70:
    #     rds["MFI"] = [inds_dict["MFI"], -1]
    # else:
    #     rds["MFI"] = [inds_dict["MFI"], 0]

    # STOCH_slowk <20 买 >80 卖
    if inds_dict["STOCH_slowk"] < 20:
        rds.append(["STOCH_slowk", inds_dict["STOCH_slowk"], 1])
    elif inds_dict["STOCH_slowk"] > 80:
        rds.append(["STOCH_slowk", inds_dict["STOCH_slowk"], -1])
    else:
        rds.append(["STOCH_slowk", inds_dict["STOCH_slowk"], 0])

    # 'STOCHF_fastk', 'STOCHF_fastd'
    if inds_dict["STOCHF_fastk"] < 20 and inds_dict["STOCHF_fastd"] < 20:
        rds.append(["STOCHF_fastk", inds_dict["STOCHF_fastk"], 1])
    elif inds_dict["STOCHF_fastk"] > 80 and inds_dict["STOCHF_fastd"] > 80:
        rds.append(["STOCHF_fastk", inds_dict["STOCHF_fastk"], -1])
    else:
        rds.append(["STOCHF_fastk", inds_dict["STOCHF_fastk"], 0])

    # ADX指标 adx指标的进场信号是+di线穿越adx线，出场信号是-di线穿越adx线。 +di=pdi, -di=mdi
    if inds_dict_0["PLUS_DI"] < inds_dict_0["ADX"] and inds_dict["PLUS_DI"] > inds_dict["ADX"]:
        rds.append(["ADX", inds_dict["ADX"], 1])
    elif inds_dict_0["MINUS_DI"] > inds_dict_0["ADX"] and inds_dict["MINUS_DI"] < inds_dict["ADX"]:
        rds.append(["ADX", inds_dict["ADX"], -1])
    else:
        rds.append(["ADX", inds_dict["ADX"], 0])

    # ADXR
    if inds_dict["PLUS_DI"] > inds_dict["MINUS_DI"] and inds_dict["ADX"] > inds_dict["ADXR"]:
        rds.append(["ADXR", inds_dict["ADXR"], 1])
    elif inds_dict["PLUS_DI"] < inds_dict["MINUS_DI"] and inds_dict["ADX"] < inds_dict["ADXR"]:
        rds.append(["ADXR", inds_dict["ADXR"], -1])
    else:
        rds.append(["ADXR", inds_dict["ADXR"], 0])

    # APO 当APO上穿0，表示买入信号；
    if inds_dict_0["APO"] <0 and inds_dict["APO"] > 0:
        rds.append(["APO", inds_dict["APO"], 1])
    elif inds_dict_0["APO"] > 0 and inds_dict["APO"] < 0:
        rds.append(["APO", inds_dict["APO"], -1])
    else:
        rds.append(["APO", inds_dict["APO"], 0])


    # Aroon AROON_aroonup 高于70，表示强势上涨；AROON_aroondown 超过70，表示强势下降；
    if inds_dict["AROON_aroonup"] >70:
        rds.append(["AROON", inds_dict["AROON_aroonup"], 1])
    elif inds_dict["AROON_aroondown"] <50:
        rds.append(["AROON", inds_dict["AROON_aroondown"], -1])
    else:
        rds.append(["AROON", 0, 0])

    # AROONOSC  阿隆震荡线 >0上升趋势, <0下降趋势
    if inds_dict["AROONOSC"] >0:
        rds.append(["AROONOSC", inds_dict["AROONOSC"], 1])
    elif inds_dict["AROONOSC"] <0:
        rds.append(["AROONOSC", inds_dict["AROONOSC"], -1])
    else:
        rds.append(["AROONOSC", 0, 0])


    return rds


def Pattern_Sign(inds_dict, close):
    rds = []
    for _k in inds_dict:
        v = inds_dict[_k]
        t = 0
        if v>0:
            t=1
        if v<0:
            t=-1
        rds.append([str(_k), v, t])
    return rds

def Sign_Percent(sigs_dict):
    pass



def Dashboard_Detail(rds):
    values = [v[-1] for v in rds]
    length = len(rds)
    pBuy = values.count(1)
    pSell = values.count(-1)
    pNeutral = values.count(0)
    return {"pBuy":pBuy, "pSell":pSell, "pNeutral":pNeutral, "total": length}


def df2factor(df,close,high,low,Open,volume):

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

    '----------------------------------------------Pattern_Recognition-------------------------------------------------------'
    # 形态学指标
    pattern_recognition = list(ndf[[i for i in list(df.columns) if i[:3] == "CDL"]])

    '----------------------------------------------Overlap_Studies_Functions-------------------------------------------------------'
    # 重叠指标
    overlap_studies_functions = ['DEMA5', 'EMA5', 'KAMA5', 'MA5', 'SMA5', 'TEMA5', 'TRIMA5', 'WMA5', 'DEMA10', 'EMA10',
                                 'KAMA10', 'MA10', 'SMA10', 'TEMA10', 'TRIMA10', 'WMA10', 'DEMA20', 'EMA20', 'KAMA20',
                                 'MA20', 'SMA20', 'TEMA20', 'TRIMA20', 'WMA20', 'DEMA30', 'EMA30', 'KAMA30', 'MA30',
                                 'SMA30', 'TEMA30', 'TRIMA30', 'WMA30', 'DEMA50', 'EMA50', 'KAMA50', 'MA50', 'SMA50',
                                 'TEMA50', 'TRIMA50', 'WMA50', 'DEMA100', 'EMA100', 'KAMA100', 'MA100', 'SMA100',
                                 'TEMA100', 'TRIMA100', 'WMA100', 'DEMA200', 'EMA200', 'KAMA200', 'MA200', 'SMA200',
                                 'TEMA200', 'TRIMA200', 'WMA200', 'HT_TRENDLINE', 'MIDPOINT', 'T3', 'ROCP', 'SAR',
                                 'SAREXT', 'MIDPRICE', 'BBANDS_upperband', 'BBANDS_middleband', 'BBANDS_lowerband',
                                 'MAMA_mama', 'MAMA_fama', 'KDJ_k', 'KDJ_d', 'KDJ_j', 'VOLUMEMA5', 'VOLUMEMA10',
                                 'VOLUMEMA20', 'VOLUMEMA30', 'VOLUMEMA50', 'VOLUMEMA100', 'VOLUMEMA200', 'DMA_dma',
                                 'DMA_ama']

    '----------------------------------------------Momentum_Indicators-------------------------------------------------------'
    # 动量类指标
    # momentum_indicators = ['ADX', 'ADXR', 'APO', 'AROON_aroondown', 'AROON_aroonup', 'AROONOSC', 'BOP', 'CCI', 'CMO', 'DX', 'MACD_macd',
    #                        'MACD_macdsignal', 'MACD_macdhist', 'MACDEXT_macd', 'MACDEXT_macdsignal', 'MACDEXT_macdhist', 'MACDFIX_macd',
    #                        'MACDFIX_macdsignal', 'MACDFIX_macdhist', 'MINUS_DI', 'MINUS_DM', 'MOM', 'PLUS_DI', 'PLUS_DM', 'PPO', 'ROC',
    #                        'ROCR', 'ROCR100', 'RSI', 'STOCH_slowk', 'STOCH_slowd', 'STOCHF_fastk', 'STOCHF_fastd', 'STOCHRSI_fastk',
    #                        'STOCHRSI_fastd', 'TRIX', 'ULTOSC', 'WILLR']
    momentum_indicators = ['ADX', 'ADXR', 'APO', 'AROON_aroondown', 'AROON_aroonup', 'AROONOSC', 'BOP', 'CCI', 'CMO',
                           'DX', 'MACD_macd', 'MACDEXT_macd', 'MACDFIX_macd', 'MINUS_DI', 'MINUS_DM', 'MOM', 'PLUS_DI',
                           'PLUS_DM', 'PPO', 'ROC', 'ROCR', 'ROCR100', 'RSI', 'STOCH_slowk', 'STOCH_slowd', 'STOCHF_fastk', 'STOCHF_fastd',
                           'STOCHRSI_fastk', 'STOCHRSI_fastd', 'TRIX', 'ULTOSC', 'WILLR']

    '----------------------------------------------result-------------------------------------------------------'
    base_dict = eval(ndf[base].to_json(orient='records'))[0]
    result = {
        "base":base_dict,
        "Overlap_Studies_Functions": Overlap_Sign(eval(ndf[overlap_studies_functions].to_json(orient='records'))[-1], base_dict["close"]),
        "Pattern_Recognition":Pattern_Sign(eval(ndf[pattern_recognition].to_json(orient='records'))[-1], base_dict["close"]),
        "Momentum_Indicators": Momentum_Sign(eval(ndf[momentum_indicators].to_json(orient='records')), base_dict["close"]),
        }

    result["Dashboard_Detail"] = {
        "Overlap_Studies_Functions":Dashboard_Detail(result["Overlap_Studies_Functions"]),
        "Pattern_Recognition":Dashboard_Detail(result["Pattern_Recognition"]),
        "Momentum_Indicators":Dashboard_Detail(result["Momentum_Indicators"]),
    }
    return result


