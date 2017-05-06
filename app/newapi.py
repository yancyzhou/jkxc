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
        self.packageid = self.get_json_argument('packageid', None)
        reps = yield self.getdata()
        rep = {}
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(
            self.Package.package_describe, self.Package.package_detail).filter(
            self.Package.package_state == 1,
            self.Package.package_id == self.packageid).first()
        rep = {'package': result.package_describe, 'money':result.package_detail}
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
            selecttimeitem = item['day'] + " " + item['Periodoftime'].split("~")[1] + ":00"
            if time.strptime(selecttimeitem, '%Y-%m-%d %H:%M:%S') < time.localtime(time.time()):
                status = 1
            item['status'] = status
        rep = {}
        reps = sorted(reps, key=lambda student: student['day'], reverse=True)
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(
            self.Courses.courses_id, self.Courses.courses_starttime, self.Courses.courses_endtime,
            self.Student_courses.sc_createtime).filter(
            self.Student_courses.sc_studentuid == self.studentid,
            self.Student_courses.sc_coursesuid == self.Courses.courses_id).all()
        courses_list = []
        for res in result:
            item = res.courses_starttime.strftime('%H:%M') + "~" + res.courses_endtime.strftime('%H:%M')
            datekey = res.courses_starttime.strftime('%Y-%m-%d')
            item_dict = {"createtime": res.sc_createtime.strftime('%Y-%m-%d %H:%M:%S'), "day": datekey}
            item_dict['Periodoftime'] = item
            courses_list.append(item_dict)
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
        Periodoftime = self.Periodoftime.split("&")
        courses = self.DbRead.query(self.Courses.courses_current_number,self.Courses.courses_limit_number).filter(self.Courses.courses_id.in_(Periodoftime),self.Courses.courses_current_number<self.Courses.courses_limit_number).all()
        if len(courses) == len(Periodoftime):
            print courses[0]
            # for item in courses:
                # item.courses_current_number += 1
            self.DbRead.commit()
        # for items in Periodoftime:
        #     try:
        #         studentCourses = self.Student_courses(sc_coursesuid=items, sc_studentuid=self.StudentOpenid)
        #         self.DbRead.add(studentCourses)
        #         self.DbRead.commit()
        #         self.DbRead.flush()
        #         self.DbRead.close()
        #     except Exception as e:
        #         print e
        #         self.DbRead.rollback()
            rep = {}
            rep['data'] = self.Periodoftime
            self.writejson(json_decode(str(ApiHTTPError(**rep))))
        else:
            try:
                print courses[0]
                for item in courses:
                    print item.courses_current_number
                self.DbRead.commit()
            except Exception as e:
                self.DbRead.commit()
            self.writejson(json_decode(str(ApiHTTPError(30002))))

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
            if res.courses_endtime<datetime.now():
                disabled = True
                description = "已关闭"
            else:
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


#获取学员教练
class Studentoftrainer(BaseHandler):
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
        result = self.DbRead.query(self.Trainer.trainer_id, self.Trainer.trainer_name, self.Trainer.trainer_code, self.Trainer.trainer_dic, self.Trainer.trainer_years,self.Trainer.trainer_headpic).filter(
            self.Student.student_wxcode == self.studentid).first()
        result1 = self.DbRead.query(func.count(1).label("studentnum")).filter(
            self.Student.student_traineruid == result.trainer_id).first()
        result2 = self.DbRead.query(func.count(1).label("learntime")).filter(
            self.Courses.courses_traineruid == result.trainer_id, self.Courses.courses_state != 4).first()
        self.DbRead.commit()
        self.DbRead.close()
        rep = {"trainer_name": result.trainer_name, "trainer_code": result.trainer_code,"trainer_headpic": result.trainer_headpic,
               "trainer_dic": result.trainer_dic, "trainer_years": result.trainer_years,
               "studentnum": result1.studentnum,"learntime": result2.learntime}
        return rep

    # 驾校场地列表
class SubSchool(BaseHandler):
    executor = ThreadPoolExecutor(8)
    @gen.coroutine
    def post(self):
        self.school = self.get_json_argument('schoolid', None)
        reps = yield self.getdata()
        rep = {}
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(
            self.Exam_place.ep_name,self.Exam_place.ep_address).filter(
            self.Exam_place.ep_schooluid == self.school).all()
        rep = []
        for res in result:
            rep.append({'name': res.ep_name, 'address': res.ep_address})
        return rep
