from __future__ import (absolute_import, division, print_function, unicode_literals)

import arrow
import backtrader as bt
import importlib
import time
import backtrader.indicators as btind

#  {'startDay': 283968000, 'endDay': 2524579200, 'kline': 'kline_day', 'myStocks': ['SH.603922'], 'market': 'SH', 'maxTimeBuffer':3, 'factors':2}
class iStrategyBase(bt.Strategy):
    params = dict(rule=dict())

    def __init__(self):
        data = self.datas[0]
        self._inds = dict()

        for cond in self.p.rule['tradeCondition']:
            if cond['modName'] == 'pattern_indicator':
                factor = f"{cond['clsName']}_{cond['params']['line']}"
            else:
                factor = cond['clsName']
            _moudle = getattr(importlib.import_module(f"api.loop_stack.loop_indicators.{cond['modName']}"), cond['clsName'])

            _sigline = cond['params'].get('line','')
            _position = cond['params']['logic'].get('position','')


            self._inds['X_'+factor+'_'+_sigline+'_'+str(_position)] = (_moudle(data, rule=cond['params']))


class iStrategy(iStrategyBase):

    def __init__(self):
        super(iStrategy, self).__init__()
        print()



        # self.result_dict = {}
        # for _ind in self._inds:
        #     self.result_dict[_ind] = {'factor':_ind, 'code':self.datas[0]._name, 'result_1d':[], 'result_2d':[], 'result_3d':[], 'result_4d':[], 'result_5d':[],
        #                      'create_time':time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), 'market':self.p.rule['market'], 'validity':0,}
        self.result_dict = {'code': self.datas[0]._name, 'result': {},
                                  'create_time': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                  'market': self.p.rule['market'], 'validity': 0,
                                 }
        # self.oscillator = btind.Oscillator()
        self.upmove = btind.UpMove()
        self.downmove = btind.DownMove()
        self.directionalindicator = btind.DirectionalIndicator()
        self.plusdirectionalindicator = btind.PlusDirectionalIndicator()
        self.minusdirectionalindicator = btind.MinusDirectionalIndicator()
        self.averagedirectionalmovementindex = btind.AverageDirectionalMovementIndex()
        self.averagedirectionalmovementindexrating = btind.AverageDirectionalMovementIndexRating()
        self.directionalmovementindex = btind.DirectionalMovementIndex()
        self.directionalmovement = btind.DirectionalMovement()
        self.relativemomentumindex = btind.RelativeMomentumIndex()
        self.zerolagindicator = btind.ZeroLagIndicator()
        self.awesomeoscillator = btind.AwesomeOscillator()
        self.zerolagexponentialmovingaverage = btind.ZeroLagExponentialMovingAverage()
        # self.heikinashi = btind.HeikinAshi()
        self.percentrank = btind.PercentRank()
        # self.movingaveragebase = btind.MovingAverageBase()
        self.weightedmovingaverage = btind.WeightedMovingAverage()
        self.vortex = btind.Vortex()
        self.accelerationdecelerationoscillator = btind.AccelerationDecelerationOscillator()
        self.priceoscillator = btind.PriceOscillator()
        self.percentagepriceoscillator = btind.PercentagePriceOscillator()
        self.percentagepriceoscillatorshort = btind.PercentagePriceOscillatorShort()
        self.ultimateoscillator = btind.UltimateOscillator()
        self.parabolicsar = btind.ParabolicSAR()
        self.macd = btind.MACD()
        self.macdhisto = btind.MACDHisto()
        # self.periodn = btind.PeriodN()
        # self.operationn = btind.OperationN()
        # self.baseapplyn = btind.BaseApplyN()
        # self.applyn = btind.ApplyN()
        self.highest = btind.Highest()
        self.lowest = btind.Lowest()
        # self.reducen = btind.ReduceN()
        self.sumn = btind.SumN()
        self.anyn = btind.AnyN()
        self.alln = btind.AllN()
        # self.findfirstindex = btind.FindFirstIndex()
        self.findfirstindexhighest = btind.FindFirstIndexHighest()
        self.findfirstindexlowest = btind.FindFirstIndexLowest()
        # self.findlastindex = btind.FindLastIndex()
        self.findlastindexhighest = btind.FindLastIndexHighest()
        self.findlastindexlowest = btind.FindLastIndexLowest()
        self.accum = btind.Accum()
        self.average = btind.Average()
        self.exponentialsmoothing = btind.ExponentialSmoothing()
        # self.exponentialsmoothingdynamic = btind.ExponentialSmoothingDynamic()
        self.weightedaverage = btind.WeightedAverage()
        self.exponentialmovingaverage = btind.ExponentialMovingAverage()
        # self.ols_slope_interceptn = btind.OLS_Slope_InterceptN()
        # self.ols_transformationn = btind.OLS_TransformationN()
        # self.ols_betan = btind.OLS_BetaN()
        # self.cointn = btind.CointN()
        self.stochasticfast = btind.StochasticFast()
        self.stochastic = btind.Stochastic()
        self.stochasticfull = btind.StochasticFull()
        self.truehigh = btind.TrueHigh()
        self.truelow = btind.TrueLow()
        self.truerange = btind.TrueRange()
        self.averagetruerange = btind.AverageTrueRange()
        # self.oscillatormixin = btind.OscillatorMixIn()
        self.prettygoodoscillator = btind.PrettyGoodOscillator()
        self.dicksonmovingaverage = btind.DicksonMovingAverage()
        self.percentchange = btind.PercentChange()
        # self.hadelta = btind.haDelta(self.data)
        self.commoditychannelindex = btind.CommodityChannelIndex()
        self.hullmovingaverage = btind.HullMovingAverage()
        self.standarddeviation = btind.StandardDeviation()
        self.meandeviation = btind.MeanDeviation()
        self.doubleexponentialmovingaverage = btind.DoubleExponentialMovingAverage()
        self.tripleexponentialmovingaverage = btind.TripleExponentialMovingAverage()
        self.williamsr = btind.WilliamsR()
        self.williamsad = btind.WilliamsAD()
        # self.dv2 = btind.DV2()
        self.truestrengthindicator = btind.TrueStrengthIndicator()
        self.ichimoku = btind.Ichimoku()
        self.adaptivemovingaverage = btind.AdaptiveMovingAverage()
        self.movingaveragesimple = btind.MovingAverageSimple()
        # self.nonzerodifference = btind.NonZeroDifference()
        # self.crossup = btind.CrossUp()
        # self.crossdown = btind.CrossDown()
        # self.crossover = btind.CrossOver()
        self.pivotpoint = btind.PivotPoint()
        self.fibonaccipivotpoint = btind.FibonacciPivotPoint()
        self.demarkpivotpoint = btind.DemarkPivotPoint()
        self.upday = btind.UpDay()
        self.downday = btind.DownDay()
        self.updaybool = btind.UpDayBool()
        self.downdaybool = btind.DownDayBool()
        self.relativestrengthindex = btind.RelativeStrengthIndex()
        self.rsi_safe = btind.RSI_Safe()
        self.rsi_sma = btind.RSI_SMA()
        self.rsi_ema = btind.RSI_EMA()
        self.trix = btind.Trix()
        self.trixsignal = btind.TrixSignal()
        self.laguerrersi = btind.LaguerreRSI()
        self.laguerrefilter = btind.LaguerreFilter()
        self.hurstexponent = btind.HurstExponent()
        self.aroonup = btind.AroonUp()
        self.aroondown = btind.AroonDown()
        self.aroonupdown = btind.AroonUpDown()
        self.aroonoscillator = btind.AroonOscillator()
        self.aroonupdownoscillator = btind.AroonUpDownOscillator()
        self.bollingerbands = btind.BollingerBands()
        self.bollingerbandspct = btind.BollingerBandsPct()
        self.momentum = btind.Momentum()
        self.momentumoscillator = btind.MomentumOscillator()
        self.rateofchange = btind.RateOfChange()
        self.rateofchange100 = btind.RateOfChange100()
        self.detrendedpriceoscillator = btind.DetrendedPriceOscillator()
        self.smoothedmovingaverage = btind.SmoothedMovingAverage()
        self.envelope = btind.Envelope()
        self.knowsurething = btind.KnowSureThing()


    def next(self):
        stock = self.datas[0]
        # _match = {'date': str(stock.datetime.date()), 'match_factor': [],'close': stock.close[0], 'high':stock.high[0],
        #           'score': {'result_1d': {}, 'result_2d': {}, 'result_3d': {}, 'result_4d': {}, 'result_5d': {}}, 'trading_days': [int(stock.datetime[-i]) for i in range(1,8)]}
        # for k in self._inds:
        #     if self._inds[k]:
        #
        #         _match['match_factor'].append(k)
        #         self.result_dict['validity'] = 1
        # 收盘价
        # for i in range(1, 6):
        #     _d = _match['score'][f'result_{i}d']
        #     try:
        #         _d["percent"] = (stock.close[i] - stock.close[0]) / stock.close[0]
        #         if _d["percent"]>0:
        #             _d["status"] = 1
        #         else:
        #             _d["status"] = 0
        #     except:
        #         _d["status"] = -1
        #
        #     # 最高价
        #     try:
        #         _d["high_percent"] = (stock.high[i] - stock.close[0]) / stock.close[0]
        #         if _d["high_percent"] > 0:
        #             _d["high_status"] = 1
        #         else:
        #             _d["high_status"] = 0
        #     except:
        #         _d["high_status"] = -1
        # self.result_dict['result'][str(int(stock.datetime[0]))] = _match

        dc = {'date': str(stock.datetime.datetime()),'close': stock.close[0], 'high':stock.high[0],'open':stock.open[0],'low':stock.low[0],'volume':stock.volume[0]}

        ########## UpMove
        dc['X_upmove'] = self.upmove.upmove[0]
        ########## DownMove
        dc['X_downmove'] = self.downmove.downmove[0]
        ########## DirectionalIndicator
        dc['X_plusDI'] = self.directionalindicator.plusDI[0]
        dc['X_minusDI'] = self.directionalindicator.minusDI[0]
        ########## PlusDirectionalIndicator
        dc['X_plusDI'] = self.plusdirectionalindicator.plusDI[0]
        ########## MinusDirectionalIndicator
        dc['X_minusDI'] = self.minusdirectionalindicator.minusDI[0]
        ########## AverageDirectionalMovementIndex
        dc['X_adx'] = self.averagedirectionalmovementindex.adx[0]
        ########## AverageDirectionalMovementIndexRating
        dc['X_adxr'] = self.averagedirectionalmovementindexrating.adxr[0]
        ########## DirectionalMovementIndex
        dc['X_plusDI'] = self.directionalmovementindex.plusDI[0]
        dc['X_minusDI'] = self.directionalmovementindex.minusDI[0]
        ########## DirectionalMovement
        dc['X_plusDI'] = self.directionalmovement.plusDI[0]
        dc['X_minusDI'] = self.directionalmovement.minusDI[0]
        ########## RelativeMomentumIndex
        dc['X_rmi'] = self.relativemomentumindex.rmi[0]
        ########## ZeroLagIndicator
        dc['X_ec'] = self.zerolagindicator.ec[0]
        ########## AwesomeOscillator
        dc['X_ao'] = self.awesomeoscillator.ao[0]
        ########## ZeroLagExponentialMovingAverage
        dc['X_zlema'] = self.zerolagexponentialmovingaverage.zlema[0]
        # ########## HeikinAshi
        # dc['X_ha_open'] = self.heikinashi.ha_open[0]
        # dc['X_ha_high'] = self.heikinashi.ha_high[0]
        # dc['X_ha_low'] = self.heikinashi.ha_low[0]
        # dc['X_ha_close'] = self.heikinashi.ha_close[0]
        # dc['X_open'] = self.heikinashi.open[0]
        # dc['X_high'] = self.heikinashi.high[0]
        # dc['X_low'] = self.heikinashi.low[0]
        # dc['X_close'] = self.heikinashi.close[0]
        ########## PercentRank
        dc['X_pctrank'] = self.percentrank.pctrank[0]
        ########## MovingAverageBase
        ########## WeightedMovingAverage
        dc['X_wma'] = self.weightedmovingaverage.wma[0]
        ########## Vortex
        dc['X_vi_plus'] = self.vortex.vi_plus[0]
        dc['X_vi_minus'] = self.vortex.vi_minus[0]
        dc['X_iViDistance'] = self.vortex.vi_plus[0] - self.vortex.vi_minus[0]

        ########## AccelerationDecelerationOscillator
        dc['X_accde'] = self.accelerationdecelerationoscillator.accde[0]
        ########## PriceOscillator
        dc['X_po'] = self.priceoscillator.po[0]
        ########## PercentagePriceOscillator
        dc['X_ppo'] = self.percentagepriceoscillator.ppo[0]
        dc['X_signal'] = self.percentagepriceoscillator.signal[0]
        dc['X_histo'] = self.percentagepriceoscillator.histo[0]
        ########## PercentagePriceOscillatorShort
        ########## UltimateOscillator
        dc['X_uo'] = self.ultimateoscillator.uo[0]
        ########## ParabolicSAR
        dc['X_psar'] = self.parabolicsar.psar[0]
        ########## MACD
        dc['X_macd'] = self.macd.macd[0]
        dc['X_signal'] = self.macd.signal[0]
        ########## MACDHisto
        dc['X_histo'] = self.macdhisto.histo[0]
        ########## PeriodN
        ########## OperationN
        ########## BaseApplyN
        ########## ApplyN
        # dc['X_apply'] = self.applyn.apply[0]
        ########## Highest
        dc['X_highest'] = self.highest.highest[0]
        ########## Lowest
        dc['X_lowest'] = self.lowest.lowest[0]
        ########## ReduceN
        # dc['X_reduced'] = self.reducen.reduced[0]
        ########## SumN
        dc['X_sumn'] = self.sumn.sumn[0]
        ########## AnyN
        dc['X_anyn'] = self.anyn.anyn[0]
        ########## AllN
        dc['X_alln'] = self.alln.alln[0]
        ########## FindFirstIndex
        # dc['X_index'] = self.findfirstindex.index[0]
        ########## FindFirstIndexHighest
        ########## FindFirstIndexLowest
        ########## FindLastIndex
        # dc['X_index'] = self.findlastindex.index[0]
        ########## FindLastIndexHighest
        ########## FindLastIndexLowest
        ########## Accum
        dc['X_accum'] = self.accum.accum[0]
        ########## Average
        dc['X_av'] = self.average.av[0]
        ########## ExponentialSmoothing
        ########## ExponentialSmoothingDynamic
        ########## WeightedAverage
        dc['X_av'] = self.weightedaverage.av[0]
        ########## ExponentialMovingAverage
        dc['X_ema'] = self.exponentialmovingaverage.ema[0]
        ########## OLS_Slope_InterceptN
        # dc['X_slope'] = self.ols_slope_interceptn.slope[0]
        # dc['X_intercept'] = self.ols_slope_interceptn.intercept[0]
        ########## OLS_TransformationN
        # dc['X_spread'] = self.ols_transformationn.spread[0]
        # dc['X_spread_mean'] = self.ols_transformationn.spread_mean[0]
        # dc['X_spread_std'] = self.ols_transformationn.spread_std[0]
        # dc['X_zscore'] = self.ols_transformationn.zscore[0]
        ########## OLS_BetaN
        # dc['X_beta'] = self.ols_betan.beta[0]
        ########## CointN
        # dc['X_score'] = self.cointn.score[0]
        # dc['X_pvalue'] = self.cointn.pvalue[0]
        ########## StochasticFast
        ########## Stochastic
        ########## StochasticFull
        dc['X_percDSlow'] = self.stochasticfull.percDSlow[0]
        ########## TrueHigh
        dc['X_truehigh'] = self.truehigh.truehigh[0]
        ########## TrueLow
        dc['X_truelow'] = self.truelow.truelow[0]
        ########## TrueRange
        dc['X_tr'] = self.truerange.tr[0]
        ########## AverageTrueRange
        dc['X_atr'] = self.averagetruerange.atr[0]
        ########## OscillatorMixIn
        ########## Oscillator
        # dc['X_osc'] = self.oscillator.osc[0]
        ########## PrettyGoodOscillator
        dc['X_pgo'] = self.prettygoodoscillator.pgo[0]
        ########## DicksonMovingAverage
        dc['X_dma'] = self.dicksonmovingaverage.dma[0]
        ########## PercentChange
        dc['X_pctchange'] = self.percentchange.pctchange[0]
        ########## haDelta
        # dc['X_haDelta'] = self.hadelta.haDelta[0]
        # dc['X_smoothed'] = self.hadelta.smoothed[0]
        ########## CommodityChannelIndex
        dc['X_cci'] = self.commoditychannelindex.cci[0]
        ########## HullMovingAverage
        dc['X_hma'] = self.hullmovingaverage.hma[0]
        ########## StandardDeviation
        dc['X_stddev'] = self.standarddeviation.stddev[0]
        ########## MeanDeviation
        dc['X_meandev'] = self.meandeviation.meandev[0]
        ########## DoubleExponentialMovingAverage
        dc['X_dema'] = self.doubleexponentialmovingaverage.dema[0]
        ########## TripleExponentialMovingAverage
        dc['X_tema'] = self.tripleexponentialmovingaverage.tema[0]
        ########## WilliamsR
        dc['X_percR'] = self.williamsr.percR[0]
        ########## WilliamsAD
        dc['X_ad'] = self.williamsad.ad[0]
        ########## DV2
        # dc['X_dv2'] = self.dv2.dv2[0]
        ########## TrueStrengthIndicator
        dc['X_tsi'] = self.truestrengthindicator.tsi[0]
        ########## Ichimoku
        dc['X_tenkan_sen'] = self.ichimoku.tenkan_sen[0]
        dc['X_kijun_sen'] = self.ichimoku.kijun_sen[0]
        dc['X_senkou_span_a'] = self.ichimoku.senkou_span_a[0]
        dc['X_senkou_span_b'] = self.ichimoku.senkou_span_b[0]
        # dc['X_chikou_span'] = self.ichimoku.chikou_span[0]
        ########## AdaptiveMovingAverage
        dc['X_kama'] = self.adaptivemovingaverage.kama[0]
        ########## MovingAverageSimple
        dc['X_sma'] = self.movingaveragesimple.sma[0]
        ########## NonZeroDifference
        # dc['X_nzd'] = self.nonzerodifference.nzd[0]
        ########## CrossUp
        ########## CrossDown
        ########## CrossOver
        # dc['X_crossover'] = self.crossover.crossover[0]
        ########## PivotPoint
        # dc['X_p'] = self.pivotpoint.p[0]
        dc['X_s1'] = self.pivotpoint.s1[0]
        dc['X_s2'] = self.pivotpoint.s2[0]
        dc['X_r1'] = self.pivotpoint.r1[0]
        dc['X_r2'] = self.pivotpoint.r2[0]
        ########## FibonacciPivotPoint
        # dc['X_p'] = self.fibonaccipivotpoint.p[0]
        dc['X_s1'] = self.fibonaccipivotpoint.s1[0]
        dc['X_s2'] = self.fibonaccipivotpoint.s2[0]
        dc['X_s3'] = self.fibonaccipivotpoint.s3[0]
        dc['X_r1'] = self.fibonaccipivotpoint.r1[0]
        dc['X_r2'] = self.fibonaccipivotpoint.r2[0]
        dc['X_r3'] = self.fibonaccipivotpoint.r3[0]
        ########## DemarkPivotPoint
        # dc['X_p'] = self.demarkpivotpoint.p[0]
        dc['X_s1'] = self.demarkpivotpoint.s1[0]
        dc['X_r1'] = self.demarkpivotpoint.r1[0]
        ########## UpDay
        dc['X_upday'] = self.upday.upday[0]
        ########## DownDay
        dc['X_downday'] = self.downday.downday[0]
        ########## UpDayBool
        dc['X_upday'] = self.updaybool.upday[0]
        ########## DownDayBool
        dc['X_downday'] = self.downdaybool.downday[0]
        ########## RelativeStrengthIndex
        dc['X_rsi'] = self.relativestrengthindex.rsi[0]
        ########## RSI_Safe
        ########## RSI_SMA
        ########## RSI_EMA
        ########## Trix
        dc['X_trix'] = self.trix.trix[0]
        ########## TrixSignal
        dc['X_signal'] = self.trixsignal.signal[0]
        ########## LaguerreRSI
        dc['X_lrsi'] = self.laguerrersi.lrsi[0]
        ########## LaguerreFilter
        dc['X_lfilter'] = self.laguerrefilter.lfilter[0]
        ########## HurstExponent
        dc['X_hurst'] = self.hurstexponent.hurst[0]
        ########## AroonUp
        dc['X_aroonup'] = self.aroonup.aroonup[0]
        ########## AroonDown
        dc['X_aroondown'] = self.aroondown.aroondown[0]
        ########## AroonUpDown
        dc['X_aroondown'] = self.aroonupdown.aroondown[0]
        ########## AroonOscillator
        dc['X_aroonosc'] = self.aroonoscillator.aroonosc[0]
        ########## AroonUpDownOscillator
        dc['X_aroonosc'] = self.aroonupdownoscillator.aroonosc[0]
        ########## BollingerBands
        dc['X_mid'] = self.bollingerbands.mid[0]
        dc['X_top'] = self.bollingerbands.top[0]
        dc['X_bot'] = self.bollingerbands.bot[0]
        ########## BollingerBandsPct
        dc['X_pctb'] = self.bollingerbandspct.pctb[0]
        ########## Momentum
        dc['X_momentum'] = self.momentum.momentum[0]
        ########## MomentumOscillator
        dc['X_momosc'] = self.momentumoscillator.momosc[0]
        ########## RateOfChange
        dc['X_roc'] = self.rateofchange.roc[0]
        ########## RateOfChange100
        dc['X_roc100'] = self.rateofchange100.roc100[0]
        ########## DetrendedPriceOscillator
        dc['X_dpo'] = self.detrendedpriceoscillator.dpo[0]
        ########## SmoothedMovingAverage
        dc['X_smma'] = self.smoothedmovingaverage.smma[0]
        ########## Envelope
        dc['X_top'] = self.envelope.top[0]
        dc['X_bot'] = self.envelope.bot[0]
        ########## KnowSureThing
        dc['X_kst'] = self.knowsurething.kst[0]
        dc['X_signal'] = self.knowsurething.signal[0]



        for k in self._inds:
            if self._inds[k]:
                dc[k] = 1
            else:
                dc[k] = 0

        # print(dc)
        # print(int(stock.datetime[0]))
        # print(stock.datetime.datetime())



        self.result_dict['result'][str(int(arrow.get(stock.datetime.datetime()).timestamp))] = dc
