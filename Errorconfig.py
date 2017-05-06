# Errorconfig
# -*- coding:utf-8 -*-
"""
======================
@author Vincent
@config file
错误信息提示描述
======================
"""

Errortypes = {
    1: "success",
    10400: "param_error",
    10401: "invalid header authorization",
    10402: "Missing authorization",
    10403: "not_authorized",
    10404: "Not found",
    10405: "method_not_allowed",
    10500: "server_error",
    20201: "User already exists",
    20200: "用户不存在！",
    20001: "The password length is less than 8 or greater than 15",
    20002: "Username or Password is Wrong!",
    30001: "IP address is not valid!",
    30002: "预约失败，请重新选择时间！",
    10410: "Missing argument '%s'"
}
Valid_Ip = ['127.0.0.1', "::1"]