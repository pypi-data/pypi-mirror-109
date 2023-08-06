#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-10 16:45
# software: PyCharm
import requests
from protocol_helper.setting import SURVEILLANCE_SYSTEM_DOMAIN, SURVEILLANCE_SYSTEM_TOKEN


class MonitoringCenterService(object):

    def __init__(self):
        self.url = SURVEILLANCE_SYSTEM_DOMAIN
        self.token = SURVEILLANCE_SYSTEM_TOKEN

    def collection_list(self):
        """
        数据获取支持的格式
        Returns:

        """
