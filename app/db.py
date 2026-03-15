import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        db_path = current_app.config["DATABASE_PATH"]
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_schema():
    db = get_db()
    db.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
        '''
    )
    db.commit()

def init_app(app):
    @app.before_request
    def ensure_schema():
        init_schema()

    app.teardown_appcontext(close_db)
