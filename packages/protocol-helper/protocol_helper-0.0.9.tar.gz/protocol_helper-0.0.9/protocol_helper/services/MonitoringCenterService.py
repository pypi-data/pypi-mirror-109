#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-10 16:45
# software: PyCharm
from abc import ABC
from protocol_helper.setting import SURVEILLANCE_SYSTEM_DOMAIN, SURVEILLANCE_SYSTEM_TOKEN
from protocol_helper.utils.RequestBase import RequestBase


class MonitoringCenterService(RequestBase, ABC):
    TIMEOUT = 10

    def __init__(self):
        self.url = SURVEILLANCE_SYSTEM_DOMAIN
        self.token = SURVEILLANCE_SYSTEM_TOKEN
        self._headers = {
                'Authorization': f'Token {self.token}'
        }

    def support_service(self):
        """
        数据获取支持的格式
        Returns:

        """
        return self.get(f"{self.url}/api/collection", timeout = self.TIMEOUT).json()

    def collection(self, mode, server_type, url):
        """

        Args:
            mode:        参考 support_service 返回数据体
            server_type: 服务类型
            url:

        Returns:

        """
        data = {
                'mode':        mode,
                'server_type': server_type,
                'url':         url
        }
        return self.post(f"{self.url}/api/collection", data = data, timeout = self.TIMEOUT).json()

    def available_agents(self):
        """
        获取一条随机可使用的代理IP
        Returns:

        """

        return self.get(f"{self.url}/api/agent/", timeout = self.TIMEOUT, headers = self._headers).json()

    def agent_status_notify(self, server_name, status):
        """
        通知代理可用状态
        Args:
            server_name:  服务器名称
            status:       状态

        Returns:

        """
        data = {
                'status':      status,
                'server_name': server_name,
        }
        return self.post(f"{self.url}/api/agent/", data = data, timeout = self.TIMEOUT, headers = self._headers).json()

    def get_proxy_configuration(self, server_name):
        """
        获取代理服务器信息
        Args:
            server_name:

        Returns:

        """

        return self.get(f"{self.url}/api/agent/{server_name}", timeout = self.TIMEOUT, headers = self._headers).json()

    def agent_lock(self, server_name, lock = 0):
        """
        设置代理服务器加锁
        Args:
            server_name:
            lock:   0=>加锁  1=>解锁

        Returns:

        """
        data = {
                'status': lock
        }
        return self.post(f"{self.url}/api/agent/{server_name}", data = data, timeout = self.TIMEOUT,
                         headers = self._headers).json()

    def get_equipment_pool(self, equipment_type):
        """
        获取代理池cookie
        Args:
            equipment_type:参考后台服务类型

        Returns:

        """
        return self.get(f"{self.url}/api/equipment-pool/{equipment_type}", timeout = self.TIMEOUT,
                        headers = self._headers).json()

    def set_equipment_pool(self, equipment_type, _hash, status):
        """
        cookies状态设置
        Args:
            equipment_type:参考后台服务类型
            _hash: 回去cookie之后会返回一个hash
            status:200=>占用中 500=>失效  50=>可用

        Returns:

        """
        data = {
                'hash':   hash,
                'status': status
        }
        return self.post(f"{self.url}/api/equipment-pool/{equipment_type}", timeout = self.TIMEOUT, data = data,
                         headers = self._headers).json()
