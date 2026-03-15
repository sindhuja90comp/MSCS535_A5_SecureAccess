from pathlib import Path
import sqlite3

# Create the SQLite database file in the project folder.
db_path = Path("secure_app.db")
conn = sqlite3.connect(db_path)
# Create the users table if it is not already there.
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
# Show where the database file was created.
print(f"Database initialized successfully at {db_path.resolve()}")
