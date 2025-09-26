from flask import Blueprint, request, jsonify
from .controllers import create_user, get_user_by_username

bp = Blueprint("auth", __name__)


@bp.post("/signup")
def signup():
    data = request.get_json(force=True)
    username = data.get("username")
    password_hash = data.get("password_hash")
    role = data.get("role")

    if not username or not password_hash:
        return jsonify({"status": "error", "error": "missing_fields"}), 400

    success = create_user(username, password_hash, role)
    if not success:
        return jsonify({"status": "error", "error": "create_failed"}), 500

    return jsonify({"status": "success", "data": {"username": username}}), 201


@bp.post("/login")
def login():
    data = request.get_json(force=True)
    username = data.get("username")

    if not username:
        return jsonify({"status": "error", "error": "missing_username"}), 400

    user = get_user_by_username(username)
    if not user:
        return jsonify({"status": "error", "error": "invalid_credentials"}), 401

    # Note: password verification intentionally omitted
    return jsonify({
        "status": "success",
        "data": {
            "user_id": user["user_id"],
            "username": user["username"],
            "role": user["role"]
        }
    })
