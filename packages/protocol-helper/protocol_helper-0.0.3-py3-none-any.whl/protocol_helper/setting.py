#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-11 12:40
# software: PyCharm

import os
from dotenv import load_dotenv

LOAD_PROJECT_PATH = os.environ.get('LOAD_PROJECT_PATH')

try:
    load_dotenv(os.path.join(LOAD_PROJECT_PATH, '.env'), encoding = 'gbk')
except UnicodeDecodeError as error:
    load_dotenv(os.path.join(LOAD_PROJECT_PATH, '.env'))
except Exception as error:
    raise error

# Monitoring Center Configuration File
SURVEILLANCE_SYSTEM_DOMAIN = os.getenv('SURVEILLANCE_SYSTEM_DOMAIN', None)
SURVEILLANCE_SYSTEM_TOKEN = os.getenv('SURVEILLANCE_SYSTEM_TOKEN', None)
