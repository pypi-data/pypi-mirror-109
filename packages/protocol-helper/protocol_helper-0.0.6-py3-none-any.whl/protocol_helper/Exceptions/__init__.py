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
