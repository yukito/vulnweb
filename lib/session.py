#!/usr/bin/env python
# coding:utf-8

import uuid
import lib.models

class ManageSession(object):

   def __init__(self, username = None, logged_in = False):
      self.csrf_token = str(uuid.uuid4())
      self.username = username
      self.password = None
      self.group_list = {}
      for group in lib.models.get_groups(username):
         self.group_list[group[0]] = group[1]
      print self.group_list
      self.loggedin = logged_in
      if logged_in:
         self.userid, _, self.job, self.firm, self.department, self.image = lib.models.get_profile(username)
         #self.userid = profile[0]
         #self.job = profile[3]
         #self.firm = profile[4]
         #self.department = profile[5]
         #self.image = profile[6]
      else:
         self.userid = None
         self.job = None
         self.firm = None
         self.department = None
         self.image = None
      self.notification = lib.models.get_notifications(username)
