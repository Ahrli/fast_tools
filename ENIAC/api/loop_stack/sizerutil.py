import math
import json
import redis

def getAdjMaxPrice(strategy,cursize,perc):
        # 最大可用现金，基于当前可用现金的比例
        max_risk = math.floor(strategy.broker.cash * strategy.p.rule['riskControl']['maxAllPositionRate'])
        # 固定佣金
        fixedcomm=0
        if("commission" in strategy.p.rule):
            fixedcomm = strategy.p.rule['commission']

        #单只股票最高购买最高上限,比如0.30
        maxRPS = strategy.p.rule['riskControl']['maxRPS']

        x = perc
        if (x > maxRPS):
            x = maxRPS

        rs =(max_risk - (fixedcomm * 2)*cursize) * x # 当前股票最大可购买的现金
        return float('{:.3f}'.format(rs)[:-1])

def getShortAdjMaxPrice(strategy,cursize,perc):
        # 最大可用现金，基于当前portvalue
        max_risk = math.floor(strategy.broker.getvalue() * strategy.p.rule['riskControl']['maxAllPositionRate'])
        # 固定佣金
        fixedcomm=0
        if("commission" in strategy.p.rule):
            fixedcomm = strategy.p.rule['commission']

        #单只股票最高购买最高上限,比如0.30
        maxRPS = strategy.p.rule['riskControl']['maxRPS']

        x = perc
        if (x > maxRPS):
            x = maxRPS

        rs =(max_risk - (fixedcomm * 2)*cursize) * x # 当前股票最大可购买的现金
        return float('{:.3f}'.format(rs)[:-1])


def getMarketDistribute(buys_pool):
    rs = dict()

    pool = redis.ConnectionPool(host='192.168.80.188', port=6379, decode_responses=True, db=0,
                                password='LOOP2themoon')  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
    rd = redis.Redis(connection_pool=pool)
    pip = rd.pipeline()
    for stock in buys_pool:
        pip.get("snapshot_format:{}".format(stock._name))

    prs=pip.execute()
    total=0    #总市值
    circular=0 #流通市值
    for snp in prs:
        mk=json.loads(snp)       
        a=round(math.sqrt(mk["totalMarketVal"]),2)
        total+=a
        b=a
        circular+=b
        mkls=list()
        mkls.append(a)
        mkls.append(b)
        rs[mk["stockCode"]]=mkls

    rs["bt_total"]=total
    rs["bt_circular"]=circular
    return rs


def getbuysize(strategy, d, cursize,com_adj_max_risk):
        pos = strategy.getposition(d)
        acc_value = strategy.broker.getvalue()  
        cash =  strategy.broker.cash    
        #Print results
        '''
        print('----------- BUY SIZING INFO START -----------')
        print('buy {},datetime: {}'.format(d._name,d.datetime.date()))
        print('cursize: {}'.format(cursize))
        print(pos)
        print('Account Value: {}'.format(acc_value))
        print('com_adj_max_risk: {}'.format(com_adj_max_risk))
        print('Cash: {}'.format(cash))
        print('data[0]: {}'.format(d[0]))
        print('------------ BUY SIZING INFO END------------')
        '''
        # 印花税
        stamp_duty=0
        if("stampDuty" in strategy.p.rule):
           stamp_duty = strategy.p.rule['stampDuty']
        
        com_adj_price = d[0] * (1 + stamp_duty )  # 购买一股份至少需要多岁钱
        
        com_adj_size = com_adj_max_risk / com_adj_price
        if com_adj_size < 0: 
           com_adj_size = 0
        # return math.floor(com_adj_size/100)*100
        return com_adj_size

def getShortSellsize(strategy, d, cursize,com_adj_max_risk):  
        # 印花税
        stamp_duty=0
        if("stampDuty" in strategy.p.rule):
           stamp_duty = strategy.p.rule['stampDuty']
        
        com_adj_price = d[0] * (1 + stamp_duty )  # 购买一股份至少需要多岁钱
        
        com_adj_size = com_adj_max_risk / com_adj_price
        if com_adj_size < 0: 
           com_adj_size = 0
        rs= math.floor(com_adj_size/100)*100
        # return rs
        return com_adj_size

def getsellsize(strategy, d):
        pos = strategy.getposition(d)
        acc_value = strategy.broker.getvalue()  
        startCash = strategy.broker.startingcash 
        cash =  strategy.broker.cash    
        #Print results
        '''
        print('----------- SELL SIZING INFO START -----------')
        print('datetime: {}'.format(d.datetime.date()))
        print(pos)
        print('Account Value: {}'.format(acc_value))
        print('startCash: {}'.format(startCash))
        print('sellCash: {}'.format(cash))
        print('data[0]: {}'.format(d[0]))
        print('------------ SELL SIZING INFO END------------')
        '''
        com_adj_size = pos.size * -1 #全卖
        # return math.floor(com_adj_size/100)*100
        return com_adj_size