# 基础因子
import talib

def talib_KDJ(high_prices, low_prices, close_prices, fastk_period=9, slowk_period=3, slowd_period=3):
    #计算kdj指标
    k, d = talib.STOCH(high_prices, low_prices, close_prices,
                                                   fastk_period=fastk_period,
                                                   slowk_period=slowk_period,
                                                   slowd_period=slowd_period)
    j = 3 * k - 2 * d
    return k, d, j


def talib_DMA(close_price, short_period=10, long_period=50):
    # 计算dma指标
    short_sma = talib.SMA(close_price, short_period)
    long_sma = talib.SMA(close_price, long_period)
    dma = short_sma - long_sma
    ama = talib.SMA(dma, short_period)
    return dma, ama