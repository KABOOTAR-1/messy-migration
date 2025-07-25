from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.user_model import get_db
import sqlite3

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)  # force ensures it's parsed as JSON
    except Exception:
        return jsonify({"msg": "Invalid or malformed JSON"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400

    try:
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE email = ?", (email,)).fetchone()
    except sqlite3.Error as e:
        return jsonify({"msg": "Database error", "error": str(e)}), 500

    if user is None:
        return jsonify({"msg": "User not found"}), 404

    try:
        if check_password_hash(user["password"], password):
            token = create_access_token(identity=user["id"])
            return jsonify(access_token=token), 200
        else:
            return jsonify({"msg": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"msg": "Password verification failed", "error": str(e)}), 500
