#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:LeisureMan
# email:LeisureMam@gmail.com
# datetime:2021-06-09 12:44
import os

from protocol_helper.Exceptions import NotStrDirectory

LOAD_PROJECT_PATH = os.environ.get('LOAD_PROJECT_PATH')
if LOAD_PROJECT_PATH is None:
    raise NotStrDirectory
