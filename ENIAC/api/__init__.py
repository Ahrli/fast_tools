# api/__init__.py
from sanic import Blueprint
# 蓝图
# from .eniac_bps.factors import factor
# from .eniac_bps.loopback import loop
# from .eniac_bps.backtrader import backtrader
# from .eniac_bps.btresultApi import api
# from .eniac_bps.piplineStatus import  pipline
# from .eniac_bps.trading import trading
# from .eniac_bps.ai import ai
# from .eniac_bps.validation import validation
# from .eniac_bps.loop_coin import loopcoin
# from .eniac_bps.financial import financial
# # from sanic_openapi import swagger_blueprint, openapi_blueprint
#
# from .loop_statistics import loop_indicators
# from .loop_stack import loop_indicators


# iquant_eniac = Blueprint.group(factor, loop, backtrader, api, pipline, trading,ai,validation, loopcoin,financial)
# eniac = Blueprint.group(factor, loop, swagger_blueprint, openapi_blueprint, url_prefix='/')
from .eniac_bps.car_info import car

iquant_eniac = Blueprint.group(car)