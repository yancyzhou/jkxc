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

#驾校套餐列表
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


#某一套餐详情
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


#学员历史学习记录
class StudentExamList(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        import time
        self.studentid = self.get_json_argument('studentid', None)
        reps = yield self.getdata()
        for item in reps:
            status = 0
            for items in item['Periodoftime']:
                selecttimeitem = item['day']+" "+items.split("~")[1]+":00"
                if time.strptime(selecttimeitem, '%Y-%m-%d %H:%M:%S')<time.localtime(time.time()):
                    status = 1
            item['status'] = status
            item['Periodoftime'] = ",".join(item['Periodoftime'])
        rep = {}
        reps = sorted(reps, key=lambda student: student['day'],reverse=True)
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(
             self.Courses.courses_id, self.Courses.courses_starttime, self.Courses.courses_endtime,self.Student_courses.sc_createtime).filter(
            self.Student_courses.sc_studentuid == self.studentid,
            self.Student_courses.sc_coursesuid == self.Courses.courses_id).all()
        rep = {}
        courses_list = []
        for res in result:
            item = res.courses_starttime.strftime('%H:%M') + "~" + res.courses_endtime.strftime('%H:%M')

            datekey = res.courses_starttime.strftime('%Y-%m-%d')
            if datekey in rep.keys():
                rep[datekey].append(item)
            else:
                rep[datekey] = [item]
            item_dict = {"createtime":res.sc_createtime.strftime('%Y-%m-%d %H:%M:%S'),"day":datekey}
            if item_dict not in courses_list:
                courses_list.append(item_dict)
        for item in courses_list:
            item['Periodoftime'] = rep[item['day']]
        self.DbRead.commit()
        self.DbRead.close()
        return courses_list

#保存学车记录
class SaveStudentExam(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.Periodoftime = self.get_json_argument("Periodoftime",None)
        self.StudentOpenid = self.get_json_argument("StudentOpenid",None)
        for item in list(self.Periodoftime):
            studentCourses = self.Student_courses(sc_coursesuid=item,sc_studentuid= self.StudentOpenid)
            self.DbRead.add(studentCourses)
        self.DbRead.commit()
        print studentCourses.sc_id
        self.DbRead.close()
        rep = {}
        rep['data'] = self.Periodoftime
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

#学员可报名列表
class StudentExamindex(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.studentid = self.get_json_argument('studentid', None)
        self.day = self.get_json_argument('day', None)
        reps = yield self.getdata()
        rep = {}
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(self.Courses.courses_id,
             self.Courses.courses_state, self.Courses.courses_starttime, self.Courses.courses_endtime,self.Courses.courses_current_number).filter(
            self.Student.student_id == self.studentid,
            self.Student.student_state == self.Courses.courses_type,
            self.Courses.courses_starttime.like(self.day+"%"),
            self.Student.student_traineruid == self.Courses.courses_traineruid).order_by(self.Courses.courses_starttime).all()
        self.DbRead.commit()
        self.DbRead.close()
        rep = []
        for res in result:
            item = res.courses_starttime.strftime('%H:%M')+"~"+res.courses_endtime.strftime('%H:%M')
            disabled = False
            description = "预约中"
            if res.courses_state == 1:
                pass
            elif res.courses_state == 3:
                disabled = True
                description = "预约已满"
            elif res.courses_state ==2:
                disabled = True
                description = "已关闭"
            tmp = {"name":item,"CoursesId":res.courses_id,"checked":False,"count":res.courses_current_number,"disabled":disabled,"description":description}
            rep.append(tmp)
        return rep
