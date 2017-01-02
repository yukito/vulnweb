#!/usr/bin/env python
# coding:utf-8

import sqlite3

def get_groups(username):
   conn = sqlite3.connect('db/groups.db')
   groups = conn.cursor().execute('select groupname from groups where username =?',(username,))
   return groups

def get_summary_of(group_name):
   conn = sqlite3.connect('db/groups.db')
   members = conn.cursor().execute('select username from groups where groupname =?',(group_name,))
   conn = sqlite3.connect('db/topics.db')
   topics = conn.cursor().execute('select distinct topic from ' + group_name)
   return members, topics

def get_posts_of(group_name, topic):
   conn = sqlite3.connect('db/topics.db')
   posts = conn.cursor().execute('select * from ' + group_name + ' where topic =?',(topic,))
   return posts

def insert_articles(group_name, topic_name, request):
   conn = sqlite3.connect('db/topics.db')
   conn.cursor().execute('insert into ' + group_name + '(topic, username, details) values(?,?,?)',(topic_name, request['username'], request['post_detail']))
   conn.commit()

def update_users(username, password):
   conn = sqlite3.connect('db/users.db')
   if check_user(username):
      conn.cursor().execute('insert into users (name, password) values(?,?)',(username, password))
      conn.commit()
      return True
   else:
      return False

def check_user(username):
   conn = sqlite3.connect('db/users.db')
   uname = conn.cursor().execute('select * from users where name =?',(username,))
   if uname.fetchone() == None:
      return True
   else:
      return False
