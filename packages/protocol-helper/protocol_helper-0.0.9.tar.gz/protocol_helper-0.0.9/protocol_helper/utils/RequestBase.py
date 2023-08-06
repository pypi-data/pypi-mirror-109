#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 16:00
# software: PyCharm
from protocol_helper.Exceptions import RequestExceptions


class RequestBase(object):
    import requests
    TIMEOUT = 60
    COOKIES = None
    HEADERS = None

    def __upload_request(self, **kwargs):
        """
        Updating the customized configuration file takes effect globally
        Args:
            **kwargs:

        Returns:

        """
        if kwargs.get('timeout', None) is None:
            kwargs.setdefault('timeout', self.TIMEOUT)

        if kwargs.get('headers', None) is None:
            kwargs.setdefault('headers', {})

        # update cookies
        if self.COOKIES is not None and kwargs.get('headers', {}).get('cookie', None) is None:
            kwargs['headers'].update({'cookie': self.COOKIES})

        # update headers
        if self.HEADERS is not None:
            kwargs['headers'] = dict(self.HEADERS, **kwargs.get('headers', {}))

        return kwargs

    def post(self, url, data = None, json = None, **kwargs):
        """

        Args:
            url:
            data:
            json:
            **kwargs:

        Returns:

        """
        kwargs = self.__upload_request(**kwargs)
        resp = self.requests.post(url, data = data, json = json, **kwargs)
        if resp.status_code != 200:
            raise RequestExceptions(resp.status_code, "Request an abnormal response", resp.text, resp)
        return resp

    def get(self, url, params = None, **kwargs):
        """

        Args:
            url:
            params:
            **kwargs:

        Returns:

        """
        kwargs = self.__upload_request(**kwargs)
        kwargs.setdefault('allow_redirects', True)
        resp = self.requests.get(url, params = params, **kwargs)
        if resp.status_code != 200:
            raise RequestExceptions(resp.status_code, "Request an abnormal response", resp.text, resp)
        return resp
