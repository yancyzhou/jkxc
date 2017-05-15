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
            self.Package.package_id, self.Package.package_name, self.Package.package_money,self.Package.package_pic).filter(
            self.Package.package_state == 1,
            self.Package.package_schooluid == self.schoolid,).all()
        self.DbRead.close()
        rep = []
        for index,res in enumerate(result):
            more_item = True
            if index > 1:
                more_item = False
            item_dict = {"package_id":res.package_id,"package_name":res.package_name, "package_money":res.package_money,"more_item":more_item,"package_pic":res.package_pic}
            rep.append(item_dict)
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
            self.Package.package_describe, self.Package.package_detail,self.Package.package_money).filter(
            self.Package.package_state == 1,
            self.Package.package_id == self.packageid).first()
        self.DbRead.close()
        rep = {'package': result.package_describe, 'money':result.package_detail}
        return rep

# 某一套餐name,price
class PackageDetail_2(BaseHandler):
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
        result = self.DbRead.query(self.Package.package_name,self.Package.package_schooluid,self.Package.package_money).filter(
            self.Package.package_state == 1,
            self.Package.package_id == self.packageid).first()
        self.DbRead.close()
        rep = {'schooluid': result.package_schooluid, 'name':result.package_name,'price': result.package_money}
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
        courses = self.DbRead.query(self.Courses).filter(self.Courses.courses_id.in_(Periodoftime),self.Courses.courses_current_number<self.Courses.courses_limit_number).with_lockmode("update").all()
        if len(courses) == len(Periodoftime):
            for item in courses:
                verify = self.DbRead.query(self.Student_courses.sc_id).filter(self.Student_courses.sc_coursesuid==item.courses_id,self.Student_courses.sc_studentuid==self.StudentOpenid).first()
                if verify is None:
                    tmp = item.courses_current_number+1
                    item.courses_current_number = tmp
                    if tmp==item.courses_limit_number:
                        item.courses_state=3
            self.DbRead.commit()
            for items in Periodoftime:
                try:
                    studentCourses = self.Student_courses(sc_coursesuid=items, sc_studentuid=self.StudentOpenid)
                    self.DbRead.add(studentCourses)
                    self.DbRead.commit()
                    self.DbRead.close()
                except Exception as e:
                    self.DbRead.rollback()
            rep = {}
            rep['data'] = self.Periodoftime
            self.writejson(json_decode(str(ApiHTTPError(**rep))))
        else:
            self.DbRead.commit()
            self.DbRead.close()
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
        self.studentid = self.get_json_argument('studentcode', None)
        reps = yield self.getdata()
        if reps:
            pass
        else:
            reps = 0
        rep = {}
        rep['data'] = reps
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        result = self.DbRead.query(self.Trainer.trainer_id, self.Trainer.trainer_name, self.Trainer.trainer_code, self.Trainer.trainer_dic, self.Trainer.trainer_years,self.Trainer.trainer_headpic).filter(
            self.Student.student_code == self.studentid,self.Trainer.trainer_id==self.Student.student_traineruid).first()
        self.DbRead.commit()
        self.DbRead.close()
        if result is None:
            return False
        result1 = self.DbRead.query(func.count(1).label("studentnum")).filter(
            self.Student.student_traineruid == result.trainer_id).first()
        self.DbRead.commit()
        self.DbRead.close()
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
            self.Exam_place).filter(
            self.Exam_place.ep_schooluid == self.school).all()
        rep = []
        for index,res in enumerate(result):
            if index==0:
                rep.append({'ep_longitude':res.ep_longitude,'ep_latitude':res.ep_latitude,'value':res.ep_id,'checked':True,'name': res.ep_name, 'description': res.ep_address})
            else:
                rep.append({'ep_longitude':res.ep_longitude,'ep_latitude':res.ep_latitude,'value':res.ep_id,'checked':False,'name': res.ep_name, 'description': res.ep_address})
        self.DbRead.close()
        return rep


#学员报名信息

class RegistratorInfo(BaseHandler):
    executor = ThreadPoolExecutor(8)

    def post(self, *args, **kwargs):
        self.OpenId = self.get_json_argument('openid',None)

        result = yield self.getdata()

        rep = {}
        rep['data'] = result
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    def getdata(self):
        res = self.Student.query(self.Student).filter(self.Student.student_wxcode==self.OpenId).one()
        return res


# get student Registration data
class GetStudentReigstantion(BaseHandler):

    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.studentcode = self.get_json_argument('studentcode',None)

        result = yield self.getdata()
        rep = {}
        rep['data'] = result
        self.writejson(json_decode(str(ApiHTTPError(**rep))))
    @run_on_executor
    def getdata(self):

        studentdata = self.DbRead.\
            query(self.Order.order_code,self.Student.student_name,self.Order.order_createtime,self.Student.student_code,self.Student.student_id_number,self.Package.package_name,self.Package.package_money,self.School.school_address).\
            filter(self.Order.order_studentuid==self.Student.student_id,self.Package.package_id==self.Student.student_packageuid,self.Package.package_schooluid==self.School.school_id,self.Student.student_code==self.studentcode).\
            first()

        self.DbRead.commit()
        self.DbRead.close()
        if studentdata is None:
            data = []
        else:
            data = [{
                "name":studentdata.student_name,
                "phonenumber":studentdata.student_code,
                "id_number":studentdata.student_id_number,
                "package_name":studentdata.package_name,
                "package_money":studentdata.package_money,
                "school_address":studentdata.school_address,
                "order_code":studentdata.order_code,
                "order_createtime":studentdata.order_createtime.strftime('%Y-%m-%d %H:%M:%S')
            }]
        return data


class Login(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.code = self.get_json_argument("code",None)
        self.phoneNum = self.get_json_argument("phoneNum",None)
        self.schoolid = self.get_json_argument("schoolid",1)
        expired_time = 3
        result = yield self.validationcode(expired_time)


        if result:
            student_select = self.DbRead.query(self.Student.student_id).filter(
                self.Student.student_code == self.phoneNum,self.Student.student_schooluid==self.schoolid).first()
            self.DbRead.commit()
            self.DbRead.close()
            if student_select:
                data = {"code":student_select.student_id}
            else:
                Student = self.Student()
                Student.student_code = self.phoneNum
                Student.student_schooluid = self.schoolid
                Student.student_create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.DbRead.add(Student)
                self.DbRead.commit()
                data = {"code":Student.student_id}
                self.DbRead.close()
        else:
            data = {"code":0}
        rep = {}
        rep['data'] = data
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def validationcode(self,expired_time):
        result = self.DbRead.query(self.SmLog.smlog_createtime).filter(self.SmLog.smlog_usercode==self.phoneNum,func.substr(self.SmLog.smlog_message,7,6)==self.code).order_by(self.SmLog.smlog_createtime.desc()).first()
        self.DbRead.commit()
        self.DbRead.close()
        res = False
        if result:
            for item in result:
                t1 = item
                t2 = datetime.now()
                if (t2-t1).seconds<=expired_time*60:
                    res = True
        return res


# 获取未完成的订单信息
class GetNotDoneOrder(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self, *args, **kwargs):
        self.studentcode = self.get_json_argument('studentcode', None)

        result = yield self.getdata()

        rep = {}
        rep['data'] = result
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        res = self.DbRead.query(self.Package.package_money, self.Order.order_state,self.Order.order_type,self.Exam_place.ep_name,self.Package.package_name, self.Order.order_code,self.Order.order_money)\
                    .filter(self.Student.student_code==self.studentcode,self.Student.student_packageuid==self.Package.package_id,self.Exam_place.ep_schooluid==self.Student.student_schooluid,self.Order.order_studentuid==self.Student.student_id).first()

        if res is not None:
            data = {'order_code':res.order_code,'packagename': res.package_name,'packagemoney':res.package_money,'ep_name':res.ep_name, 'order_money':res.order_money,'order_state':res.order_state,'order_type':res.order_type}
        else:
            data = 0
        return data