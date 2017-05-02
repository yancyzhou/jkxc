# -*- coding:utf-8 -*-
'''
======================
@author Vincent
======================
'''
from __future__ import division
from tornado import gen,escape
from datetime import datetime,timedelta
from Handler import BaseHandler,ApiHTTPError
from auth import jwtauth
from tornado.escape import json_decode,json_encode
from sqlalchemy import func, extract, distinct
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from model.models import *
import requests
import json


class PackageIndex(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.schoolid = self.get_json_argument('schoolid', None)
        reps = yield self.getdata()
        rep = {}
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(
            self.Package.package_id, self.Package.package_name, self.Package.package_money).filter(
            self.Package.package_state == 1,
            self.Package.package_schooluid == self.schoolid,).all()
        rep = {}
        for res in result:
            rep[res[0]] = {"package_name":res[1], "package_money":res[2]}
        return rep

import base64
import json
from Crypto.Cipher import AES


class WXBizDataCrypt:

    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decryptData(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

class GetUserinfo(BaseHandler):

class PackageDetail(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.schoolid = self.get_json_argument('schoolid', None)
        self.packageid = self.get_json_argument('packageid', None)
        reps = yield self.getdata()
        rep = {}
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(
            self.Package.package_describe).filter(
            self.Package.package_state == 1,
            self.Package.package_schooluid == self.schoolid,
            self.Package.package_id == self.packageid).all()
        rep = {self.packageid: result[0]}
        return rep
        self.daterange = self.get_json_argument('StartDate',[])
        self.province = self.get_json_argument('province', None)
        if len(self.daterange)==0:
            self.startdate = (datetime.now()-timedelta(days=30)).strftime("%Y-%m-%d")
            self.enddate = datetime.now().strftime("%Y-%m-%d")
        else:
            self.startdate = self.daterange[0][:10]
            self.enddate = self.daterange[1][:10]
        self.substrlength = 4 if self.province and self.province!='all' else 2
        rep = yield self.getdata()
        province = []
        total = []
        if len(rep['data']) > 0:
            rep['data'] = sorted(rep['data'], key=lambda x:x['total'])
            for item in rep['data']:
                if self.substrlength == 2:
                    try:
                        province_tmp = self.provinces[item['provinces']]
                    except KeyError as e:
                        province_tmp = "未知"
                else:
                    if item['provinces'][:2] in self.city:
                        province_tmp = self.city[item['provinces'][:2]]
                    else:
                        if item['provinces'] not in self.citylist.keys():
                            province_tmp = "联考"
                        else:
                            try:
                                province_tmp = self.citylist[item['provinces']]
                            except KeyError as e:
                                province_tmp = "未知"
                province.append(province_tmp)
                total.append(item['total'])
            rep['data'] = {}
            rep['data']['provinces'] = province
            rep['data']['total'] = sum(total)
            rep['data']['count'] = total
            self.writejson(json_decode(str(ApiHTTPError(**rep))))
        else:
            rep['data'] = {}
            rep['data']['provinces'] = province
            rep['data']['total'] = sum(total)
            rep['data']['count'] = total
            self.writejson(json_decode(str(ApiHTTPError(**rep))))
        self.code = self.get_json_argument("code",None)
        self.appId = 'wxad81631247e48b3e'
        client = httpclient.AsyncHTTPClient()
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" %(self.appId,'fd82d4c64dbfead96192e31df1146741',self.code)
        response = yield client.fetch(url)

        # result = yield self.getdata()

        result = json_decode(response.body)
        result.pop("session_key")
        rep = {}
        rep['data'] = result
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):

        sessionKey = 'tiihtNczf5v6AKRyjwEUhQ=='
        encryptedData = 'CiyLU1Aw2KjvrjMdj8YKliAjtP4gsMZMQmRzooG2xrDcvSnxIMXFufNstNGTyaGS9uT5geRa0W4oTOb1WT7fJlAC+oNPdbB+3hVbJSRgv+4lGOETKUQz6OYStslQ142dNCuabNPGBzlooOmB231qMM85d2/fV6ChevvXvQP8Hkue1poOFtnEtpyxVLW1zAo6/1Xx1COxFvrc2d7UL/lmHInNlxuacJXwu0fjpXfz/YqYzBIBzD6WUfTIF9GRHpOn/Hz7saL8xz+W//FRAUid1OksQaQx4CMs8LOddcQhULW4ucetDf96JcR3g0gfRK4PC7E/r7Z6xNrXd2UIeorGj5Ef7b1pJAYB6Y5anaHqZ9J6nKEBvB4DnNLIVWSgARns/8wR2SiRS7MNACwTyrGvt9ts8p12PKFdlqYTopNHR1Vf7XjfhQlVsAJdNiKdYmYVoKlaRv85IfVunYzO0IKXsyl7JCUjCpoG20f0a04COwfneQAGGwd5oa+T8yO5hzuyDb/XcxxmK01EpqOyuxINew=='
        iv = 'r7BXXKkLb8qrSNn05n0qiA=='

        pc = WXBizDataCrypt(self.appId, sessionKey)

        rep = pc.decryptData(encryptedData, iv)
        return rep


