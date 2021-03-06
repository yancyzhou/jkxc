# -*- coding:utf-8 -*-
'''
======================
@author Vincent
======================
'''
from __future__ import division
from tornado import gen, httpclient
from Handler import BaseHandler, ApiHTTPError
from tornado.escape import json_decode
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
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
    execute = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.code = self.get_json_argument("code", None)
        self.appId = 'wxad81631247e48b3e'
        client = httpclient.AsyncHTTPClient()
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=%s&secret=%s&js_code=%s&grant_type=authorization_code" % (
            self.appId, 'fd82d4c64dbfead96192e31df1146741', self.code)
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


class getstudent(BaseHandler):

    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.studentcode = self.get_json_argument("studentcode", None)
        res = yield self.getdata()
        rep = {}
        rep['data'] = res
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):

        res = self.DbRead.query(self.Student.student_id).filter(self.Student.student_code ==
                                                                self.studentcode, self.Student.student_packageuid == self.Package.package_id).first()

        if res is not None:
            result = 1
        else:
            result = 0
        self.DbRead.commit()
        self.DbRead.close()
        return result


class getstudent_state(BaseHandler):

    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.studentcode = self.get_json_argument("studentcode", None)
        res = yield self.getdata()
        rep = {}
        rep['data'] = res
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):

        res = self.DbRead.query(self.Student.student_code, self.Student.student_state).filter(
            self.Student.student_code == self.studentcode).first()

        if res is not None:
            result = {'student_state': res.student_state}
        else:
            result = {'student_state': -1}
        self.DbRead.commit()
        self.DbRead.close()
        return result
