#!/usr/bin/env python
# coding:utf-8

from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response
import uuid
import lib.models
from lib.session import ManageSession
from lib.manage_user import is_correct_user

app = Flask(__name__)

session_list = {}

@app.before_request
def csrf_protection():
   if request.method == "POST":
      uid = request.cookies.get('sessionid')
      token = session_list[uid].csrf_token
      if token != str(request.form['_csrf_token']):
         abort(403)

@app.route('/')
def index():
   if request.cookies.get('sessionid') in session_list:
      uid = request.cookies.get('sessionid')
      return render_template('index.html', user = session_list[uid])
   return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
   if not request.cookies.get('sessionid') in session_list:
      uid = str(uuid.uuid4())
      session_list[uid] = ManageSession()
      content = render_template('login.html', anti_csrf_token = session_list[uid].csrf_token)
      response = make_response(content)
      response.set_cookie('sessionid', value = uid, path = '/', httponly = True)
      return response
   elif request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      if is_correct_user(username, password):
         uid = request.cookies.get('sessionid')
         session_list.pop(uid)
         uid = str(uuid.uuid4())
         session_list[uid] = ManageSession(username)
         content = redirect(url_for('index'))
         response = make_response(content)
         response.set_cookie('sessionid', value = uid, path = '/', httponly = True)
         return response
   return render_template('login.html', anti_csrf_token = session_list[uid].csrf_token)

@app.route('/logout')
def logout():
   uid = request.cookies.get('sessionid')
   session_list.pop(uid)
   return redirect(url_for('index'))

@app.route('/signup')
def signup():
   return render_template('signup.html')

@app.route('/group/<group_name>')
def group_summary(group_name):
   if request.cookies.get('sessionid') in session_list:
      members, topics = lib.models.get_summary_of(group_name)
      return render_template('group.html', groupname = group_name, members = members, topics = topics)
   return redirect(url_for('login'))

@app.route('/group/<group_name>/<topic_name>', methods=['GET', 'POST'])
def board(group_name, topic_name):
   if request.cookies.get('sessionid') in session_list:
      uid = request.cookies.get('sessionid')
      if request.method == 'POST':
         lib.models.insert_articles(group_name, topic_name, request.form)
      posts = lib.models.get_posts_of(group_name, topic_name)
      return render_template('board.html', groupname = group_name, posts = posts, topicname = topic_name, user = session_list[uid])
   return redirect(url_for('login'))

def generate_csrf_token():
   uid = request.cookies.get('sessionid')
   session_list[uid].csrf_token = str(uuid.uuid4())
   return session_list[uid].csrf_token

app.config['SECRET_KEY'] = str(uuid.uuid4())
app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=80)
