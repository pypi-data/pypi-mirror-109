#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 17:42
# software: PyCharm
from abc import ABC

from protocol_helper.Exceptions import DefaultException
from protocol_helper.services.BaseService import BaseService
from protocol_helper.utils.RequestBase import RequestBase


class WeiBoPcCollectionService(RequestBase, BaseService, ABC):
    HEADERS = {
            'x-requested-with': 'XMLHttpRequest',
            'user-agent':       'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/90.0.4430.72 Safari/537.36 ',
            'accept':           'application/json, text/plain, */*',
    }

    def __init__(self):
        super(WeiBoPcCollectionService, self).__init__()

    def get_random_cookies(self):
        """
        随机返回一条cookies
        Returns:

        """
        resp = self.eoms.get_equipment_pool('WeiBoH5PCAFaZHU')
        if resp.get('status_code', None) != 0:
            raise DefaultException(resp.get('messages', resp))

        self.HEADERS.update({'cookie': resp['data']['cookie']})
        return resp['data']

    def set_cookies(self, value):
        """
        设置全局cookies
        Args:
            value:

        Returns:

        """
        self.COOKIES = value

    def get_topic(self, title):
        """
        微博话题
        支持格式 #吴一凡# 吴一凡

        Returns:

        """
        params = {"containerid": f"100103type=1&q={title}&t=0", "page": "1", "count": "20"}
        return self.get('https://weibo.com/ajax/search/all', params = params).json()

    def get_article(self, mid):
        """
        微博博文
        Args:
            mid: 微博文章mid

        Returns:

        """
        params = {'id': mid}
        return self.get('https://weibo.com/ajax/statuses/show', params = params).json()

    def get_fans(self, uid = None, custom = None):
        """
        微博主页

        uid 与  custom 不能同时为空

        Args:
            uid:   uid
            custom:custom

        Returns:

        """
        params = {}
        if uid is not None:
            params.update({'uid': uid})
        if custom is not None:
            params.update({'custom': custom})
        return self.get('https://weibo.com/ajax/profile/info', params = params).json()

    def get_user_article(self, uid, page = 1):
        """
        获取用户博文
        :param uid:     微博uid
        :param page:   获取页数
        :return:
        """
        params = {}
        if uid is not None:
            params.update({'uid': uid})
        if page is not None:
            params.update({'page': page})
        return self.get(f"https://weibo.com/ajax/statuses/mymblog", params = params).json()
