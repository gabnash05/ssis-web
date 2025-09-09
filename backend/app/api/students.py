from flask import Blueprint, request, jsonify

bp = Blueprint("students", __name__)

@bp.route("/", methods=["GET"])
def list_students():
    """Simple list endpoint supporting query params: page, per_page, sort_by, order, q"""
