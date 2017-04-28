#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
======================
@version: 1.0
@author: vincentzhou
@contact: python@vip.126.com
@site: http://analytics.septnet.cn
@software: PyCharm
@file: pay.py
@time: 2017/4/28 11:32
======================
"""
from Handler import BaseHandler, ApiHTTPError
from tornado import gen
from tornado.escape import json_decode
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
import urllib, urllib2, requests, random, hashlib, sys


class SetOrder(BaseHandler):
    def XmlData(self,id):
        appidvalue = "填写自己的appid"  # appid
        attachvalue = "PayTest"
        mch_idvalue = "填写自己的mchid"  # mch_id
        nonce_strvalue = self.GetRandomStr
        bodyvalue = "NATIVETest"
        out_trade_novalue = id
        total_feevalue = "998"  # 价格
        spbill_create_ipvalue = "192.168.1.3"
        notify_urlvalue = "http://www.baidu.com"  # 用户回调URL地址
        trade_typevalue = "NATIVE"
        product_idvalue = "12235413214070356458058"
        key = "填写自己的校验key"  # 用户配置

        formatstr = 'appid=%s&attach=%s&body=%s&mch_id=%s&nonce_str=%s&notify_url=%s&out_trade_no=%s&product_id=%s' \
                    '&spbill_create_ip=%s&total_fee=%s&trade_type=%s&key=%s' % (
                    appidvalue, attachvalue, bodyvalue, mch_idvalue, nonce_strvalue, \
                    notify_urlvalue, out_trade_novalue, product_idvalue, spbill_create_ipvalue, total_feevalue,
                    trade_typevalue, key)

        print formatstr
        mobj = hashlib.md5()
        mobj.update(formatstr)
        signvalue = mobj.hexdigest()
        signvalue = signvalue.upper()
        print signvalue

        xmlstart = "<xml>\r\n"
        appid = "<appid>" + appidvalue + "</appid>\r\n"
        attach = "<attach>" + attachvalue + "</attach>\r\n"
        mch_id = "<mch_id>" + mch_idvalue + "</mch_id>\r\n"
        nonce_str = "<nonce_str>" + nonce_strvalue + "</nonce_str>\r\n"
        body = "<body>" + bodyvalue + "</body>\r\n"
        out_trade_no = "<out_trade_no>" + out_trade_novalue + "</out_trade_no>\r\n"
        total_fee = "<total_fee>" + total_feevalue + "</total_fee>\r\n"
        spbill_create_ip = "<spbill_create_ip>" + spbill_create_ipvalue + "</spbill_create_ip>\r\n"
        notify_url = "<notify_url>" + notify_urlvalue + "</notify_url>\r\n"
        trade_type = "<trade_type>" + trade_typevalue + "</trade_type>\r\n"
        product_id = "<product_id>" + product_idvalue + "</product_id>\r\n"
        sign = "<sign>" + signvalue + "</sign>\r\n"
        xmlend = "</xml>"
        result = xmlstart + appid + attach + mch_id + nonce_str + body + out_trade_no + total_fee + spbill_create_ip + notify_url + trade_type + product_id + sign + xmlend
        print result
        return result


    def Post(self,data):
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        headers = {"Content-Type": "text/xml"}
        rep = urllib2.Request(url=url, headers=headers, data=data)
        response = urllib2.urlopen(rep)
        res = response.read()
        return res


    def post(self, *args, **kwargs):
        type = sys.getfilesystemencoding()
        result = self.Post(self.XmlData("123511654189415"))
        print result.decode('utf-8').encode(type)