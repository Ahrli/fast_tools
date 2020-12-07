#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import arrow
from pandasql import sqldf

pysqldf = lambda x: sqldf(x, globals())
import elasticsearch
from elasticsearch import Elasticsearch
import requests
import json
from configparser import ConfigParser
from funcutils import search_mysql, cq_avg, es_insert, es_alias, get_es_alias, search_mysql_slave
import pandas as pd
import datetime


## 加载配置
cfg = ConfigParser()
cfg.read('config.ini')

#定义es配置
es_cfg = 'prd_es'
version = cfg.get('version', 'version')


def main():
    ## 定义数据
    dfmg = pd.DateFrame([{'oeCode':1,'avgPrice30':30},{'oeCode':2,'avgPrice30':60}])
    
    # 初始化连接ES 定义别名
    alias = 'global_autopart_avg_price'
    es = Elasticsearch([cfg.get(es_cfg, 'host')], http_auth=(cfg.get(es_cfg, 'u'), cfg.get(es_cfg, 'p')),
                       port=cfg.get(es_cfg, 'port'))

    # 查询索引别名 判断是否有索引别名
    old_indexname = get_es_alias(es, alias)

    #  创建索引,创建新索引的名称 字段
    if old_indexname == None:
        update_indexname = alias + f'_{version}_a'
    elif old_indexname.endswith('b'):
        update_indexname = alias + f'_{version}_a'
    else:
        update_indexname = alias + f'_{version}_b'

    # 索引基础body
    body_es = {
        "settings": {"number_of_shards": "3",
                     "number_of_replicas": "1",
                     "refresh_interval": "5s",

                     "analysis": {
                         "analyzer": "ik",
                         "search_analyzer": "ik"
                     }
                     },

        "mappings": {
        }}
    base_map = {

        'provinceId': {
            "type": "keyword"
        },
        'categoryName': {
            "type": "keyword"
        },
        'oeCode': {
            "type": "keyword"
        },
        'avgPrice30': {
            "type": "keyword"
        },
        'avgPrice60': {
            "type": "keyword"
        },
        'avgPrice90': {
            "type": "keyword"
        },

    }
    body_es["mappings"][alias] = {"properties": base_map, "dynamic": "false", }
    es.indices.create(index=update_indexname, body=body_es)

    # 导入数据
    index_name = update_indexname
    type_name = alias
    dict_list = []
    ##########################
    rs_lt = dfmg.to_dict('r')

    for redata in rs_lt:
        dc = {"_index": index_name, "_type": type_name}
        dc["_source"] = redata
        # dc['_id'] = str(int(redata["provinceId"])) + '_' + str(redata["oeCode"] )# code+create_time作为id，更新和防止多条
        dict_list.append(dc)

    ##########################

    if len(dict_list) > 0:
        es_insert(dict_list, index_name, es)
        kldict_list = []

    # 切换索引
    es_alias(es, update_indexname, alias, old_indexname)
    # 切换成功后查询索引别名指向
    new_alias_indexname = get_es_alias(es, alias)
    # 若指向最新索引别名 删除旧索引
    if new_alias_indexname == update_indexname and old_indexname:
        es.indices.delete(old_indexname)


if __name__ == '__main__':
    main()
