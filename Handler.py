# -*- encoding:utf-8 -*-
from tornado.web import RequestHandler
from Errorconfig import Errortypes,city_list,provincescode_name,provinceslist,city
from tornado import gen
from tornado.escape import json_decode, json_encode, to_unicode
from model import models



class ApiHTTPError(Exception):
    def __init__(self, status_code=1, log_message=None, *args, **kwargs):
        self.status_code = status_code
        self.log_message = log_message
        self.reason = kwargs.get('reason', None)
        self.data = kwargs.get('data', {'message': Errortypes[self.status_code]})
        if log_message and not args:
            self.log_message = log_message.replace('%', '%%')

    def __str__(self):
        result = json_encode({'code': self.status_code, 'message': Errortypes[self.status_code], 'data': self.data})
        return result


class BaseHandler(RequestHandler):
    _data = None

    @gen.coroutine
    def writejson(self, obj):
        self._status_code = 200
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.write(obj), {'Content-Type': 'application/json;'}
        self.finish()

    def write_error(self, status_code, **kwargs):
        if status_code == 404:
            self.writejson(json_decode(str(ApiHTTPError(10405))))
        elif status_code == 500:
            self.writejson(json_decode(str(ApiHTTPError(10500))))
        else:
            self.writejson(json_decode(str(ApiHTTPError(10500))))

    @property
    def Staff(self):
        return models.Staff

    @property
    def DbRead(self):
        return self.application.DbRead

    @property
    def Student(self):
        return models.Student

    @property
    def Trainer(self):
        return models.Trainer

    @property
    def School(self):
        return models.School

    @property
    def Courses(self):
        return models.Courses

    @property
    def Exam_place(self):
        return models.Exam_place

    @property
    def Order(self):
        return models.Order

    @property
    def Package(self):
        return models.Package

    @property
    def Student_courses(self):
        return models.Student_courses

    def get_json_arguments(self, args, **kwargs):
        result = json_decode(self.request.body)
        for item in args:
            if item in kwargs:
                result[item] = self.get_json_argument(item, kwargs[item])
            else:
                result[item] = self.get_json_argument(item)
        return result

    def get(self, *args, **kwargs):
        self.writejson(json_decode(str(ApiHTTPError(10405))))

    def post(self, *args, **kwargs):
        self.writejson(json_decode(str(ApiHTTPError(10405))))

    '''
    Get the json data format
    '''

    def get_json_argument(self, name, default=None):
        args = json_decode(self.request.body)
        name = to_unicode(name)
        if name in args:
            return args[name]
        elif default is not None:
            return default
        else:
            msg = "Missing argument '%s'" % name
            result = json_decode(str(ApiHTTPError(10410)))
            result['message'] = msg
            self.writejson(result)


class NotFound(BaseHandler):
    def get(self):
        self.writejson(json_decode(str(ApiHTTPError(10404))))
    def post(self):
        self.writejson(json_decode(str(ApiHTTPError(10404))))
