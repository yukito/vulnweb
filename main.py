#!/usr/bin/env python
# coding:utf-8

from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response
import uuid
import lib.models
from lib.session import ManageSession
from lib.manage_user import is_correct_user

app = Flask(__name__)

session_list = {}

@app.route('/')
def index():
   if request.cookies.get('sessionid') in session_list:
      uid = request.cookies.get('sessionid')
      return render_template('index.html', user = session_list[uid])
   return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      print username, password
      if is_correct_user(username, password):
         uid = str(uuid.uuid4())
         session_list[uid] = ManageSession(username)
         content = redirect(url_for('index'))
         response = make_response(content)
         response.set_cookie('sessionid', value = uid, path = '/', httponly = True)
         return response
   return render_template('login.html')

@app.route('/logout')
def logout():
   uid = request.cookies.get('sessionid')
   session_list.pop(uid)
   return redirect(url_for('index'))

@app.route('/group/<group_name>')
def group_summary(group_name):
   if request.cookies.get('sessionid') in session_list:
      members, boards = get_summary_of(group_name)
      return render_template('group.html', members = members, boards = boards)
   return redirect(url_for('login'))

app.config['SECRET_KEY'] = str(uuid.uuid4())

if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=80)
