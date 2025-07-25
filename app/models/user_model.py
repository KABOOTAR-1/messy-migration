import sqlite3
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DB_PATH'])
        g.db.row_factory = sqlite3.Row
    return g.db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    db.commit()

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def user_to_dict(user_row):
    return {
        'id': user_row['id'],
        'name': user_row['name'],
        'email': user_row['email']
    }
