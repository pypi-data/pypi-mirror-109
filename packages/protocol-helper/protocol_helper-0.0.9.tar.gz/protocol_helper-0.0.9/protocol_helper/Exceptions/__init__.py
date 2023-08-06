#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 15:15
# software: PyCharm

class BaseExceptions(Exception):
    MESSAGE = "Error base class"


class NotSetDirectory(BaseExceptions):
    MESSAGE = "未设置项目目录"


class RequestExceptions(BaseExceptions):
    MESSAGE = "请求响应码错误"

    def __init__(self, status_code, message, response, resp):
        """

        Args:
            status_code: 响应code
            message:     自定义错误信息
            response:    返回内容
            resp:        返回对象
        """
        self.status_code = status_code
        self.message = message
        self.response = response
        self.resp = resp
