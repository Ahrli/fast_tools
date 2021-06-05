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
from sanic_openapi import doc
import json
from ..loop_stack import FACTOR_btrun as fb
from ..loop_stack import LOCAL_btrun as lc
from ..loop_stack import CSV_btrun as cb

# from ..loop_stack.config.STRATEGY_json import *
backtrader = Blueprint('backtrader', url_prefix='/backtrader', strict_slashes=True)


# # @factor.route('/statistics/<code>/<kline_index>/<timekey>')#, version='v1', name='Dto')
# @backtrader.route('/statistics/<code>/<kline_index>')#, version='v1', name='Dto')
# @doc.summary('获取指定日期因子')
# async def index_k_line(request, code, kline_index):
#     with Timer() as timer:
#         try:
#             # _t = time.strftime('%Y-%m-%d',time.localtime(int(timekey)))
#             _r = tb.startRun({"myStocks": [code],
#                               "kline": kline_index,
#                                 # "date": _t
#                               })
#             status = 1
#         except Exception as e:
#             _r = {'message': str(e)}
#             status = 0
#     return response.json(
#         {'status': status,
#         "create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#         "use_time": f"{timer.cost:.2f}",
#         "data": _r},
#         headers = {'X-Served-By': 'sanic'},
#         status=200
#     )


@backtrader.route('/calculate/<code>/<kline_index>/<ranger>/<count>')  # , version='v1', name='Dto')
@doc.summary('bt因子计算')
async def factor_calculate(request, code, kline_index, ranger, count):
    with Timer() as timer_cal:
        starttime, endtime = ranger.split(",")
        rule = {"startDay": starttime, "endDay": endtime, "kline": kline_index,
                "myStocks": [code], "market": "SH", "factor_type": "all", "mongo_col": kline_index, }
        try:
            data = fb.startRun(rule, count)
            status = 1
        except Exception as e:
            data = {'message': str(e)}
            status = 0

    return response.json(
        {'status': status,
         "create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time_es": f"{timer_cal.cost:.2f}",
         "data": data, },
        headers={'X-Served-By': 'sanic'},
        status=200
    )


@backtrader.route('/airun/<code>/<kline_index>/<longshort>/<ranger>')  # , version='v1', name='Dto')
@doc.summary('backtrader回测')
async def factor_calculate(request, code, kline_index, longshort, ranger):
    configJson = {"okex.btc_long": "api/loop_stack/config/STRATEGY_json/BTC_long.json",
                  "okex.btc_short": "api/loop_stack/config/STRATEGY_json/BTC_short.json",
                  "bp500_short": "api/loop_stack/config/STRATEGY_json/FINANCE_short.json",
                  "okex_long": "api/loop_stack/config/STRATEGY_json/BTC_long.json",
                  "okex_short": "api/loop_stack/config/STRATEGY_json/BTC_short.json",
                  "us_short": "api/loop_stack/config/STRATEGY_json/FINANCE_short.json",
                  "us_long": "api/loop_stack/config/STRATEGY_json/FINANCE_long.json",
                  "sh_short": "api/loop_stack/config/STRATEGY_json/SH_short.json",
                  "sh_long": "api/loop_stack/config/STRATEGY_json/SH_long.json",
                  }
    starttime, endtime = ranger.split(",")
    with Timer() as timer_cal:
        try:
            cj = configJson[f"{code.split('.')[0].lower()}_{longshort.lower()}"]
            with open(cj) as f:
                rule = json.load(f)
                # rule["kline"] = [kline_index]
                rule["kline"] = kline_index
                rule["myStocks"] = [code]
                rule["startDay"] = int(starttime)
                rule["endDay"] = int(endtime)
            # print(rule)
            data = lc.startRun(rule)
            status = 1
        except Exception as e:
            data = {'message': str(e)}
            status = 0

    return response.json(
        {'status': status,
         "create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time_es": f"{timer_cal.cost:.2f}",
         "data": data, },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )


@backtrader.route('/csvrun/<code>/<csvfile>/<longshort>/<ranger>')  # , version='v1', name='Dto')
@doc.summary('backtrader回测_CSV')
async def factor_calculate(request, code, csvfile, longshort, ranger):
    configJson = {"okex.btc_long": "api/loop_stack/config/STRATEGY_json/BTC_long.json",
                  "okex.btc_short": "api/loop_stack/config/STRATEGY_json/BTC_short.json",
                  "bp500_short": "api/loop_stack/config/STRATEGY_json/FINANCE_short.json",
                  "okex_long": "api/loop_stack/config/STRATEGY_json/BTC_long.json",
                  "okex_short": "api/loop_stack/config/STRATEGY_json/BTC_short.json",
                  "us_short": "api/loop_stack/config/STRATEGY_json/FINANCE_short.json",
                  "us_long": "api/loop_stack/config/STRATEGY_json/FINANCE_long.json",
                  "sh_short": "api/loop_stack/config/STRATEGY_json/SH_short.json",
                  "sh_long": "api/loop_stack/config/STRATEGY_json/SH_long.json",
                  }
    starttime, endtime = ranger.split(",")
    with Timer() as timer_cal:
        try:
            cj = configJson[f"{code.split('.')[0].lower()}_{longshort.lower()}"]
            with open(cj) as f:
                rule = json.load(f)
                # rule["kline"] = [kline_index]
                rule["kline"] = csvfile
                rule["myStocks"] = [code]
                rule["startDay"] = int(starttime)
                rule["endDay"] = int(endtime)
            # print(rule)
            data = cb.startRun(rule)
            status = 1
        except Exception as e:
            data = {'message': str(e)}
            status = 0

    return response.json(
        {'status': status,
         "create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time_es": f"{timer_cal.cost:.2f}",
         "data": data, },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )
