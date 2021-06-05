from backtrader import Indicator
import backtrader.indicators as btind
import copy
import backtrader as bt

# todo 生成因子信号的基类
class iBaseIndicator(Indicator):
    '''
    因子基类:
    byValue: price：与data.close比较,
             数字：signal与值比较
    '''
    # lines = ('iquant', )
    params = dict(rule=list())

    def __init__(self):
        # 深度复制(而非浅复制或引用)，args,logic改变时,不改变rule
        # self.args = list(map(int, copy.deepcopy(self.p.rule['args'])))
        self.sigline = copy.deepcopy(self.p.rule.get('line','')).lower()
        self.args = copy.deepcopy(self.p.rule['args'])
        try:
            int(self.args[-1])
            self.args = list(map(int, self.args))
        except:
            self.args = list(map(int, self.args[:-1])) + self.args[-1:]

        self.logic = copy.deepcopy(self.p.rule['logic'])

        # 判断logic是否有值，否则给一个默认值
        self.logic['byValue']  = self.logic.get('byValue', 0)
        self.logic['byMax'] = float(self.logic.get('byMax', 5))
        self.logic['compare'] = self.logic.get('compare', 'ge')
        # logic的底部/顶部
        self.logic['position'] = self.logic.get('position', 0)

        # 判断byValue是收盘价还是数字
        if self.logic['byValue'] == '{close}':
            self.logic['byValue'] = self.data.close
        # elif self.logic['byValue'] == '{open}':
        #     self.logic['byValue'] = self.data.open
        else:
            self.logic['byValue'] = [float(self.logic['byValue'])]

    def prenext(self):
        self.next()



# todo KDJ因子
class iKdj(Indicator):
    '''
    KDJ因子算法：
        1、n日RSV=（Cn－Ln）/（Hn－Ln）×100
        2、当日K值=2/3×前一日K值+1/3×当日RSV
        3、当日D值=2/3×前一日D值+1/3×当日K值
        4、若无前一日K 值与D值，则可分别用50来代替。
        5、J值=3*当日K值-2*当日D值

    参数：('period', 20)，20日KDJ

    结果：生成三个信号，k,d,j在图上为三根线

    参考：https://ichihedge.wordpress.com/2017/03/22/indicator-calculating-kdj/
    '''
    lines = ('k', 'd', 'j', )
    params = (
        ('period', 20),
        ('a', 3),
        ('b', 3),
    )

    def __init__(self):
        # try:
        #     print(self.data.close[0])
        #     Ln = bt.Min(self.data.close, period=self.p.period)
        #     Hn = bt.Max(self.data.high, period=self.p.period)
        #     Cn = self.data.close[0]
        #     RSV = (Cn - Ln) / (Hn - Ln) * 100
        #     self.lines.k = K = (self.p.a - 1) / self.p.a * self.lines.k[-1] + 1 / self.p.a * RSV
        #     self.lines.d = D = (self.p.b - 1) / self.p.b * self.lines.d[-1] + 1 / self.p.b * K
        #     self.lines.j = J = 3 * K - 2 * D
        # except Exception as e:
        #     print(e)
        #     self.lines.k = K = 50
        #     self.lines.d = D = 50
        #     self.lines.j = J = 3 * K - 2 * D
        pass

    def next(self):
        try:
            Ln = min(self.data.close.get(size=self.p.period))
            Hn = max(self.data.high.get(size=self.p.period))
            Cn = self.data[0]
            RSV = (Cn - Ln) / (Hn - Ln) * 100
            self.lines.k[0] = K = (self.p.a-1)/self.p.a * self.lines.k[-1] + 1/self.p.a * RSV
            self.lines.d[0] = D = (self.p.b-1)/self.p.b * self.lines.d[-1] + 1/self.p.b * K
            self.lines.j[0] = J = 3 * K - 2 * D
        except Exception as e:
            self.lines.k[0] = K = 50
            self.lines.d[0] = D = 50
            self.lines.j[0] = J = 3 * K - 2 * D


# todo DMA因子
class iDma(Indicator):
    '''
    因子计算：
        1、DMA=股价短期平均值—股价长期平均值
        2、AMA=DMA短期平均值

    参数：('short', 10),短期平均周期，   ('long', 50),长期平均周期

    结果：生成dma, ama两个信号，在图上显示为两根线

    参考：https://baike.baidu.com/item/平行线差指标/220914?fr=aladdin
    '''
    lines = ('dma', 'ama', )
    params = (
        ('short', 10),
        ('long', 50),
    )

    def __init__(self):
        self.short_sma = btind.SimpleMovingAverage(self.data, period=self.p.short)
        self.long_sma = btind.SimpleMovingAverage(self.data, period=self.p.long)
        self.lines.dma = self.short_sma - self.long_sma
        self.lines.ama = btind.SimpleMovingAverage(self.lines.dma, period=self.p.short)