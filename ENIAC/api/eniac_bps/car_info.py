#!/usr/bin/env python3
# -*- coding: utf-8 -*-





#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from sanic import Blueprint
# from sanic import response
# from ..eniacutil import query_es, df2factor, query_es_kline_series
# import numpy as np
from sanic_openapi import doc

car = Blueprint('car_info', url_prefix='/car_info', strict_slashes=True)


@car.route('/car')
@doc.summary('车型信息')
async def index_k_line(request):
    return 'hello'
