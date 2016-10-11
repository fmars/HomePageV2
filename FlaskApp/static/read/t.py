# -*- coding: utf-8 -*-
import json
e1 = {
    'id': 1,
    'title': u'浪潮之巅',
    'date': '03/2015',
    'comments': ['What is the next technical revolution?'],
}

e2 = {
    'id': 2,
    'title': '链接、装载与库',
    'date': '07/2015',
    'comments': ['Everything is CPU, Memory and I/Os'],
}


e3 = {
    'id': 3,
    'title': 'Effective Modern C++: Improve Your Use of C++11 and C++14',
    'date': '09/2015',
    'comments': ['C++11 is so much amazing so much awesome. And I think it\'s time to switch to another one, maybe Python, for most of the cases.'],
}

e4 = {
    'id': 4,
    'title': 'Learn Vimscript the Hard Way',
    'date': '11/2015',
    'comments': ['<a target="_blank" href="https://github.com/fmars/reasier">Reasier (make Read easier)</a>'],
}

e5 = {
    'id': 5,
    'title': 'Flask-Python',
    'date': '01/2016',
    'comments': ['<a target="_blank" href="https://github.com/fmars/HomePageV2">HomePageV2</a>'],
}

e6 = {
    'id': 6,
    'title': '长生剑， 孔雀翎， 碧玉刀， 多情环， 霸王枪， 拳头',
    'date': '02/2016',
    'comments': ['所以我说的第二种武器，并不是孔雀翎，而是信心！'],
}


e7 = {
    'id': 7,
    'title': 'MapReduce: Simplified Data Processing on Large Clusters',
    'date': '03/2016',
    'comments': ['In a large distributed system, failure on some particular single server, master for example, is unlikely and which may not need to be taken care of specifically. However server failure happened to normal server (network, hardware issue) should be handled as a common scenario.'],
}


e8 = {
    'id': 8,
    'title': 'Learn how Python works and write idiomatic Python',
    'date': '03/2016',
    'comments': [
        '<a href="https://jeffknupp.com/blog/2013/02/14/drastically-improve-your-python-understanding-pythons-execution-model/">Understanding Python\'s execution model</a>',
        '<a href="https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/">Pythonic Object Oriented Language</a>',
        '<a href="http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/">Decorator!</a>',
        '<a href="http://www.tutorialspoint.com/python/python_classes_objects.htm">Class</a>',
        '<a href="https://jeffknupp.com/blog/2014/06/18/improve-your-python-python-classes-and-object-oriented-programming/">Class</a>',
        '<a href="http://flask.pocoo.org/docs/0.10/tutorial/">Flask sqlite database</a>',
        '<a href="https://docs.python.org/2/tutorial/modules.html">Module</a>',
    ]
}


e9 = {
    'id': 9,
    'title': 'Regex basics',
    'date': '04/2016',
    'comments': [
        'http://www.regular-expressions.info/tutorial.html',
        'http://www.zytrax.com/tech/web/regex.htm',
    ],
}


e10 = {
    'id': 10,
    'title': 'Design Patter',
    'date': '10/2016',
    'comments': ['Factory'],
}

data = [e1,e2,e3,e4,e5,e6,e7,e8,e9,e10]
with open('read.json','w') as output:
    json.dump(data, output)
