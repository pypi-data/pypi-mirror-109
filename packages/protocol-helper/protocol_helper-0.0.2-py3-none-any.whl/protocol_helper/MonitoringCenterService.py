#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-10 16:45
# software: PyCharm
import requests


class MonitoringCenterService(object):

    def __init__(self, url, token):
        self.url = url
        self.token = token

    def collection_list(self):
        """
        数据获取支持的格式
        Returns:

        """
