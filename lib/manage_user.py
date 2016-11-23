#!/usr/bin/env python
# coding:utf-8

import sqlite3

def is_correct_user(username, password):
   conn = sqlite3.connect('db/users.db')
   print conn.cursor().execute('select password from users where name =?',(username,)).fetchone()
   if conn.cursor().execute('select password from users where name =?',(username,)).fetchone()[0] == password:
      return True
   else:
      return False
