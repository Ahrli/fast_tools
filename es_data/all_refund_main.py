#!/usr/bin/env python3
# -*- coding: utf-8 -*-





from funcutils import LOG ,serialize,w_ods
logger = LOG().get_logger()
from elasticsearch import Elasticsearch
import pandas as pd
import arrow

host = 'es-cn-4591kk1gx0001hr6m.elasticsearch.aliyuncs.com'
port = 9200
u = 'hqp_pro'
p = '3injYv7L6NjKqh'
index = 'global_all_refund'
def main(index):
    # index = 'coin_min1_a'
    es = Elasticsearch([host], http_auth=(u, p), port=port)
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
    lt = []
    df = pd.DataFrame(serialize(res["hits"]["hits"]))
    # df.to_csv(f'{index}.csv', mode='a', index=False)
    scroll_size = len(res['hits']['hits'])
    lt.append(df)
    while (scroll_size > 0):
        try:
            res = es.scroll(scroll_id=sid, scroll='10m')
            sid = res['_scroll_id']
            scroll_size = len(res['hits']['hits'])
            lt.append(pd.DataFrame(serialize(res["hits"]["hits"])))
        except Exception as e:
            print(e)
            logger.warning(f'当前失败,原因{e}')
    df = pd.concat(lt)
    df['@timestamp']=df['@timestamp'].apply(lambda x:arrow.get(x).format('YYYY-MM-DD HH:mm:ss'))
    df['createDT']=df['createDT'].apply(lambda x:arrow.get(x).format('YYYY-MM-DD HH:mm:ss'))
    df['updateDT']=df['updateDT'].apply(lambda x:arrow.get(x).format('YYYY-MM-DD HH:mm:ss'))
    print(df)
    w_ods(df, 'ods_zqp', i, 'replace')

if __name__ == '__main__':
    for i in ['global_all_refund'
              ]:
        print(i)
        main(i)
