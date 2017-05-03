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
from Handler import BaseHandler,ApiHTTPError
from tornado.escape import json_decode,json_encode
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from sqlalchemy import func, extract, distinct
import json,random,time
from datetime import datetime
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
        code = self.generate_verification_code() #验证码
        exp_time = "3" #失效时间，单位为分钟
        single_sender = SmsSender.SmsSingleSender(appid, appkey)
        params = [code, exp_time]
        smlog_message = "您的验证码是%s，请于%s分钟内填写。如非本人操作，请忽略本短信。" % (code,exp_time)
        ext = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = single_sender.send_with_param("86", self.phoneNumber, templ_id, params, "", "", ext)
        rsp = json.loads(result)
        if rsp['result']!=0:
            pass
        else:
            smlog = self.SmLog(smlog_usercode=self.phoneNumber,smlog_message=smlog_message,smlog_createtime=rsp['ext'])
            self.DbRead.add(smlog)
            self.DbRead.commit()
            self.DbRead.close()
        result ={}
        result['data'] = {"data":rsp}
        self.writejson(json_decode(str(ApiHTTPError(**result))))

    def generate_verification_code(self,len=6):
        ''' 随机生成6位的验证码 '''
        code_list = []
        for i in range(10):  # 0-9数字
            code_list.append(str(i))
        myslice = random.sample(code_list, len)  # 从list中随机获取6个元素，作为一个片断返回
        verification_code = ''.join(myslice)  # list to string
        return verification_code


class ValidationCode(BaseHandler):

    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.code = self.get_json_argument("code",None)
        self.phoneNum = self.get_json_argument("phoneNum",None)
        expired_time = 3
        result = yield self.validationcode(expired_time)
        print result
        rep = {}
        rep['data'] = result
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def validationcode(self,expired_time):

        result = self.DbRead.query(self.SmLog)\
            .filter(self.SmLog.smlog_usercode==self.phoneNum,func.substr(self.SmLog.smlog_message,7,6)==self.code)\
            .order_by(self.SmLog.smlog_createtime.desc()).first()
        count = 0
        if result:
            for item in result:
                t1 = datetime.strptime(item.smlog_createtime, '%Y-%m-%d %H:%M:%S')
                t2 = datetime.now()
                if (t2-t1).seconds<=180:
                    count = 1
        return count

