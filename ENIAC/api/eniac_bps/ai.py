#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pendulum
# from ENIAC import Timer
import toolkit
if toolkit.__version__=="1.7.20":
    from toolkit.managers import Timer
else:
    from toolkit.tools.managers import Timer
from sanic import Blueprint
from sanic import response
from ..eniacutil import query_es, df2factor, query_es_kline_series
import numpy as np
from sanic_openapi import doc

ai = Blueprint('ai', url_prefix='/ai', strict_slashes=True)


@ai.route('/<code>/<kline_index>/<ranger>')  # , version='v1', name='Dto')
@doc.summary('拉取k线')
async def index_k_line(request, code, kline_index, ranger):
    with Timer() as timer:
        with Timer() as timer_es:
            df = query_es(kline_index, code, ranger)
        if len(df) > 0:
            data = df[['create_time', 'close', 'high', 'low', 'open', 'volume', 'time_key']].sort_values(by='time_key',
                                                                                                         ascending=True)
            data = eval(data.to_json(orient='records'))
        else:
            data = []
    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "data": data},
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )
