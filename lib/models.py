#!/usr/bin/env python
# coding:utf-8

import sqlite3

def get_profile(username):
   conn = sqlite3.connect('db/vulnweb.db')
   conn.text_factory = str
   userid, uname, _, job, firm, department, image = conn.cursor().execute('select * from users where name =?',(username,)).fetchone()
   return userid, uname, job, firm, department, image

def get_image(userid):
   conn = sqlite3.connect('db/vulnweb.db')
   conn.text_factory = str
   image = conn.cursor().execute('select image from users where id =?',(userid,)).fetchone()[0]
   return image

def get_groups(username):
   conn = sqlite3.connect('db/vulnweb.db')
   groups = conn.cursor().execute('select groupname, role from groupMembers where username =?',(username,))
   return groups

def get_summary_of(group_name):
   conn = sqlite3.connect('db/vulnweb.db')
   members = conn.cursor().execute('select username from groupMembers where groupname =?',(group_name,))
   try:
      topics = conn.cursor().execute('select topic from groupTopics where groupname =?', (group_name,))
   except:
      topic_summary = []
   else:
      topic_summary = []
      conn = sqlite3.connect('db/topics.db')
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
   conn = sqlite3.connect('db/vulnweb.db')
   if check_user(username):
      conn.cursor().execute('insert into users (name, password) values(?,?)',(username, password))
      conn.commit()
      return True
   else:
      return False

def update_groups(groupname, description, members):
   conn = sqlite3.connect('db/vulnweb.db')
   conn.cursor().execute('insert into groups (groupname, description) values(?,?)',(groupname, description))
   conn.commit()
   add_members(groupname, members)
   conn = sqlite3.connect('db/topics.db')
   conn.cursor().execute('create table ' + groupname + ' (id integer primary key autoincrement, topic varchar(32) NOT NULL, username varchar(32) NOT NULL, details text, timestamp default CURRENT_TIMESTAMP)')
   conn.commit()

def update_profile(username, a_username, job, firm, department, image):
   conn = sqlite3.connect('db/vulnweb.db')
   conn.text_factory = str
   conn.cursor().execute('update users set name =?, job =?, firm =?, department =?, image= ? where name =?',(a_username, job, firm, department, image.read(), username))
   conn.commit()

def update_password(username, password):
   conn = sqlite3.connect('db/vulnweb.db')
   conn.text_factory = str
   conn.cursor().execute('update users set password= ? where name =?',(password, username))
   conn.commit()

def add_members(groupname, members):
   for member in members.split():
      if check_member(member, groupname):
         conn = sqlite3.connect('db/vulnweb.db')
         conn.cursor().execute('insert into groupMembers (username, groupname) values(?,?)',(member, groupname))
         conn.commit()
      else:
         pass

def remove_members(groupname, members):
   for member in members.split():
      if not check_member(member, groupname):
         conn = sqlite3.connect('db/vulnweb.db')
         conn.cursor().execute('delete from groupMembers where username = ? and groupname = ?',(member, groupname))
         conn.commit()
      else:
         pass

# for initializing topic
def update_topics(topicname, username, description, groupname):
   conn = sqlite3.connect('db/topics.db')
   if conn.cursor().execute('select * from ' + groupname + ' where topic =?', (topicname,)).fetchone() == None:
      conn.cursor().execute('insert into ' + groupname + ' (topic, username, details) values(?,?,?)',(topicname, username, description))
      conn.commit()
      conn = sqlite3.connect('db/vulnweb.db')
      conn.cursor().execute('insert into groupTopics (topic, groupname) values(?,?)',(topicname, groupname, ))
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
   conn = sqlite3.connect('db/vulnweb.db')
   result = []
   for group in conn.cursor().execute("select groupname, description from groups where groupname like '%" + word + "%'"):
      result.append(group)
   print result
   return result

def invite_members(groupname, username, members):
   for member in members.split():
      if check_member(member, groupname) and not check_user(member):
         conn = sqlite3.connect('db/vulnweb.db')
         conn.cursor().execute('insert into notifications (name, type, details) values(?, "invitation", "' + username + ' ' + groupname + '")',(member,))
         conn.commit()
      else:
         pass

def get_notifications(username):
   conn = sqlite3.connect('db/vulnweb.db')
   notifications = []
   for notification in  conn.cursor().execute('select * from notifications where name =?', (username,)):
      note = [i for i in notification]
      if notification[2] == "invitation":
         note[3] = "<a href='/group/" + notification[3].split()[1] + "'>Received invitaion from " + notification[3].split()[0] + "</a>"
      notifications.append(note)
   return notifications

def get_recently_update(username):
   conn = sqlite3.connect('db/vulnweb.db')
   query = 'select * from '
   for gname in conn.cursor().execute('select groupname from groupMembers where username = ?', (username,)):
      conn = sqlite3.connect('db/topics.db')
      query += gname[0] + ' union all select * from '
   query = query[:(len(query) - 24)] + 'order by timestamp limit 10'
   return conn.cursor().execute(query)

def check_user(username):
   conn = sqlite3.connect('db/vulnweb.db')
   uname = conn.cursor().execute('select * from users where name =?',(username,))
   if uname.fetchone() == None:
      return True
   else:
      return False

def check_member(username, groupname):
   conn = sqlite3.connect('db/vulnweb.db')
   uname = conn.cursor().execute('select * from groupMembers where username =? and groupname =?',(username, groupname,))
   if uname.fetchone() == None:
      return True
   else:
      return False
