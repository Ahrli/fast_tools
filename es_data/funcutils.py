#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random

import requests
from lxml import etree
import arrow

from redis import StrictRedis, ConnectionPool
from retrying import retry

import requests
import json
# http代理接入服务器地址端口
from sqlalchemy import create_engine

proxyHost = "http-proxy-t3.dobel.cn"
proxyPort = "9180"
# 账号密码
proxyUser = "QIHESHANGWU0BDEQK3L023423"
proxyPass = "FKjJvy34"
proxyMeta = f"http://{proxyUser}:{proxyPass}@{proxyHost}:{proxyPort}"
proxies = {
"http": proxyMeta,
"https": proxyMeta,
}


import logging
class LOG():
    @staticmethod
    def get_logger():
        # 第一步，创建一个logger
        logger = logging.getLogger()
        logger.setLevel(logging.INFO) # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        logfile = f"./{arrow.now().format('YYYY-MM-DDHH:mm:ss')}.txt"
        fh = logging.FileHandler(logfile, mode='a') # open的打开模式这里可以进行参考
        fh.setLevel(logging.DEBUG) # 输出到file的log等级的开关
        # 第三步，再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.WARNING) # 输出到console的log等级的开关
        # 第四步，定义handler的输出格式
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # 第五步，将logger添加到handler里面
        logger.addHandler(fh)
        logger.addHandler(ch)

        # logger.critical()
        # logger.error()
        # logger.warning()
        # logger.info()
        # logger.debug()

        return logger

def serialize(hit):
        # fields = hit["fields"]
        #
        # for k in fields:
        #     fields[k] = fields[k][0]
        fields=[]
        for k in hit:
            fields.append(k['_source'])
        return fields
# cd /dags/tyre && /root/anaconda3/bin/python3  jybd_main.py
def w_ods(df, db, table, if_exists):
    '''
    '''

    engine = create_engine(
        #         f'mysql+pymysql://root:LOOP2themoon@rm-uf6rozhp0o3za68tt.mysql.rds.aliyuncs.com:3306/loop_coin?charset=utf8'
        #         f'mysql+pymysql://zhangyulei:VXjh79q7QXeunQLc@rm-wz93i2t71vgjuuj33.mysql.rds.aliyuncs.com:3306/?charset=utf8'
        f"mysql+pymysql://hqp_haitao:hqp_haitao@123@172.16.9.232:3306/{db}?charset=utf8"
    )

    df.to_sql(table, engine, if_exists=if_exists)