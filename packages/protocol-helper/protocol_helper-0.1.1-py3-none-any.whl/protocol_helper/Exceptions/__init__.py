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


class DefaultException(BaseExceptions):
    MESSAGE = "默认异常,用于不重要的异常"


class RequestException(Exception):

    def __init__(self, resp):
        """

        Args:
            resp: request
        """
        self.status_code = resp.status_code
        self.message = "请求非正常响应"
        self.response = resp.text
        self.resp = resp
