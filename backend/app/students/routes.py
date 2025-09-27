from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from typing import Dict, Any
from ..utils.route_utils import make_response
from .services import search_students, create_student, get_student, update_student, delete_student

bp = Blueprint("students", __name__)


@bp.get("/")
@jwt_required()
def list_students_route():
    try:
        page = max(int(request.args.get("page", 1)), 1)
        page_size = max(min(int(request.args.get("page_size", 50)), 100), 1)
    except ValueError:
        return make_response({"status": "error", "error": "invalid_pagination"}, 400)

    sort_by = request.args.get("sort_by", "id_number")
    sort_order = request.args.get("order", "ASC").upper()
    search_term = request.args.get("q", "")
    search_by = request.args.get("search_by", "")

    results, total_count = search_students(
        sort_by=sort_by,
        sort_order=sort_order,
        search_term=search_term,
        search_by=search_by,
        page=page,
        page_size=page_size,
    )

    return make_response({
        "status": "success",
        "data": results,
        "meta": {"page": page, "per_page": page_size, "total": total_count},
    })


@bp.post("/")
@jwt_required()
def create_student_route():
    data: Dict[str, Any] = request.get_json(force=True) or {}
    try:
        create_student(data)
    except ValueError as e:
        return make_response({"status": "error", "error": str(e)}, 400)
    except Exception:
        return make_response({"status": "error", "error": "create_failed"}, 500)

    return make_response({"status": "success", "data": {"id_number": data["id_number"]}}, 201)


@bp.get("/<id_number>")
@jwt_required()
def get_student_route(id_number: str):
    student = get_student(id_number)
    if not student:
        return make_response({"status": "error", "error": "not_found"}, 404)
    return make_response({"status": "success", "data": student})


@bp.put("/<id_number>")
@jwt_required()
def update_student_route(id_number: str):
    updates = request.get_json(force=True) or {}
    try:
        success = update_student(id_number, updates)
    except ValueError as e:
        return make_response({"status": "error", "error": str(e)}, 400)
    except Exception:
        return make_response({"status": "error", "error": "update_failed"}, 500)

    if not success:
        return make_response({"status": "error", "error": "not_found_or_no_changes"}, 404)

    return make_response({"status": "success", "data": {"id_number": id_number}})


@bp.delete("/<id_number>")
@jwt_required()
def delete_student_route(id_number: str):
    try:
        success = delete_student(id_number)
    except Exception:
        return make_response({"status": "error", "error": "delete_failed"}, 500)

    if not success:
        return make_response({"status": "error", "error": "not_found"}, 404)

    return make_response({"status": "success", "data": {"id_number": id_number}})
