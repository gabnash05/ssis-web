from flask import Blueprint, request, jsonify
from typing import Dict, Any
from .helpers import (
    list_students, count_students, create_student, get_student,
    update_student, delete_student, validate_student_payload
)

bp = Blueprint("students", __name__)
 

@bp.get("/")
def list_students_route():
    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = max(min(int(request.args.get("per_page", 50)), 100), 1)
    except ValueError:
        return jsonify({"status": "error", "error": "invalid_pagination"}), 400

    sort_by = request.args.get("sort_by", "id_number")
    order = request.args.get("order", "ASC").upper()
    q = request.args.get("q")

    allowed_sort = {"id_number", "first_name", "last_name", "year_level", "gender", "program_code"}
    if sort_by not in allowed_sort:
        sort_by = "id_number"
    if order not in {"ASC", "DESC"}:
        order = "ASC"

    filters = ""
    params = {}
    if q:
        filters = "WHERE (id_number ILIKE :q OR first_name ILIKE :q OR last_name ILIKE :q)"
        params["q"] = f"%{q}%"

    total = count_students(filters, params)
    offset = (page - 1) * per_page
    students = list_students(filters, params, sort_by, order, per_page, offset)

    return jsonify({
        "status": "success",
        "data": students,
        "meta": {"page": page, "per_page": per_page, "total": total},
    })


@bp.post("/")
def create_student_route():
    data: Dict[str, Any] = request.get_json(force=True) or {}
    try:
        if not validate_student_payload(data):
            return jsonify({"status": "error", "error": "invalid_payload"}), 400
        create_student(data)
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception:
        return jsonify({"status": "error", "error": "create_failed"}), 500

    return jsonify({"status": "success", "data": {"id_number": data["id_number"]}}), 201


@bp.get("/<id_number>")
def get_student_route(id_number: str):
    student = get_student(id_number)
    if not student:
        return jsonify({"status": "error", "error": "not_found"}), 404
    return jsonify({"status": "success", "data": student})


@bp.put("/<id_number>")
def update_student_route(id_number: str):
    updates = request.get_json(force=True) or {}
    try:
        success = update_student(id_number, updates)
    except ValueError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception:
        return jsonify({"status": "error", "error": "update_failed"}), 500

    if not success:
        return jsonify({"status": "error", "error": "not_found_or_no_changes"}), 404
    return jsonify({"status": "success", "data": {"id_number": id_number}})


@bp.delete("/<id_number>")
def delete_student_route(id_number: str):
    try:
        success = delete_student(id_number)
    except Exception:
        return jsonify({"status": "error", "error": "delete_failed"}), 500

    if not success:
        return jsonify({"status": "error", "error": "not_found"}), 404
    return jsonify({"status": "success", "data": {"id_number": id_number}})
