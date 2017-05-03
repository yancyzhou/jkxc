#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
======================
@version: 1.0
@author: vincentzhou
@contact: python@vip.126.com
@site: http://analytics.septnet.cn
@software: PyCharm
@file: sms.py
@time: 2017/5/2 18:40
======================
"""
from __future__ import division
from tornado import gen,escape,httpclient
from datetime import datetime,timedelta
from Handler import BaseHandler,ApiHTTPError
from auth import jwtauth
from tornado.escape import json_decode,json_encode
from sqlalchemy import func, extract, distinct
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from model.models import *
import json
import lib.Qcloud.Sms.sms as SmsSender


# 定义发送短信的类
class SmsSenders(BaseHandler):
    executor = ThreadPoolExecutor(8)
    sdkappid = 1400029906
    appkey = "f7c3511daa34e1db9a1973c9f4efad15"
    # 构造函数，把appid和appkey传入
    @gen.coroutine
    def post(self, *args, **kwargs):
        self.nationCode = "86"
        self.phoneNumber = self.get_json_argument("phoneNumber",None)
        appid = self.sdkappid
        appkey = self.appkey
        templ_id = 18108

        single_sender = SmsSender.SmsSingleSender(appid, appkey)
        params = ["5678", "3"]
        result = single_sender.send_with_param("86", self.phoneNumber, templ_id, params, "", "", "")
        rsp = json.loads(result)
        self.writejson(json_decode(str(ApiHTTPError(**rsp))))


