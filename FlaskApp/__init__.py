from flask import Flask, render_template, Markup
from flask import request, redirect
from flask import session, g, url_for,abort, flash
from werkzeug.routing import BaseConverter
from contextlib import closing
import os
import time
import logging
import sqlite3
import sys
import db_helper
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db/app.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]
app.url_map.converters['regex'] = RegexConverter

@app.route("/")
@app.route("/me")
def render_homepage_me():
    app.logger.debug("me rendered")
    return render_template("HomepageMe.html")
	
@app.route("/write")
def render_homepage_write():
    app.logger.debug("write rendered")
    path = "/var/www/HomePageV2/FlaskApp/static/write"
    file_tree = read_file_tree(path)
    return render_template("HomepageWrite.html", file_tree = file_tree)
    
@app.route("/read")
def render_homepage_read():
    app.logger.debug("read rendered")
    return render_template("HomepageRead.html")    

@app.route("/xtodo")
def render_homepage_xtodo():
    app.logger.debug("xtodo rendered")
    dbPath = os.path.join(app.root_path, 'db/sm.db')
    db = db_helper.get_db(dbPath)
    cur = db.execute('select content, time, res from entries order by id desc')
    entries = cur.fetchall()
    app.logger.debug(str(entries))
    return render_template("HomepageXtodo.html", entries=entries)
   
@app.route("/contact")
def render_homepage_contact():
    app.logger.debug("contact rendered")
    comments = get_comments()
    return render_template("HomepageContact.html", comments=comments)
    
@app.route("/comment", methods = ["POST"])
def comment():
    app.logger.debug("comment rendered")
    name = request.form["name"]
    if not name:
        name = "anonymous"
    content = request.form["content"]
    store_comment(name, content)
    return redirect("contact")

app.debug = True
    
if __name__ == "__main__":
    app.run(debug=True)
    
def get_comments():
    db = db_helper.get_db(app.config['DATABASE'])
    sql = 'select name, content, date from comments order by id desc'
    cur = db.execute(sql)
    entries = cur.fetchall()
    return entries
   
def store_comment(name, content):
    conn = sqlite3.connect("/var/www/HomePageV2/FlaskApp.db")
    cur = conn.cursor()
    # Create table
    c.execute('''CREATE TABLE stocks
                         (date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

    date = time.strftime("%x")
    data = "@@@".join([name, content, date])
    delimeter = "###"
    db_path = "/var/www/HomePageV2/FlaskApp/static/comments/comments"
    with open(db_path, "a") as file:
        if os.stat(db_path).st_size != 0:
            file.write(delimeter)
        file.write(data)

    
def read_file_tree(path):
    fileName = path
    baseName = os.path.basename(fileName)
    showName = ""
    showDate = ""
    num = 0
    if baseName != "write":
        if os.path.isdir(path):
            if len(baseName.split("-")) != 3:
                return dict(baseName=baseName, showName="error_dir", showDate="", children=[], num = 0)
            [num, showName, showDate] = baseName.split("-")
            showName = showName.replace("_", " ")
        else:
            noExtname = baseName[:-5]
            if len(noExtname.split("-")) != 3:
                return dict(baseName=baseName, showName="error_file", showDate="", children=[], num = 0)
            [num, showName, showDate] = noExtname.split("-")
        
    tree = dict(baseName=baseName, showName=showName, showDate=showDate, children=[], num=int(num))
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            if len(name.split("-")) == 3:                
                fn = os.path.join(path, name)
                tree['children'].append(read_file_tree(fn))
    if tree["children"]:
        tree['children'] = sorted(tree['children'], key = lambda item: item["num"])
    return tree
