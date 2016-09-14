from flask import Flask, render_template, Markup
from flask import request, redirect
from flask import session, url_for,abort, flash
from werkzeug.routing import BaseConverter
from contextlib import closing
import logging
import os
import sys
import libs.db_helper as db_helper
import libs.file_helper as file_helper
import libs.login_helper as login_helper
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/app.db'),
    WRITE=os.path.join(app.root_path, 'static/write'),
    DEBUG=True,
    SECRET_KEY='development key',
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter

@app.route("/")
@app.route("/me")
def homepage_me():
    app.logger.debug("me rendered")
    return render_template("HomepageMe.html")
	
@app.route("/write")
def homepage_write():
    app.logger.debug("write rendered")
    file_tree = file_helper.read_file_tree(app.config['WRITE'])
    return render_template("HomepageWrite.html", file_tree = file_tree)
    
@app.route("/read")
def homepage_read():
    app.logger.debug("read rendered")
    return render_template("HomepageRead.html")    

@app.route("/xtodo", methods=['GET', 'POST'])
def homepage_xtodo():
    app.logger.debug("xtodo rendered")
    if request.method == 'POST':
        user = session['user']
        todo = request.form['todo']
        days = request.form['days']
        detail = request.form['detail']
        level = request.form['level']
        email = request.form['email']
        auto_fail = request.form['autoFail']
        app.logger.debug(str(request.form))
        if user and todo:
            db_helper.xtodo_store_entry(app.config['DATABASE'], 
                    user, todo, days, detail,
                    level, email, auto_fail)
            flash("Your todo added")
    entries = db_helper.xtodo_get_entries(app.config['DATABASE'])
    user_icon_path = 'static/img/user_photos/'
    return render_template("TODO/Todo.html", entries=entries, 
            user_icon_path=user_icon_path)

@app.route("/xtodo_update_res", methods=['GET', 'POST'])
def xtodo_update_res():
    app.logger.debug("xtodo update res")
    id = request.form['id']
    user = request.form['user']
    if not 'user' in session or user != session['user']:
        flash("don't change others todo")
    elif not id:
        flash("please click again")
    else:
        id = int(id)
        res = request.form['res']
        db_helper.xtodo_update_res(app.config['DATABASE'], id, res)
    return redirect("xtodo")
   
@app.route("/contact")
def homepage_contact():
    app.logger.debug("contact rendered")
    comments = db_helper.get_comments(app.config['DATABASE'])
    return render_template("HomepageContact.html", comments=comments)
    
@app.route("/comment", methods = ["POST"])
def comment():
    app.logger.debug("comment rendered")
    name = request.form["name"]
    if not name:
        name = "anonymous"
    content = request.form["content"]
    if not content:
        flash("What you wanna me to store, empty?")
    else:
        db_helper.store_comment(app.config['DATABASE'], name, content)
        flash("Comment posted.")
    return redirect("contact")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if login_helper.login_check(username, password):
            session['logged_in'] = True
            session['user'] = request.form['username']
            flash('You were logged in')
            app.logger.debug(username + " logged in")
            return redirect(url_for('homepage_me'))
        else:
            error = "Username/password incorrect"
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    flash('You were logged out')
    return redirect(request.referrer)

# use git pull to synch content in aws host with github
# which allows to update website server without login into
# which can be convenient.
@app.route('/pull')
def pull():
    app.logger.debug('git pull request received')
    PATH = '/var/www/HomePageV2'
    os.chdir(PATH)
    CMD = 'git pull --verbose'
    os.system(CMD)
    return redirect('/')

@app.teardown_appcontext
def close_db(error):
    db_helper.close_db(error)

if __name__ == "__main__":
    app.run(debug=True)
