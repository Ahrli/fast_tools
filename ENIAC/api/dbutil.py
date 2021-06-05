from pymongo import MongoClient
from elasticsearch import Elasticsearch

def get_mongo_btresult(sid):
    mongoUrl='mongodb://root:dds-uf66@192.168.80.200:3717,192.168.80.201:3717/admin?replicaSet=mgset-10450573'
    db = "loopLog"
    collection = "Demo"
    with MongoClient(mongoUrl) as client:
        collection = client[db][collection]
        data = collection.find({"sid": sid})
    #     print(sid)
    #     print(type(sid))
    # print(list(data)[0])
    r = list(data)[0]
    del(r["_id"])
    return r

# a = get_mongo_btresult(33)
# print(a)


def get_es_stock_data(dim='btc_classifer'):
    sql = {

        "query": {
            "term": {
                "code": {
                    "value": "OKEX.BTC",
                    "boost": 1
                }
            },

        },
        "_source": False,
        "stored_fields": "_none_",
        "docvalue_fields": [
            "updownMatrixArray",
            'close'
        ],
        "sort": [
            {
                "create_time": {
                    "order": "desc"
                }
            }
        ]
    }

    def serialize(hit):
        fields = hit["fields"]
        for k in fields:
            fields[k] = fields[k][0]
        return fields
    es = Elasticsearch(['192.168.80.183'], http_auth=('elastic', 'LOOP2themoon'), port=9200)
    res = es.search(index=dim, doc_type=dim, body=sql, size=1)
    try:
        # res = es.search(index=dim, doc_type=dim, body=sql, size=10000)
        df = (list(map(serialize, res["hits"]["hits"])))
    except Exception as e:
        return None, None
    return df[0]['updownMatrixArray'], df[0]['close']