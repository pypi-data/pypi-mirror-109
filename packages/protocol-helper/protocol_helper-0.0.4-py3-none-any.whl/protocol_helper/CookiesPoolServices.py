#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-10 16:44
# software: PyCharm
import os


class CookiesPoolServices(object):
    def __init__(self):
        pass

    def ceshi(self):
        print(os.environ.get("CESHI_URL"))
