# -*- coding:utf-8 -*-
import tornado.web
import jwt
import datetime
import hashlib
from Handler import BaseHandler, ApiHTTPError
from tornado import gen
from tornado.escape import json_decode
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor

SECRET = 'my_secret_key'

'''
登录成功生成token
'''


class AuthHandler(BaseHandler):
    executor = ThreadPoolExecutor(8)
    def _set_token(self):
        self.encodeds = jwt.encode({
            'relate_info': 1,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)},
            SECRET,
            algorithm='HS256')

    @run_on_executor
    def _get_db_user_resource(self):
        resource = self.DbRead.query(self.Staff).filter(self.Staff.staff_code == self.username).first()
        self.DbRead.close()
        if resource:
            pass
        else:
            self.writejson(json_decode(str(ApiHTTPError(20200))))
            return False
        self.is_admin = 1
        self.name = resource.staff_name
        self.id = str(resource.staff_id)
        MD5_key = hashlib.md5()
        MD5_key.update(self.passwd)
        inputpasswrod = MD5_key.hexdigest()
        if inputpasswrod.upper() == resource.RU_User_md5Key:
            self._set_token()
            response = {'data': {"token":self.encodeds,"user":{'usercode':self.username,'username': self.name, 'user_id': self.id,'is_admin':self.is_admin}}}
        else:
            self.writejson(json_decode(str(ApiHTTPError(20002))))
            return False
        return response

    @gen.coroutine
    def post(self):
        self.username = self.get_json_argument("username")
        self.passwd = self.get_json_argument('password')
        response = yield self._get_db_user_resource()
        if response:
            self.writejson(json_decode(str(ApiHTTPError(**response))))