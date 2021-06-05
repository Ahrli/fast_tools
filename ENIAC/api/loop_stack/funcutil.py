import json
import time

import arrow
import backtrader as bt
from functools import reduce

def swapVal(mp, key, val):
    if (mp == "timeReturn" or mp == "annualReturn"):
        val = mustRound(val, 4)
        return val

    return changeDict(key, val)

def changeDict(key, val):
    if (isinstance(val, bt.utils.autodict.AutoOrderedDict)):
        f = dict()
        for k, v in val.items():
            if (isinstance(v, bt.utils.autodict.AutoOrderedDict)):
                f[k] = changeDict(k, v)
            else:
                f[k] = myRound(k, v)

        return f

    if (isinstance(val, list)):
        listRound(val, 2)
        return val

    return myRound(key, val)

def myRound(k, v):
    if (k == "sqn" or k == "drawdown"):
        v = mustRound(v, 4)
        return v

    return mustRound(v, 2)

def mustRound(x, num):
    if (isinstance(x, float)):
        return round(x, num)
    else:
        return x

def listRound(f, num):
    for i, d in enumerate(f):
        if (isinstance(d, list)):
            listRound(d, num)
        else:
            f[i] = mustRound(d, num)

def addRs(mp, xdd, analyzer):
    # print("analyzer result:", mp)
    hdd = dict()
    for key, val in analyzer.get_analysis().items():
        # print('key: {}  value:{}'.format(key, val))
        hdkey=str(key)
        hdd[hdkey] = swapVal(mp, key, val)

    xdd[mp] = hdd

def addTrRs(mp, xdd, analyzer):
    # print("analyzer result:", mp)
    hdd = dict()
    for key, val in analyzer.get_analysis().items():
        hdkey=int(time.mktime(key.timetuple()))*1000
        val=round(val*100,2)
        hdd[hdkey] = swapVal(mp, key, val)

    xdd[mp] = funcTr(hdd)#转换收益率

def funcTr(timeReturn):
    trlist = [('0',1)]+list(timeReturn.items())
    def fn(y, t):
        return t[0], y[1] * (1 + t[1]/100)
    r = list(map(lambda x: (x[0], round((x[1]-1)*100,2)), [reduce(fn, trlist[:i+1]) for i in range(len(trlist))]))
    return dict(r[1:])

def addRecordsRs(mp,xdd, analyzer,bullBear):
    # print("analyzer result:", mp)
    hdd = dict()
    lastp = dict()
    for key, val in analyzer.get_analysis().items():
        #print('key: {}  value:{}'.format(key, val))
        hdkey=int(time.mktime(key.timetuple()))*1000
        ls = swapVal(mp, key, val)
        #dpos=pnlt.get(hdkey,dict())
        for als in ls:
            b=als[4]
            a=lastp.get(als[3],0.0)
            c=0.0 #盈利金额
            yi=0.0 #收益率
            #建仓
            if((als[0]>0 and bullBear==0)or (als[0]<0 and bullBear!=0)):
                pass
                lastp[als[3]] = b#记录建仓的值
            else:#平仓
                pass
                c=b+a
                yi=round(c*100/abs(a),2)
                del lastp[als[3]]
              
            als.append(c)
            als.append(yi)

        hdd[hdkey]=ls

    xdd[mp] = hdd

# def saveRedis(excuteId, hdd):
#     pool = redis.ConnectionPool(host='192.168.80.188', port=6379, decode_responses=True, db=0,
#                                 password='LOOP2themoon')  # host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
#     rd = redis.Redis(connection_pool=pool)
#     rd.set("backtrader:{}".format(excuteId), json.dumps(hdd, ensure_ascii=False), ex=3600 * 24 * 7)
#     rd.connection_pool.disconnect()
#     pool.disconnect()


# key = '2017-11-02 00:00:00'
# val = [[1, 287.78, 0, 'OKEX.ETH', -287.78]]
#
# a = swapVal('demo', key, val)
# print(a)
#
# c=lastp.get(als[3],0.0)
def loopresult(r,rule):
    lt = []
    # a = ["category","stockCode","stockType","imgUrl","volume","price","stockName","type","turnover","profit","profitRate",]
    a = ["volume","price",  'unknow', "stockCode","turnover","profit","profitRate",   ]
    total_times = 0
    won = 0
    for k,v in r['records'].items():

        dc = {}
        dc['date']=k
        ltt = []
        for i in v:
            _dc = dict(zip(a, i))
            if _dc['volume'] >0:

                _dc['type']=0

            else:
                _dc['type'] = 1
            _dc['category'] = (_dc['stockCode']).split('.')[0]
            _dc['stockName'] = (_dc['stockCode'])
            ltt.append(_dc)
            if _dc['profitRate']<0:
                won += 1
            total_times += 1


        dc['records']=ltt
        lt.append(dc)


    data_dc ={}
    for i in r.keys():
        if i=="records":
            continue
        data_dc[i] = r[i]
    data_dc['transactionRecordVO'] =lt
    # 倒叙
    data_dc["transactionRecordVO"].reverse()
    # data_dc["sqn"] =r['sqn']
    # data_dc["timeReturn"] =r['timeReturn']
    # data_dc["annualReturn"] =r['annualReturn']
    # data_dc["sharpeRatio"] =r['sharpeRatio']
    # data_dc["drawDown"] =r['drawDown']
    # data_dc["tradeAnalyzer"] =r['tradeAnalyzer']
    # data_dc["create_time"] =r['create_time']
    #
    timeReturn = list(r["timeReturn"].items())

    data_dc["startDay"] =arrow.get(timeReturn[0][0]/1000).to("local").format('YYYY-MM-DD')
    data_dc["endDay"] =arrow.get(timeReturn[-1][0]/1000).to("local").format('YYYY-MM-DD')
    data_dc["startCash"] =rule['startCash']
    data_dc["won"] =round(100 -(won/total_times)*100,2)

    # data_dc["endDay"] =rule['endDay']

    # print(json.dumps(data_dc))
    dc = {}
    for k,v in data_dc["timeReturn"].items():
        dc[str(k)] = v
    data_dc["timeReturn"] =dc

    return data_dc

# # 1522512000000
# a = arrow.get(1522512000).format('YYYY-MM-DD')
# print(a)
#
# print(arrow.get(1570723200).to("local").format('YYYY-MM-DD'))
# print(arrow.get(1570464000).to("local").format('YYYY-MM-DD'))
# print(arrow.get(1570723200).to("local").format('YYYY-MM-DD'))