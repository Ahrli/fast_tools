from elasticsearch import Elasticsearch
import os
import pandas as pd
import pendulum
import functools
from pandasql import sqldf
import numpy as np
from retrying import retry
# global systemSignal
systemSignal = os.system('ls /.dockerenv')

@retry()
def get_es_group_stacks(codes=['US.APLE',
                               'US.TSLA',
                               'US.GOOG',
                               'US.FB',
                               'US.NVDA',
                               'US.AMD',
                               'US.AMZN',
                               'US.BABA'],
                        dim='kline_day',
                        startTS=pendulum.now().add(years=-5).timestamp(), # 默认5年数据
                        endTS=pendulum.now().timestamp()):

    es = Elasticsearch(['192.168.80.183'], http_auth=('elastic', 'LOOP2themoon'), port=9200)

    def serialize(hit):
        fields = hit["fields"]
        for k in fields:
            fields[k] = fields[k][0]
        return fields

    @retry(stop_max_attempt_number=5)
    def get_es_stock(code='US.APLE',
                     dim='kline_day',
                     startTS=pendulum.now().add(years=-5).timestamp(),  # 默认5年数据
                     endTS=pendulum.now().timestamp()):
        sql = {
            "query":
                {"bool": {"must": [{"bool": {"must": [{"term": {"code": {"value": code, "boost": 1}}},
                                                      {"range": {"time_key": {"from": int(startTS), "to": None,
                                                                              "include_lower": False,
                                                                              "include_upper": False, "boost": 1}}}],
                                             "adjust_pure_negative": True, "boost": 1}},
                                   {"range": {"time_key": {"from": None, "to": int(endTS), "include_lower": False,
                                                           "include_upper": False, "boost": 1}}}],
                          "adjust_pure_negative": True, "boost": 1}},
            "_source": False,
            "stored_fields": "_none_",
            "docvalue_fields": ["close", "code", "create_time", "high", "low", "open", "pe", "spider_time", "time_key",
                                "turnover", "turnover_rate", "volume"],
            "sort": [{"_doc": {"order": "asc"}}]}
        res = es.search(index=dim, doc_type=dim, body=sql, size=100000)
        global df, fdf

        try:
            # res = es.search(index=dim, doc_type=dim, body=sql, size=100000)
            df = pd.DataFrame(list(map(serialize, res["hits"]["hits"]))).sort_values(by='time_key', ascending=True)
            # df.set_index(['create_time'], inplace=True, )
            # df.index = pd.DatetimeIndex(df.index)
            # todo 更改为前复权
            adjfactor_sql = {
                "query": {"term": {"code": {"value": code, "boost": 1}}},
                "_source": False,
                "stored_fields": "_none_",
                "docvalue_fields": ["ex_div_date", "qfq_x", "qfq_y"],
                "sort": [{"_doc": {"order": "asc"}}]
            }
            if systemSignal == 0:
                join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date desc) group by create_time order by create_time ;"
            else:
                join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date asc) group by create_time order by create_time ;"

            # join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date desc) group by create_time order by create_time ;"

            res_adj = es.search(index='adjustments', doc_type='adjustments', body=adjfactor_sql, size=100000)
            hits_adj = res_adj["hits"]["hits"]
            if len(hits_adj) > 0:
                fdf = pd.DataFrame(list(map(serialize, hits_adj))).sort_values(by='ex_div_date', ascending=True)
                # fdf['ex_div_date'] = fdf['ex_div_date'].apply(lambda T: time.strftime("%Y-%m-%d", time.strptime(T, "%Y-%m-%dT%H:%M:%S.000Z")))
                pysqldf = lambda q: sqldf(q, globals())
                # 线上docker环境， 降序5，4，3，2，1
                qfq_df = pysqldf(join_sql)
                for i in ['close', 'open', 'low', 'high']:
                    qfq_df[f'{i}'] = qfq_df[f'{i}'] * qfq_df['qfq_x'] + qfq_df['qfq_y']
                    qfq_df[f'{i}'] = qfq_df[f'{i}'].apply(float)
                # qfq_df.set_index(['create_time'], inplace=True, )
                # qfq_df.index = pd.DatetimeIndex(qfq_df.index)
            else:
                qfq_df = df
            qfq_df.set_index(['create_time'], inplace=True, )
            qfq_df.index = pd.DatetimeIndex(qfq_df.index)
        except Exception as e:
            qfq_df = pd.DataFrame()
        return qfq_df

    partical_get_es_stock = functools.partial(get_es_stock, dim=dim, startTS=startTS, endTS=endTS)
    return map(partical_get_es_stock, codes)


def get_all_factor_df(codes=['US.AAPL'],
                      topN=2,  # 取top n 支股票进行调仓
                      barNum=4,  # 调仓bar间隔
                      minP=0.1 , # 最小可信概率
                      bottomV=1,  # 最小可信概率
                      topV=2,  # 最小可信概率
                      longshort = 0, # 0做多，1做空
                      dim = "classification_2",
                      startTS=pendulum.now().add(years=-5).timestamp(), # 默认5年数据
                      endTS=pendulum.now().timestamp()
                      ):
    # todo 查询es中股票： "updownMatrixArray", "pMatrixArray"
    # partical_get_es_stock = functools.partial(get_es_group_stacks_p,dim=dim, startTS=startTS, endTS=endTS)
    target_list = list(get_es_group_stacks_p(codes=codes, dim=dim, startTS=startTS, endTS=endTS))
    # todo 对股票进行规则排序，返回每只股票的买卖矩阵
    updownMatrix_dict = {}
    pMatrix_dict = {}
    for i in range(len(target_list)):
        if len(target_list[i])==0:
            updownMatrix_dict[codes[i]] = pd.Series()
            pMatrix_dict[codes[i]] = pd.Series()
        else:
            updownMatrix_dict[codes[i]] = target_list[i]['updownMatrixArray'].astype(np.float128)
            pMatrix_dict[codes[i]] = target_list[i]['pMatrixArray'].astype(np.float128)
    # 股票池的涨跌矩阵
    updownMatrix_df = pd.DataFrame(updownMatrix_dict)
    updownMatrix_df.fillna(0, inplace=True)
    updownMatrix_array = updownMatrix_df.values
    # 涨跌概率矩阵
    pMatrix_df = pd.DataFrame(pMatrix_dict)
    pMatrix_df.fillna(0, inplace=True)
    pMatrix_array = pMatrix_df.values
    # todo 调用matrix_2_transaction ，对涨跌矩阵和概率矩阵进行计算
    predict_stocks_array = matrix_2_transaction(pMatrix=pMatrix_array,
                                                updownMatrix=updownMatrix_array,
                                                topN=topN,
                                                barNum=barNum,
                                                minP=minP,
                                                topV=topV,
                                                bottomV=bottomV,
                                                longshort = longshort,)
    # todo，计算的涨跌矩阵转：DataFrame，按序将买卖点，赋值给股票df的volume字段
    predict_stocks_df = pd.DataFrame(predict_stocks_array)
    predict_stocks_df.index = updownMatrix_df.index
    for i in range(len(target_list)):
        if len(target_list[i])>0:
            target_list[i]['volume'] = predict_stocks_df[i]
    return target_list


def get_es_group_stacks_p(codes=['US.APLE',
                               'US.TSLA',
                               'US.GOOG',
                               'US.FB',
                               'US.NVDA',
                               'US.AMD',
                               'US.AMZN',
                               'US.BABA'],
                        dim='classification_2',
                        startTS=pendulum.now().add(years=-5).timestamp(), # 默认5年数据
                        endTS=pendulum.now().timestamp(),
                        autotype = "qfq"):

    es = Elasticsearch(['192.168.80.183'], http_auth=('elastic', 'LOOP2themoon'), port=9200)

    def serialize(hit):
        fields = hit["fields"]
        for k in fields:
            fields[k] = fields[k][0]
        return fields

    # @retry(stop_max_attempt_number=5)
    def get_es_stock(code='US.APLE',
                     dim='kline_day',
                     startTS=pendulum.now().add(years=-5).timestamp(),  # 默认5年数据
                     endTS=pendulum.now().timestamp()):
        sql = {
            "query":
                {"bool": {"must": [{"bool": {"must": [{"term": {"code": {"value": code, "boost": 1}}},
                                                      {"range": {"time_key": {"from": int(startTS), "to": None,
                                                                              "include_lower": False,
                                                                              "include_upper": False, "boost": 1}}}],
                                             "adjust_pure_negative": True, "boost": 1}},
                                   {"range": {"time_key": {"from": None, "to": int(endTS), "include_lower": False,
                                                           "include_upper": False, "boost": 1}}}],
                          "adjust_pure_negative": True, "boost": 1}},
            "_source": False,
            "stored_fields": "_none_",
            "docvalue_fields": ["close", "code", "create_time", "high", "low", "open", "pe", "spider_time", "time_key",
                                "turnover", "turnover_rate", "volume", "updownMatrixArray", "pMatrixArray"],
            "sort": [{"_doc": {"order": "asc"}}]}
        res = es.search(index=dim, doc_type=dim, body=sql, size=100000)
        print(res)
        global df, fdf

        try:
            # res = es.search(index=dim, doc_type=dim, body=sql, size=100000)
            df = pd.DataFrame(list(map(serialize, res["hits"]["hits"]))).sort_values(by='time_key', ascending=True)
            if autotype != "qfq":
                df.set_index(['create_time'], inplace=True, )
                df.index = pd.DatetimeIndex(df.index)
                return df
            # todo 更改为前复权
            adjfactor_sql = {
                "query": {"term": {"code": {"value": code, "boost": 1}}},
                "_source": False,
                "stored_fields": "_none_",
                "docvalue_fields": ["ex_div_date", "qfq_x", "qfq_y"],
                "sort": [{"_doc": {"order": "asc"}}]
            }
            if systemSignal == 0:
                join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date desc) group by create_time order by create_time ;"
            else:
                join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date asc) group by create_time order by create_time ;"

            # join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date desc) group by create_time order by create_time ;"

            res_adj = es.search(index='adjustments', doc_type='adjustments', body=adjfactor_sql, size=100000)
            hits_adj = res_adj["hits"]["hits"]
            if len(hits_adj) > 0:
                fdf = pd.DataFrame(list(map(serialize, hits_adj))).sort_values(by='ex_div_date', ascending=True)
                # fdf['ex_div_date'] = fdf['ex_div_date'].apply(lambda T: time.strftime("%Y-%m-%d", time.strptime(T, "%Y-%m-%dT%H:%M:%S.000Z")))
                pysqldf = lambda q: sqldf(q, globals())
                # 线上docker环境， 降序5，4，3，2，1
                qfq_df = pysqldf(join_sql)
                for i in ['close', 'open', 'low', 'high']:
                    qfq_df[f'{i}'] = qfq_df[f'{i}'] * qfq_df['qfq_x'] + qfq_df['qfq_y']
                    qfq_df[f'{i}'] = qfq_df[f'{i}'].apply(float)
                # qfq_df.set_index(['create_time'], inplace=True, )
                # qfq_df.index = pd.DatetimeIndex(qfq_df.index)
            else:
                qfq_df = df
            qfq_df.set_index(['create_time'], inplace=True, )
            qfq_df.index = pd.DatetimeIndex(qfq_df.index)
        except Exception as e:
            qfq_df = pd.DataFrame()
        return qfq_df

    partical_get_es_stock = functools.partial(get_es_stock, dim=dim, startTS=startTS, endTS=endTS)
    return map(partical_get_es_stock, codes)




def matrix_2_transaction(pMatrix=np.array([1]),  # 概率矩阵，可以不传
                         updownMatrix=np.array([1]), # 2 分类时 为 涨跌矩阵 / 多分类时 为 标签矩阵 / 财务&滑动 为 数值矩阵 (a-b)/a
                         topN=2,  # 取 top n 支股票进行调仓
                         barNum=4,  # 调仓 bar 间隔
                         minP=0.5,  # 最小可信概率
                         bottomV=0,  #  期望下界
                         topV=5,  #  期望上界
                         longshort=0, # 1是做空，0是做多
                         ):  # 概率矩阵 + 涨跌（标签）矩阵  2 交易矩阵

    #  1. 处理做多做空的数据正负，用户后续排序
    if longshort == 0:
        pass
    else :
        updownMatrix = updownMatrix * -1  # 做空则 变换符号

    #  2. pMatrix 若为默认值，则重置为 类 updownMatrix 的 1 矩阵
    if len(pMatrix) != 1: # 此时不为默认值
        pass
    else : # 此时为默认值，需要转化类 updownMatrix 的 1 矩阵
        pMatrix = np.ones(updownMatrix.shape)

    pMatrix = pMatrix - np.random.random(pMatrix.shape) * 0.00000001
    x = pMatrix * updownMatrix  # 大于0 的项 代表 涨的概率
    x[x < minP * bottomV] = -6  # 将 概率小于 0.1 的项 格式化为 -6 特征值
    x[x >  topV] = -6  # 相当于期望外的置 -6

    for i in range(topN):  # 采集 top N 轮  ，每轮采集同一行中，最大的一个概率，将其重置为 -7
        for i, j in zip(range(np.shape(x)[0]), np.argmax(x, axis=1)):  # np.argmax(x, axis=1) 最大概率的 index
            if x[i, j] == -6:
                pass
            else:
                x[i, j] = -7

                # x # 把同一行，最大的n个项，依次格式化 -7 特征值
    # X 为持仓矩阵
    y = np.where(x == -7)  # 持仓index

    if y[0].size == 0:  # 如果找不到一个持仓点，则直接返回 0 矩阵               步骤 1
        return np.zeros(list(np.shape(x)), dtype='i')  # 全0数组
    else:
        firstBar = y[0][0]  # 首个持仓 bar  index
        # 把首个交易bar 及其后面的bar 非 -7 目标值，重置为0～1 的随机数
        for i in range(y[0][0], np.shape(x)[0]):
            for j in range(np.shape(x)[1]):
                if x[i, j] != -7:
                    x[i, j] = np.random.rand()

        if y[0][0] > 0:  # 如果首个持仓不是首bar， 把之前的bar 都重置为 0    ,表示不交易
            for i in range(y[0][0]):
                for j in range(len(x[y[0][0]])):
                    x[i, j] = 0

                    # 从 首个持仓 bar 开始， 按照 barNum 做 diff 下项 减 上项

        # 下项减上项结果
        # 为0 的代表 继续下项持仓 格式化为 0
        # 为 大负 <-4 就是买入 格式化为  1
        # 为 大正 > 4 则是卖出 格式化为  -1

        # 确定最后一个调仓bar
        # 可用bar 数 / barNum  积 取正  * barNum
        lastBar = (np.shape(x)[0] - y[0][0]) // barNum * barNum

        x_b = x.copy()

        for i in range((np.shape(x)[0] - y[0][0]) // barNum):  # 从首个持仓bar+barNum 开始计算 diff
            for j in range(np.shape(x)[1]):
                if firstBar + barNum * (i + 1) < x.shape[0]:
                    _diff = x_b[firstBar + barNum * (i + 1), j] - x_b[firstBar + barNum * i, j]
                    if _diff == 0:  # 为0 的代表 继续下项持仓 格式化为 0
                        x[firstBar + barNum * (i + 1), j] = 0
                    elif _diff < -4:  # 为 大负 <-4 就是买出 格式化为  1
                        x[firstBar + barNum * (i + 1), j] = 1
                    elif _diff > 4:  # 为 大正 > 4  则是卖入 格式化为  -1
                        x[firstBar + barNum * (i + 1), j] = -1
                    else:  # 其他值 不操作， 格式化为 0
                        x[firstBar + barNum * (i + 1), j] = 0

                        # 将首个持仓 重置
        for i in range(len(x[y[0][0]])):  # 将首个持仓 bar 的 股票  重置为 1 ，否则为 0 ,在后面执行
            if x[[y[0][0]], i] == -7:
                x[[y[0][0]], i] = 1
            else:
                x[[y[0][0]], i] = 0

                # 从首个持仓bar 开始 ，只要不是 1，-1 0 的一律 格式化为 0 到bar 尾为止
        for i in range(np.shape(x)[0]):
            for j in range(np.shape(x)[1]):
                if x[i, j] not in (0, 1, -1):
                    x[i, j] = 0
                else:
                    pass
        if longshort == 1:
            return x * -1
        return x * -1
