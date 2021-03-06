# -*- coding:utf-8 -*-
from app import *
from admin import *
from Handler import NotFound
Handlers = [
    # (r"/download/(.*)", Download),
    # (r'/api/auth', AuthHandler),
    (r'/api/auth', AdminLogin),
    (r'/api/packagedetail', PackageDetail),
    (r'/api/packagedetail_2', PackageDetail_2),
    (r'/api/package', PackageIndex),
    (r'/api/studentcourseslist', StudentExamList),
    (r'/api/studentcoursesindex', StudentExamindex),
    (r'/api/SaveStudentExam', SaveStudentExam),
    (r'/api/Studentoftrainer', Studentoftrainer),
    (r'/api/GetUserinfo', GetUserinfo),
    (r'/api/SmsSender', SmsSenders),
    (r'/api/SetOrder', SetOrder),
    (r'/api/validationcode', ValidationCode),
    (r'/api/login', Login),
    (r'/api/getstudent', getstudent),
    (r'/api/getstudent_state', getstudent_state),
    (r'/api/subschool', SubSchool),
    (r'/api/PayResult', PayResult),
    (r'/api/PaySucess', PaySucess),
    (r'/api/GetNotDoneOrder', GetNotDoneOrder),
    (r'/api/CloseOrder', CloseOrder),
    (r'/api/GetStudentReigstantion', GetStudentReigstantion),
    (r'/api/getfree/(.*)/(.*)', getFree),
    (r'/api/getstudent/(.*)/(.*)', getStudent),
    (r".*", NotFound),
]
