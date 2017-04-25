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
from sqlalchemy import func,extract,distinct
from concurrent.futures import ThreadPoolExecutor
from tornado.concurrent import run_on_executor
from model.models import *

@jwtauth
class IndexHandler(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.daterange = self.get_json_argument('StartDate',[])
        self.province = self.get_json_argument('province',None)
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
            rep['data'] = sorted(rep['data'],key=lambda x:x['total'])

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

    @run_on_executor
    def getdata(self):
        if self.province and self.province!="all":
            result = self.DrdsRead.query(
                func.substr(self.Exampaper.olap_ASIResponseSummary_ru, 1, self.substrlength).label('provinces'),
                func.sum(self.Exampaper.olap_ASIResponseSummary_total).label("total")).filter(
                self.Exampaper.olap_ASIResponseSummary_createdTime >= self.startdate,self.Exampaper.olap_ASIResponseSummary_createdTime <= self.enddate,
                func.substr(self.Exampaper.olap_ASIResponseSummary_ru, 1, 2) == self.province).group_by('provinces').all()
        else:
            result = self.DrdsRead.query(func.substr(self.Exampaper.olap_ASIResponseSummary_ru, 1, self.substrlength).label('provinces'), func.sum(self.Exampaper.olap_ASIResponseSummary_total).label("total")).filter(self.Exampaper.olap_ASIResponseSummary_createdTime >= self.startdate,self.Exampaper.olap_ASIResponseSummary_createdTime <= self.enddate).group_by('provinces').all()
        data = []
        rep = {}
        rep['data'] = []
        for item in result:
            data.append({"total":int(item.total),"provinces":item.provinces})
            rep['data'] = data
        return rep

@jwtauth
class GetStudent(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.province = self.get_json_argument('province',None)
        self.substrlength = 4 if self.province and self.province!='all' else 2
        rep = yield self.getstudentcount()
        province = []
        total = []
        if len(rep['data']) > 0:
            rep['data'] = sorted(rep['data'],key=lambda x:x['total'])

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
            rep['data']['provname'] = self.provinces[self.province]
            rep['data']['count'] = total
            rep['data']['total'] = sum(total)
            self.writejson(json_decode(str(ApiHTTPError(**rep))))
        else:
            rep['data'] = {}
            rep['data']['provinces'] = province
            rep['data']['provname'] = self.provinces[self.province]
            rep['data']['count'] = total
            rep['data']['total'] = sum(total)
            self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getstudentcount(self):
        if self.province and self.province!="all":
            result = self.DrdsRead.query(
                func.substr((self.olap_student.olap_Student_ru), 1, self.substrlength).label('provinces'),
                func.count(self.olap_student.olap_Student_id).label("total")).filter(
                func.substr(self.olap_student.olap_Student_ru, 1, 2) == self.province).group_by('provinces').all()
        else:
            result = self.DrdsRead.query(func.substr(self.olap_student.olap_Student_ru, 1, self.substrlength).label('provinces'), func.count(self.olap_student.olap_Student_id).label("total")).filter().group_by('provinces').all()
        data = []
        rep = {}
        rep['data'] = []
        for item in result:
            data.append({"total":int(item.total),"provinces":item.provinces})
            rep['data'] = data
        return rep

@jwtauth
class PaperAnalytics(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self):
        self.daterange = self.get_json_argument('StartDate',[])
        self.province = self.get_json_argument('province',None)
        self.kpi = self.get_json_argument('kpi',None)
        self.province = [int(i) for i in self.province]
        if len(self.daterange)==0:
            self.startdate = (datetime.now()-timedelta(days=30)).strftime("%Y-%m-%d")
            self.enddate = datetime.now().strftime("%Y-%m-%d")
        else:
            self.startdate = self.daterange[0][:10]
            self.enddate = self.daterange[1][:10]
        self.substrlength = 2
        dateline = self.SetTimeline()
        rep = yield self.getdata()
        if len(rep['data']) > 0:
            data = {}
            for item in rep['data']:
                if item.keys()[0] not in data.keys():
                    data[item.keys()[0]] = [item.values()[0]]
                else:
                    data[item.keys()[0]].append(item.values()[0])
            result = []
            data_province_name = []
            for datakey,dataitem in data.items():
                data_province = {}
                data_province_name.append(datakey)
                data_date = [value.keys()[0] for value in dataitem]
                for itemline in dateline:
                    if itemline not in data_date:
                        dataitem.append({itemline:0})
                tmp_sorted = sorted(dataitem,key=lambda x:x.keys()[0])
                data_province["type"] = "line"
                data_province["name"] = datakey
                data_province["smooth"] = True
                data_province["markPoint"]= {
                               "data": [
                                   {"type": 'max', "name": '最大值'},
                                   {"type": 'min', "name": '最小值'}
                               ]
                           }
                data_province["data"] = [tmp_item.values()[0] for tmp_item in tmp_sorted]
                result.append(data_province)
            result = sorted(result, key=lambda x: x['data'][0])
            rep['data'] = {}
            rep['data']['series'] = result
            rep['data']['dateline'] = dateline
            rep['data']['province_list'] = data_province_name
            self.writejson(json_decode(str(ApiHTTPError(**rep))))
        else:
            rep['data'] = {}
            rep['data']['series'] = []
            rep['data']['dateline'] = []
            rep['data']['province_list'] = []
            self.writejson(json_decode(str(ApiHTTPError(**rep))))

    def SetTimeline(self):
        if self.kpi == "month":
            Timeformat = "%Y-%m"
            days = 31
        elif self.kpi =="week":
            Timeformat = "%Y-%W"
            days = 7
        else:
            Timeformat = "%Y-%m-%d"
            days = 1
        date_list = []
        begin_date = datetime.strptime(self.startdate, "%Y-%m-%d")
        end_date = datetime.strptime(self.enddate, "%Y-%m-%d")
        while begin_date <= end_date:
            date_str = begin_date.strftime(Timeformat)
            date_list.append(date_str)
            begin_date += timedelta(days=days)
        if end_date.strftime(Timeformat) in date_list:
            pass
        else:
            date_list.append(end_date.strftime(Timeformat))
        return date_list

    @run_on_executor
    def getdata(self):
        if self.kpi=='month':
            year_field = func.extract('year', self.Exampaper.olap_ASIResponseSummary_createdTime)
            month_field = func.extract('month', self.Exampaper.olap_ASIResponseSummary_createdTime)
            kpi_field = year_field*100+month_field
        elif self.kpi=='week':
            year_field = func.extract('year', self.Exampaper.olap_ASIResponseSummary_createdTime)
            week_field = func.extract('week', self.Exampaper.olap_ASIResponseSummary_createdTime)
            kpi_field = year_field*100+week_field
        if self.kpi=='day':
            result = self.DrdsRead.query(
                func.substr(self.Exampaper.olap_ASIResponseSummary_ru, 1, self.substrlength).label('provinces'),
                func.sum(self.Exampaper.olap_ASIResponseSummary_total).label("total"),self.Exampaper.olap_ASIResponseSummary_createdTime).filter(
                self.Exampaper.olap_ASIResponseSummary_createdTime >= self.startdate, self.Exampaper.olap_ASIResponseSummary_createdTime <= self.enddate,
                func.substr(self.Exampaper.olap_ASIResponseSummary_ru, 1, self.substrlength).in_(self.province)).group_by(self.Exampaper.olap_ASIResponseSummary_createdTime,
                                                                                                           'provinces').all()
        else:
            result = self.DrdsRead.query(func.substr(self.Exampaper.olap_ASIResponseSummary_ru, 1, self.substrlength).label('provinces'), kpi_field.label("kpi"),func.sum(self.Exampaper.olap_ASIResponseSummary_total).label("total")).filter(self.Exampaper.olap_ASIResponseSummary_createdTime >= self.startdate,self.Exampaper.olap_ASIResponseSummary_createdTime <= self.enddate,func.substr(self.Exampaper.olap_ASIResponseSummary_ru, 1, self.substrlength).in_(self.province)).group_by("kpi",'provinces').all()
        data = []
        rep = {}
        rep['data'] = []
        for item in result:
            if self.kpi=='day':
                data.append({self.provinces[item.provinces]:{item.olap_ASIResponseSummary_createdTime.strftime("%Y-%m-%d"): int(item.total)}})
            else:
                data.append({self.provinces[item.provinces]:{str(item.kpi)[:4]+"-"+str(item.kpi)[4:]:int(item.total)}})
            rep['data'] = data
        return rep

@jwtauth
class GetProvince(BaseHandler):
    def get(self, *args, **kwargs):
        rep = {}
        rep['data'] = self.provinces
        rep['data']['all'] = "全国"

        self.writejson(json_decode(str(ApiHTTPError(**rep))))
@jwtauth
class GetUserAction(BaseHandler):
    executor = ThreadPoolExecutor(8)


    @gen.coroutine
    def post(self, *args, **kwargs):
        self.rucode = self.get_json_argument('rucode',None)
        self.grad = self.get_json_argument('grad','')
        self.selectdate = self.get_json_argument('selectdate','')
        self.domains = self.get_json_argument('domains',[])
        if self.selectdate == '':
            self.startdate = unicode(datetime.now().strftime("%Y-%m-%d"))
            self.enddate = unicode((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))
        else:
            self.startdate = self.selectdate[:10]
            self.enddate = (datetime.strptime(self.startdate, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        rep = yield self.getuserlogdata()
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getuserlogdata(self):
        if self.rucode:
            schoolguid_obj = self.DbRead.query(self.SchoolTenant.RU_SchoolTenant_schoolGuid).filter(self.SchoolTenant.RU_SchoolTenant_ruCode==self.rucode).first()
            if self.grad:
                userlist = self.DbRead.query(self.UserStudent.RU_Userstudent_code).filter(self.UserStudent.RU_Userstudent_schoolGuid==schoolguid_obj[0],self.UserStudent.RU_Userstudent_grade==self.grad).all()
            else:
                userlist = self.DbRead.query(self.UserStudent.RU_Userstudent_code).filter(self.UserStudent.RU_Userstudent_schoolGuid==schoolguid_obj[0]).all()
        else:
            if self.grad:
                userlist = self.DbRead.query(self.UserStudent.RU_Userstudent_code).filter(self.UserStudent.RU_Userstudent_grade==self.grad).all()
            else:
                userlist = 'all'
        data = []
        year_field = func.extract('year', self.olap_userlog.olap_Userlog_createdTime)
        month_field = func.extract('month', self.olap_userlog.olap_Userlog_createdTime)
        day_field = func.extract('day', self.olap_userlog.olap_Userlog_createdTime)
        kpi_field = year_field * 10000 + month_field * 100 + day_field
        for item in self.domains:
            if item['value']:
                if userlist != 'all':
                    userlist = [i[0] for i in userlist]
                    result = self.DrdsUserLogRead.query(self.olap_userlog.olap_Userlog_usercode).filter(self.olap_userlog.olap_Userlog_eventtype==item['event_type'],self.olap_userlog.olap_Userlog_createdTime>self.startdate,self.olap_userlog.olap_Userlog_createdTime<self.enddate,self.olap_userlog.olap_Userlog_usercode.in_(userlist),self.olap_userlog.olap_Userlog_eventvalue==item['value']).all()
                else:
                    result = self.DrdsUserLogRead.query(self.olap_userlog.olap_Userlog_usercode).filter(
                        self.olap_userlog.olap_Userlog_eventtype == item['event_type'],
                        self.olap_userlog.olap_Userlog_createdTime > self.startdate,
                        self.olap_userlog.olap_Userlog_createdTime < self.enddate,self.olap_userlog.olap_Userlog_eventvalue==item['value']).all()
            else:
                if userlist != 'all':
                    userlist = [i[0] for i in userlist]
                    result = self.DrdsUserLogRead.query(self.olap_userlog.olap_Userlog_usercode).filter(self.olap_userlog.olap_Userlog_eventtype==item['event_type'],self.olap_userlog.olap_Userlog_createdTime>self.startdate,self.olap_userlog.olap_Userlog_createdTime<self.enddate,self.olap_userlog.olap_Userlog_usercode.in_(userlist)).all()
                else:
                    result = self.DrdsUserLogRead.query(self.olap_userlog.olap_Userlog_usercode).filter(
                        self.olap_userlog.olap_Userlog_eventtype == item['event_type'],
                        self.olap_userlog.olap_Userlog_createdTime > self.startdate,
                        self.olap_userlog.olap_Userlog_createdTime < self.enddate).all()
            userlog_pv = len(result)
            userlog_uv = len(list(set(result)))
            data.append({"name":item['event_type'],"UV":userlog_uv,"PV":userlog_pv})
        rep = {}
        rep['data'] = data
        return rep


@jwtauth
class GetTotal(BaseHandler):
    executor = ThreadPoolExecutor(8)
    @gen.coroutine
    def get(self, *args, **kwargs):

        rep = yield self.getdata()
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):
        studenttotal = self.DrdsRead.query(func.count(self.olap_student.olap_Student_id).label("total")).filter().first()
        papertotal = self.DrdsRead.query(func.sum(self.Exampaper.olap_ASIResponseSummary_total).label("total")).filter().first()
        ordertotal = self.DbRead.query(func.sum(self.ru_order.RU_Order_money).label("total")).filter(self.ru_order.RU_Order_state==1).first()
        usertotal = self.DbRead.query(func.count(self.UserStudent.RU_Userstudent_id).label("total")).filter().first()
        self.DrdsRead.close()
        self.DbRead.close()
        rep = {}
        rep['data'] = {"studenttotal":int(studenttotal.total),"papertotal":int(papertotal.total),"usertotal":int(usertotal.total),"ordertotal":round(ordertotal.total,2)}
        return rep

@jwtauth
class SaveKpi(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self, *args, **kwargs):

        self.title = self.get_json_argument("title",None)
        self.id = self.get_json_argument("id",None)
        self.value = self.get_json_argument("value",[])
        result = yield self.savedata()
        rep={}
        rep['data'] = result
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def savedata(self):

        if self.id ==-1:
            if self.title and self.value:
                new_kpi = olap_userlogkpi(kpi_title=self.title,kpi_value=json_encode(self.value))
                self.DrdsRead.add(new_kpi)
                self.DrdsRead.commit()
                rep = new_kpi.kpi_id
                self.DrdsRead.close()
                return rep
        else:
            if self.title and self.value:
                kpi = self.DrdsRead.query(self.olap_userlogkpi).filter(self.olap_userlogkpi.kpi_id == self.id).first()
                kpi.kpi_title = self.title
                kpi.kpi_value = json_encode(self.value)
                self.DrdsRead.commit()
                self.DrdsRead.close()
                return self.id
@jwtauth
class DelKpi(BaseHandler):
    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def post(self, *args, **kwargs):

        self.id = self.get_json_argument("id",None)
        result = yield self.deletedata()
        rep={}
        rep['data'] = result
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def deletedata(self):

        if self.id:
            kpi = self.DrdsRead.query(self.olap_userlogkpi).filter(self.olap_userlogkpi.kpi_id == self.id).first()
            self.DrdsRead.delete(kpi)
            self.DrdsRead.commit()
            self.DrdsRead.close()
            return self.id
@jwtauth
class GetKpi(BaseHandler):

    executor = ThreadPoolExecutor(8)

    @gen.coroutine
    def get(self):
        result = yield self.getdata()
        rep = {}
        rep['data'] = result
        self.writejson(json_decode(str(ApiHTTPError(**rep))))

    @run_on_executor
    def getdata(self):

        result = self.DrdsRead.query(self.olap_userlogkpi).all()
        self.DrdsRead.close()
        res = []
        for item in result:
            res.append({"value":json_decode(item.kpi_value),"label":item.kpi_title,"id":item.kpi_id})
        return res