import os
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
