import sqlite3
from flask import current_app, g

def get_db():
    if "db" not in g:
        # Open one database connection for the current request.
        db_path = current_app.config["DATABASE_PATH"]
        g.db = sqlite3.connect(db_path)
        # Return rows like dictionaries so columns can be read by name.
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    # Close the connection after the request ends.
    db = g.pop("db", None)
    if db is not None:
        db.close()

def init_schema():
    db = get_db()
    # Create the users table if it does not exist yet.
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
        # Make sure the table exists before handling a request.
        init_schema()

    app.teardown_appcontext(close_db)
