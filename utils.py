# -*- coding:utf-8 -*-
from app import *
from admin import *
from Handler import NotFound
Handlers = [
    # (r"/download/(.*)", Download),
    (r'/api/auth', AuthHandler),
    (r'/api/packagedetail', PackageDetail),
    (r'/api/package', PackageIndex),
    (r'/api/studentcourseslist', StudentExamList),
    (r'/api/studentcoursesindex', StudentExamindex),
    (r'/api/SaveStudentExam', SaveStudentExam),
    (r'/api/GetUserinfo', GetUserinfo),
    (r'/api/SmsSender', SmsSenders),
    (r'/api/validationcode', ValidationCode),
    (r".*", NotFound),
]
