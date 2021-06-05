import pandas as pd
from pymongo import MongoClient
from pymongo.errors import BulkWriteError, DuplicateKeyError
from pymongo import InsertOne
import arrow
import pendulum
import numpy as np


# mongo 2 df
def read_mongo(  # ='BTC_statistics_v3',
        db='kline_factors',
        collection='bt_day_GEMINI',
        query={},  # 查询
        select={'_id': 0},  # 选择字段
        sortby="_id",  # 排序字段
        upAndDown=1,  # 升序
        # limitNum=9999999999, # 限制数量
        limitNum=999999,  # 限制数量
        # url='mongodb://root:dds-uf66@dds-uf66056e937ca0941.mongodb.rds.aliyuncs.com:3717,dds-uf66056e937ca0942.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-10450573',
        url='mongodb://192.168.249.154:27017',
        no_id=0,  # 默认不删除_id
        _dtype='float32'):
    """ Read from Mongo and Store into DataFrame """
    # Connect to MongoDB
    with MongoClient(url) as client:
        collection = client[db][collection]

        data = collection.find(query, select).sort(sortby, upAndDown).limit(limitNum)

        df = pd.DataFrame(list(data),
                          dtype=_dtype)
    # Delete the _id
    if no_id:
        del df['_id']
    return df


def read_mongo_aggregate(
        db='stock_data',
        collection='dfcf_ajax_data',
        pipline=[
            {"$match": {"date": "2020-03-31",
                        "$or": [{'market': 'SH'},
                                {'market': 'SZ'}]}},
            {"$group": {"_id": {"mc": "$mc",
                                "Type": "$Type",
                                },

                        "num": {"$sum": 1},
                        "cgsz": {"$sum": "$cgsz"}}},
            {"$project": {"mc": "$_id.mc",
                          "Type": "$_id.Type",
                          "num": "$num",
                          "cgsz": "$cgsz"}},
            {'$sort': {"num": -1}},
            {'$limit': 99999999}],
        url='mongodb://192.168.249.154:27017',
        no_id=1,  # 默认不删除_id
        _dtype='float32'):
    """ Read from Mongo and Store into DataFrame """
    # Connect to MongoDB
    with MongoClient(url) as client:
        collection = client[db][collection]
        data = collection.aggregate(pipline)
        df = pd.DataFrame(list(data), dtype=_dtype)
    # Delete the _id

    if no_id:
        del df['_id']
    return df


# df 2 mongo
def update_mongo(db='kline_factors',
                 collection='test_collection_4',
                 _df=pd.DataFrame(np.random.randn(6, 4),
                                  index=pd.date_range('20130101', periods=6),
                                  columns=['time_key', 'A', 'B', 'C']),
                 _id=['time_key', 'OKEX.BTC'],  # 最后一个字段为标签，之前为df的字段
                 url='mongodb://root:dds-uf66@dds-uf66056e937ca0941.mongodb.rds.aliyuncs.com:3717,dds-uf66056e937ca0942.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-10450573',
                 limitNum=1000,  # todo 每 1000行 提交mongo 1次
                 bulk=0,  # 是否批量提交 默认不批量提交，从而记录非重复_id数量
                 ):
    _list = _df.to_dict(orient='records')
    with MongoClient(url) as client:
        collection = client[db][collection]
        data = []
        num = 0
        if bulk == 1:
            for i, j in zip(_list, list(_df[_id[0]])):
                i['_id'] = f"{j}_{_id[-1]}"
                data.append(InsertOne(i))
            try:
                collection.bulk_write(data,
                                      # ordered=False, # 是否有序写入
                                      )
                return len(_df)
            except BulkWriteError as bwe:
                print(bwe.details)
                return -1
        else:
            for i, j in zip(_list, list(_df[_id[0]])):
                i['_id'] = f"{j}_{_id[-1]}"
                try:
                    collection.insert_one(i)
                    num += 1
                except DuplicateKeyError as bwe:
                    # print(bwe.details)
                    pass
            return num
