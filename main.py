#!/usr/bin/env python
# coding:utf-8

from flask import Flask, session, redirect, url_for, escape, request, render_template, make_response, Response
import uuid
import lib.models
from lib.session import ManageSession
from lib.manage_user import is_correct_user
from lib.auth import requires_auth

app = Flask(__name__)

session_list = {}

@app.before_request
def csrf_protection():
   if request.method == "POST" and request.cookies.get('sessionid') in session_list:
      uid = request.cookies.get('sessionid')
      token = session_list[uid].csrf_token
      if token != str(request.form['_csrf_token']):
         return "Error 403", 403

@app.before_request
#@requires_auth
def is_loggedin():
   if request.path == '/login':
      pass
# issue: if user logged in, it should be directed toward index page.
#      uid = request.cookies.get('sessionid')
#      if session_list[uid].loggedin:
#         return redirect(url_for('index'))
   elif 'static' in request.path: #or request.path == '/signup':
      pass
   elif not request.cookies.get('sessionid') in session_list:
      return redirect(url_for('login'))
   elif request.path == '/signup':
      pass
   else:
      uid = request.cookies.get('sessionid')
      if not session_list[uid].loggedin:
         return redirect(url_for('login'))

@app.after_request
def set_nocache(response):
   response.headers['Cache-Control'] = 'no-cache'
   return response

@app.route('/')
def index():
   uid = request.cookies.get('sessionid')
   update = lib.models.get_recently_update(session_list[uid].username)
   return render_template('index.html', user = session_list[uid], updates = update)

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
      uid = request.cookies.get('sessionid')
      username = request.form['username']
      password = request.form['password']
      if is_correct_user(username, password):
         session_list.pop(uid)
         uid = str(uuid.uuid4())
         session_list[uid] = ManageSession(username, True)
         content = redirect(url_for('index'))
         response = make_response(content)
         response.set_cookie('sessionid', value = uid, path = '/', httponly = True)
         return response
      else:
         return render_template('login.html', anti_csrf_token = session_list[uid].csrf_token)
   else:
      uid = request.cookies.get('sessionid')
      return render_template('login.html', anti_csrf_token = session_list[uid].csrf_token)

@app.route('/logout')
def logout():
   uid = request.cookies.get('sessionid')
   session_list.pop(uid)
   return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
   if request.method == 'POST':
      username = request.form['username']
      password = request.form['password']
      if lib.models.update_users(username, password):
         return render_template('registered.html')
      else:
         return render_template('signup.html', message = "This username already exist.")
   return render_template('signup.html')

@app.route('/group/<group_name>')
def group_summary(group_name):
   if lib.models.check_group_exist(group_name):
      members, topics = lib.models.get_summary_of(group_name)
      uid = request.cookies.get('sessionid')
      return render_template('group.html', groupname = group_name, members = members, topics = topics, user = session_list[uid])
   else:
      return "404 Not Found", 404

@app.route('/management/<group_name>')
def management_group(group_name):
   if lib.models.check_group_exist(group_name):
      configuration, members = lib.models.get_group_config(group_name)
      uid = request.cookies.get('sessionid')
      return render_template('mgroup.html', groupname = group_name, config = configuration, members = members, user = session_list[uid])
   else:
      return "404 Not Found", 404

@app.route('/create_group', methods=['GET', 'POST'])
def create_group():
   uid = request.cookies.get('sessionid')
   if request.method == 'POST':
      groupname = request.form['groupname']
      description = request.form['description']
      members = request.form['members']
      lib.models.update_groups(groupname, description, members)
      session_list[uid] = ManageSession(session_list[uid].username, True)
      return render_template('index.html', user = session_list[uid])
   return render_template('create_group.html', user = session_list[uid])

@app.route('/create_topic/<group_name>', methods=['GET', 'POST'])
def create_topic(group_name):
   uid = request.cookies.get('sessionid')
   if request.method == 'POST':
      topicname = request.form['topicname']
      description = request.form['description']
      if lib.models.update_topics(topicname, session_list[uid].username, description, group_name):
         return redirect('/group/' + group_name)
      else:
         return render_template('create_topic.html', user = session_list[uid], groupname = group_name, flag = True)
   return render_template('create_topic.html', user = session_list[uid], groupname = group_name)

@app.route('/group/<group_name>/<topic_name>', methods=['GET', 'POST'])
def board(group_name, topic_name):
   uid = request.cookies.get('sessionid')
   if request.method == 'POST':
      lib.models.insert_articles(group_name, topic_name, request.form)
   posts = lib.models.get_posts_of(group_name, topic_name)
   return render_template('board.html', groupname = group_name, posts = posts, topicname = topic_name, description = posts[0], user = session_list[uid])

@app.route('/article/<group_name>/<topic_name>')
def get_article(group_name, topic_name):
   uid = request.cookies.get('sessionid')
   posts = lib.models.get_posts_of(group_name, topic_name)
   return render_template('article.html', groupname = group_name, posts = posts[1:], topicname = topic_name, user = session_list[uid])

@app.route('/edit/<group_name>/<topic_name>', methods=['POST'])
def edit_article(group_name, topic_name):
   uid = request.cookies.get('sessionid')
   article_id = request.form['article_id'].split('_')[1]
   posts = lib.models.update_article(group_name, request.form['post_detail'], article_id)
   return redirect('/group/' + group_name + '/' + topic_name)

@app.route('/delete/<group_name>/<topic_name>', methods=['POST'])
def delete_article(group_name, topic_name):
   uid = request.cookies.get('sessionid')
   article_id = request.form['article_id'].split('_')[1]
   lib.models.delete_article(group_name, article_id)
   return '{"result": True}'

@app.route('/search/group', methods=['GET', 'POST'])
def search_group():
   uid = request.cookies.get('sessionid')
   if request.method == 'POST':
      word = request.form['search_word']
      result = lib.models.search_group(word)
      if result:
         return render_template('gsearch_result.html', result = result)
      else:
         return ""
   return render_template('gsearch.html', user = session_list[uid])

@app.route('/add_member/<group_name>', methods=['POST'])
def add_member(group_name):
   uid = request.cookies.get('sessionid')
   lib.models.add_members(group_name, session_list[uid].username)
   session_list[uid] = ManageSession(session_list[uid].username, True)
   return redirect('/group/' + group_name)

@app.route('/leave_group/<group_name>', methods=['POST'])
def leave_group(group_name):
   uid = request.cookies.get('sessionid')
   lib.models.remove_members(group_name, session_list[uid].username)
   session_list[uid] = ManageSession(session_list[uid].username, True)
   return redirect('/group/' + group_name)

@app.route('/invite_member/<group_name>', methods=['GET', 'POST'])
def invite_member(group_name):
   uid = request.cookies.get('sessionid')
   if request.method == 'POST':
      members = request.form['members']
      lib.models.invite_members(group_name, session_list[uid].username, members)
      return redirect('/group/' + group_name)
   return render_template('invite_member.html', groupname = group_name, user = session_list[uid])

@app.route('/edit_profile')
def get_edit_profile():
   uid = request.cookies.get('sessionid')
   return render_template('edit_profile.html', user = session_list[uid])

@app.route('/edit/password', methods=['GET', 'POST'])
def change_password():
   uid = request.cookies.get('sessionid')
   if request.method == 'POST':
      username = session_list[uid].username
      password = request.form['c_password']
      if is_correct_user(username, password):
         new_password = request.form['n_password']
         lib.models.update_password(username, new_password)
         return "True"
      else:
         return "False"
   return render_template('change_password.html', user = session_list[uid])

@app.route('/edit/profile', methods=['GET', 'POST'])
def edit_profile():
   uid = request.cookies.get('sessionid')
   if request.method == 'POST':
      image = request.files['image']
      username = request.form['username']
      job = request.form['job']
      firm = request.form['firm']
      department = request.form['department']
      lib.models.update_profile(session_list[uid].username, username, job, firm, department, image.stream)
      return redirect(url_for('index'))
   return render_template('eprofile.html', user = session_list[uid])

@app.route('/member/<user_name>')
def show_profile(user_name):
   uid = request.cookies.get('sessionid')
   profile = lib.models.get_profile(user_name)
   return render_template('profile.html', profile = profile, user = session_list[uid])

@app.route('/image/<user_id>')
def send_image(user_id):
   data = lib.models.get_image(user_id)
   fp = open("tmp/.tmp", "w+b")
   if data:
      fp.write(data)   
   else:
      fp.close()
      redirect('/static/sample/Lenna.png')
   return Response(data, mimetype ='image/png')

@app.route('/check_user')
def check_user():
   if lib.models.check_user(request.args.get('username')):
      return True
   else:
      return False

@app.route('/get_token')
def get_token():
   return generate_csrf_token()

def generate_csrf_token():
   uid = request.cookies.get('sessionid')
   session_list[uid].csrf_token = str(uuid.uuid4())
   return session_list[uid].csrf_token

app.config['SECRET_KEY'] = str(uuid.uuid4())
app.jinja_env.globals['csrf_token'] = generate_csrf_token

if __name__ == '__main__':
   app.debug = True
   app.run(host='0.0.0.0', port=80)
