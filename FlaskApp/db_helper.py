import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from __init__ import app as app

def connect_db(dbPath):
    """Connects to the specific database."""
    rv = sqlite3.connect(dbPath)
    rv.row_factory = sqlite3.Row
    return rv

def get_db(dbPath):
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db(dbPath)
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
