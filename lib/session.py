#!/usr/bin/env python
# coding:utf-8

import uuid
import lib.models

GUEST_KEY = 'A1F91954-DEAD-41BE-A7D1-AFDABD398E2F'

class ManageSession(object):

   def __init__(self, username = None, logged_in = False, mode='user'):
      self.csrf_token = str(uuid.uuid4())
      self.username = username
      self.password = None
      self.group_list = {}
      self.loggedin = logged_in
      if logged_in and mode=='user':
         self.login(username)
      if mode == 'guest':
         self.userid = None
         self.job = None
         self.firm = None
         self.department = None
         self.image = None
         self.login(GUEST_KEY)

   def login(self, username):
      for group in lib.models.get_groups(username):
         self.group_list[group[0]] = group[1]
      self.userid, _, self.job, self.firm, self.department, self.image = lib.models.get_profile(username)
      self.notification = lib.models.get_notifications(username)
