# import backtrader.indicators as btind
# from . import compare_price as compare
import backtrader.talib as btalib
from .base_indicator import iBaseIndicator
import talib
import numpy as np

'''
因子：形态识别
分类：
   函数名：CDL2CROWS
   名称：Two Crows 两只乌鸦
   integer = CDL2CROWS(open, high, low, close)
   ```
   函数名：CDL3BLACKCROWS
   名称：Three Black Crows 三只乌鸦
   integer = CDL3BLACKCROWS(open, high, low, close)
   ```
   函数名：CDL3INSIDE
   名称： Three Inside Up/Down 三内部上涨和下跌
   integer = CDL3INSIDE(open, high, low, close)
   ```
   函数名：CDL3LINESTRIKE
   名称： Three-Line Strike 三线打击
   integer = CDL3LINESTRIKE(open, high, low, close)
   ```
   函数名：CDL3OUTSIDE
   名称：Three Outside Up/Down 三外部上涨和下跌
   integer = CDL3OUTSIDE(open, high, low, close)
   ```
   函数名：CDL3STARSINSOUTH
   名称：Three Stars In The South 南方三星
   integer = CDL3STARSINSOUTH(open, high, low, close)
   ```
   函数名：CDL3WHITESOLDIERS
   名称：Three Advancing White Soldiers 三个白兵
   integer = CDL3WHITESOLDIERS(open, high, low, close)
   ```
   函数名：CDLABANDONEDBABY
   名称：Abandoned Baby 弃婴
   integer = CDLABANDONEDBABY(open, high, low, close, penetration=0)
   ```
   函数名：CDLADVANCEBLOCK
   名称：Advance Block 大敌当前
   integer = CDLADVANCEBLOCK(open, high, low, close)
   ```
   函数名：CDLBELTHOLD
   名称：Belt-hold 捉腰带线
   integer = CDLBELTHOLD(open, high, low, close)
   ```
   函数名：CDLBREAKAWAY
   名称：Breakaway 脱离
   integer = CDLBREAKAWAY(open, high, low, close)
   ```
   函数名：CDLCLOSINGMARUBOZU
   名称：Closing Marubozu 收盘缺影线
   integer = CDLCLOSINGMARUBOZU(open, high, low, close)
   ```
   函数名：CDLCONCEALBABYSWALL
   名称： Concealing Baby Swallow 藏婴吞没
   integer = CDLCONCEALBABYSWALL(open, high, low, close)
   ```
   函数名：CDLCOUNTERATTACK
   名称：Counterattack 反击线
   integer = CDLCOUNTERATTACK(open, high, low, close)
   ```
   函数名：CDLDARKCLOUDCOVER
   名称：Dark Cloud Cover 乌云压顶
   integer = CDLDARKCLOUDCOVER(open, high, low, close, penetration=0)
   ```
   函数名：CDLDOJI
   名称：Doji 十字
   integer = CDLDOJI(open, high, low, close)
   ```
   函数名：CDLDOJISTAR
   名称：Doji Star 十字星
   integer = CDLDOJISTAR(open, high, low, close)
   ```
   函数名：CDLDRAGONFLYDOJI
   名称：Dragonfly Doji 蜻蜓十字/T形十字
   integer = CDLDRAGONFLYDOJI(open, high, low, close)
   ```
   函数名：CDLENGULFING
   名称：Engulfing Pattern 吞噬模式
   integer = CDLENGULFING(open, high, low, close)
   ```
   函数名：CDLEVENINGDOJISTAR
   名称：Evening Doji Star 十字暮星
   integer = CDLEVENINGDOJISTAR(open, high, low, close, penetration=0)
   ```
   函数名：CDLEVENINGSTAR
   名称：Evening Star 暮星
   integer = CDLEVENINGSTAR(open, high, low, close, penetration=0)
   ```
   函数名：CDLGAPSIDESIDEWHITE
   名称：Up/Down-gap side-by-side white lines 向上/下跳空并列阳线
   integer = CDLGAPSIDESIDEWHITE(open, high, low, close)
   ```
   函数名：CDLGRAVESTONEDOJI
   名称：Gravestone Doji 墓碑十字/倒T十字
   integer = CDLGRAVESTONEDOJI(open, high, low, close)
   ```
   函数名：CDLHAMMER
   名称：Hammer 锤头
   integer = CDLHAMMER(open, high, low, close)
   ```
   函数名：CDLHANGINGMAN
   名称：Hanging Man 上吊线
   integer = CDLHANGINGMAN(open, high, low, close)
   ```
   函数名：CDLHARAMI
   名称：Harami Pattern 母子线
   integer = CDLHARAMI(open, high, low, close)
   ```
   函数名：CDLHARAMICROSS
   名称：Harami Cross Pattern 十字孕线
   integer = CDLHARAMICROSS(open, high, low, close)
   ```
   函数名：CDLHIGHWAVE
   名称：High-Wave Candle 风高浪大线
   integer = CDLHIGHWAVE(open, high, low, close)
   ```
   函数名：CDLHIKKAKE
   名称：Hikkake Pattern 陷阱
   integer = CDLHIKKAKE(open, high, low, close)
   ```
   函数名：CDLHIKKAKEMOD
   名称：Modified Hikkake Pattern 修正陷阱
   integer = CDLHIKKAKEMOD(open, high, low, close)
   ```
   函数名：CDLHOMINGPIGEON
   名称：Homing Pigeon 家鸽
   integer = CDLHOMINGPIGEON(open, high, low, close)
   ```
   函数名：CDLIDENTICAL3CROWS
   名称：Identical Three Crows 三胞胎乌鸦
   integer = CDLIDENTICAL3CROWS(open, high, low, close)
   ```
   函数名：CDLINNECK
   名称：In-Neck Pattern 颈内线
   integer = CDLINNECK(open, high, low, close)
   ```
   函数名：CDLINVERTEDHAMMER
   名称：Inverted Hammer 倒锤头
   integer = CDLINVERTEDHAMMER(open, high, low, close)
   ```
   函数名：CDLKICKING
   名称：Kicking 反冲形态
   integer = CDLKICKING(open, high, low, close)
   ```
   函数名：CDLKICKINGBYLENGTH
   名称：Kicking - bull/bear determined by the longer marubozu 由较长缺影线决定的反冲形态
   integer = CDLKICKINGBYLENGTH(open, high, low, close)
   ```
   函数名：CDLLADDERBOTTOM
   名称：Ladder Bottom 梯底
   integer = CDLLADDERBOTTOM(open, high, low, close)
   ```
   函数名：CDLLONGLEGGEDDOJI
   名称：Long Legged Doji 长脚十字
   integer = CDLLONGLEGGEDDOJI(open, high, low, close)
   ```
   函数名：CDLLONGLINE
   名称：Long Line Candle 长蜡烛
   integer = CDLLONGLINE(open, high, low, close)
   ```
   函数名：CDLMARUBOZU
   名称：Marubozu 光头光脚/缺影线
   integer = CDLMARUBOZU(open, high, low, close)
   ```
   函数名：CDLMATCHINGLOW
   名称：Matching Low 相同低价
   integer = CDLMATCHINGLOW(open, high, low, close)
   ```
   函数名：CDLMATHOLD
   名称：Mat Hold 铺垫
   integer = CDLMATHOLD(open, high, low, close, penetration=0)
   ```
   函数名：CDLMORNINGDOJISTAR
   名称：Morning Doji Star 十字晨星
   integer = CDLMORNINGDOJISTAR(open, high, low, close, penetration=0)
   ```
   函数名：CDLMORNINGSTAR
   名称：Morning Star 晨星
   integer = CDLMORNINGSTAR(open, high, low, close, penetration=0)
   ```
   函数名：CDLONNECK
   名称：On-Neck Pattern 颈上线
   integer = CDLONNECK(open, high, low, close)
   ```
   函数名：CDLPIERCING
   名称：Piercing Pattern 刺透形态
   integer = CDLPIERCING(open, high, low, close)
   ```
   函数名：CDLRICKSHAWMAN
   名称：Rickshaw Man 黄包车夫
   integer = CDLRICKSHAWMAN(open, high, low, close)
   ```
   函数名：CDLRISEFALL3METHODS
   名称：Rising/Falling Three Methods 上升/下降三法
   integer = CDLRISEFALL3METHODS(open, high, low, close)
   ```
   函数名：CDLSEPARATINGLINES
   名称：Separating Lines 分离线
   integer = CDLSEPARATINGLINES(open, high, low, close)
   ```
   函数名：CDLSHOOTINGSTAR
   名称：Shooting Star 射击之星
   integer = CDLSHOOTINGSTAR(open, high, low, close)
   ```
   函数名：CDLSHORTLINE
   名称：Short Line Candle 短蜡烛
   integer = CDLSHORTLINE(open, high, low, close)
   ```
   函数名：CDLSPINNINGTOP
   名称：Spinning Top 纺锤
   integer = CDLSPINNINGTOP(open, high, low, close)
   ```
   函数名：CDLSTALLEDPATTERN
   名称：Stalled Pattern 停顿形态
   integer = CDLSTALLEDPATTERN(open, high, low, close)
   ```
   函数名：CDLSTICKSANDWICH
   名称：Stick Sandwich 条形三明治
   integer = CDLSTICKSANDWICH(open, high, low, close)
   ```
   函数名：CDLTAKURI
   名称：Takuri (Dragonfly Doji with very long lower shadow)
   探水竿
   integer = CDLTAKURI(open, high, low, close)
   ```
   函数名：CDLTASUKIGAP
   名称：Tasuki Gap 跳空并列阴阳线
   integer = CDLTASUKIGAP(open, high, low, close)
   ```
   函数名：CDLTHRUSTING
   名称：Thrusting Pattern 插入
   integer = CDLTHRUSTING(open, high, low, close)
   ```
   函数名：CDLTRISTAR
   名称：Tristar Pattern 三星
   integer = CDLTRISTAR(open, high, low, close)
   ```
   函数名：CDLUNIQUE3RIVER
   名称：Unique 3 River 奇特三河床
   integer = CDLUNIQUE3RIVER(open, high, low, close)
   ```
   函数名：CDLUPSIDEGAP2CROWS
   名称：Upside Gap Two Crows 向上跳空的两只乌鸦
   integer = CDLUPSIDEGAP2CROWS(open, high, low, close)
   ```
   函数名：CDLXSIDEGAP3METHODS
   名称：Upside/Downside Gap Three Methods 上升/下降跳空三法
   integer = CDLXSIDEGAP3METHODS(open, high, low, close)
   ```
'''


class iPatternUp(iBaseIndicator):

    lines = ('pup', )
    params = dict(rule=list())
    penetration0 = ['CDLABANDONEDBABY','CDLDARKCLOUDCOVER','CDLEVENINGDOJISTAR','CDLEVENINGSTAR','CDLMATHOLD','CDLMORNINGDOJISTAR','CDLMORNINGSTAR']

    def __init__(self):
        super(iPatternUp, self).__init__()
        sigline = self.sigline.upper()
        if sigline in self.penetration0:
            self.pattern = eval(f'btalib.{sigline}(self.data.open, self.data.high, self.data.low, self.data.close, penetration=0)')

        else:
            self.pattern = eval(f'btalib.{sigline}(self.data.open, self.data.high, self.data.low, self.data.close)')
        # self.lines.pattern = eval(f'btalib.{self.sigline}(self.data.open, self.data.high,self.data.low, self.data.close)')

    def next(self):
        # print(self.data.datetime.date())
        # print(self.pattern[0])
        self.lines.pup[0] = self.pattern[0] > 0




class iPatternDown(iBaseIndicator):
    lines = ('pdown', )
    params = dict(rule=list())
    penetration0 = ['CDLABANDONEDBABY','CDLDARKCLOUDCOVER','CDLEVENINGDOJISTAR','CDLEVENINGSTAR','CDLMATHOLD','CDLMORNINGDOJISTAR','CDLMORNINGSTAR']

    def __init__(self):
        super(iPatternDown, self).__init__()
        sigline = self.sigline.upper()

        if sigline in self.penetration0:
            self.pattern = eval(f'btalib.{sigline}(self.data.open, self.data.high, self.data.low, self.data.close, penetration=0)')

        else:
            self.pattern = eval(f'btalib.{sigline}(self.data.open, self.data.high, self.data.low, self.data.close)')

    def next(self):
        self.lines.pdown[0] = self.pattern[0] < 0