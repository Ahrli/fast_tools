# trading 计算
import pendulum
# from ENIAC import Timer
import toolkit
if toolkit.__version__=="1.7.20":
    from toolkit.managers import Timer
else:
    from toolkit.tools.managers import Timer
from sanic import Blueprint
from sanic import response
from ..eniacutil import query_es_signal,query_es_profit_loss
from sanic_openapi import doc
trading = Blueprint('trading', url_prefix='/trading', strict_slashes=True)


@trading.route('/signal/<code>/<kline_index>/<interval>')#, version='v1', name='Dto')
@doc.summary('实时交易信号')
async def trading_signal(request, code, kline_index, interval):
    code = code.upper()
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                data = query_es_signal(kline_index, code, interval)
            except Exception as e:
                data = {"state":-1, "message":str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "data": data},
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )



@trading.route('/stop/<stype>/<code>/<kline_index>')#, version='v1', name='Dto')
@doc.summary('止盈止损统计')
async def trading_signal(request, code, kline_index, stype):
    code = code.upper()
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                data = query_es_profit_loss(stype, kline_index, code)
                # loss_list = []
                # profit_list = []
                # if stype == "long":
                #     for _d in data:
                #         if _d["最终收益"] < 0:
                #             loss_list.append(_d)
                #         else:
                #             profit_list.append(_d)
            except Exception as e:
                data = {"state":-1, "message":str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "count": len(data),
         "data": data
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )
