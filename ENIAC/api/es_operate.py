import pandas as pd
import requests
import arrow
import re
from elasticsearch import Elasticsearch

# df 单字段生成新字段
def conduct_dataframe(df, conductField, func, *arg):
    iterator = map(func, df[conductField], *arg)
    iteratorS = pd.Series(iterator, index=df.index)
    return iteratorS


def conduct_mul_dataframe(df,func,*arg):
    iterator = map(func,*arg)
    iteratorS = pd.Series(iterator,index=df.index)
    return iteratorS



def es_sql_df(host="192.168.80.183",
           port="9200",
           auth="Basic ZWxhc3RpYzpMT09QMnRoZW1vb24=",
           sql="SELECT plate_name FROM stock_plate group by plate_name"
#            sql="SELECT * FROM stock_plate"   
          ):
    
    url = f"http://{host}:{port}/_xpack/sql"

    payload = """{"query" : """ + '"' + f"{sql}" + '"' + """}"""
#     print (payload)
    headers = {
        'content-type': "application/json",
        'authorization': f"{auth}"
        }    
    response = requests.request("POST", url, data=payload, headers=headers)
    
    columns = [ i['name'] for i in response.json()['columns']]
#     print(columns)
    
    df = pd.DataFrame(response.json()['rows'])
    
    df.columns = columns

    # todo 超数量 解决游标问题
    while "cursor" in response.json():
        try:
            cursor = response.json()['cursor']
            payload = """{"cursor" : """ + '"' + f"{cursor}" + '"' + """}"""
            response = requests.request("POST", url, data=payload, headers=headers)
            dfMore = pd.DataFrame(response.json()['rows'])
            dfMore.columns = columns
        #         print(dfMore)
            df = df.append(dfMore,
                      ignore_index=1) # 忽略索引，保证自增
        except:
            pass

    
    return df


def deal_q_time(t="2014-09-19T00:00:00.000Z"):
    if arrow.get(t).month > 9:
        return arrow.get(t).format("YYYY") + "12"
    elif arrow.get(t).month > 6:
        return arrow.get(t).format("YYYY") + "09"
    elif arrow.get(t).month > 3:
        return arrow.get(t).format("YYYY") + "06"
    else:
        return arrow.get(t).format("YYYY") + "03"


def es_query_df(host="192.168.80.183",
              port="9200",
              auth="Basic ZWxhc3RpYzpMT09QMnRoZW1vb24=",
              sql="SELECT plate_name FROM stock_plate group by plate_name",
              ):

    url = f"http://{host}:{port}/_xpack/sql/translate"
    querystring = {"format": "json"}
    # payload = "{\n    \"query\" : \"SELECT plate_name,plate_code FROM stock_plate where plate_type = 'INDUSTRY' and category = 'SZ'\"\n}"
    payload = """{"query" : """ + '"' + f"{sql}" + '"' + """}"""

    headers = {
        'content-type': "application/json",
        'authorization': f"{auth}"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
    # sql转换，index正则
    query_sql =response.json()
    del(query_sql["size"])
    # dims = re.findall(r'FROM(.*)WHERE', sql, re.IGNORECASE)
    dims = re.findall(r'FROM (.*?) ', sql+" ", re.IGNORECASE)
    # dim = ""
    if dims:
        dim = dims[0].replace(" ","")
    else:
        return pd.DataFrame()
    # 调用es包方法请求数据
    es = Elasticsearch([host], http_auth=('elastic', 'LOOP2themoon'), port=port)
    res = es.search(index=dim, doc_type=dim, body=query_sql, size=10000)

    def serialize(hit):
        fields = hit["fields"]
        for k in fields:
            fields[k] = fields[k][0]
        return fields

    df = pd.DataFrame(list(map(serialize, res["hits"]["hits"])))
    return df