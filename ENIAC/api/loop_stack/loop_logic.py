# todo 因子运算（loop_indicators）
def compare(x, condition):
    if condition["compare"] == "gt":
        return x > condition["byValue"]
    if condition["compare"] == "ge":
        return x >= condition["byValue"]
    if condition["compare"] == "lt":
        return x < condition["byValue"]
    if condition["compare"] == "le":
        return x <= condition["byValue"]
    if condition["compare"] == "eq":
        return x == condition["byValue"]
    if condition["compare"] == "in":
        return (x > condition["byValue"] and x <= condition["byMax"])
    return


# todo 因子运算（loop_indicators）
def compare_price(x, condition):
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


DAYS = '5'  # 连续几天多头/空头

PATTERNS = ['CDL2CROWS', 'CDL3BLACKCROWS', 'CDL3INSIDE', 'CDL3LINESTRIKE', 'CDL3OUTSIDE', 'CDL3STARSINSOUTH',
            'CDL3WHITESOLDIERS', 'CDLABANDONEDBABY', 'CDLADVANCEBLOCK', 'CDLBELTHOLD', 'CDLBREAKAWAY',
            'CDLCLOSINGMARUBOZU', 'CDLCONCEALBABYSWALL', 'CDLCOUNTERATTACK', 'CDLDARKCLOUDCOVER', 'CDLDOJI',
            'CDLDOJISTAR', 'CDLDRAGONFLYDOJI', 'CDLENGULFING', 'CDLEVENINGDOJISTAR', 'CDLEVENINGSTAR',
            'CDLGAPSIDESIDEWHITE', 'CDLGRAVESTONEDOJI', 'CDLHAMMER', 'CDLHANGINGMAN', 'CDLHARAMI', 'CDLHARAMICROSS',
            'CDLHIGHWAVE', 'CDLHIKKAKE', 'CDLHIKKAKEMOD', 'CDLHOMINGPIGEON', 'CDLIDENTICAL3CROWS', 'CDLINNECK',
            'CDLINVERTEDHAMMER', 'CDLKICKING', 'CDLKICKINGBYLENGTH', 'CDLLADDERBOTTOM', 'CDLLONGLEGGEDDOJI',
            'CDLLONGLINE', 'CDLMARUBOZU', 'CDLMATCHINGLOW', 'CDLMATHOLD', 'CDLMORNINGDOJISTAR', 'CDLMORNINGSTAR',
            'CDLONNECK', 'CDLPIERCING', 'CDLRICKSHAWMAN', 'CDLRISEFALL3METHODS', 'CDLSEPARATINGLINES',
            'CDLSHOOTINGSTAR', 'CDLSHORTLINE', 'CDLSPINNINGTOP', 'CDLSTALLEDPATTERN', 'CDLSTICKSANDWICH', 'CDLTAKURI',
            'CDLTASUKIGAP', 'CDLTHRUSTING', 'CDLTRISTAR', 'CDLUNIQUE3RIVER', 'CDLUPSIDEGAP2CROWS',
            'CDLXSIDEGAP3METHODS']

# ma, macd, kdj, rsi   ema, dma, vma   boll(long,short)
TRADERATIONS_CROSS = [{"clsName": "iMacdCrossGolden", "modName": "macd_indicator",
                       "params": {"args": ["12", "26", "9"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iKdjCrossGolden", "modName": "kdj_indicator",
                       "params": {"args": ["9", "3", "3"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iRsiCrossGolden", "modName": "rsi_indicator",
                       "params": {"args": ["6", "12", "30"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iMaCrossGolden", "modName": "ma_indicator",
                       "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iMacdCrossDie", "modName": "macd_indicator",
                       "params": {"args": ["12", "26", "9"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iKdjCrossDie", "modName": "kdj_indicator",
                       "params": {"args": ["9", "3", "3"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iRsiCrossDie", "modName": "rsi_indicator",
                       "params": {"args": ["6", "12", "30"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iMaCrossDie", "modName": "ma_indicator",
                       "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iVmaCrossGolden", "modName": "vma_indicator",
                       "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iVmaCrossDie", "modName": "vma_indicator",
                       "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iEmaCrossGolden", "modName": "ema_indicator",
                       "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iEmaCrossDie", "modName": "ema_indicator",
                       "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iDmaCrossGolden", "modName": "dma_indicator",
                       "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iDmaCrossDie", "modName": "dma_indicator",
                       "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                       },

                      ]

TRADERATIONS_HEAD = [{"clsName": "iBollLong", "modName": "boll_indicator",
                      "params": {"args": ["20", "2", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iBollShort", "modName": "boll_indicator",
                      "params": {"args": ["20", "2", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iMacdLong", "modName": "macd_indicator",
                      "params": {"args": ["12", "26", "9", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iMacdShort", "modName": "macd_indicator",
                      "params": {"args": ["12", "26", "9", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iMaLong", "modName": "ma_indicator",
                      "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iMaShort", "modName": "ma_indicator",
                      "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iRsiLong", "modName": "rsi_indicator",
                      "params": {"args": ["6", "12", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iRsiShort", "modName": "rsi_indicator",
                      "params": {"args": ["6", "12", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iVmaLong", "modName": "vma_indicator",
                      "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iVmaShort", "modName": "vma_indicator",
                      "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iEmaLong", "modName": "ema_indicator",
                      "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iEmaShort", "modName": "ema_indicator",
                      "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iDmaCrossLong", "modName": "dma_indicator",
                      "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     {"clsName": "iDmaCrossShort", "modName": "dma_indicator",
                      "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      },
                     ]

PATTERNUP = [{"clsName": "iPatternUp", "modName": "pattern_indicator",
              "params": {"args": ["10"], "logic": {"byValue": 0, "compare": "ge"}, 'line': _l, }} for _l in PATTERNS]
PATTERNDOWN = [{"clsName": "iPatternDown", "modName": "pattern_indicator",
                "params": {"args": ["10"], "logic": {"byValue": 0, "compare": "ge"}, 'line': _l}} for _l in PATTERNS]

PATTERN = PATTERNUP + PATTERNDOWN
MOMENTUM = TRADERATIONS_CROSS + TRADERATIONS_HEAD

TRADERATIONS_CROSS1 = [{"clsName": "iZlindCrossGolden", "modName": "zlind_indicator",
                        "params": {"args": ["5", 50, "10", 50], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iZlindCrossDie", "modName": "zlind_indicator",
                        "params": {"args": ["5", 50, "10", 50], "logic": {"byValue": 0, "compare": "ge"}}
                        },

                       {"clsName": "iZlemaCrossGolden", "modName": "zlema_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iZlemaCrossDie", "modName": "zlema_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },

                       {"clsName": "iWMSRCrossGolden", "modName": "wmsr_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iWMSRCrossDie", "modName": "wmsr_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iWmaCrossGolden", "modName": "wma_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iWmaCrossDie", "modName": "wma_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iVmaCrossGolden", "modName": "vma_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iVmaCrossDie", "modName": "vma_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iViCrossGolden", "modName": "vi_indicator",
                        "params": {"args": ["14"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iViCrossDie", "modName": "vi_indicator",
                        "params": {"args": ["14"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iUoCrossGolden", "modName": "uo_indicator",
                        "params": {"args": [7, 14, 28, 14, 28, 56], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iUoCrossDie", "modName": "uo_indicator",
                        "params": {"args": [7, 14, 28, 14, 28, 56], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iTSICrossGolden", "modName": "tsi_indicator",
                        "params": {"args": [25, 13, 1, 50, 26, 2], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iTSICrossDie", "modName": "tsi_indicator",
                        "params": {"args": [25, 13, 1, 50, 26, 2], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iTrixCrossGolden", "modName": "trix_indicator",
                        "params": {"args": [9, 15], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iTrixCrossDie", "modName": "trix_indicator",
                        "params": {"args": [9, 15], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iStochasticSlowCrossGolden", "modName": "stochasticSlow_indicator",
                        "params": {"args": [14, 3, 28, 6], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iStochasticSlowCrossDie", "modName": "stochasticSlow_indicator",
                        "params": {"args": [14, 3, 28, 6], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iSMMACrossGolden", "modName": "smma_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iSMMACrossDie", "modName": "smma_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iRocCrossGolden", "modName": "roc_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iRocCrossDie", "modName": "roc_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iRmiCrossGolden", "modName": "rmi_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iRmiCrossDie", "modName": "rmi_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPriceoscillatorCrossGolden", "modName": "priceoscillator_indicator",
                        "params": {"args": [12, 26, 9], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPriceoscillatorCrossDie", "modName": "priceoscillator_indicator",
                        "params": {"args": [12, 26, 9], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPGOCrossGolden", "modName": "prettygoodoscillator_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPGOCrossDie", "modName": "prettygoodoscillator_indicator",
                        "params": {"args": ["5", "10"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPoCrossGolden", "modName": "po_indicator",
                        "params": {"args": [6, 13, 12, 26], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPoCrossDie", "modName": "po_indicator",
                        "params": {"args": [6, 13, 12, 26], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPctRankCrossGolden", "modName": "percentrank_indicator",
                        "params": {"args": [25, 50], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPctRankCrossDie", "modName": "percentrank_indicator",
                        "params": {"args": [25, 50], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPctChangeCrossGolden", "modName": "percentchange_indicator",
                        "params": {"args": ["15", "30"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iPctChangeCrossDie", "modName": "percentchange_indicator",
                        "params": {"args": ["15", "30"], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iMomentumOscCrossGolden", "modName": "momosc_indicator",
                        "params": {"args": [12, 24], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iMomentumOscCrossDie", "modName": "momosc_indicator",
                        "params": {"args": [12, 24], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iMomentumCrossGolden", "modName": "momentum_indicator",
                        "params": {"args": [12, 26, ], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iMomentumCrossDie", "modName": "momentum_indicator",
                        "params": {"args": [12, 26, ], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iLrsiCrossGolden", "modName": "lrsi_indicator",
                        "params": {"args": [5, 10], "logic": {"byValue": 0, "compare": "ge", 'gamma': [0.5]}}
                        },
                       {"clsName": "iLrsiCrossDie", "modName": "lrsi_indicator",
                        "params": {"args": [5, 10], "logic": {"byValue": 0, "compare": "ge", 'gamma': [0.5]}}
                        },
                       {"clsName": "iKstCrossGolden", "modName": "kst_indicator",
                        "params": {"args": [10, 15, 20, 30, 10, 10, 10, 15, 9],
                                   "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iKstCrossDie", "modName": "kst_indicator",
                        "params": {"args": [10, 15, 20, 30, 10, 10, 10, 15, 9],
                                   "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iKamaCrossGolden", "modName": "kama_indicator",
                        "params": {"args": [10, 2, 30, 20, 2, 30], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iKamaCrossDie", "modName": "kama_indicator",
                        "params": {"args": [10, 2, 30, 20, 2, 30], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iHmaCrossGolden", "modName": "hma_indicator",
                        "params": {"args": [5, 10], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iHmaCrossDie", "modName": "hma_indicator",
                        "params": {"args": [5, 10], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       # {"clsName": "iHaDeltaCrossGolden", "modName": "haDelta_indicator",
                       #  "params": {"args": [5, 10], "logic": {"byValue": 0, "compare": "ge"}}
                       #  },
                       # {"clsName": "iHaDeltaCrossDie", "modName": "haDelta_indicator",
                       #  "params": {"args": [5, 10], "logic": {"byValue": 0, "compare": "ge"}}
                       #  },
                       # {"clsName": "iDv2CrossGolden", "modName": "dv2_indicator",
                       #  "params": {"args": [126, 252], "logic": {"byValue": 0, "compare": "ge"}}
                       #  },
                       # {"clsName": "iDv2CrossDie", "modName": "dv2_indicator",
                       #  "params": {"args": [126, 252], "logic": {"byValue": 0, "compare": "ge"}}
                       #  },
                       {"clsName": "iDpoCrossGolden", "modName": "dpo_indicator",
                        "params": {"args": [20, 40], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iDpoCrossDie", "modName": "dpo_indicator",
                        "params": {"args": [20, 40], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iAtrCrossGolden", "modName": "atr_indicator",
                        "params": {"args": [14, 28], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iAtrCrossDie", "modName": "atr_indicator",
                        "params": {"args": [14, 28], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iAroonUpDownCrossGolden", "modName": "aroon_indicator",
                        "params": {"args": [14, 28], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iAroonUpDownCrossDie", "modName": "aroon_indicator",
                        "params": {"args": [14, 28], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iCciCrossGolden", "modName": "cci_indicator",
                        "params": {"args": [5, 10], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iCciCrossDie", "modName": "cci_indicator",
                        "params": {"args": [5, 10], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iHurstCrossGolden", "modName": "hurst_indicator",
                        "params": {"args": [40, 80], "logic": {"byValue": 0, "compare": "ge"}}
                        },
                       {"clsName": "iHurstCrossDie", "modName": "hurst_indicator",
                        "params": {"args": [40, 80], "logic": {"byValue": 0, "compare": "ge"}}
                        },

                       ]
TRADERATIONS_HEAD1 = [{"clsName": "iKdjLong", "modName": "kdj_indicator",
                       "params": {"args": ["9", "3", "3", DAYS,50], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iKdjShort", "modName": "kdj_indicator",
                       "params": {"args": ["9", "3", "3", DAYS,50], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iHurstLong", "modName": "hurst_indicator",
                       "params": {"args": [40, 80, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iHurstShort", "modName": "hurst_indicator",
                       "params": {"args": [40, 80, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iCciLong", "modName": "cci_indicator",
                       "params": {"args": [5, 10, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iCciShort", "modName": "cci_indicator",
                       "params": {"args": [5, 10, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iAroonUpDownLong", "modName": "aroon_indicator",
                       "params": {"args": [14, 28, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iAroonUpDownShort", "modName": "aroon_indicator",
                       "params": {"args": [14, 28, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iAtrLong", "modName": "atr_indicator",
                       "params": {"args": [14, 28, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iAtrShort", "modName": "atr_indicator",
                       "params": {"args": [14, 28, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iDpoLong", "modName": "dpo_indicator",
                       "params": {"args": [20, 40, DAYS], "logic": {"byValue": 0, "compare": "ge", 'position': 0}}
                       },
                      {"clsName": "iDpoShort", "modName": "dpo_indicator",
                       "params": {"args": [20, 40, DAYS], "logic": {"byValue": 0, "compare": "ge", 'position': 0}}
                       },
                      # {"clsName": "iDv2Long", "modName": "dv2_indicator",
                      #  "params": {"args": [126, 252, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      #  },
                      # {"clsName": "iDv2Short", "modName": "dv2_indicator",
                      #  "params": {"args": [126, 252, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      #  },

                      #  {"clsName": "iHaDeltaLong", "modName": "haDelta_indicator",
                      #  "params": {"args": [5, 10, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      #  },
                      # {"clsName": "iHaDeltaShort", "modName": "haDelta_indicator",
                      #  "params": {"args": [5, 10, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                      #  },
                      {"clsName": "iHmaLong", "modName": "hma_indicator",
                       "params": {"args": [5, 10, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iHmaShort", "modName": "hma_indicator",
                       "params": {"args": [5, 10, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iKamaLong", "modName": "kama_indicator",
                       "params": {"args": [10, 2, 30, 20, 2, 30, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iKamaShort", "modName": "kama_indicator",
                       "params": {"args": [10, 2, 30, 20, 2, 30, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iKstLong", "modName": "kst_indicator",
                       "params": {"args": [10, 15, 20, 30, 10, 10, 10, 15, 9, DAYS],
                                  "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iKstShort", "modName": "kst_indicator",
                       "params": {"args": [10, 15, 20, 30, 10, 10, 10, 15, 9, DAYS],
                                  "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iLrsiLong", "modName": "lrsi_indicator",
                       "params": {"args": [5, 10, DAYS], "logic": {"byValue": 0, "compare": "ge", 'gamma': [0.5]}}
                       },
                      {"clsName": "iLrsiShort", "modName": "lrsi_indicator",
                       "params": {"args": [5, 10, DAYS], "logic": {"byValue": 0, "compare": "ge", 'gamma': [0.5]}}
                       },
                      {"clsName": "iMomentumLong", "modName": "momentum_indicator",
                       "params": {"args": [12, 26, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iMomentumShort", "modName": "momentum_indicator",
                       "params": {"args": [12, 26, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iMomentumOscLong", "modName": "momosc_indicator",
                       "params": {"args": [12, 24, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iMomentumOscShort", "modName": "momosc_indicator",
                       "params": {"args": [12, 24, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPctChangeLong", "modName": "percentchange_indicator",
                       "params": {"args": [15, 30, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPctChangeShort", "modName": "percentchange_indicator",
                       "params": {"args": [15, 30, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPctRankLong", "modName": "percentrank_indicator",
                       "params": {"args": [25, 50, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPctRankShort", "modName": "percentrank_indicator",
                       "params": {"args": [25, 50, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPoLong", "modName": "po_indicator",
                       "params": {"args": [6, 13, 12, 26, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPoShort", "modName": "po_indicator",
                       "params": {"args": [6, 13, 12, 26, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPGOLong", "modName": "prettygoodoscillator_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPGOShort", "modName": "prettygoodoscillator_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPriceoscillatorLong", "modName": "priceoscillator_indicator",
                       "params": {"args": [12, 26, 9, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iPriceoscillatorShort", "modName": "priceoscillator_indicator",
                       "params": {"args": [12, 26, 9, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iZlindShort", "modName": "zlind_indicator",
                       "params": {"args": ["5", 50, "10", 50, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iZlindLong", "modName": "zlind_indicator",
                       "params": {"args": ["5", 50, "10", 50, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },

                      {"clsName": "iZlemaLong", "modName": "zlema_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iZlemaShort", "modName": "zlema_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },

                      {"clsName": "iWMSRLong", "modName": "wmsr_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iWMSRShort", "modName": "wmsr_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iWmaLong", "modName": "wma_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iWmaShort", "modName": "wma_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iVmaLong", "modName": "vma_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iVmaShort", "modName": "vma_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iViLong", "modName": "vi_indicator",
                       "params": {"args": ['14', DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iViShort", "modName": "vi_indicator",
                       "params": {"args": ["14", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iUoLong", "modName": "uo_indicator",
                       "params": {"args": [7, 14, 28, 14, 28, 56, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iUoShort", "modName": "uo_indicator",
                       "params": {"args": [7, 14, 28, 14, 28, 56, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iTSILong", "modName": "tsi_indicator",
                       "params": {"args": [25, 13, 1, 50, 26, 2, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iTSIShort", "modName": "tsi_indicator",
                       "params": {"args": [25, 13, 1, 50, 26, 2, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iTrixLong", "modName": "trix_indicator",
                       "params": {"args": [9, 15, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iTrixShort", "modName": "trix_indicator",
                       "params": {"args": [9, 15, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iStochasticSlowLong", "modName": "stochasticSlow_indicator",
                       "params": {"args": [14, 3, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iStochasticSlowShort", "modName": "stochasticSlow_indicator",
                       "params": {"args": [14, 3, DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iSMMALong", "modName": "smma_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iSMMAShort", "modName": "smma_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iRocLong", "modName": "roc_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iRocShort", "modName": "roc_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iRmiLong", "modName": "rmi_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      {"clsName": "iRmiShort", "modName": "rmi_indicator",
                       "params": {"args": ["5", "10", DAYS], "logic": {"byValue": 0, "compare": "ge"}}
                       },
                      ]
topshort_day = 3
TRADERATIONS_TopShort = [{"clsName": "iAroonUpDownTop", "modName": "aroon_indicator",
      "params": {"args": [14, topshort_day], "logic": {"byValue": 0, "compare": "ge"}, 'line': 'aroonup'}
      },
     {"clsName": "iAroonUpDownBottom", "modName": "aroon_indicator",
      "params": {"args": [14, topshort_day], "logic": {"byValue": 0, "compare": "ge"}, 'line': 'aroondown'}
      },
     {"clsName": "iAtrTop", "modName": "atr_indicator",
      "params": {"args": [14, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iAtrBottom", "modName": "atr_indicator",
      "params": {"args": [14, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {'clsName': 'iBollTop', 'modName': 'boll_indicator',
      'params': {'args': ['20', '2', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'top'}},
     {'clsName': 'iBollTop', 'modName': 'boll_indicator',
      'params': {'args': ['20', '2', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'mid'}},
     {'clsName': 'iBollTop', 'modName': 'boll_indicator',
      'params': {'args': ['20', '2', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'bot'}},
     {'clsName': 'iBollTop', 'modName': 'boll_indicator',
      'params': {'args': ['20', '2', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'bandwith'}},
     {'clsName': 'iBollBottom', 'modName': 'boll_indicator',
      'params': {'args': ['20', '2', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'top'}},
     {'clsName': 'iBollBottom', 'modName': 'boll_indicator',
      'params': {'args': ['20', '2', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'mid'}},
     {'clsName': 'iBollBottom', 'modName': 'boll_indicator',
      'params': {'args': ['20', '2', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'bot'}},
     {'clsName': 'iBollBottom', 'modName': 'boll_indicator',
      'params': {'args': ['20', '2', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'bandwith'}},

     {"clsName": "iCciTop", "modName": "cci_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iCciBottom", "modName": "cci_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {'clsName': 'iDmaTop', 'modName': 'dma_indicator',
      'params': {'args': ['5', '10', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'dma'}},
     {'clsName': 'iDmaTop', 'modName': 'dma_indicator',
      'params': {'args': ['5', '10', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'ama'}},
     {'clsName': 'iDmaBottom', 'modName': 'dma_indicator',
      'params': {'args': ['5', '10', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'dma'}},
     {'clsName': 'iDmaBottom', 'modName': 'dma_indicator',
      'params': {'args': ['5', '10', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'ama'}},
     {"clsName": "iDpoTop", "modName": "dpo_indicator",
      "params": {"args": [20, topshort_day], "logic": {"byValue": 0, "compare": "ge", 'position': 0}}
      },
     {"clsName": "iDpoBottom", "modName": "dpo_indicator",
      "params": {"args": [20, topshort_day], "logic": {"byValue": 0, "compare": "ge", 'position': 0}}
      },
     # {"clsName": "iDv2Top", "modName": "dv2_indicator",
     #  "params": {"args": [252, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
     #  },
     # {"clsName": "iDv2Bottom", "modName": "dv2_indicator",
     #  "params": {"args": [252, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
     #  },
     {"clsName": "iEmaTop", "modName": "ema_indicator",
      "params": {"args": ["5", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iEmaBottom", "modName": "ema_indicator",
      "params": {"args": ["5", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },

     {"clsName": "iHmaTop", "modName": "hma_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iHmaBottom", "modName": "hma_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },

     {"clsName": "iHurstTop", "modName": "hurst_indicator",
      "params": {"args": [40, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iHurstBottom", "modName": "hurst_indicator",
      "params": {"args": [40, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iKamaTop", "modName": "kama_indicator",
      "params": {"args": [10, 2, 30, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iKamaBottom", "modName": "kama_indicator",
      "params": {"args": [10, 2, 30, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {'clsName': 'iKdjTop', 'modName': 'kdj_indicator',
      'params': {'args': ['9', '3', '3', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'k'}},
     {'clsName': 'iKdjTop', 'modName': 'kdj_indicator',
      'params': {'args': ['9', '3', '3', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'd'}},
     {'clsName': 'iKdjTop', 'modName': 'kdj_indicator',
      'params': {'args': ['9', '3', '3', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'j'}},
     {'clsName': 'iKdjBottom', 'modName': 'kdj_indicator',
      'params': {'args': ['9', '3', '3', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'k'}},
     {'clsName': 'iKdjBottom', 'modName': 'kdj_indicator',
      'params': {'args': ['9', '3', '3', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'd'}},
     {'clsName': 'iKdjBottom', 'modName': 'kdj_indicator',
      'params': {'args': ['9', '3', '3', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'j'}},

     {'clsName': 'iKstTop', 'modName': 'kst_indicator',
      'params': {'args': [10, 15, 20, 30, 10, 10, 10, 15, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'},
                 'line': 'kst'}},
     {'clsName': 'iKstTop', 'modName': 'kst_indicator',
      'params': {'args': [10, 15, 20, 30, 10, 10, 10, 15, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'},
                 'line': 'signal'}},
     {'clsName': 'iKstBottom', 'modName': 'kst_indicator',
      'params': {'args': [10, 15, 20, 30, 10, 10, 10, 15, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'},
                 'line': 'kst'}},
     {'clsName': 'iKstBottom', 'modName': 'kst_indicator',
      'params': {'args': [10, 15, 20, 30, 10, 10, 10, 15, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'},
                 'line': 'signal'}},
     {"clsName": "iLrsiTop", "modName": "lrsi_indicator",
      "params": {"args": [6, topshort_day], "logic": {"byValue": 0, "compare": "ge", 'gamma': [0.5]}}
      },
     {"clsName": "iLrsiBottom", "modName": "lrsi_indicator",
      "params": {"args": [6, topshort_day], "logic": {"byValue": 0, "compare": "ge", 'gamma': [0.5]}}
      },
     {"clsName": "iMaTop", "modName": "ma_indicator",
      "params": {"args": ["5", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iMaBottom", "modName": "ma_indicator",
      "params": {"args": ["5", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {'clsName': 'iMacdTop', 'modName': 'macd_indicator',
      'params': {'args': ['12', '26', '9', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'dif'}},
     {'clsName': 'iMacdTop', 'modName': 'macd_indicator',
      'params': {'args': ['12', '26', '9', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'dea'}},
     {'clsName': 'iMacdTop', 'modName': 'macd_indicator',
      'params': {'args': ['12', '26', '9', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'hist'}},
     {'clsName': 'iMacdBottom', 'modName': 'macd_indicator',
      'params': {'args': ['12', '26', '9', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'dif'}},
     {'clsName': 'iMacdBottom', 'modName': 'macd_indicator',
      'params': {'args': ['12', '26', '9', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'dea'}},
     {'clsName': 'iMacdBottom', 'modName': 'macd_indicator',
      'params': {'args': ['12', '26', '9', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'hist'}},

     {"clsName": "iMomentumTop", "modName": "momentum_indicator",
      "params": {"args": [12, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iMomentumBottom", "modName": "momentum_indicator",
      "params": {"args": [12, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iMomentumOscTop", "modName": "momosc_indicator",
      "params": {"args": [12, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iMomentumOscBottom", "modName": "momosc_indicator",
      "params": {"args": [12, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iPctChangeTop", "modName": "percentchange_indicator",
      "params": {"args": [30, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iPctChangeBottom", "modName": "percentchange_indicator",
      "params": {"args": [30, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iPctRankTop", "modName": "percentrank_indicator",
      "params": {"args": [50, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iPctRankBottom", "modName": "percentrank_indicator",
      "params": {"args": [50, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iPoTop", "modName": "po_indicator",
      "params": {"args": [12, 26, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iPoBottom", "modName": "po_indicator",
      "params": {"args": [12, 26, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iPGOTop", "modName": "prettygoodoscillator_indicator",
      "params": {"args": ["14", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iPGOBottom", "modName": "prettygoodoscillator_indicator",
      "params": {"args": ["14", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {'clsName': 'iPriceoscillatorTop', 'modName': 'priceoscillator_indicator',
      'params': {'args': [12, 26, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'ppo'}},
     {'clsName': 'iPriceoscillatorTop', 'modName': 'priceoscillator_indicator',
      'params': {'args': [12, 26, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'signal'}},
     {'clsName': 'iPriceoscillatorTop', 'modName': 'priceoscillator_indicator',
      'params': {'args': [12, 26, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'histo'}},
     {'clsName': 'iPriceoscillatorBottom', 'modName': 'priceoscillator_indicator',
      'params': {'args': [12, 26, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'ppo'}},
     {'clsName': 'iPriceoscillatorBottom', 'modName': 'priceoscillator_indicator',
      'params': {'args': [12, 26, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'signal'}},
     {'clsName': 'iPriceoscillatorBottom', 'modName': 'priceoscillator_indicator',
      'params': {'args': [12, 26, 9, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'histo'}},
     {"clsName": "iRmiTop", "modName": "rmi_indicator",
      "params": {"args": ["5", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iRmiBottom", "modName": "rmi_indicator",
      "params": {"args": ["5", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iRocTop", "modName": "roc_indicator",
      "params": {"args": ["12", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iRocBottom", "modName": "roc_indicator",
      "params": {"args": ["12", topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iRsiTop", "modName": "rsi_indicator",
      "params": {"args": [14, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iRsiBottom", "modName": "rsi_indicator",
      "params": {"args": [14, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iSMMATop", "modName": "smma_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iSMMABottom", "modName": "smma_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {'clsName': 'iStochasticSlowTop', 'modName': 'stochasticSlow_indicator',
      'params': {'args': [14, 3, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'perck'}},
     {'clsName': 'iStochasticSlowTop', 'modName': 'stochasticSlow_indicator',
      'params': {'args': [14, 3, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'percd'}},
     {'clsName': 'iStochasticSlowBottom', 'modName': 'stochasticSlow_indicator',
      'params': {'args': [14, 3, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'perck'}},
     {'clsName': 'iStochasticSlowBottom', 'modName': 'stochasticSlow_indicator',
      'params': {'args': [14, 3, topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'percd'}},
     {"clsName": "iTrixTop", "modName": "trix_indicator",
      "params": {"args": [15, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iTrixBottom", "modName": "trix_indicator",
      "params": {"args": [15, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iTSITop", "modName": "tsi_indicator",
      "params": {"args": [25, 13, 1, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iTSIBottom", "modName": "tsi_indicator",
      "params": {"args": [25, 13, 1, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iUoTop", "modName": "uo_indicator",
      "params": {"args": [7, 14, 28, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iUoBottom", "modName": "uo_indicator",
      "params": {"args": [7, 14, 28, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {'clsName': 'iViTop', 'modName': 'vi_indicator',
      'params': {'args': ['14', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'vi_plus'}},
     {'clsName': 'iViTop', 'modName': 'vi_indicator',
      'params': {'args': ['14', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'vi_minus'}},
     {'clsName': 'iViBottom', 'modName': 'vi_indicator',
      'params': {'args': ['14', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'vi_plus'}},
     {'clsName': 'iViBottom', 'modName': 'vi_indicator',
      'params': {'args': ['14', topshort_day], 'logic': {'byValue': 0, 'compare': 'ge'}, 'line': 'vi_minus'}},
     {"clsName": "iVmaTop", "modName": "vma_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iVmaBottom", "modName": "vma_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iWmaTop", "modName": "wma_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iWmaBottom", "modName": "wma_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iWMSRTop", "modName": "wmsr_indicator",
      "params": {"args": [14, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iWMSRBottom", "modName": "wmsr_indicator",
      "params": {"args": [14, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iZlemaTop", "modName": "zlema_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iZlemaBottom", "modName": "zlema_indicator",
      "params": {"args": [5, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iZlindBottom", "modName": "zlind_indicator",
      "params": {"args": [5, 50, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     {"clsName": "iZlindTop", "modName": "zlind_indicator",
      "params": {"args": [5, 50, topshort_day], "logic": {"byValue": 0, "compare": "ge"}}
      },
     ]
position = [{'clsName': 'iMacdCrossGolden', 'modName': 'macd_indicator',
             'params': {'args': ['12', '26', '9'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iMacdCrossGolden', 'modName': 'macd_indicator',
             'params': {'args': ['12', '26', '9'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iMacdCrossDie', 'modName': 'macd_indicator',
             'params': {'args': ['12', '26', '9'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iMacdCrossDie', 'modName': 'macd_indicator',
             'params': {'args': ['12', '26', '9'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iCciCrossGolden', 'modName': 'cci_indicator',
             'params': {'args': [5, 10], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iCciCrossGolden', 'modName': 'cci_indicator',
             'params': {'args': [5, 10], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iCciCrossDie', 'modName': 'cci_indicator',
             'params': {'args': [5, 10], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iCciCrossDie', 'modName': 'cci_indicator',
             'params': {'args': [5, 10], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iDmaCrossGolden', 'modName': 'dma_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iDmaCrossGolden', 'modName': 'dma_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iDmaCrossDie', 'modName': 'dma_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iDmaCrossDie', 'modName': 'dma_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iDpoCrossGolden', 'modName': 'dpo_indicator',
             'params': {'args': [20, 40], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iDpoCrossGolden', 'modName': 'dpo_indicator',
             'params': {'args': [20, 40], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iDpoCrossDie', 'modName': 'dpo_indicator',
             'params': {'args': [20, 40], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iDpoCrossDie', 'modName': 'dpo_indicator',
             'params': {'args': [20, 40], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iHurstCrossGolden', 'modName': 'hurst_indicator',
             'params': {'args': [40, 80], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iHurstCrossGolden', 'modName': 'hurst_indicator',
             'params': {'args': [40, 80], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iHurstCrossDie', 'modName': 'hurst_indicator',
             'params': {'args': [40, 80], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iHurstCrossDie', 'modName': 'hurst_indicator',
             'params': {'args': [40, 80], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iKstCrossGolden', 'modName': 'kst_indicator',
             'params': {'args': [10, 15, 20, 30, 10, 10, 10, 15, 9],
                        'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iKstCrossGolden', 'modName': 'kst_indicator',
             'params': {'args': [10, 15, 20, 30, 10, 10, 10, 15, 9],
                        'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iKstCrossDie', 'modName': 'kst_indicator',
             'params': {'args': [10, 15, 20, 30, 10, 10, 10, 15, 9],
                        'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iKstCrossDie', 'modName': 'kst_indicator',
             'params': {'args': [10, 15, 20, 30, 10, 10, 10, 15, 9],
                        'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iPctChangeCrossGolden', 'modName': 'percentchange_indicator',
             'params': {'args': ['15', '30'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iPctChangeCrossGolden', 'modName': 'percentchange_indicator',
             'params': {'args': ['15', '30'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iPctChangeCrossDie', 'modName': 'percentchange_indicator',
             'params': {'args': ['15', '30'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iPctChangeCrossDie', 'modName': 'percentchange_indicator',
             'params': {'args': ['15', '30'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iPGOCrossGolden', 'modName': 'prettygoodoscillator_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iPGOCrossGolden', 'modName': 'prettygoodoscillator_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iPGOCrossDie', 'modName': 'prettygoodoscillator_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iPGOCrossDie', 'modName': 'prettygoodoscillator_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iPriceoscillatorCrossGolden', 'modName': 'priceoscillator_indicator',
             'params': {'args': [12, 26, 9], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iPriceoscillatorCrossGolden', 'modName': 'priceoscillator_indicator',
             'params': {'args': [12, 26, 9], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iPriceoscillatorCrossDie', 'modName': 'priceoscillator_indicator',
             'params': {'args': [12, 26, 9], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iPriceoscillatorCrossDie', 'modName': 'priceoscillator_indicator',
             'params': {'args': [12, 26, 9], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iRmiCrossGolden', 'modName': 'rmi_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iRmiCrossGolden', 'modName': 'rmi_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iRmiCrossDie', 'modName': 'rmi_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iRmiCrossDie', 'modName': 'rmi_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iRsiCrossGolden', 'modName': 'rsi_indicator',
             'params': {'args': ['6', '12', '30'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iRsiCrossGolden', 'modName': 'rsi_indicator',
             'params': {'args': ['6', '12', '30'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iRsiCrossDie', 'modName': 'rsi_indicator',
             'params': {'args': ['6', '12', '30'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iRsiCrossDie', 'modName': 'rsi_indicator',
             'params': {'args': ['6', '12', '30'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iStochasticSlowCrossGolden', 'modName': 'stochasticSlow_indicator',
             'params': {'args': [14, 3, 28, 6], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iStochasticSlowCrossGolden', 'modName': 'stochasticSlow_indicator',
             'params': {'args': [14, 3, 28, 6], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iStochasticSlowCrossDie', 'modName': 'stochasticSlow_indicator',
             'params': {'args': [14, 3, 28, 6], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iStochasticSlowCrossDie', 'modName': 'stochasticSlow_indicator',
             'params': {'args': [14, 3, 28, 6], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iTrixCrossGolden', 'modName': 'trix_indicator',
             'params': {'args': [9, 15], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iTrixCrossGolden', 'modName': 'trix_indicator',
             'params': {'args': [9, 15], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iTrixCrossDie', 'modName': 'trix_indicator',
             'params': {'args': [9, 15], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iTrixCrossDie', 'modName': 'trix_indicator',
             'params': {'args': [9, 15], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iTSICrossGolden', 'modName': 'tsi_indicator',
             'params': {'args': [25, 13, 1, 50, 26, 2], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iTSICrossGolden', 'modName': 'tsi_indicator',
             'params': {'args': [25, 13, 1, 50, 26, 2], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iTSICrossDie', 'modName': 'tsi_indicator',
             'params': {'args': [25, 13, 1, 50, 26, 2], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iTSICrossDie', 'modName': 'tsi_indicator',
             'params': {'args': [25, 13, 1, 50, 26, 2], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iUoCrossGolden', 'modName': 'uo_indicator',
             'params': {'args': [7, 14, 28, 14, 28, 56], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iUoCrossGolden', 'modName': 'uo_indicator',
             'params': {'args': [7, 14, 28, 14, 28, 56], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iUoCrossDie', 'modName': 'uo_indicator',
             'params': {'args': [7, 14, 28, 14, 28, 56], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iUoCrossDie', 'modName': 'uo_indicator',
             'params': {'args': [7, 14, 28, 14, 28, 56], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},
            {'clsName': 'iWMSRCrossGolden', 'modName': 'wmsr_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': 1}}},
            {'clsName': 'iWMSRCrossGolden', 'modName': 'wmsr_indicator',
             'params': {'args': ['5', '10'], 'logic': {'byValue': 0, 'compare': 'ge', 'position': -1}}},


            ]

TRADERATIONS = {'mom': MOMENTUM, 'pat': PATTERN, 'all': PATTERN + MOMENTUM+TRADERATIONS_CROSS1 + TRADERATIONS_HEAD1 + TRADERATIONS_TopShort+position,
                'test1': [{"clsName": "iViDistance", "modName": "vi_indicator",
                           "params": {"args": ["14"], "logic": {"byValue": 0, "compare": "ge"}}
                           }, ]
                }
