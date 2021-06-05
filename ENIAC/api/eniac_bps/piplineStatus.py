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
import pymysql
import pandas as pd
pipline = Blueprint('pipline', url_prefix='/pipline', strict_slashes=True)



def read_mysql(sql="select * from model_feature_state where state = 0"):
    conn=pymysql.connect(host='rm-uf6rozhp0o3za68tt.mysql.rds.aliyuncs.com',
                         port=3306,
                         user='root',
                         passwd='LOOP2themoon',
                         db='ac',
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


@pipline.route('/status/<code>')#, version='v1', name='Dto')
@doc.summary('建模数据管道状态查询')
async def pipline_status_pick(request, code):

    with Timer() as timer_cal:
        if int(code) != 2:
            try:
                data = read_mysql(f"select * from model_state  where state = {code}")
                status = 1
                data = data.to_dict(orient='records')
            except Exception as e:
                data = {'message': str(e)}
                status = 0

        else: #  符合2-3的项
            try:
                data = read_mysql(sql="select model_state.* from model_state left join (select code, max(period_type) as period_type from model_state where state < 2 group by code) as df2 on model_state.code = df2.code where model_state.state = 2  and model_state.period_type > df2.period_type")
                status = 1
                data = data.to_dict(orient='records')
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






