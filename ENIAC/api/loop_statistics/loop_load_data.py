import functools
import pendulum
import pandas as pd
from elasticsearch import Elasticsearch
from retrying import retry
import redis
import arrow
import json
from futu import OpenQuoteContext
from functools import reduce
from pandasql import sqldf
import os

# global systemSignal
systemSignal = os.system('ls /.dockerenv')

# @retry()
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
            # res = es.search(index=dim, doc_type=dim, body=sql, size=10000)
            df = pd.DataFrame(list(map(serialize, res["hits"]["hits"]))).sort_values(by='time_key', ascending=True)
            # df.set_index(['create_time'], inplace=True, )
            # df.index = pd.DatetimeIndex(df.index)
            # todo 更改为前复权
            adjfactor_sql = {
                "query": {"term": {"code": {"value": code, "boost": 1}}},
                "_source": False,
                "stored_fields": "_none_",
                "docvalue_fields": ["ex_div_date", "x", "y"],
                "sort": [{"_doc": {"order": "asc"}}]
            }
            if systemSignal == 0:
                join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date desc) group by create_time order by create_time ;"
            else:
                join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date asc) group by create_time order by create_time ;"

            # join_sql = "select * from (select * from df left join fdf where df.create_time < fdf.ex_div_date order by fdf.ex_div_date desc) group by create_time order by create_time ;"

            res_adj = es.search(index='adjustments_a', doc_type='adjustments', body=adjfactor_sql, size=100000)
            hits_adj = res_adj["hits"]["hits"]
            if len(hits_adj) > 0:
                fdf = pd.DataFrame(list(map(serialize, hits_adj))).sort_values(by='ex_div_date', ascending=True)
                # fdf['ex_div_date'] = fdf['ex_div_date'].apply(lambda T: time.strftime("%Y-%m-%d", time.strptime(T, "%Y-%m-%dT%H:%M:%S.000Z")))
                pysqldf = lambda q: sqldf(q, globals())
                # 线上docker环境， 降序5，4，3，2，1
                qfq_df = pysqldf(join_sql)
                for i in ['close', 'open', 'low', 'high']:
                    qfq_df[f'{i}'] = qfq_df[f'{i}'] * qfq_df['x'] + qfq_df['y']
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


def get_redis_group_stacks(codes):
    redis_pool = redis.ConnectionPool(host='192.168.80.188', port=6379, decode_responses=True, db=0, password='LOOP2themoon')

    @retry(stop_max_attempt_number=5)
    def get_redis_stack(code):
        redis_connect = redis.Redis(connection_pool=redis_pool)
        try:
            result = json.loads(redis_connect.get(f'snapshot_format:{code}'), encoding='utf-8')
            redis_connect.connection_pool.disconnect()
            df = pd.DataFrame([result])
            update_time = arrow.get(pendulum.from_format(result['update_time'], 'YYYY-MM-DD HH:mm:ss', tz='Asia/Shanghai'))
            df['create_time'] = update_time.to('local').format('YYYY-MM-DD')
            df['time_key'] = update_time.timestamp
            df['spider_time'] = update_time.to('local').format('YYYY-MM-DD HH:mm:ss')
            # df = df.loc[:, ['last_price', 'code', 'high_price', 'low_price', 'open_price', 'pe_ratio', 'spider_time', 'time_key', 'turnover', 'turnover_rate', 'volume', 'create_time']]
            df = df.loc[:, ['lastPrice', 'stockCode', 'highPrice', 'lowPrice', 'openPrice', 'peRatio', 'spider_time', 'time_key', 'volume', 'create_time']]
            df.set_index(['create_time'], inplace=True, )
            df.index = pd.DatetimeIndex(df.index)
            # df.columns = ['close', 'code', 'high', 'low', 'open', 'pe', 'spider_time', 'time_key','turnover', 'turnover_rate', 'volume']
            df.columns = ['close', 'code', 'high', 'low', 'open', 'pe', 'spider_time', 'time_key', 'volume']
            return df
        except:
            return None

    def addf(df1, df2):
        return df1.append(df2)
    try:
        results = reduce(addf, [c for c in map(get_redis_stack, codes) if str(c) != 'None'])
    except:
        results = None
    redis_pool.disconnect()
    return results



def get_futu_group_stacks(codes):
    quote_ctx = OpenQuoteContext(host='192.168.80.195', port=31118)
    code_lists = list()
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
    code_lists += list(chunks(codes, 400))

    @retry(stop_max_attempt_number=5)
    def get_futu_stack(code_list):
        ret, df = quote_ctx.get_market_snapshot(code_list)
        try:
            update_time = arrow.get(pendulum.from_format(list(df['update_time'])[0], 'YYYY-MM-DD HH:mm:ss', tz='Asia/Shanghai'))
            df['create_time'] = update_time.to('local').format('YYYY-MM-DD')
            df['time_key'] = update_time.timestamp
            df['spider_time'] = update_time.to('local').format('YYYY-MM-DD HH:mm:ss')
            df = df.loc[:, ['last_price', 'code', 'high_price', 'low_price', 'open_price', 'pe_ratio', 'spider_time', 'time_key', 'turnover', 'turnover_rate', 'volume', 'create_time']]
            df.set_index(['create_time'], inplace=True, )
            df.index = pd.DatetimeIndex(df.index)
            df.columns = ['close', 'code', 'high', 'low', 'open', 'pe', 'spider_time', 'time_key', 'turnover', 'turnover_rate', 'volume']
            return df
        except:
            # 去掉不正确的stock
            if 'Unknow stock' in df:
                error_codes = [code_list.pop(code_list.index(cl)) for cl in code_list if df.split(' ')[-1] in cl]
            if code_list:
                rdf = get_futu_stack(code_list)
                return rdf
            return None

    def addf(df1, df2):
        return df1.append(df2)
    try:
        results = reduce(addf, [c for c in map(get_futu_stack, code_lists) if str(c) != 'None'])
    except:
        results = None
    quote_ctx.close()
    return results
# rule = {'startDay': 283968000, 'endDay': 2524579200, 'kline': 'kline_day', 'myStocks': ['US..AEX'], 'market': 'US'}
# a = get_es_group_stacks(codes = ['SH.600000'],dim=rule["kline"],startTS=rule['startDay'],endTS=rule['endDay'])
# print(list(a))

# a = get_es_group_stacks(codes=['SH.600563'], dim='kline_day', startTS=1104508800, endTS=1136044800)
# print(list(a)[0])


