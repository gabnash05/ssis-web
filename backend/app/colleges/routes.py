from flask import Blueprint, request, jsonify
from typing import Dict, Any
from .helpers import (
    list_colleges, count_colleges, create_college, update_college, delete_college
)

bp = Blueprint("colleges", __name__)


@bp.get("/")
def list_colleges_route():
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = max(min(int(request.args.get("per_page", 50)), 100), 1)
    except ValueError:
        return jsonify({"status": "error", "error": "invalid_pagination"}), 400

    sort_by = request.args.get("sort_by", "college_code")
    order = request.args.get("order", "ASC").upper()
    q = request.args.get("q")

    allowed_sort = {"college_code", "college_name"}
    if sort_by not in allowed_sort:
        sort_by = "college_code"
    if order not in {"ASC", "DESC"}:
        order = "ASC"

    filters = ""
    params: Dict[str, Any] = {}
    if q:
        filters = "WHERE (college_code ILIKE :q OR college_name ILIKE :q)"
        params["q"] = f"%{q}%"

    total = count_colleges(filters, params)
    offset = (page - 1) * per_page
    rows = list_colleges(filters, params, sort_by, order, per_page, offset)

    return jsonify({
        "status": "success",
        "data": rows,
        "meta": {"page": page, "per_page": per_page, "total": total},
    })


@bp.post("/")
def create_college_route():
    data: Dict[str, Any] = request.get_json(force=True) or {}
    try:
        create_college(data)
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception:
        return jsonify({"status": "error", "error": "create_failed"}), 500

    return jsonify({"status": "success", "data": {"college_code": data["college_code"]}}), 201


@bp.put("/<college_code>")
def update_college_route(college_code: str):
    updates = request.get_json(force=True) or {}
    try:
        success = update_college(college_code, updates)
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception:
        return jsonify({"status": "error", "error": "update_failed"}), 500

    if not success:
        return jsonify({"status": "error", "error": "not_found_or_no_changes"}), 404
    return jsonify({"status": "success", "data": {"college_code": college_code}})


@bp.delete("/<college_code>")
def delete_college_route(college_code: str):
    try:
        success = delete_college(college_code)
    except Exception:
        return jsonify({"status": "error", "error": "delete_failed"}), 500

    if not success:
        return jsonify({"status": "error", "error": "not_found_or_referenced"}), 404
    return jsonify({"status": "success", "data": {"college_code": college_code}})
