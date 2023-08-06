#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 16:00
# software: PyCharm


class RequestBase(object):
    import requests

    def post(self, url, data = None, json = None, **kwargs):
        """

        Args:
            url:
            data:
            json:
            **kwargs:

        Returns:

        """
        return self.requests.post(url, data = data, json = json, **kwargs)

    def get(self, url, params = None, **kwargs):
        """

        Args:
            url:
            params:
            **kwargs:

        Returns:

        """
        kwargs.setdefault('allow_redirects', True)
        return self.requests.get(url, params = params, **kwargs)
