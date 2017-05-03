# -*- coding:utf-8 -*-
from app import *
from admin import *
from Handler import NotFound
Handlers = [
    # (r"/download/(.*)", Download),
    (r'/api/auth', AuthHandler),
    (r'/newapi/packagedetail', PackageDetail),
    (r'/newapi/package', PackageIndex),
    (r'/newapi/studentcourseslist', StudentExamList),
    (r'/newapi/studentcoursesindex', StudentExamindex),
    (r'/api/GetUserinfo', GetUserinfo),
    (r'/sms/SmsSender', SmsSenders),
    (r".*", NotFound),
]
