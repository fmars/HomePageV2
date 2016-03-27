from flask import Flask, render_template, Markup
from flask import request, redirect
from flask import session, url_for,abort, flash
from werkzeug.routing import BaseConverter
from contextlib import closing
import logging
import os
import sys
import db_helper
import file_helper
import login_helper
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

@app.route("/xtodo")
def homepage_xtodo():
    app.logger.debug("xtodo rendered")
    dbPath = os.path.join(app.root_path, 'db/sm.db')
    db = db_helper.get_db(dbPath)
    cur = db.execute('select content, time, res from entries order by id desc')
    entries = cur.fetchall()
    app.logger.debug(str(entries))
    return render_template("HomepageXtodo.html", entries=entries)
   
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
    flash('You were logged out')
    return redirect(url_for('homepage_me'))

@app.teardown_appcontext
def close_db(error):
    db_helper.close_db(error)

if __name__ == "__main__":
    app.run(debug=True)
