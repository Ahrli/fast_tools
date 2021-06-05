#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pendulum
import arrow
import pandas as pd
from sanic import Blueprint
from sanic import response
from sanic_openapi import doc
from sanic_cors import cross_origin
import pysnooper
from ..models import APIVALIDATION
# from ..eniacutil import ApiValidation
from ..es_operate import es_sql_df, conduct_dataframe, deal_q_time, conduct_mul_dataframe, es_query_df
from ..mongo_operate import read_mongo, read_mongo_aggregate
from ..eniacutil import query_es
import toolkit

if toolkit.__version__ == "1.7.20":
    from toolkit.managers import Timer
else:
    from toolkit.tools.managers import Timer
import numpy as np
import urllib.parse

financial = Blueprint('financial', url_prefix='/financial', strict_slashes=True)


@financial.route('/class', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股票板块类型')
@doc.description('股票板块类型包括 INDUSTRY 行业板块 REGION 地域板块 CONCEPT 概念板块 other 其它板块')
async def get_big_class(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                data = es_sql_df(sql=f"SELECT plate_type FROM stock_plate group by plate_type")

            except Exception as e:
                data = {"state": -1, "message": str(e)}
        data = list(data['plate_type'])

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


@financial.route('/shareholder/statistics/<market>/<subtype>', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('板块股东统计')
@doc.description('此板块下股东数据全返回')
async def get_shareholder_statistics(request, market, subtype):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                usesubtype = "'" + subtype + "'"
                usemarket = "'" + market + "'"
                data = es_sql_df(
                    sql=f"SELECT code,code_name FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
                codes = list(data['code'])
                # print(codes)
                sdf = read_mongo(db="stock_data", collection="gdrs", select={'_id': 0})
                df = sdf.loc[sdf['code'].isin(codes),]
                data = df.replace("--", 0).to_dict('recodes')


            except Exception as e:
                data = {"state": -1, "message": str(e)}

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


@financial.route('/shareholder/detail', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股东数据')
@doc.description('股东数据')
async def get_shareholder_detail(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(request.args)
                # print(request.body)
                sdf = read_mongo(db="stock_data",
                                 collection="institution_cq",
                                 query={'date': request.args['date'][0],
                                        request.args['field'][0]: {'$ne': None}},
                                 # todo None Null "NaN" 都没有生效，目前多查2倍数据后，过滤
                                 select={'_id': 0},
                                 sortby=request.args['field'][0],
                                 upAndDown=int(request.args['sort'][0]),
                                 limitNum=int(request.args['limit'][0]) * 2)
                # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
                sdf = sdf.fillna(value=0)
                # print(len(sdf))
                start = (int(request.args['page'][0]) - 1) * int(request.args['size'][0])
                end = start + int(request.args['size'][0])

                sdf = sdf.loc[sdf[request.args['field'][0]] != 0,]
                # if int(request.args['sort'][0]) == 1:
                #     sdf = sdf.sort_values(by=request.args['field'][0], ascending=1)
                # else:
                #     sdf = sdf.sort_values(by=request.args['field'][0], ascending=0)
                num = len(sdf)
                # print(len(sdf))
                sdf = sdf[start:end]
                # print(sdf)
                # sdf = sdf.sort_values(by=request.args['field'][0], ascending=int(request.args['sort'][0]))
                # print(sdf[request.args['field'][0]])
                data = sdf.to_dict('recodes')
                # print(data[0])
                # print(len(data))
                # data=data.fillna(value=0)


            except Exception as e:
                num = 0
                data = {"state": -1, "message": str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "count": len(data),
         "all_num": num,
         "data": data
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )


@financial.route('/shareholder/onedetail', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('单只股票股东持股数据')
@doc.description('单只股票股东持股数据')
async def get_shareholder_onedetail(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(request.args)
                # print(request.body)
                sdf = read_mongo(db="stock_data",
                                 collection="institution_cq",
                                 query={'code': request.args['code'][0]},
                                 # todo None Null "NaN" 都没有生效，目前多查2倍数据后，过滤
                                 select={'_id': 0},
                                 )
                # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
                # print(sdf)
                # print(sdf)
                sdf = sdf.replace([np.inf, -np.inf], np.nan)
                # print(sdf)
                sdf = sdf.fillna(value=0)
                print(sdf)
                data = sdf.to_dict('recodes')



            except Exception as e:
                data = {"state": -1, "message": str(e)}

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


@financial.route('/class/<market>/<ctype>', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股票子板块查询')
@doc.description('股票子板块 market 可选 SZ SH HK US 0 ctype 可选 INDUSTRY 行业板块 REGION 地域板块 CONCEPT 概念板块 other 其它板块')
async def get_subtype_name(request, market, ctype):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                usectype = "'" + ctype + "'"
                usemarket = "'" + market + "'"
                data = es_sql_df(
                    sql=f"SELECT plate_name,plate_code FROM stock_plate where plate_type = {usectype} and category = {usemarket} ")
                data = data.drop_duplicates().to_dict('recodes')
            except Exception as e:
                data = {"state": -1, "message": str(e)}

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


@financial.route('/allclass', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股票全板块')
@doc.description('股票子板块 market 可选 SZ SH HK US 0 ctype 可选 INDUSTRY 行业板块 REGION 地域板块 CONCEPT 概念板块 other 其它板块')
async def get_all_class(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                data = []
                for mkt in ['SH', 'SZ', 'US', 'HK']:
                    for ctp in ['INDUSTRY', 'REGION', 'CONCEPT', 'other']:
                        usectype = "'" + ctp + "'"
                        usemarket = "'" + mkt + "'"
                        try:
                            dataone = es_sql_df(
                                sql=f"SELECT plate_name,plate_code FROM stock_plate where plate_type = {usectype} and category = {usemarket} ")
                            # print(dataone)
                            dataone = dataone.drop_duplicates().to_dict('recodes')
                            # dataone = dataone.to_dict('recodes')
                        # print(dataone)
                        except:
                            dataone = []
                        data.append({"market": mkt, "plate_type": ctp, "plate": dataone})
                        # print(data)
            except Exception as e:
                data = {"state": -1, "message": str(e)}

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


@financial.route('/allcode', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股票全名称')
@doc.description('拉取全股票板块归属')
async def get_all_class(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                data = es_sql_df(sql=f"SELECT * FROM  stock_code ")
                # print(dataone)
                data = data.to_dict('recodes')
                # dataone = dataone.to_dict('recodes')
            # print(dataone)
            except Exception as e:
                data = {"state": -1, "message": str(e)}

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


@financial.route('/code/<market>/<subtype>', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股票子板块中的股票')
@doc.description('股票子板块股票 market 可选 SZ SH HK US ')
async def get_code_from_subtype(request, market, subtype):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(subtype)
                usesubtype = "'" + subtype + "'"
                usemarket = "'" + market + "'"
                data = es_sql_df(
                    sql=f"SELECT code,code_name FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
                data = data.to_dict('recodes')
            except Exception as e:
                data = {"state": -1, "message": str(e)}
        # data = list(data['code'])

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


@financial.route('/detail/<market>/<subtype>/<dim>', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('子板块所有股票财报详情')
@doc.description('子板块所有股票 market 可选 SZ SH HK US ')
async def get_subtype_detail(request, market, subtype, dim):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(subtype)
                usesubtype = "'" + subtype + "'"
                usemarket = "'" + market + "'"
                usedim = "'" + dim + "'"
                data = es_sql_df(
                    sql=f"SELECT code,code_name FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
                codes = list(data['code'])
                # print(codes)

                # print(codes)
                # usecodes = " ( " + "".join([" code = " + c + " or " for c in ["'" + i + "'" for i in codes]])[
                #                    :-3] + " ) "
                # print(usecodes)
                if dim == "Year":
                    fdata = read_mongo(db="stock_data",
                                       collection="finance",
                                       query={'InfoSource': 'FY',
                                              '$or': [{'code': c} for c in codes]
                                              }
                                       ,
                                       select={'_id': 0,
                                               # 'code': 1,
                                               # 'cgsz': 1,
                                               # 'date': 1
                                               },
                                       )
                    # fdata = es_sql_df(sql=f"SELECT * FROM finance_calculate where {usecodes} and InfoSource = 'FY' ")

                else:
                    fdata = read_mongo(db="stock_data",
                                       collection="finance",
                                       query={
                                           '$or': [{'code': c} for c in codes],
                                           'InfoSource': {
                                               '$ne': "FY"
                                           }
                                       }
                                       ,
                                       select={'_id': 0,
                                               # 'code': 1,
                                               # 'cgsz': 1,
                                               # 'date': 1
                                               },
                                       )

                    # fdata = es_sql_df(sql=f"SELECT * FROM finance_calculate where {usecodes} and InfoSource != 'FY' ")

                # print(fdata)
                fdata = fdata.fillna(value=0)
                fdata = fdata.loc[fdata['PB'] != 0,]
                fdata['code_name'] = conduct_dataframe(fdata, 'code',
                                                       lambda code: list(data.loc[data['code'] == code, 'code_name'])[
                                                           0])
                # print(fdata)
                # print(data)
                # print(fdata)
                # print(fdata['code'])
                # fdata = pd.merge(data,fdata,how = 'left', on='code')

                if dim == "Quarter":
                    data = []
                    fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY-MM"))
                    for t in list(fdata['time'].drop_duplicates()):
                        data.append({"dim": t, "result": fdata.loc[(fdata['time'] == t),].to_dict("records")})

                elif dim == "Year":
                    data = []
                    fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY"))
                    for t in list(fdata['time'].drop_duplicates()):
                        data.append({"dim": t, "result": fdata.loc[(fdata['time'] == t),].to_dict("records")})
                else:
                    pass

                # data = data.to_dict('recodes')

            except Exception as e:
                data = {"state": -1, "message": str(e)}
        # data = list(data['code'])

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


@financial.route('/onedetail/<code>/<dim>', methods=['GET', 'OPTIONS'])
@doc.summary('单只股票财报详情')
@doc.description('单只股票财报详情 可选  Quarter Years')
async def get_one_code_detail(request, code, dim):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                usecode = "'" + code + "'"
                usedim = "'" + dim + "'"
                # usesubtype = "'" + subtype + "'"
                # data = es_sql_df(sql=f"SELECT code FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
                # codes = list(data['code'])
                # # print(codes)
                # usecodes = " ( " + "".join([" code = " + c + " or "  for c in ["'" + i + "'" for i in codes]])[:-3] + " ) "
                if dim == "Year":
                    fdata = read_mongo(db="stock_data",
                                       collection="finance",
                                       query={'InfoSource': 'FY',
                                              'code': code
                                              }
                                       ,
                                       sortby='EndDate',
                                       select={'_id': 0,
                                               # 'code': 1,
                                               # 'cgsz': 1,
                                               # 'date': 1
                                               },
                                       )
                    # fdata = es_sql_df(
                    #     sql=f"SELECT * FROM finance_calculate where code = {usecode} and InfoSource = 'FY' ")

                else:
                    fdata = read_mongo(db="stock_data",
                                       collection="finance",
                                       query={
                                           'code': code,
                                           'InfoSource': {
                                               '$ne': "FY"
                                           }
                                       }
                                       ,
                                       sortby='EndDate',
                                       select={'_id': 0,
                                               # 'code': 1,
                                               # 'cgsz': 1,
                                               # 'date': 1
                                               },
                                       )

                    # fdata = es_sql_df(
                    #     sql=f"SELECT * FROM finance_calculate where code = {usecode} and InfoSource != 'FY' ")

                # print(fdata)
                fdata = fdata.fillna(value=0)
                fdata = fdata.loc[fdata['PB'] != 0,]
                # print(fdata)
                if dim == "Quarter":
                    data = []
                    fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY-MM"))
                    for t in list(fdata['time'].drop_duplicates()):
                        data.append({"dim": t, "result": fdata.loc[(fdata['time'] == t),].to_dict("records")})

                elif dim == "Year":
                    data = []
                    fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY"))
                    for t in list(fdata['time'].drop_duplicates()):
                        data.append({"dim": t, "result": fdata.loc[(fdata['time'] == t),].to_dict("records")})
                else:
                    pass

                # data = data.to_dict('recodes')

            except Exception as e:
                data = {"state": -1, "message": str(e)}
        # data = list(data['code'])
        # print(data)

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


@financial.route('/calculate/<code>/<kline_index>/<ranger>/<dim>/<autotype>', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('k线季度年度均值计算')
@doc.description('k线季度年度均值计算 可选  Quarter Years')
async def kline_calculate(request, code, kline_index, ranger, dim, autotype):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                data = query_es(kline_index, code, ranger, autotype)
                if dim == "Quarter":
                    data['time'] = conduct_dataframe(data, "create_time", deal_q_time)
                    data = data[['time', 'close']].groupby('time').mean()
                    # print(data)
                    data['time'] = data.index
                    data = data.to_dict('recodes')
                else:
                    data['time'] = conduct_dataframe(data, "create_time", lambda s: arrow.get(s).format("YYYY"))
                    data = data[['time', 'close']].groupby('time').mean()
                    # print(data)
                    data['time'] = data.index
                    data = data.to_dict('recodes')


            except Exception as e:
                data = {"state": -1, "message": str(e)}
        # data = list(data['code'])

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


@financial.route('/statistics/<market>/<subtype>/<dim>', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('子板块所有股票财报统计')
@doc.description('子板块所有股票 market 可选 SZ HK US ')
async def get_subtype_statistics(request, market, subtype, dim):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(subtype)
                usesubtype = "'" + subtype + "'"
                usemarket = "'" + market + "'"
                usedim = "'" + dim + "'"
                data = es_sql_df(
                    sql=f"SELECT code FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
                codes = list(data['code'])
                # print(codes)
                usecodes = " ( " + "".join([" code = " + c + " or " for c in ["'" + i + "'" for i in codes]])[
                                   :-3] + " ) "
                # print(usecodes)
                if dim == "Year":
                    fdata = read_mongo(db="stock_data",
                                       collection="finance",
                                       query={'InfoSource': 'FY',
                                              '$or': [{'code': c} for c in codes]
                                              }
                                       ,
                                       select={'_id': 0,
                                               # 'code': 1,
                                               # 'cgsz': 1,
                                               # 'date': 1
                                               },
                                       )
                    # fdata = es_sql_df(sql=f"SELECT * FROM finance_calculate where {usecodes} and InfoSource = 'FY' ")

                else:
                    fdata = read_mongo(db="stock_data",
                                       collection="finance",
                                       query={
                                           '$or': [{'code': c} for c in codes],
                                           'InfoSource': {
                                               '$ne': "FY"
                                           }
                                       }
                                       ,
                                       select={'_id': 0,
                                               # 'code': 1,
                                               # 'cgsz': 1,
                                               # 'date': 1
                                               },
                                       )
                    # fdata = es_sql_df(sql=f"SELECT * FROM finance_calculate where {usecodes} and InfoSource != 'FY' ")

                # print(fdata)
                # fdata = fdata.fillna(value=0)

                if dim == "Quarter":
                    # data = []/financial/statistics
                    fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY-MM"))

                    # for t in list(fdata['time'].drop_duplicates()):
                    #     data.append({"dim":t,"result":fdata.loc[(fdata['time'] == t),].to_dict("records")})

                elif dim == "Year":
                    # data = []
                    fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY"))

                    # for t in list(fdata['time'].drop_duplicates()):
                    #     data.append({"dim":t,"result":fdata.loc[(fdata['time'] == t),].to_dict("records")})
                else:
                    pass

                del fdata['EndDate']
                del fdata['code']
                # del fdata['spider_time']
                del fdata['time_key']
                # print("fdata")
                # print(fdata)

                mindata = fdata.groupby("time").min()
                mindata['code'] = 'min'
                mindata['time'] = mindata.index

                maxdata = fdata.groupby("time").max()  # axis=0,skipna=True)
                maxdata['code'] = 'max'
                maxdata['time'] = maxdata.index

                mediandata = fdata.groupby("time").median()  # axis=0,skipna=True)
                mediandata['code'] = 'medain'
                mediandata['time'] = mediandata.index

                adata = pd.concat([mindata, maxdata, mediandata],
                                  ignore_index=0, sort=False)  # 默认设置，索引可重复

                adata = adata.fillna(value=0)
                # print("adata")
                # print(adata)
                data = []
                # print(list(adata['time'].drop_duplicates()))
                for t in list(adata['time'].drop_duplicates()):
                    data.append({"dim": t, "result": adata.loc[(adata['time'] == t),].to_dict("records")})

                # data = data.to_dict('recodes')
                # print("data")
                # print(data)

            except Exception as e:
                data = {"state": -1, "message": str(e)}
        # data = list(data['code'])

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


#
# @financial.route('/statistics/Q/<market>/<subtype>/<dim>', methods=['GET', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('子板块所有股票财报统计')
# @doc.description('子板块所有股票 market 可选 SH SZ HK US ')
# async def get_subtype_statistics(request, market, subtype, dim):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 # print(subtype)
#                 usesubtype = "'" + subtype + "'"
#                 usemarket = "'" + market + "'"
#                 usedim = "'" + dim + "'"
#                 data = es_sql_df(
#                     sql=f"SELECT code,code_name FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
#                 codes = list(data['code'])
#
#                 # print(codes)
#                 usecodes = " ( " + "".join([" code = " + c + " or " for c in ["'" + i + "'" for i in codes]])[
#                                    :-3] + " ) "
#                 # print(usecodes)
#                 if dim == "Year":
#                     fdata = es_sql_df(sql=f"SELECT * FROM finance_calculate where {usecodes} and InfoSource = 'FY' ")
#                 elif dim == "Quarter" and market == "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where {usecodes} and ( InfoSource = 'Q1' or InfoSource = 'Q2' or InfoSource = 'Q3' or InfoSource = 'Q4' ) ")
#                 elif dim == "QuarterTotal" and market == "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where {usecodes} and ( InfoSource = 'Q6' or InfoSource = 'Q9' ) ")
#                 elif dim == "QuarterTotal" and market != "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where {usecodes} and ( InfoSource = 'Q3' or InfoSource = 'Q6' or InfoSource = 'Q9' ) ")
#
#                 else:
#                     fdata = es_sql_df(sql=f"SELECT * FROM finance_calculate where {usecodes} and InfoSource = 'Q100' ")
#
#                 # print(fdata)
#                 fdata = fdata.fillna(value=0)
#                 fdata = fdata.loc[fdata['PB'] != 0,]
#                 fdata['code_name'] = conduct_dataframe(fdata, 'code',
#                                                        lambda code: list(data.loc[data['code'] == code, 'code_name'])[
#                                                            0])
#                 # print(fdata)
#                 # print(data)
#                 # print(fdata)
#                 # print(fdata['code'])
#                 # fdata = pd.merge(data,fdata,how = 'left', on='code')
#
#                 if dim != "Year":
#                     fdata['time'] = conduct_mul_dataframe(fdata, lambda q, s: arrow.get(s).format("YYYY") + q,
#                                                           fdata['InfoSource'], fdata['EndDate'])
#
#
#                 elif dim == "Year":
#                     fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY"))
#                 else:
#                     pass
#
#                 del fdata['EndDate']
#                 del fdata['code']
#                 del fdata['spider_time']
#                 del fdata['time_key']
#                 # print("fdata")
#                 # print(fdata)
#
#                 mindata = fdata.groupby("time").min()
#                 mindata['code'] = 'min'
#                 mindata['time'] = mindata.index
#
#                 maxdata = fdata.groupby("time").max()  # axis=0,skipna=True)
#                 maxdata['code'] = 'max'
#                 maxdata['time'] = maxdata.index
#
#                 mediandata = fdata.groupby("time").median()  # axis=0,skipna=True)
#                 mediandata['code'] = 'medain'
#                 mediandata['time'] = mediandata.index
#
#                 adata = pd.concat([mindata, maxdata, mediandata],
#                                   ignore_index=0, sort=False)  # 默认设置，索引可重复
#
#                 adata = adata.fillna(value=0)
#                 # print("adata")
#                 # print(adata)
#                 data = []
#                 # print(list(adata['time'].drop_duplicates()))
#                 for t in list(adata['time'].drop_duplicates()):
#                     data.append({"dim": t, "result": adata.loc[(adata['time'] == t),].to_dict("records")})
#
#                 # data = data.to_dict('recodes')
#                 # print("data")
#                 # print(data)
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#         # data = list(data['code'])
#
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "data": data
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )

#
# @financial.route('/detail/Q/<market>/<subtype>/<dim>', methods=['GET', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('子板块所有股票财报详情')
# @doc.description('子板块所有股票 \n market 可选 SZ SH HK US \n dim : Quarter QuarterTotal Year')
# async def get_subtype_detail(request, market, subtype, dim):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 # print(subtype)
#                 usesubtype = "'" + subtype + "'"
#                 usemarket = "'" + market + "'"
#                 usedim = "'" + dim + "'"
#                 data = es_sql_df(
#                     sql=f"SELECT code,code_name FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
#                 codes = list(data['code'])
#                 # print(codes)
#
#                 # print(codes)
#                 usecodes = " ( " + "".join([" code = " + c + " or " for c in ["'" + i + "'" for i in codes]])[
#                                    :-3] + " ) "
#                 # print(usecodes)
#                 if dim == "Year":
#                     fdata = es_sql_df(sql=f"SELECT * FROM finance_calculate where {usecodes} and InfoSource = 'FY' ")
#                 elif dim == "Quarter" and market == "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where {usecodes} and ( InfoSource = 'Q1' or InfoSource = 'Q2' or InfoSource = 'Q3' or InfoSource = 'Q4' ) ")
#                 elif dim == "QuarterTotal" and market == "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where {usecodes} and ( InfoSource = 'Q6' or InfoSource = 'Q9' ) ")
#                 elif dim == "QuarterTotal" and market != "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where {usecodes} and ( InfoSource = 'Q3' or InfoSource = 'Q6' or InfoSource = 'Q9' ) ")
#
#                 else:
#                     fdata = es_sql_df(sql=f"SELECT * FROM finance_calculate where {usecodes} and InfoSource = 'Q100' ")
#
#                 # print(fdata)
#                 fdata = fdata.fillna(value=0)
#                 fdata = fdata.loc[fdata['PB'] != 0,]
#                 fdata['code_name'] = conduct_dataframe(fdata, 'code',
#                                                        lambda code: list(data.loc[data['code'] == code, 'code_name'])[
#                                                            0])
#                 # print(fdata)
#                 # print(data)
#                 # print(fdata)
#                 # print(fdata['code'])
#                 # fdata = pd.merge(data,fdata,how = 'left', on='code')
#
#                 if dim != "Year":
#                     data = []
#                     fdata['time'] = conduct_mul_dataframe(fdata, lambda q, s: arrow.get(s).format("YYYY") + q,
#                                                           fdata['InfoSource'], fdata['EndDate'])
#                     for t in list(fdata['time'].drop_duplicates()):
#                         data.append({"dim": t, "result": fdata.loc[(fdata['time'] == t),].to_dict("records")})
#
#                 elif dim == "Year":
#                     data = []
#                     fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY"))
#                     for t in list(fdata['time'].drop_duplicates()):
#                         data.append({"dim": t, "result": fdata.loc[(fdata['time'] == t),].to_dict("records")})
#                 else:
#                     pass
#
#                 # data = data.to_dict('recodes')
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#         # data = list(data['code'])
#
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "all_num": len(fdata),
#          "data": data
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )
#
#
# # @financial.route('/onedetail/<subtype>/<code>/<dim>')#, version='v1', name='Dto')
# @financial.route('/onedetail/Q/<code>/<dim>', methods=['GET', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('单只股票财报详情')
# @doc.description('单只股票财报详情 可选  Quarter QuarterTotal Years')
# async def get_one_code_detail(request, code, dim):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 usecode = "'" + code + "'"
#                 usedim = "'" + dim + "'"
#                 market = code[:2]
#                 # usesubtype = "'" + subtype + "'"
#                 # data = es_sql_df(sql=f"SELECT code FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
#                 # codes = list(data['code'])
#                 # # print(codes)
#                 # usecodes = " ( " + "".join([" code = " + c + " or "  for c in ["'" + i + "'" for i in codes]])[:-3] + " ) "
#                 if dim == "Year":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where code = {usecode} and InfoSource = 'FY' ")
#
#                 elif dim == "Quarter" and market == "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where code = {usecode} and ( InfoSource = 'Q1' or InfoSource = 'Q2' or InfoSource = 'Q3' or InfoSource = 'Q4' ) ")
#                 elif dim == "QuarterTotal" and market == "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where code = {usecode} and ( InfoSource = 'Q6' or InfoSource = 'Q9' ) ")
#                 elif dim == "QuarterTotal" and market != "US":
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where code = {usecode} and ( InfoSource = 'Q3' or InfoSource = 'Q6' or InfoSource = 'Q9' ) ")
#
#                 else:
#                     fdata = es_sql_df(
#                         sql=f"SELECT * FROM finance_calculate where code = {usecode} and InfoSource = 'Q100' ")
#
#                 # print(fdata)
#                 fdata = fdata.fillna(value=0)
#                 fdata = fdata.loc[fdata['PB'] != 0,]
#                 # print(fdata)
#
#                 if dim != "Year":
#                     data = []
#                     fdata['time'] = conduct_mul_dataframe(fdata, lambda q, s: arrow.get(s).format("YYYY") + q,
#                                                           fdata['InfoSource'], fdata['EndDate'])
#                     for t in list(fdata['time'].drop_duplicates()):
#                         data.append({"dim": t, "result": fdata.loc[(fdata['time'] == t),].to_dict("records")})
#
#                 elif dim == "Year":
#                     data = []
#                     fdata['time'] = conduct_dataframe(fdata, "EndDate", lambda s: arrow.get(s).format("YYYY"))
#                     for t in list(fdata['time'].drop_duplicates()):
#                         data.append({"dim": t, "result": fdata.loc[(fdata['time'] == t),].to_dict("records")})
#                 else:
#                     pass
#
#                 # data = data.to_dict('recodes')
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#         # data = list(data['code'])
#         # print(data)
#
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "data": data
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )

#
# @financial.route('/fund/statistics', methods=['GET', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('机构数据统计')
# @doc.description('汇总机构总市值')
# async def get_fund_statistics(request):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 # print(request.args)
#                 # print(request.body)
#                 sdf = read_mongo(db="stock_data",
#                                  collection="ths_position_data",
#                                  # collection="dfcf_jjcc_data",
#                                  query={'date': request.args['date'][0]},
#                                  select={'_id': 0,
#                                          'mc': 1,
#                                          'jglx': 1,
#
#                                          # 'date':1,
#                                          'cgsz': 1},
#                                  )
#                 # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
#                 # print(sdf)
#
#                 sdf['type'] = conduct_dataframe(sdf, "cgsz", lambda _s: isinstance(_s, float))
#                 sdf = sdf.loc[sdf['type'] == 1,]
#                 # print(sdf['type'])
#                 del sdf['type']
#                 # sdf = sdf.loc[sdf['cgsz'] != "-",]
#                 # print(sdf.loc[sdf['cgsz'] == '不足0.01%'])
#                 sdf['cgsz'] = conduct_dataframe(sdf, "cgsz", float)
#                 sdf = sdf.fillna(value=0)
#                 df1 = sdf[['mc', 'cgsz', 'jglx']].groupby(['mc', 'jglx']).sum().reset_index()
#                 df2 = sdf[['mc', 'cgsz', 'jglx']].groupby(['mc', 'jglx']).count().reset_index()
#                 df1['num'] = df2['cgsz']
#                 sdf = df1
#                 # print(sdf)
#                 if int(request.args['sort'][0]) == 1:
#                     sdf = sdf.sort_values(by=request.args['field'][0], ascending=1)
#                 else:
#                     sdf = sdf.sort_values(by=request.args['field'][0], ascending=0)
#
#                 # print(sdf)
#
#                 start = (int(request.args['page'][0]) - 1) * int(request.args['size'][0])
#                 end = start + int(request.args['size'][0])
#                 count_num = len(sdf)
#                 sdf = sdf[start:end]
#                 data = sdf.to_dict('recodes')
#
#
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "count_num": count_num,
#          "data": data
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )
#
#
# @financial.route('/fund/detail', methods=['POST', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('机构数据详情')
# @doc.description('汇总机构数据详情')
# async def get_fund_detail(request):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 # print(request.args)
#                 import json
#                 _json = json.loads(str(request.body, "utf-8"))
#                 # print(json.loads(str(request.body,"utf-8"))['mc'])
#                 sdf = read_mongo(db="stock_data",
#                                  collection="ths_position_data",
#                                  # collection="dfcf_jjcc_data",
#                                  query={'mc': _json['mc']},
#                                  select={'_id': 0},
#                                  )
#                 # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
#                 # print(sdf)
#                 # sdf = sdf.fillna(value=0)
#                 # sdf = sdf[['jglx','mc','cysl']].groupby(['mc','jglx']).sum().reset_index()
#                 # print(sdf)
#                 # if int(request.args['sort'][0]) == 1:
#                 #     sdf = sdf.sort_values(by='cysl', ascending=1)
#                 # else:
#                 #     sdf = sdf.sort_values(by='cysl', ascending=0)
#                 #
#                 # start = (int(request.args['page'][0])-1)*int(request.args['size'][0])
#                 # end = start + int(request.args['size'][0])
#                 # count_num=len(sdf)
#                 # sdf = sdf[start:end]
#                 # print(sdf)
#                 sdf = sdf.fillna(value=0)
#                 data = sdf.to_dict('recodes')
#
#
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "data": data
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )
#
#
# @financial.route('/fund/bk', methods=['POST', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('机构数据板块详情')
# @doc.description('汇总机构板块详情')
# async def get_funds_bk(request):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 # print(request.args)
#                 import json
#                 _json = json.loads(str(request.body, "utf-8"))
#                 # print(json.loads(str(request.body,"utf-8"))['mc'])
#                 sdf = read_mongo(db="stock_data",
#                                  collection="ths_position_data",
#                                  # collection="dfcf_jjcc_data",
#                                  query={'mc': _json['mc']},
#                                  select={'_id': 0,
#                                          'code': 1,
#                                          'cgsz': 1,
#                                          'date': 1},
#                                  )
#                 # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
#                 # print(sdf)
#                 # sdf = sdf.fillna(value=0)
#                 # sdf = sdf[['jglx','mc','cysl']].groupby(['mc','jglx']).sum().reset_index()
#                 # print(sdf)
#                 # if int(request.args['sort'][0]) == 1:
#                 #     sdf = sdf.sort_values(by='cysl', ascending=1)
#                 # else:
#                 #     sdf = sdf.sort_values(by='cysl', ascending=0)
#                 #
#                 # start = (int(request.args['page'][0])-1)*int(request.args['size'][0])
#                 # end = start + int(request.args['size'][0])
#                 # count_num=len(sdf)
#                 # sdf = sdf[start:end]
#                 # print(sdf)
#                 # print(sdf.loc[sdf['date']=="2018-09-30",])
#                 # sdf = sdf.loc[sdf['date']=="2018-09-30",]
#                 codes = list(sdf['code'].drop_duplicates())
#                 dates = list(sdf['date'].drop_duplicates())
#                 # if len(codes) <= 1:
#                 #     usecodes = " ( " + "".join([" code = " + c + " or "  for c in ["'" + i + "'" for i in codes]])[:-3] + " ) "
#                 #     fdata = es_sql_df(sql=f"SELECT code,plate_name FROM stock_plate where code = codes[0] and plate_type = 'INDUSTRY' ")
#                 #
#                 #
#                 # else:
#                 usecodes = " ( " + "".join([" code = " + c + " or " for c in ["'" + i + "'" for i in codes]])[
#                                    :-3] + " ) "
#                 # print(usecodes)
#                 # print(usecodes)
#                 fdata = es_sql_df(
#                     sql=f"SELECT code,plate_name FROM stock_plate where {usecodes} and plate_type = 'INDUSTRY' ")
#                 # fdata = es_sql_df(sql=f"SELECT code,plate_name FROM stock_plate where {usecodes} and plate_type = 'other' ")
#                 # print(fdata)
#                 # print(fdata)
#                 data = []
#                 # print(fdata)
#
#                 for d in dates:
#                     try:
#                         ndf = pd.merge(sdf.loc[sdf['date'] == d,], fdata, on='code', how='right')
#                         ndf = ndf.dropna(how='any')
#                         _sum = sum(ndf['cgsz'])
#
#                         # 计算百分比
#                         # ndf['cgsz'] = conduct_dataframe(ndf,"cgsz",lambda _s : _s/_sum)
#                         # print(ndf)
#
#                         rdf = pd.pivot_table(ndf,
#                                              index=['date'],
#                                              columns=['plate_name'],
#                                              values='cgsz',
#                                              aggfunc=sum).reset_index()
#                         # print(rdf)
#                         # print(d)
#                         result = rdf.to_dict('recodes')
#                         # print(result)
#                         onedata = {"date": result[0]['date']}
#                         onedata['bk'] = list(result[0].keys())[1:]
#                         onedata['value'] = list(result[0].values())[1:]
#
#                         data.append(onedata)
#                     except:
#                         pass
#
#                     # data.append(rdf.to_dict('recodes'))
#                 fdata = es_sql_df(
#                     sql=f"SELECT code,plate_name FROM stock_plate where {usecodes} and plate_type = 'CONCEPT' ")
#                 data1 = []
#                 for d in dates:
#                     try:
#                         ndf = pd.merge(sdf.loc[sdf['date'] == d,], fdata, on='code', how='right')
#                         ndf = ndf.dropna(how='any')
#                         _sum = sum(ndf['cgsz'])
#                         # ndf['cgsz'] = conduct_dataframe(ndf,"cgsz",lambda _s : _s/_sum)
#                         # print(ndf)
#                         rdf = pd.pivot_table(ndf,
#                                              index=['date'],
#                                              columns=['plate_name'],
#                                              values='cgsz',
#                                              aggfunc=sum).reset_index()
#
#                         result = rdf.to_dict('recodes')
#                         onedata = {"date": result[0]['date']}
#                         onedata['bk'] = list(result[0].keys())[1:]
#                         onedata['value'] = list(result[0].values())[1:]
#
#                         data1.append(onedata)
#                     except:
#                         pass
#                 # print(data)
#
#                 # print(len(sdf))
#                 # print(ndf)
#                 # print(len(ndf))
#
#                 # sdf = sdf.fillna(value=0)
#                 # rdf = pd.pivot_table(ndf,index=['date'],
#                 #                columns=['plate_name'],
#                 #                values='cgsz',
#                 #                aggfunc=lambda x : x/sum(x))
#                 # print(rdf)
#                 # data = sdf.to_dict('recodes')
#
#
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "data": data,
#          "data_CONCEPT": data1
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )
#
#
# @financial.route('/funds/statisticsion', methods=['GET', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('基金数据统计')
# @doc.description('汇总基金总市值')
# async def get_fund2_statistics(request):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 # print(request.args)
#                 # print(request.body)
#                 sdf = read_mongo(db="stock_data",
#                                  collection="dfcf_jjcc_data",
#                                  # collection="dfcf_jjcc_data",
#                                  query={'date': request.args['date'][0]},
#                                  select={'_id': 0,
#                                          'mc': 1,
#                                          'cgsz': 1},
#                                  )
#                 # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
#                 # print(sdf)
#                 # sdf = sdf.fillna(value=0)
#                 # print(sdf)
#                 # sdf = sdf.loc[sdf['cgsz'] != "---",]
#                 # sdf['cgsz'] = conduct_dataframe(sdf,"cgsz",float)
#                 sdf['type'] = conduct_dataframe(sdf, "cgsz", lambda _s: isinstance(_s, float))
#                 sdf = sdf.loc[sdf['type'] == 1,]
#                 # print(sdf['type'])
#                 del sdf['type']
#                 # print(len(sdf))
#                 # print(sdf)
#                 # sdf['']
#
#                 # sdf = sdf[['mc','cgsz']].groupby(['mc']).sum().reset_index()
#                 df1 = sdf[['mc', 'cgsz']].groupby(['mc']).sum().reset_index()
#                 df2 = sdf[['mc', 'cgsz']].groupby(['mc']).count().reset_index()
#                 df1['num'] = df2['cgsz']
#                 sdf = df1
#                 # print(sdf)
#
#                 if int(request.args['sort'][0]) == 1:
#                     sdf = sdf.sort_values(by=request.args['field'][0], ascending=1)
#                 else:
#                     sdf = sdf.sort_values(by=request.args['field'][0], ascending=0)
#
#                 start = (int(request.args['page'][0]) - 1) * int(request.args['size'][0])
#                 end = start + int(request.args['size'][0])
#                 count_num = len(sdf)
#                 sdf = sdf[start:end]
#                 data = sdf.to_dict('recodes')
#
#
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "count_num": count_num,
#          "data": data
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )
#
#
# @financial.route('/funds/detail', methods=['POST', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('基金数据详情')
# @doc.description('汇总基金详情')
# async def get_funds_detail(request):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 # print(request.args)
#                 import json
#                 _json = json.loads(str(request.body, "utf-8"))
#                 # print(json.loads(str(request.body,"utf-8"))['mc'])
#                 sdf = read_mongo(db="stock_data",
#                                  collection="dfcf_jjcc_data",
#                                  # collection="dfcf_jjcc_data",
#                                  query={'mc': _json['mc']},
#                                  select={'_id': 0},
#                                  )
#                 # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
#                 # print(sdf)
#                 # sdf = sdf.fillna(value=0)
#                 # sdf = sdf[['jglx','mc','cysl']].groupby(['mc','jglx']).sum().reset_index()
#                 # print(sdf)
#                 # if int(request.args['sort'][0]) == 1:
#                 #     sdf = sdf.sort_values(by='cysl', ascending=1)
#                 # else:
#                 #     sdf = sdf.sort_values(by='cysl', ascending=0)
#                 #
#                 # start = (int(request.args['page'][0])-1)*int(request.args['size'][0])
#                 # end = start + int(request.args['size'][0])
#                 # count_num=len(sdf)
#                 # sdf = sdf[start:end]
#                 # print(sdf)
#                 codes = list(sdf['code'].drop_duplicates())
#
#                 sdf = sdf.fillna(value=0)
#                 data = sdf.to_dict('recodes')
#
#
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "data": data
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )
#
#
# @financial.route('/funds/bk', methods=['POST', 'OPTIONS'])
# # @cross_origin(financial)
# @doc.summary('基金数据板块详情')
# @doc.description('汇总基金板块详情')
# async def get_funds_bk(request):
#     with Timer() as timer:
#         with Timer() as timer_es:
#             try:
#                 # print(request.args)
#                 import json
#                 _json = json.loads(str(request.body, "utf-8"))
#                 # print(json.loads(str(request.body,"utf-8"))['mc'])
#                 sdf = read_mongo(db="stock_data",
#                                  collection="dfcf_jjcc_data",
#                                  # collection="dfcf_jjcc_data",
#                                  query={'mc': _json['mc']},
#                                  select={'_id': 0,
#                                          'code': 1,
#                                          'cgsz': 1,
#                                          'date': 1},
#                                  )
#                 # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
#                 # print(sdf)
#                 # sdf = sdf.fillna(value=0)
#                 # sdf = sdf[['jglx','mc','cysl']].groupby(['mc','jglx']).sum().reset_index()
#                 # print(sdf)
#                 # if int(request.args['sort'][0]) == 1:
#                 #     sdf = sdf.sort_values(by='cysl', ascending=1)
#                 # else:
#                 #     sdf = sdf.sort_values(by='cysl', ascending=0)
#                 #
#                 # start = (int(request.args['page'][0])-1)*int(request.args['size'][0])
#                 # end = start + int(request.args['size'][0])
#                 # count_num=len(sdf)
#                 # sdf = sdf[start:end]
#                 # print(sdf)
#                 codes = list(sdf['code'].drop_duplicates())
#                 dates = list(sdf['date'].drop_duplicates())
#
#                 usecodes = " ( " + "".join([" code = " + c + " or " for c in ["'" + i + "'" for i in codes]])[
#                                    :-3] + " ) "
#                 # print(usecodes)
#                 fdata = es_sql_df(
#                     sql=f"SELECT code,plate_name FROM stock_plate where {usecodes} and plate_type = 'INDUSTRY' ")
#                 data = []
#                 for d in dates:
#                     try:
#                         ndf = pd.merge(sdf.loc[sdf['date'] == d,], fdata, on='code', how='right')
#                         ndf = ndf.dropna(how='any')
#                         _sum = sum(ndf['cgsz'])
#                         # ndf['cgsz'] = conduct_dataframe(ndf,"cgsz",lambda _s : _s/_sum)
#                         # print(ndf)
#                         rdf = pd.pivot_table(ndf,
#                                              index=['date'],
#                                              columns=['plate_name'],
#                                              values='cgsz',
#                                              aggfunc=sum).reset_index()
#
#                         result = rdf.to_dict('recodes')
#                         onedata = {"date": result[0]['date']}
#                         onedata['bk'] = list(result[0].keys())[1:]
#                         onedata['value'] = list(result[0].values())[1:]
#
#                         data.append(onedata)
#                         # print(data)
#                     except:
#                         pass
#
#                 fdata = es_sql_df(
#                     sql=f"SELECT code,plate_name FROM stock_plate where {usecodes} and plate_type = 'CONCEPT' ")
#                 data1 = []
#                 for d in dates:
#                     try:
#                         ndf = pd.merge(sdf.loc[sdf['date'] == d,], fdata, on='code', how='right')
#                         ndf = ndf.dropna(how='any')
#                         _sum = sum(ndf['cgsz'])
#                         # ndf['cgsz'] = conduct_dataframe(ndf,"cgsz",lambda _s : _s/_sum)
#                         # print(ndf)
#                         rdf = pd.pivot_table(ndf,
#                                              index=['date'],
#                                              columns=['plate_name'],
#                                              values='cgsz',
#                                              aggfunc=sum).reset_index()
#
#                         result = rdf.to_dict('recodes')
#                         onedata = {"date": result[0]['date']}
#                         onedata['bk'] = list(result[0].keys())[1:]
#                         onedata['value'] = list(result[0].values())[1:]
#
#                         data1.append(onedata)
#                     except:
#                         pass
#
#                     # data.append(rdf.to_dict('recodes'))
#
#                 # print(len(sdf))
#                 # print(ndf)
#                 # print(len(ndf))
#
#                 # sdf = sdf.fillna(value=0)
#                 # rdf = pd.pivot_table(ndf,index=['date'],
#                 #                columns=['plate_name'],
#                 #                values='cgsz',
#                 #                aggfunc=lambda x : x/sum(x))
#                 # print(rdf)
#                 # data = sdf.to_dict('recodes')
#
#
#
#             except Exception as e:
#                 data = {"state": -1, "message": str(e)}
#     # print(data1)
#     return response.json(
#         {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
#          "use_time": f"{timer.cost:.2f}",
#          "use_time_es": f"{timer_es.cost:.2f}",
#          "count": len(data),
#          "data": data,
#          "data_CONCEPT": data1
#          },
#         headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
#         status=200
#     )


@financial.route('/allfunds/statisticsion', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('全机构数据统计')
@doc.description('汇总全机构总市值')
async def get_allfund_statistics(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(request.args)
                # print(request.body)
                # count_num = 0
                sdf = read_mongo(db="stock_data",
                                 collection="dfcf_ajax_data_top",
                                 # collection="dfcf_jjcc_data",
                                 query={'date': request.args['date'][0],
                                        'market': request.args['market'][0],
                                        },
                                 select={'_id': 0,
                                         'mc': 1,
                                         'Type': 1,
                                         'num': 1,
                                         'cgsz': 1,
                                         'ratio': 1},
                                 sortby=request.args['field'][0],  # 排序字段
                                 upAndDown=int(request.args['sort'][0]),  # 升序
                                 limitNum=99999,  # 限制数量
                                 )
                print(len(sdf))
                print(arrow.now())

                start = (int(request.args['page'][0]) - 1) * int(request.args['size'][0])
                end = start + int(request.args['size'][0])
                try:
                    count_num = len(sdf)
                    sdf = sdf[start:end]
                    sdf = sdf.fillna(value='---')
                    data = sdf.to_dict('recodes')
                except:
                    count_num = 0
                    data = []


            except Exception as e:
                data = {"state": -1, "message": str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "count": len(data),
         "count_num": count_num,
         "data": data
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )


@financial.route('/allfunds/range', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('全机构季度区间')
@doc.description('全机构季度区间')
async def get_allfund_range(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(request.args)
                # print(request.body)
                # count_num = 0
                sdf = read_mongo_aggregate(db="stock_data",
                                           collection="dfcf_ajax_data_top",
                                           pipline=[
                                               {"$match": {'market': request.args['market'][0]}},
                                               {"$group": {"_id": {"date": "$date"}}},
                                               {"$project": {"date": "$_id.date"}},
                                               {'$sort': {"date": 1}},
                                               # {'$limit': 99999999}
                                           ],
                                           )
                data = list(sdf['date'])#.to_dict('recodes')





            except Exception as e:
                data = {"state": -1, "message": str(e)}

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


@financial.route('/allfunds/detail', methods=['POST', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('全机构数据详情')
@doc.description('汇总全机构详情')
async def get_allfund_detail(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(request.args)
                import json
                _json = json.loads(str(request.body, "utf-8"))
                # print(json.loads(str(request.body,"utf-8"))['mc'])
                sdf = read_mongo(db="stock_data",
                                 collection="dfcf_ajax_data",
                                 # collection="dfcf_jjcc_data",
                                 query={'mc': _json['mc'],
                                        # 'time_key':{"$gt":1520041600}
                                        },
                                 select={'_id': 0,
                                         'SCode': 0,
                                         'SName': 0,
                                         'RDate': 0,
                                         'SHCode': 0,
                                         'SHName': 0,
                                         'InstSName': 0,
                                         'InstCode': 0,
                                         # 'date':1,
                                         # 'code':1,
                                         # 'cysl':1,
                                         # 'ShareHDNum_ratio':1,
                                         # 'cgsz':1,
                                         # 'Vposition_ratio':1,
                                         # 'TabRate':1,
                                         # 'TabRate_ratio':1,
                                         # 'TabProRate':1,
                                         # 'TabProRate_ratio':1
                                         },
                                 )
                # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
                # print(sdf)
                # sdf = sdf.fillna(value=0)
                # sdf = sdf[['jglx','mc','cysl']].groupby(['mc','jglx']).sum().reset_index()
                # print(sdf)
                # if int(request.args['sort'][0]) == 1:
                #     sdf = sdf.sort_values(by='cysl', ascending=1)
                # else:
                #     sdf = sdf.sort_values(by='cysl', ascending=0)
                #
                # start = (int(request.args['page'][0])-1)*int(request.args['size'][0])
                # end = start + int(request.args['size'][0])
                # count_num=len(sdf)
                # sdf = sdf[start:end]
                # print(sdf)
                # codes = list(sdf['code'].drop_duplicates())

                sdf = sdf.fillna(value=0)
                data = sdf.to_dict('recodes')



            except Exception as e:
                data = {"state": -1, "message": str(e)}

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


@financial.route('/allfunds/bk', methods=['POST', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('全机构数据板块详情')
@doc.description('汇总全机构板块详情')
async def get_allfund_bk(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(request.args)
                import json
                _json = json.loads(str(request.body, "utf-8"))
                # print(json.loads(str(request.body,"utf-8"))['mc'])
                sdf = read_mongo(db="stock_data",
                                 collection="dfcf_ajax_data",
                                 # collection="dfcf_jjcc_data",
                                 query={'mc': _json['mc']},
                                 select={'_id': 0,
                                         'code': 1,
                                         'cgsz': 1,
                                         'date': 1},
                                 )
                # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
                # print(sdf)
                # sdf = sdf.fillna(value=0)
                # sdf = sdf[['jglx','mc','cysl']].groupby(['mc','jglx']).sum().reset_index()
                # print(sdf)
                # if int(request.args['sort'][0]) == 1:
                #     sdf = sdf.sort_values(by='cysl', ascending=1)
                # else:
                #     sdf = sdf.sort_values(by='cysl', ascending=0)
                #
                # start = (int(request.args['page'][0])-1)*int(request.args['size'][0])
                # end = start + int(request.args['size'][0])
                # count_num=len(sdf)
                # sdf = sdf[start:end]
                # print(sdf)
                codes = list(sdf['code'].drop_duplicates())
                dates = list(sdf['date'].drop_duplicates())

                usecodes = " ( " + "".join([" code = " + c + " or " for c in ["'" + i + "'" for i in codes]])[
                                   :-3] + " ) "
                # print(usecodes)
                fdata = es_sql_df(
                    sql=f"SELECT code,plate_name FROM stock_plate where {usecodes} and plate_type = 'INDUSTRY' ")
                data = []
                for d in dates:
                    try:
                        ndf = pd.merge(sdf.loc[sdf['date'] == d,], fdata, on='code', how='right')
                        ndf = ndf.dropna(how='any')
                        _sum = sum(ndf['cgsz'])
                        # ndf['cgsz'] = conduct_dataframe(ndf,"cgsz",lambda _s : _s/_sum)
                        # print(ndf)
                        rdf = pd.pivot_table(ndf,
                                             index=['date'],
                                             columns=['plate_name'],
                                             values='cgsz',
                                             aggfunc=sum).reset_index()

                        result = rdf.to_dict('recodes')
                        onedata = {"date": result[0]['date']}
                        onedata['bk'] = list(result[0].keys())[1:]
                        onedata['value'] = list(result[0].values())[1:]

                        data.append(onedata)
                    except:
                        pass

                    # data.append(rdf.to_dict('recodes'))
                fdata = es_sql_df(
                    sql=f"SELECT code,plate_name FROM stock_plate where {usecodes} and plate_type = 'CONCEPT' ")
                data1 = []
                for d in dates:
                    try:
                        ndf = pd.merge(sdf.loc[sdf['date'] == d,], fdata, on='code', how='right')
                        ndf = ndf.dropna(how='any')
                        _sum = sum(ndf['cgsz'])
                        # ndf['cgsz'] = conduct_dataframe(ndf,"cgsz",lambda _s : _s/_sum)
                        # print(ndf)
                        rdf = pd.pivot_table(ndf,
                                             index=['date'],
                                             columns=['plate_name'],
                                             values='cgsz',
                                             aggfunc=sum).reset_index()

                        result = rdf.to_dict('recodes')
                        onedata = {"date": result[0]['date']}
                        onedata['bk'] = list(result[0].keys())[1:]
                        onedata['value'] = list(result[0].values())[1:]

                        data1.append(onedata)
                    except:
                        pass

                # print(len(sdf))
                # print(ndf)
                # print(len(ndf))

                # sdf = sdf.fillna(value=0)
                # rdf = pd.pivot_table(ndf,index=['date'],
                #                columns=['plate_name'],
                #                values='cgsz',
                #                aggfunc=lambda x : x/sum(x))
                # print(rdf)
                # data = sdf.to_dict('recodes')



            except Exception as e:
                data = {"state": -1, "message": str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "count": len(data),
         "data": data,
         "data_CONCEPT": data1
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )


@financial.route('/allfunds/code', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股票数据板块详情')
@doc.description('汇总股票详情')
async def get_allfund_code(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(request.args)
                import json
                # _json=json.loads(str(request.body,"utf-8"))
                # print(json.loads(str(request.body,"utf-8"))['mc'])
                sdf = read_mongo(db="stock_data",
                                 collection="dfcf_ajax_data",
                                 # collection="dfcf_jjcc_data",
                                 query={'code': request.args['code'][0],
                                        'date': request.args['date'][0]},
                                 select={'_id': 0,
                                         'SCode': 0,
                                         'SName': 0,
                                         'RDate': 0,
                                         'SHCode': 0,
                                         'SHName': 0,
                                         'InstSName': 0,
                                         'InstCode': 0,
                                         },
                                 )
                # sdf['jdgjdiffrate'] = conduct_mul_dataframe(sdf,lambda _u,_d:_u/_d,sdf['jdgjdiff'],sdf['sjgj'])
                # print(sdf)
                # sdf = sdf.fillna(value=0)
                # sdf = sdf[['jglx','mc','cysl']].groupby(['mc','jglx']).sum().reset_index()
                # print(sdf)
                # if int(request.args['sort'][0]) == 1:
                #     sdf = sdf.sort_values(by='cysl', ascending=1)
                # else:
                #     sdf = sdf.sort_values(by='cysl', ascending=0)
                #
                # start = (int(request.args['page'][0])-1)*int(request.args['size'][0])
                # end = start + int(request.args['size'][0])
                # count_num=len(sdf)
                # sdf = sdf[start:end]
                # print(sdf)

                # data.append(rdf.to_dict('recodes'))

                # print(len(sdf))
                # print(ndf)
                # print(len(ndf))
                # print(sdf)
                sdf = sdf.fillna(value=0)

                # rdf = pd.pivot_table(ndf,index=['date'],
                #                columns=['plate_name'],
                #                values='cgsz',
                #                aggfunc=lambda x : x/sum(x))
                # print(rdf)
                data = sdf.to_dict('recodes')



            except Exception as e:
                data = {"state": -1, "message": str(e)}

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


@financial.route('/allfunds/income', methods=['POST', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('全机构income详情')
@doc.description('全机构income详情')
async def get_allfund_income(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                # print(request.args)
                import json
                _json = json.loads(str(request.body, "utf-8"))
                # print(json.loads(str(request.body,"utf-8"))['mc'])
                sdf = read_mongo(db="stock_data",
                                 collection="dfcf_jj_ratio_data",
                                 # collection="dfcf_jjcc_data",
                                 query={'name': _json['mc']},
                                 select={'_id': 0,
                                         'year': 1,
                                         'jd': 1,
                                         'ratio': 1
                                         },
                                 )
                sdf = sdf.fillna(value=0)
                sdf = sdf.replace("Q1", "-03-31")
                sdf = sdf.replace("Q2", "-06-30")
                sdf = sdf.replace("Q3", "-09-30")
                sdf = sdf.replace("Q4", "-12-31")
                sdf['date'] = conduct_mul_dataframe(sdf, lambda _year, _jd: str(int(_year)) + str(_jd), sdf['year'],
                                                    sdf['jd'])
                del sdf['year']
                del sdf['jd']
                data = sdf.to_dict('recodes')

                # print(len(sdf))
                # print(ndf)
                # print(len(ndf))

                # sdf = sdf.fillna(value=0)
                # rdf = pd.pivot_table(ndf,index=['date'],
                #                columns=['plate_name'],
                #                values='cgsz',
                #                aggfunc=lambda x : x/sum(x))
                # print(rdf)
                # data = sdf.to_dict('recodes')



            except Exception as e:
                data = {"state": -1, "message": str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "count": len(data),
         "data": data,
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )


@financial.route('/code/allfunds', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股票下全机构持仓')
@doc.description('查询某股票全机构持仓情况')
async def get_code_allfunds(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:

                sdf = read_mongo(db="stock_data",
                                 collection="dfcf_ajax_data",
                                 # collection="dfcf_jjcc_data",
                                 query={'code': request.args['code'][0],
                                        'TabRate': {
                                            '$gt': float(request.args['rate'][0])
                                        }
                                        },
                                 limitNum=1300,
                                 select={'_id': 0,
                                         # 'year': 1,
                                         # 'jd': 1,
                                         # 'ratio': 1
                                         },
                                 )
                # print(sdf)
                sdf = sdf.fillna(value=0)

                data = sdf.to_dict('recodes')

                # print(len(sdf))
                # print(ndf)
                # print(len(ndf))

                # sdf = sdf.fillna(value=0)
                # rdf = pd.pivot_table(ndf,index=['date'],
                #                columns=['plate_name'],
                #                values='cgsz',
                #                aggfunc=lambda x : x/sum(x))
                # print(rdf)
                # data = sdf.to_dict('recodes')



            except Exception as e:
                data = {"state": -1, "message": str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "count": len(data),
         "data": data,
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )


@financial.route('/code/analysis', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('股票下板块和财报分析')
@doc.description('股票下板块和财报分析')
async def get_code_analysis(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                market = request.args['code'][0][:2]
                if market == 'HK':
                    InfoSource = 'FY'
                else:
                    InfoSource = 'Q'
                sdf = read_mongo(db="stock_data",
                                 collection="finance_KR",
                                 # collection="dfcf_jjcc_data",
                                 query={'code': request.args['code'][0],
                                        'market': market,  # request.args['market'][0],
                                        'InfoSource': InfoSource,
                                        # 'TabProRate': {
                                        #        '$gt': float(request.args['rate'][0])
                                        #    }
                                        },
                                 select={'_id': 0,
                                         # 'year': 1,
                                         # 'jd': 1,
                                         # 'ratio': 1
                                         },
                                 )
                sdf = sdf.fillna(value=0)

                data = sdf.to_dict('recodes')
                # print(data)

                # print(len(sdf))
                # print(ndf)
                # print(len(ndf))

                # sdf = sdf.fillna(value=0)
                # rdf = pd.pivot_table(ndf,index=['date'],
                #                columns=['plate_name'],
                #                values='cgsz',
                #                aggfunc=lambda x : x/sum(x))
                # print(rdf)
                # data = sdf.to_dict('recodes')

                # 查询股票板块
                usecode = "'" + request.args['code'][0] + "'"
                # print(usecode)
                fdf = es_sql_df(
                    sql=f"SELECT plate_name FROM stock_plate where code = {usecode} ")
                # print(fdf)
                bklist = list(set(list(fdf['plate_name'])))
                # data_bk = fdf.to_dict('recodes')

                fdata = read_mongo(db="stock_data",
                                   collection="finance_KR",
                                   query={'market': market
                                          },
                                   select={'_id': 0,
                                           #                            'code': 1,
                                           #                            'cgsz': 1,
                                           #                            'date': 1
                                           },

                                   )
                adf = fdata.dropna(how='any')
                vdf = adf.describe(percentiles=[.10, .20, .30, .40, .50, .60, .70, .80, .90]).reset_index()[4:13]
                # print(vdf)
                # print(list(vdf.columns))
                GPA = {}
                for n in list(vdf.columns)[1:]:
                    vdata = list(vdf[n])
                    for num in list(range(8, -1, -1)):
                        if float(sdf[n][0]) >= float(vdata[num]):
                            pass
                            #             print(list(vdf['index'])[num])
                            GPA[n] = list(vdf['index'])[num]
                            break
                        # else:
                        #     print(1)
                # print(GPA)








            except Exception as e:
                data = {"state": -1, "message": str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "count": len(data),
         "data": data,
         "bk": bklist,
         "GPA": GPA,
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )


@financial.route('/bk/analysis', methods=['GET', 'OPTIONS'])
# @cross_origin(financial)
@doc.summary('按所选板块或全部数据按关键字段排序')
@doc.description('')
async def get_bk_analysis(request):
    with Timer() as timer:
        with Timer() as timer_es:
            try:
                usesubtype = "'" + request.args['subtype'][0] + "'"
                usemarket = "'" + request.args['market'][0] + "'"
                if request.args['subtype'][0] != "all":
                    data = es_sql_df(
                        sql=f"SELECT code,code_name FROM stock_plate where plate_code = {usesubtype} and category = {usemarket} ")
                    codes = list(data['code'])
                else:
                    # data = es_sql_df(
                    #     sql=f"SELECT code,code_name FROM stock_plate where category = {usemarket} ")
                    # codes = list(data['code'])
                    codes = []

                # print(codes)
                if request.args['market'][0][:2] == "HK":
                    InfoSource = 'FY'
                else:
                    InfoSource = 'Q'

                if len(codes) == 0:
                    query_result = {  # '$or': [{'code': c} for c in codes],
                        'market': request.args['market'][0],
                        'ST': 0,
                        'InfoSource': InfoSource,
                        'bar': {'$gt': 10},
                        request.args['field'][0]: {'$gt': 0},
                        'OperatingProfit': {'$gt': 0},
                    }
                else:
                    query_result = {'$or': [{'code': c} for c in codes],
                                    'market': request.args['market'][0],
                                    'ST': 0,
                                    'InfoSource': InfoSource,
                                    'bar': {'$gt': 10},
                                    request.args['field'][0]: {'$gt': 0},
                                    'OperatingProfit': {'$gt': 0},
                                    }

                sdf = read_mongo(db="stock_data",
                                 collection="finance_KR",
                                 # collection="dfcf_jjcc_data",
                                 query=query_result,
                                 sortby=request.args['field'][0],
                                 limitNum=10,
                                 upAndDown=-1,
                                 select={'_id': 0,
                                         'InfoSource': 0,
                                         'ST': 0,
                                         'market': 0,
                                         'bar': 0,
                                         'ST': 0,

                                         # 'year': 1,
                                         # 'jd': 1,
                                         # 'ratio': 1
                                         },
                                 )
                sdf = sdf.replace([np.inf, -np.inf], np.nan)
                sdf.dropna(how='any')
                sdf = sdf.fillna(value=0)
                sdf = sdf.loc[sdf[request.args['field'][0]] != 0]

                # print(sdf)

                data = sdf.to_dict('recodes')

                # print(len(sdf))
                # print(ndf)
                # print(len(ndf))

                # sdf = sdf.fillna(value=0)
                # rdf = pd.pivot_table(ndf,index=['date'],
                #                columns=['plate_name'],
                #                values='cgsz',
                #                aggfunc=lambda x : x/sum(x))
                # print(rdf)
                # data = sdf.to_dict('recodes')

                # # 查询股票板块
                # usecode = "'" + request.args['code'][0] + "'"
                # # print(usecode)
                # fdf = es_sql_df(
                #     sql=f"SELECT plate_name FROM stock_plate where code = {usecode} ")
                # # print(fdf)
                # bklist = list(set(list(fdf['plate_name'])))
                # # data_bk = fdf.to_dict('recodes')





            except Exception as e:
                data = {"state": -1, "message": str(e)}

    return response.json(
        {"create_time": pendulum.now().format('YYYY-MM-DD HH:mm:ss'),
         "use_time": f"{timer.cost:.2f}",
         "use_time_es": f"{timer_es.cost:.2f}",
         "count": len(data),
         "data": data,
         # "bk": bklist
         },
        headers={'X-Served-By': 'sanic', "Access-Control-Allow-Origin": "*"},
        status=200
    )
