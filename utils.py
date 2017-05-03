# -*- coding:utf-8 -*-
from app import *
from admin import *
from Handler import NotFound
Handlers = [
    # (r"/download/(.*)", Download),
    # (r"/api/SetFile", SetFile),
    (r'/api/auth', AuthHandler),
    (r'/newapi/packagedetail', PackageDetail),
    (r'/newapi/package', PackageIndex),
    (r'/newapi/studentcourseslist', StudentExamList),
    (r'/newapi/studentcoursesindex', StudentExamindex),
    # (r'/api/GetUserinfo', GetUserinfo),
    (r'/sms/SmsSender', SmsSenders),
    # (r'/api/IndexHandler', IndexHandler),
    # (r'/api/GetProvince', GetProvince),
    # (r'/api/PaperAnalytics', PaperAnalytics),
    # (r'/api/GetUserAction', GetUserAction),#未使用
    # (r'/api/GetStudent', GetStudent),
    # (r'/api/GetUserDataTotal', GetUserDataTotal),
    # (r'/api/GetUserDataAnalytics', GetUserDataAnalytics),
    # (r'/api/GetOrderTotal', GetOrderTotal),
    # (r'/api/GetOrderAnalytics', GetOrderAnalytics),
    # (r'/api/GetTotal', GetTotal),
    # (r'/api/SaveKpi', SaveKpi),
    # (r'/api/GetKpi', GetKpi),
    # (r'/api/GetUserActions', GetUserActions),
    # (r'/api/DelKpi', DelKpi),
    # (r'/api/GetMonth', GetMonth),
    # (r'/api/GetMonthProvinces', GetMonthProvinces),
    # (r'/api/GetMPS', GetMPS),
    # (r'/api/GetSalesmanList', GetSalesmanList),
    (r".*", NotFound),
]
