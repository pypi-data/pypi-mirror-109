#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 16:34
# software: PyCharm
from abc import ABC

from protocol_helper.utils.RequestBase import RequestBase


class WeiBoCollectionService(RequestBase, ABC):
    TIMEOUT = 30

    def __init__(self):
        super(WeiBoCollectionService, self).__init__()

        self.uid = None
        self.gsid = None
        self.aid = None
        self.s = None
        self.ua = "BLA-AL00_6.0.1_WeiboIntlAndroid_3660"

    def guest_login(self):
        """

        Returns:

        """

    def get_topics(self, title):
        """
        获取粉丝数据
        Args:
            title:话题内容

        Returns:

        """
        params = {
            "v_f": "2",
            "s": self.s,
            "source": "4215535043",
            "wm": "2468_1001",
            "gsid": self.gsid,
            "count": "20",
            "containerid": f"231522type%3D1%26q%3D{title}",
            "from": "1299295010",
            "i": "4366450",
            "c": "weicoabroad",
            "ua": self.ua,
            "lang": "zh_CN",
            "page": "1",
            "aid": self.aid,
            "v_p": "72"
        }

        return self.get('https://api.weibo.cn/2/cardlist', params=params).json()

    def get_article(self, url):
        """
        获取文章数据
        Args:
            url:

        Returns:

        """
