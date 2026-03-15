from flask import jsonify, request
from .auth import register_user, authenticate_user, fetch_user

def register_routes(app):
    @app.get("/")
    def home():
        return jsonify({
            "message": "SecureAccess is running over HTTPS.",
            "endpoints": ["/register", "/login", "/user/<username>"]
        })

    @app.post("/register")
    def register():
        data = request.get_json(silent=True) or {}
        username = data.get("username", "").strip()
        password = data.get("password", "")

        success, message = register_user(username, password)
        status = 201 if success else 400
        return jsonify({"success": success, "message": message}), status

    @app.post("/login")
    def login():
        data = request.get_json(silent=True) or {}
        username = data.get("username", "").strip()
        password = data.get("password", "")

        success, user = authenticate_user(username, password)
        if success:
            return jsonify({"success": True, "message": "Login successful.", "user": user})
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

    @app.get("/user/<username>")
    def get_user(username):
        user = fetch_user(username)
        if user:
            return jsonify({"success": True, "user": user})
        return jsonify({"success": False, "message": "User not found."}), 404
