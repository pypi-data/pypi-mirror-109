#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 16:34
# software: PyCharm
from abc import ABC

from protocol_helper.utils import RequestBase


class WeiBoCollectionService(RequestBase, ABC):

    def __init__(self):
        super(WeiBoCollectionService, self).__init__()

    def get_fans(self, url):
        """
        获取粉丝数据
        Args:
            url:

        Returns:

        """

    def get_article(self, url):
        """
        获取文章数据
        Args:
            url:

        Returns:

        """
