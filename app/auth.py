from sqlite3 import IntegrityError
from .db import get_db
from .security import hash_password, verify_password, validate_username, validate_password

def register_user(username: str, password: str):
    # Check the username before saving it.
    if not validate_username(username):
        return False, "Username must be 3-30 characters and contain only letters, numbers, _, ., or -."
    # Check the password rules before saving it.
    if not validate_password(password):
        return False, "Password must be at least 8 characters and include uppercase, lowercase, and a number."

    db = get_db()
    try:
        # Use placeholders so user input is treated as data, not SQL code.
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        db.commit()
        return True, "User registered securely."
    except IntegrityError:
        # This happens when the username is already in the table.
        return False, "Username already exists."

def authenticate_user(username: str, password: str):
    db = get_db()
    # Look up the user with a parameterized query.
    user = db.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    # Compare the entered password with the saved password hash.
    if user and verify_password(user["password_hash"], password):
        return True, {"id": user["id"], "username": user["username"]}
    return False, None

def fetch_user(username: str):
    db = get_db()
    # Return basic user data without exposing the password hash.
    user = db.execute(
        "SELECT id, username FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    return dict(user) if user else None
