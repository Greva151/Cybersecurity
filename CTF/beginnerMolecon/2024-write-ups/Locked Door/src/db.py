import sqlite3
from flask import current_app, g

DBPATH = 'file:/database.db?mode=ro'

def get_db():

    if 'db' not in g:
        g.db = sqlite3.connect(DBPATH, uri=True)
        g.db.row_factory = sqlite3.Row
        #with current_app.open_resource('schema.sql') as f:
        #    g.db.executescript(f.read().decode('utf8'))

    return g.db

def close_db(e=None):

    db = g.pop('db', None)

    if db is not None:
        db.close()
    

def query_db(query, args=(), one=False):

    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()

    return (rv[0] if rv else None) if one else rv

