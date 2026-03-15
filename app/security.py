import re
from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    # Turn a plain password into a secure hash.
    return generate_password_hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    # Check whether the entered password matches the saved hash.
    return check_password_hash(password_hash, password)

def validate_username(username: str) -> bool:
    # Allow only simple usernames with safe characters.
    return bool(username) and bool(re.fullmatch(r"[A-Za-z0-9_.-]{3,30}", username))

def validate_password(password: str) -> bool:
    # Require a minimum length first.
    if not password or len(password) < 8:
        return False
    # Check for uppercase, lowercase, and number characters.
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit
