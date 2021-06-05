# factor 计算
# from ENIAC import Timer
import toolkit
if toolkit.__version__=="1.7.20":
    from toolkit.managers import Timer
else:
    from toolkit.tools.managers import Timer
from sanic import Blueprint
from sanic import response
from redis import StrictRedis
# from factor_server_docker.ENIAC.api.eniacutil import query_es, df2factor
from ..dbutil import get_mongo_btresult,get_es_stock_data
# import numpy as np
from sanic_openapi import doc
# import pandas as pd
# import time
api = Blueprint('api', url_prefix='/api', strict_slashes=True)


@api.route('/btresult/<sid>')#, version='v1', name='Dto')
@doc.summary('因子计算')
async def backtrader_result(request, sid):

    with Timer() as timer:
        try:
            data = get_mongo_btresult(int(sid))
            print(data)
            status = 1
        except Exception as e:
            data = {'message': str(e)}
            status = 0

    return response.json(
        # {'status': status,
        # "create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
        # "use_time": f"{timer.cost:.2f}",
        # "data": data,},
        data,
        headers = {'X-Served-By': 'sanic', "Access-Control-Allow-Origin":"*"},
        status=200
    )


@api.route('/key/<tag>/<dim>')
@doc.summary('实时ai因子预测')
async def tag_handler(request, tag,dim):
    rd = StrictRedis(host="192.168.80.188", port=6379, db=2, password='LOOP2themoon')
    #查询redis是否更新
    data = (rd.get(tag)).decode('utf-8')
    # print(request.body)
    # print(request.args)
    #如果没有更新 直接返回状态 0 不操作
    if int(data)==0:
        r = { 'status':0}
    # 如果data 不等于0 先修改redis数据为0  然后查询es返回结果
    else:
        rd.set('okex_btc' , 0)
        sy,close = get_es_stock_data(dim=dim)
        r = {'status': 1, 'signal':sy,'price':close}
    return response.json(
        r,
        headers = {'X-Served-By': 'sanic', "Access-Control-Allow-Origin":"*"},
        status=200
    )