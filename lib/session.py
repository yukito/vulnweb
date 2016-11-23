#!/usr/bin/env python
# coding:utf-8

import uuid

class ManageSession(object):

   def __init__(self, username):
      self._csrf_token = uuid.uuid4()
      self.username = username
      self.password = None
