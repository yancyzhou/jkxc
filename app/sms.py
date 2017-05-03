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
        code = self.generate_verification_code_v2()
        single_sender = SmsSender.SmsSingleSender(appid, appkey)
        params = [code, "3"]
        result = single_sender.send_with_param("86", self.phoneNumber, templ_id, params, "", "", "")
        rsp = json.loads(result)
        self.writejson(json_decode(str(ApiHTTPError(**rsp))))



    def generate_verification_code_v2(self):
        import random
        ''' 随机生成6位的验证码 '''
        code_list = []
        for i in range(2):
            random_num = random.randint(0, 9) # 随机生成0-9的数字
            # 利用random.randint()函数生成一个随机整数a，使得65<=a<=90
            # 对应从“A”到“Z”的ASCII码
            a = random.randint(65, 90)
            b = random.randint(97, 122)
            random_uppercase_letter = chr(a)
            random_lowercase_letter = chr(b)
            code_list.append(str(random_num))
            code_list.append(random_uppercase_letter)
            code_list.append(random_lowercase_letter)
        verification_code = ''.join(code_list)
        return verification_code