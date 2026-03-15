from pathlib import Path
import sqlite3

db_path = Path("secure_app.db")
conn = sqlite3.connect(db_path)
conn.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    '''
)
conn.commit()
conn.close()
print(f"Database initialized successfully at {db_path.resolve()}")
