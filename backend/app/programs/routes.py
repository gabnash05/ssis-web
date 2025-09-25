from flask import Blueprint, request, jsonify
from typing import Dict, Any
from .helpers import (
    list_programs, count_programs, create_program, update_program, delete_program
)

bp = Blueprint("programs", __name__)


@bp.get("/")
def list_programs_route():
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = max(min(int(request.args.get("per_page", 50)), 100), 1)
    except ValueError:
        return jsonify({"status": "error", "error": "invalid_pagination"}), 400

    sort_by = request.args.get("sort_by", "program_code")
    order = request.args.get("order", "ASC").upper()
    q = request.args.get("q")

    allowed_sort = {"program_code", "program_name", "college_code"}
    if sort_by not in allowed_sort:
        sort_by = "program_code"
    if order not in {"ASC", "DESC"}:
        order = "ASC"

    filters = ""
    params: Dict[str, Any] = {}
    if q:
        filters = "WHERE (program_code ILIKE :q OR program_name ILIKE :q OR college_code ILIKE :q)"
        params["q"] = f"%{q}%"

    total = count_programs(filters, params)
    offset = (page - 1) * per_page
    rows = list_programs(filters, params, sort_by, order, per_page, offset)

    return jsonify({
        "status": "success",
        "data": rows,
        "meta": {"page": page, "per_page": per_page, "total": total},
    })


@bp.post("/")
def create_program_route():
    data: Dict[str, Any] = request.get_json(force=True) or {}
    try:
        create_program(data)
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception:
        return jsonify({"status": "error", "error": "create_failed"}), 500

    return jsonify({"status": "success", "data": {"program_code": data["program_code"]}}), 201


@bp.put("/<program_code>")
def update_program_route(program_code: str):
    updates = request.get_json(force=True) or {}
    try:
        success = update_program(program_code, updates)
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception:
        return jsonify({"status": "error", "error": "update_failed"}), 500

    if not success:
        return jsonify({"status": "error", "error": "not_found_or_no_changes"}), 404
    return jsonify({"status": "success", "data": {"program_code": program_code}})


@bp.delete("/<program_code>")
def delete_program_route(program_code: str):
    try:
        success = delete_program(program_code)
    except Exception:
        return jsonify({"status": "error", "error": "delete_failed"}), 500

    if not success:
        return jsonify({"status": "error", "error": "not_found"}), 404
    return jsonify({"status": "success", "data": {"program_code": program_code}})
