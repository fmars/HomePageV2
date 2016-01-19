from flask import Flask, render_template, Markup
from werkzeug.routing import BaseConverter
import os
import logging
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

app.debug = True
    
if __name__ == "__main__":
    app.run(debug=True)
    
def read_file_tree(path):
    fileName = path
    baseName = os.path.basename(fileName)
    showName = ""
    showDate = ""
    if baseName != "write":
        if os.path.isdir(path):
            if len(baseName.split("-")) != 2:
                return dict(baseName=baseName, showName="error", showDate="", children=[])
            [showName, showDate] = baseName.split("-")
            showName = showName.replace("_", " ")
        else:
            noExtname = baseName[:-5]
            if len(noExtname.split("-")) != 2:
                return dict(baseName=baseName, showName="error", showDate="", children=[])
            [showName, showDate] = noExtname.split("-")
        
    tree = dict(baseName=baseName, showName=showName, showDate=showDate, children=[])
    try: lst = os.listdir(path)
    except OSError:
        pass #ignore errors
    else:
        for name in lst:
            fn = os.path.join(path, name)
            tree['children'].append(read_file_tree(fn))
    def cmp(showDate):
        app.logger.debug(showDate)
        [month, year] = showDate.split(".")
        return year + month
    tree['children'] = sorted(tree['children'], key = lambda item: cmp(item["showDate"]))
    return tree