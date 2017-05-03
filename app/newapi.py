# -*- coding:utf-8 -*-
'''
======================
@author Vincent
======================
'''
from __future__ import division
from tornado import gen, escape, httpclient
from datetime import datetime,timedelta
from Handler import BaseHandler,ApiHTTPError
from auth import jwtauth
from tornado.escape import json_decode,json_encode
from sqlalchemy import func, extract, distinct
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from model.models import *
import requests,base64,json
from crypto import Cipher


#套餐列表
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


#套餐详情
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


#学员学习记录
class StudentExamList(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.studentid = self.get_json_argument('studentid', None)
        reps = yield self.getdata()
        rep = {}
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(
             self.Courses.courses_id, self.Courses.courses_starttime, self.Courses.courses_endtime).filter(
            self.Student_courses.sc_studentuid == self.studentid,
            self.Student_courses.sc_coursesuid == self.Courses.courses_id).all()
        rep = {}
        for res in result:
            rep[res[0]] = {"starttime":str(res[1]), "endtime":str(res[2])}
        return rep


#学员报名列表
class StudentExamindex(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.studentid = self.get_json_argument('studentid', None)
        reps = yield self.getdata()
        rep = {}
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(
             self.Courses.courses_id, self.Courses.courses_starttime, self.Courses.courses_endtime).filter(
            self.Student.student_id == self.studentid,
            # self.Courses.courses_state == 1,
            self.Student.student_traineruid == self.Courses.courses_traineruid).all()
        rep = {}
        for res in result:
            rep[res[0]] = {"starttime":str(res[1]), "endtime":str(res[2])}
        return rep
