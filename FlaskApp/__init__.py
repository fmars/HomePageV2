from flask import Flask, render_template, Markup
from werkzeug.routing import BaseConverter
import os
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
    return render_template("HomepageMe.html")
	
@app.route("/write")
def render_homepage_write():
    path = "/var/www/HomePageV2/FlaskApp/static/write"
    file_tree = read_file_tree(path)
    app.logger.debug(file_tree)
    return render_template("HomepageWrite.html", file_tree = file_tree)
    
@app.route("/read")
def render_homepage_read():
    return render_template("HomepageRead.html")    

app.debug = True
    
if __name__ == "__main__":
    app.run(debug=True)
    
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