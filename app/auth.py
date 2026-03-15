from sqlite3 import IntegrityError
from .db import get_db
from .security import hash_password, verify_password, validate_username, validate_password

def register_user(username: str, password: str):
    if not validate_username(username):
        return False, "Username must be 3-30 characters and contain only letters, numbers, _, ., or -."
    if not validate_password(password):
        return False, "Password must be at least 8 characters and include uppercase, lowercase, and a number."

    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        db.commit()
        return True, "User registered securely."
    except IntegrityError:
        return False, "Username already exists."

def authenticate_user(username: str, password: str):
    db = get_db()
    user = db.execute(
        "SELECT id, username, password_hash FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    if user and verify_password(user["password_hash"], password):
        return True, {"id": user["id"], "username": user["username"]}
    return False, None

def fetch_user(username: str):
    db = get_db()
    user = db.execute(
        "SELECT id, username FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    return dict(user) if user else None
