#!/usr/bin/env python
# coding:utf-8

import sqlite3

def get_groups(username):
   conn = sqlite3.connect('db/groupMembers.db')
   groups = conn.cursor().execute('select groupname from groupMembers where username =?',(username,))
   return groups

def get_summary_of(group_name):
   conn = sqlite3.connect('db/groupMembers.db')
   members = conn.cursor().execute('select username from groupMembers where groupname =?',(group_name,))
   conn = sqlite3.connect('db/topics.db')
   try:
      topics = conn.cursor().execute('select distinct topic from ' + group_name)
   except:
      topic_summary = []
   else:
      topic_summary = []
      for topic in topics:
         topic_summary.append(conn.cursor().execute('select * from ' + group_name + ' where topic =? limit 1', (topic[0],)).fetchone())
   return members, topic_summary

def get_posts_of(group_name, topic):
   conn = sqlite3.connect('db/topics.db')
   posts = []
   for article in conn.cursor().execute('select * from ' + group_name + ' where topic =?',(topic,)):
      posts.append(article)
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

def update_groups(groupname, description, members):
   conn = sqlite3.connect('db/groups.db')
   conn.cursor().execute('insert into groups (groupname, description) values(?,?)',(groupname, description))
   conn.commit()
   add_members(groupname, members)
   conn = sqlite3.connect('db/topics.db')
   conn.cursor().execute('create table ' + groupname + ' (id integer primary key autoincrement, topic varchar(32) NOT NULL, username varchar(32) NOT NULL, details text, timestamp default CURRENT_TIMESTAMP)')
   conn.commit()

def add_members(groupname, members):
   conn = sqlite3.connect('db/groupMembers.db')
   for member in members.split():
      conn.cursor().execute('insert into groupMembers (username, groupname) values(?,?)',(member, groupname))
   conn.commit()

def update_topics(topicname, username, description, groupname):
   conn = sqlite3.connect('db/topics.db')
   if conn.cursor().execute('select * from ' + groupname + ' where topic =?', (topicname,)).fetchone() == None:
      conn.cursor().execute('insert into ' + groupname + ' (topic, username, details) values(?,?,?)',(topicname, username, description))
      conn.commit()
      return True
   else:
      return False

def update_article(groupname, article, article_id):
   conn = sqlite3.connect('db/topics.db')
   conn.cursor().execute('update ' + groupname + ' set details =? where id =?',(article, article_id))
   conn.commit()

def delete_article(groupname, article_id):
   conn = sqlite3.connect('db/topics.db')
   conn.cursor().execute('delete from ' + groupname + ' where id =?', (article_id,))
   conn.commit()

def search_group(word):
   conn = sqlite3.connect('db/groups.db')
   result = []
   for group in conn.cursor().execute("select groupname, description from groups where groupname like '%" + word + "%'"):
      result.append(group)
   return result

def check_user(username):
   conn = sqlite3.connect('db/users.db')
   uname = conn.cursor().execute('select * from users where name =?',(username,))
   if uname.fetchone() == None:
      return True
   else:
      return False
