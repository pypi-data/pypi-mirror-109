#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 16:34
# software: PyCharm
from abc import ABC

from protocol_helper.Exceptions import RequestException
from protocol_helper.services.BaseService import BaseService
from protocol_helper.utils.RequestBase import RequestBase


class WeiBoAppCollectionService(RequestBase, BaseService, ABC):

    def __init__(self):
        super(WeiBoAppCollectionService, self).__init__()

        self.uid = None
        self.gsid = None
        self.aid = None
        self.s = None
        self.comment_s = None
        self.ua = "BLA-AL00_6.0.1_WeiboIntlAndroid_3660"

    def guest_login(self):
        """

        Returns:

        """

        # 获取设备
        try:
            resp = self.eoms.get_weibo_registered_equipment()
        except RequestException as error:
            raise error
        except Exception as error:
            raise error
        headers = {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Host':         'api.weibo.cn',
                'User-Agent':   'okhttp/3.12.1'
        }
        # 注册设备可用
        data = resp['data']['equipment']
        resp = self.post('https://api.weibo.cn/2/guest/login', data = data, headers = headers)
        if resp.status_code != 200:
            raise RequestException(resp)
        data = resp.json()
        if data.get('errmsg', None):
            return data.get('errmsg', None)
        self.uid = data['uid']
        self.gsid = data['gsid']
        self.aid = data['aid']
        data = self.eoms.get_weibo_s(self.uid)
        if data.get('status_code', None) != 0:
            return "获取 s 加密错误"
        self.s = data['data']['s']
        self.comment_s = data['data']['comment_s']
        return "success"

    def get_topics(self, title):
        """
        获取话题数据
        Args:
            title:话题内容

        Returns:

        """
        params = {
                "v_f":         "2",
                "s":           self.s,
                "source":      "4215535043",
                "wm":          "2468_1001",
                "gsid":        self.gsid,
                "count":       "20",
                "containerid": f"231522type%3D1%26q%3D{title}",
                "from":        "1299295010",
                "i":           "4366450",
                "c":           "weicoabroad",
                "ua":          self.ua,
                "lang":        "zh_CN",
                "page":        "1",
                "aid":         self.aid,
                "v_p":         "72"
        }

        return self.get('https://api.weibo.cn/2/cardlist', params = params).json()

    def get_article(self, url):
        """
        获取文章数据
        Args:
            url:

        Returns:

        """
