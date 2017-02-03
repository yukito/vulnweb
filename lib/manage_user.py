#!/usr/bin/env python
# coding:utf-8

import sqlite3

def is_correct_user(username, password):
   conn = sqlite3.connect('db/vulnweb.db')
   try:
      pwd = conn.cursor().execute('select password from users where name =?',(username,)).fetchone()
      if pwd[0] == password:
         return True
   except:
      return False
   else:
      return False
