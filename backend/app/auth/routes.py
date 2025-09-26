from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    jwt_required,
    get_jwt_identity,
)
from ..utils.route_utils import make_response
from .services import create_user, authenticate_user

bp = Blueprint("auth", __name__)


@bp.post("/signup")
def signup():
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not email or not password:
            return make_response({"status": "error", "error": "missing_fields"}, 400)

        success = create_user(email, password, role)
        if not success:
            return make_response({"status": "error", "error": "create_failed"}, 500)

        return make_response({"status": "success", "data": {"email": email}}, 201)

    except Exception as e:
        return make_response({"status": "error", "error": str(e)}, 500)


@bp.post("/login")
def login():
    try:
        data = request.get_json(force=True)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return make_response({"status": "error", "error": "missing_fields"}, 400)

        user = authenticate_user(email, password)
        if not user:
            return make_response({"status": "error", "error": "invalid_credentials"}, 401)

        access_token = create_access_token(identity=user)

        resp = make_response({"status": "success", "data": user}, 200)
        set_access_cookies(resp, access_token)
        return resp

    except Exception as e:
        return make_response({"status": "error", "error": str(e)}, 500)


@bp.post("/logout")
def logout():
    try:
        resp = make_response({"status": "success", "message": "logged_out"}, 200)
        unset_jwt_cookies(resp)
        return resp
    except Exception as e:
        return make_response({"status": "error", "error": str(e)}, 500)


@bp.get("/me")
@jwt_required()
def me():
    try:
        identity = get_jwt_identity()
        return make_response({"status": "success", "data": identity}, 200)
    except Exception as e:
        return make_response({"status": "error", "error": str(e)}, 500)
