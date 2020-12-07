#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from sqlalchemy import create_engine
import elasticsearch
from elasticsearch import Elasticsearch
import requests
import json,datetime

from elasticsearch.helpers import bulk
from pandasql import sqldf
import arrow
__author__ = 'Ahrli Tao'


def es_judge(old_indexname, new_dict):
    '''判断是否需要更新field'''
    es = Elasticsearch(['192.168.80.183'], http_auth=('elastic', 'LOOP2themoon'), port=9200)

    try:
        map_name = es.indices.get_mapping(index=old_indexname + '_a')
        indexname = old_indexname + '_a'
        new_indexname = old_indexname + '_b'
    except elasticsearch.NotFoundError as e:
        indexname = old_indexname + '_b'
        new_indexname = old_indexname + '_a'
    print('新的索引名称为:', new_indexname)
    # 执行更新
    update_es_field(indexname, new_indexname, new_dict, es)

    return new_indexname


def update_es_field(indexname, new_indexname, new_dict, es):
    '''建立索引'''

    # 添加的double类型字段
    add_map = {}
    for key, value in new_dict.items():

        type_ = type(value)

        if key in ['code', 'name', 'category']:
            add_map[key] = {
                "type": "keyword"
            }
            continue
        elif key in ['update_time']:

            add_map[key] = {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
            }
            continue

        elif type_ is str or key in ['fiftyTwoWeekRange', 'currency']:

            add_map[key] = {
                "type": "text"
            }
        elif type_ is bool:
            add_map[key] = {
                "type": "boolean"
            }
        else:

            add_map[key] = {
                "type": "double"
            }

    base_map = add_map

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
    update_name = indexname.split("_")[0]
    body_es["mappings"][update_name] = {"properties": base_map, "dynamic": "false", }
    # 创建新的索引
    es.indices.create(index=new_indexname, body=body_es)


def transfer_alias(new_indexname, update_name):
    '''
    索引别名切换
    :param new_indexname:
    :param update_name:
    :return:
    '''
    symbol = new_indexname.split("_")[1]

    es = Elasticsearch(['192.168.80.183'], http_auth=('elastic', 'LOOP2themoon'), port=9200)
    # 去除使用中的索引别名
    if symbol == 'a':
        indexname = new_indexname.split('_')[0] + '_b'
    else:
        indexname = new_indexname.split('_')[0] + '_a'

    try:
        es.indices.delete_alias(index=indexname, name=update_name)
    except elasticsearch.exceptions.NotFoundError as e:
        pass

    # 切换到更新的索引别名

    es.indices.put_alias(index=new_indexname, name=update_name)
    print('新的索引名称为:', new_indexname)
    print('新的索引alias为:', update_name)

    # 删除原来索引
    try:
        es.indices.delete(index=indexname)
    except elasticsearch.exceptions.NotFoundError as e:
        pass
    es.indices.put_settings(index=new_indexname, body={"max_result_window": 50000})


def es_window_size(new_indexname):
    url = f"http://192.168.80.183:9200/{new_indexname}/_settings"

    payload = '''{ "index" : { "max_result_window" : 50000 } }'''
    headers = {
        'content-type': "application/json",
        'authorization': "Basic ZWxhc3RpYzpMT09QMnRoZW1vb24=",
        'cache-control': "no-cache",
        'postman-token': "f400bd82-f92d-ae8d-cff3-5d9f362fdcf6"
    }

    response = requests.request("PUT", url, data=payload, headers=headers)

    print(response.text)

def transfer_alias_request(new_indexname, update_name):
    '''

    :param new_indexname:
    :param update_name:
    :return:
    '''


    symbol = new_indexname.split("_")[1]
    # 去除使用中的索引别名
    if symbol == 'a':
        indexname = new_indexname.split('_')[0] + '_b'
    else:
        indexname = new_indexname.split('_')[0] + '_a'

    #互推切换索引别名
    remove_dc = {"index": indexname, "alias": update_name}
    add_dc = {"index": new_indexname, "alias": update_name}

    url = "http://192.168.80.183:9200/_aliases"
    a = {"actions": [{"remove": remove_dc},
                     {"add": add_dc}]
         }

    payload = json.dumps(a)

    headers = {
        'content-type': "application/json",
        'authorization': "Basic ZWxhc3RpYzpMT09QMnRoZW1vb24=",
        'cache-control': "no-cache",
        'postman-token': "b7475c09-23b4-30ef-a8bc-390aa4e23c1c"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)




    #删除旧的索引数据
    url = f"http://192.168.80.183:9200/{indexname}"
    headers = {
        'authorization': "Basic ZWxhc3RpYzpMT09QMnRoZW1vb24=",
        'cache-control': "no-cache",
        'postman-token': "e943e02b-c213-a2b6-4c9d-4ef5b906a612"
    }
    response = requests.request("DELETE", url, headers=headers)
    print(response.text)




def cq_avg(df,days,area):
    df = df[df['createDT'] >= arrow.now().shift(days=days).format('YYYY-MM-DD')]
    x = f'select  categoryName,oe_code,provinceID, avg(buyerMakeupPrice) {area} from df t group by provinceID ,oe_code'
    df = sqldf(x, locals())
    df = df.rename(columns={'oe_code': 'oeCode', "provinceID": 'provinceId'})
    df = df.apply(pd.to_numeric, errors='ignore')  # 转换默认类型
    df = df.where(df.notnull(), None)
    df = df.round({area: 2})
    df['oeCode'] = df['oeCode'].apply(lambda  x:(str(x)).strip())
    if area.endswith('30') ==False:
        df = df.drop(['categoryName',], axis=1)

    return df

def es_insert(dict_list, index_name,es):
    '''数据批量导入写入es'''
    res = bulk(es, dict_list, index=index_name, raise_on_error=True)
    print(res)
    pass

def es_alias(es,update_indexname,alias,old_indexname):
    # 互推切换索引别名
    if old_indexname:
        remove_dc = {"index": old_indexname, "alias": alias}
        add_dc = {"index": update_indexname, "alias": alias}
        body = {"actions": [{"remove": remove_dc},
                         {"add": add_dc}]
             }
        es.indices.update_aliases(body)
    else:
        es.indices.put_alias(update_indexname, alias)

def get_es_alias(es,alias):
    indexname=None
    try:
        indexname = es.indices.get_alias(alias)
        indexname = list(indexname.keys())[0]
    except elasticsearch.exceptions.NotFoundError as e:
        pass
    return indexname

if __name__ == '__main__':
    transfer_alias_request('t_b', 't')

