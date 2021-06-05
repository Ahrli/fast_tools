# factor 计算
import pendulum
# from ENIAC import Timer
import toolkit
if toolkit.__version__=="1.7.20":
    from toolkit.managers import Timer
else:
    from toolkit.tools.managers import Timer
from sanic import Blueprint
from sanic import response
from ..eniacutil import query_es, df2factor,query_es_kline_series,cq_sign
import numpy as np
from sanic_openapi import doc
factor = Blueprint('factor', url_prefix='/factor', strict_slashes=True)


@factor.route('/calculate/<code>/<kline_index>/<ranger>')#, version='v1', name='Dto')
@doc.summary('talib因子计算')
async def factor_calculate(request, code, kline_index, ranger):

    with Timer() as timer:
        with Timer() as timer_es:
            df = query_es(kline_index, code, ranger)
        try:
            high = np.array(list(df['high']))
            close = np.array(list(df['close']))
            low = np.array(list(df['low']))
            Open = np.array(list(df['open']))
            volume = np.array(list(map(float, list(df['volume']))))
            data = df2factor(df,close,high,low,Open,volume)
            del df
            status = 1
        except Exception as e:
            data = {'message': str(e)}
            status = 0

    return response.json(
        {'status': status,
        "create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
        "use_time": f"{timer.cost:.2f}",
        "use_time_es": f"{timer_es.cost:.2f}",
        "data": data,},
        headers = {'X-Served-By': 'sanic', "Access-Control-Allow-Origin":"*"},
        status=200
    )

@factor.route('/calculate/sign/<code>/<kline_index>/<ranger>')#, version='v1', name='Dto')
@doc.summary('拉取因子')
async def index_k_line(request, code, kline_index, ranger):
    with Timer() as timer:
        with Timer() as timer_es:
            rangers = ranger.split(',')
            SY_TIME = int(rangers[0])
            if int(rangers[1]) - int(rangers[0])<60*60*24*365:
                rangers[0]=int(rangers[1])-60*60*24*365
                ranger = str(rangers[0])+','+rangers[1]
            df = query_es(kline_index, code, ranger, 'qfq')
        if len(df)>0:
            data = df[['create_time','close','high','low','open','volume','time_key']].sort_values(by='time_key', ascending=True)
            data = cq_sign(data)
            data = data[data['time_key']>int(SY_TIME)]
            data = eval(data.to_json(orient='records'))
        else:
            data = []
    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
        "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
        "data": data},
        headers = {'X-Served-By': 'sanic', "Access-Control-Allow-Origin":"*"},
        status=200
    )

@factor.route('/kline/<code>/<kline_index>/<ranger>/<autotype>')#, version='v1', name='Dto')
@doc.summary('拉取因子')
async def index_k_line(request, code, kline_index, ranger, autotype):
    with Timer() as timer:
        with Timer() as timer_es:
            df = query_es(kline_index, code, ranger, autotype)
        if len(df)>0:
            data = df[['create_time','close','high','low','open','volume','time_key']].sort_values(by='time_key', ascending=True)
            data = eval(data.to_json(orient='records'))
        else:
            data = []
    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
        "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
        "data": data},
        headers = {'X-Served-By': 'sanic', "Access-Control-Allow-Origin":"*"},
        status=200
    )

@factor.route('/series/<code>/<kline_index>')#, version='v1', name='Dto')
@doc.summary('k线连续性')
async def series_k_line(request, code, kline_index):
    with Timer() as timer:
        with Timer() as timer_es:
            result = query_es_kline_series(kline_index, code)
    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         # 实际数据
         "start_time": int(result["min"]),
         "end_time": int(result["max"]),
         "real_bar": int(result["count"]),
         "calculate_bar": f"{result['calculate_bar']:.2f}",
         "data": result["data"],
         "period": result["period"],
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )
