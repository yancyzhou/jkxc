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
import urllib2, random, hashlib, sys


class SetOrder(BaseHandler):
    def set_md5(self,string):
        mobj = hashlib.md5()
        mobj.update(string)
        signvalue = mobj.hexdigest()
        signvalue = signvalue.upper()
        return signvalue

    def XmlData(self):
        openidvalue = self.openid
        appidvalue = self.AppID  # appid
        attachvalue = self.attachvalue
        mch_idvalue = "1467218302"  # mch_id
        nonce_strvalue = self.GetRandomStr
        bodyvalue = "NATIVE"
        out_trade_novalue = self.id
        total_feevalue = self.total_fee  # 价格
        spbill_create_ipvalue = "120.210.166.7"
        notify_urlvalue = "https://jk.jikexueche.com"  # 用户回调URL地址
        trade_typevalue = "JSAPI"
        key = self.key  # 用户配置

        formatstr = 'appid=%s&attach=%s&body=%s&mch_id=%s&nonce_str=%s&notify_url=%s&openid=%s&out_trade_no=%s&spbill_create_ip=%s&total_fee=%s&trade_type=%s&key=%s' % (
                    appidvalue, attachvalue,bodyvalue,mch_idvalue,nonce_strvalue,notify_urlvalue,openidvalue,out_trade_novalue, spbill_create_ipvalue, total_feevalue,
                    trade_typevalue, key)

        signvalue = self.set_md5(formatstr)

        xmlstart = "<xml>\r\n"
        appid = "<appid>" + appidvalue + "</appid>\r\n"
        attach = "<attach>" + attachvalue + "</attach>\r\n"
        mch_id = "<mch_id>" + mch_idvalue + "</mch_id>\r\n"
        openid = "<openid>" + openidvalue + "</openid>\r\n"
        nonce_str = "<nonce_str>" + nonce_strvalue + "</nonce_str>\r\n"
        body = "<body>" + bodyvalue + "</body>\r\n"
        out_trade_no = "<out_trade_no>" + out_trade_novalue + "</out_trade_no>\r\n"
        total_fee = "<total_fee>" + total_feevalue + "</total_fee>\r\n"
        spbill_create_ip = "<spbill_create_ip>" + spbill_create_ipvalue + "</spbill_create_ip>\r\n"
        notify_url = "<notify_url>" + notify_urlvalue + "</notify_url>\r\n"
        trade_type = "<trade_type>" + trade_typevalue + "</trade_type>\r\n"
        sign = "<sign>" + signvalue + "</sign>\r\n"
        xmlend = "</xml>"

        result = xmlstart + appid + attach+body+mch_id+nonce_str+notify_url+openid+out_trade_no+spbill_create_ip+total_fee+trade_type+sign+ xmlend
        return result


    def Posts(self,data):
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        headers = {"Content-Type": "text/xml"}
        rep = urllib2.Request(url=url, headers=headers, data=data)
        response = urllib2.urlopen(rep)
        res = response.read()
        return res


    def post(self, *args, **kwargs):
        try:
            import xml.etree.cElementTree as ET
        except ImportError:
            import xml.etree.ElementTree as ET
        import time
        type = sys.getfilesystemencoding()
        self.AppID = "wxad81631247e48b3e"
        self.id  = "JIKEXUECHE"+str(time.time()).replace(".","")+str(random.randint(10,100))
        self.attachvalue = "JKXC"
        self.total_fee = "1"
        self.openid = "orIf80Cg6Lp8jk7iR55x6GH-5Z5A"
        self.key = "jike712YMiinoo736Rexhu1217Nan909"
        result = self.Posts(self.XmlData())
        response =  result.decode('utf-8').encode(type)
        print response
        xml2obj = {}
        root = ET.fromstring(response)
        for child_list in root.findall("*"):
            xml2obj[child_list.tag]=child_list.text
        timestramp = str(time.time()).replace(".","")
        signstr = "appId=%s&nonceStr=%s&package=prepay_id=%s&signType=MD5&timeStamp=%s&key=%s" % (self.AppID,xml2obj['nonce_str'],xml2obj['prepay_id'],timestramp,self.key)
        print signstr
        secondsign = self.set_md5(signstr)
        print secondsign
        rep = {}
        rep['data'] = {"paysign":secondsign,"out_trade_no":self.id,"prepayid":xml2obj['prepay_id'],"nonceStr":xml2obj['nonce_str'],"timestramp":timestramp}
        self.writejson(json_decode(str(ApiHTTPError(**rep))))