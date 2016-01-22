from flask import Flask, render_template, Markup
from flask import request, redirect
from werkzeug.routing import BaseConverter
import os
import time
import logging
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)

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
    delimeter = "###"
    db_path = "/var/www/HomePageV2/FlaskApp/static/comments/comments"
    data = ""
    with open(db_path, "r") as file:
        data = file.read()
    
    parts = data.split(delimeter)
    app.logger.debug(parts)
    comments = []
    for part in parts:
        if len(part.split("@@@")) != 3:
            continue
        [name, content, date] = part.split("@@@")
        pair = dict(name=name, content=content, date=date)
        comments.append(pair)
    app.logger.debug(comments)
    return comments
    
def store_comment(name, content):
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