import os
from dotenv import load_dotenv

# Load values from a local .env file if one exists.
load_dotenv()

class Config:
    # Use environment values when available, otherwise fall back to defaults.
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    DATABASE_PATH = os.getenv("DATABASE_PATH", "secure_app.db")
    JSON_SORT_KEYS = False
