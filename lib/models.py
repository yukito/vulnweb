#!/usr/bin/env python
# coding:utf-8

import sqlite3

def get_groups(username):
   conn = sqlite3.connect('db/groups.db')
   return conn.cursor().execute('select groupname from groups where username =?',(username,))

def get_summary_of(group_name):
   pass
