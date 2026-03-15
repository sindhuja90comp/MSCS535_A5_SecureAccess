from flask import Flask
from .config import Config
from .db import init_app
from .routes import register_routes

def create_app():
    # Create the main Flask app object.
    app = Flask(__name__)
    # Load settings such as the secret key and database path.
    app.config.from_object(Config)
    # Connect database helpers and URL routes to the app.
    init_app(app)
    register_routes(app)
    return app
