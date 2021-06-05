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
import pymysql
import pandas as pd
import copy
import time,datetime
from ..models import YieldDto

# factor
from ..eniacutil import query_es
from ..coinutil import df2factor
import numpy as np


loopcoin = Blueprint('loopCoin', url_prefix='/loopcoin', strict_slashes=True)



def read_mysql(sql="select * from model_feature_state where user_id = 1 and api_id=1 order by time_key asc"):
    conn=pymysql.connect(host='rm-uf6rozhp0o3za68tt.mysql.rds.aliyuncs.com',
                         port=3306,
                         user='root',
                         passwd='LOOP2themoon',
                         db='loop_coin',
                         use_unicode=True,
                         charset="utf8")
    cursor = conn.cursor()
    cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED ;")
    cursor.execute("START TRANSACTION ;")
    df=pd.read_sql(sql,con=conn)
    cursor.execute("COMMIT;")
    cursor.close()
    conn.close()
    return df

def reversion_rate(assets_data):
    print(assets_data)
    data = copy.deepcopy(assets_data)
    profits_rp = data[0]["profits"]  # 复权收益
    assets_rp = data[0]["total_assets"] - data[0]["profits"]  # 复权充值
    if assets_rp > 0:
        yield_rp = profits_rp / assets_rp  # 复权收益率
    else:
        yield_rp = 0
    yield_rp_trend = [{"time_key":data[0]['time_key'], "yield_rp":yield_rp}]
    # top_up 充值 withdrawal 提现
    # 找出第一笔赢利
    for i in range(1, len(data)):
        d = data[i]
        tarp = (d["top_up"] - data[i - 1]["top_up"]) / (1 + yield_rp)  # 复权充值
        tyrp = (d["top_up"] - data[i - 1]["top_up"]) - tarp  # 复权收益

        warp = (d["withdrawal"] - data[i - 1]["withdrawal"]) / (1 + yield_rp)  # 复权提现
        wyrp = (d["withdrawal"] - data[i - 1]["withdrawal"]) - warp  # 复权收益

        assets_rp = assets_rp + tarp - warp
        profits_rp = profits_rp + tyrp - wyrp + d["profits"] - data[i - 1]["profits"]
        if assets_rp > 0:
            yield_rp = profits_rp / assets_rp
        else:
            yield_rp = 0
        yield_rp_trend.append({"time_key":d['time_key'], "yield_rp":yield_rp})

    total_profits = data[-1]["profits"]

    return { "total_assets":data[-1]["total_assets"],
             "total_profits": total_profits,
             "yield_rp": yield_rp,
             "yield_rp_trend": yield_rp_trend,}

@loopcoin.route('/yield')#, version='v1', name='Dto')
@doc.summary('用户-交易所-收益率')
@doc.description('计算用户交易所收益率')
@doc.consumes(YieldDto, location='args', required=True)
async def yield_statistics(request):

    with Timer() as timer_cal:
        try:
            # 日收益算出复权收益
            data_sql = read_mysql(f"select * from coin_assets_day  where user_id = {int(request.args['user'][0])} and api_id= {int(request.args['api'][0])} order by time_key asc")
            status = 1
            if data_sql.to_dict(orient='records'):
                data = reversion_rate(data_sql.to_dict(orient='records'))
            else:
                data = {"yield_rp_trend":[]}
            data_last = read_mysql(f"select * from coin_yield  where user_id = {int(request.args['user'][0])} and api_id= {int(request.args['api'][0])}").to_dict(orient='records')
            if data_last:
                data_last = data_last[-1]
                data["yield_rp_trend"].append({"time_key":int(time.mktime(datetime.date.today().timetuple())),"yield_rp": data_last["yield_rp"]})
                data["total_assets"] = data_last["total_assets"]
                data["total_profits"] = data_last["total_profits"]
                data["yield_rp"] = data_last["yield_rp"]
                data["today_profits"] = data_last["today_profits"]
                data["yield_rp_24h"] = data_last["yield_rp_24h"]
                data["today_status"] = 1
            else:
                data["today_status"] =-1

        except Exception as e:
            data = {'message': str(e)}
            status = 0


    return response.json(
        {'status': status,
        "create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
        "use_time_mysql": f"{timer_cal.cost:.2f}",
        "data": data,},
        headers = {'X-Served-By': 'sanic'},
        status=200
    )


@loopcoin.route('/dashboard/<code>/<kline_index>/<ranger>')#, version='v1', name='Dto')
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