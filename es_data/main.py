#!/usr/bin/env python3
# -*- coding: utf-8 -*-





from funcutils import LOG ,serialize
logger = LOG().get_logger()
from elasticsearch import Elasticsearch
import pandas as pd

def main(index):
    # index = 'coin_min1_a'
    es = Elasticsearch(['192.168.80.183'], http_auth=('elastic', 'LOOP2themoon'), port=9200)
    # 总条数
    count = es.count(index=index)['count']

    # 每页显示条数
    page_line  = 10000
    #显示多少页
    if (count%page_line==0):
        page = (int)(count/page_line)
    else:
        page = (int)(count/page_line+1)

    # Elasticsearch 需要保持搜索的上下文环境多久 游标查询过期时间为10分钟(10m)

    res = es.search(index=index,body={
                "query":{
                    "match_all":{}
                },

            },
            size = page_line,
            scroll='10m',
                            )
    sid = res['_scroll_id']
    df = pd.DataFrame(serialize(res["hits"]["hits"])).sort_values(by='time_key', ascending=True)
    df.to_csv(f'{index}.csv', mode='a', index=False)
    scroll_size = len(res['hits']['hits'])
    while (scroll_size > 0):
        try:
            res = es.scroll(scroll_id=sid, scroll='10m')
            sid = res['_scroll_id']
            scroll_size = len(res['hits']['hits'])
            (pd.DataFrame(serialize(res["hits"]["hits"])).sort_values(by='time_key', ascending=True)).to_csv(f'{index}.csv', mode='a', header=False,index=False)
        except Exception as e:
            print(e)
            logger.warning(f'当前失败,原因{e}')
if __name__ == '__main__':
    for i in ['coin_min3_a','coin_min5_a','coin_min30_a','coin_min60_a','coin_min120_a','coin_min240_a','coin_min720_a','coin_day_a','coin_week_a',
        'kline_day_d','kline_min120_a', 'kline_min15_a', 'kline_min180_a', 'kline_min1_a', 'kline_min240_a', 'kline_min30_a',
        'kline_min360_a', 'kline_min5_a', 'kline_min60_a', 'kline_min720_a', 'kline_month_a', 'kline_week_a',
              ]:
        print(i)
        main(i)
