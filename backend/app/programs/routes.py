from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from typing import Dict, Any
from ..utils.route_utils import make_response
from .services import search_programs, create_program, update_program, delete_program

bp = Blueprint("programs", __name__)


@bp.get("/")
@jwt_required()
def list_programs_route():
    try:
        try:
            page = max(int(request.args.get("page", 1)), 1)
            page_size = max(min(int(request.args.get("page_size", 50)), 100), 1)
        except ValueError:
            return make_response({"status": "error", "error": "invalid_pagination"}, 400)

        sort_by = request.args.get("sort_by", "program_code")
        sort_order = request.args.get("order", "ASC").upper()
        search_term = request.args.get("q", "")
        search_by = request.args.get("search_by", "")

        results, total_count = search_programs(
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

    except Exception as e:
        return make_response({"status": "error", "error": str(e)}, 500)


@bp.post("/")
@jwt_required()
def create_program_route():
    data: Dict[str, Any] = request.get_json(force=True) or {}
    try:
        create_program(data)
    except ValueError as e:
        return make_response({"status": "error", "error": str(e)}, 400)
    except Exception:
        return make_response({"status": "error", "error": "create_failed"}, 500)

    return make_response({"status": "success", "data": {"program_code": data["program_code"]}}, 201)


@bp.put("/<program_code>")
@jwt_required()
def update_program_route(program_code: str):
    updates = request.get_json(force=True) or {}
    try:
        success = update_program(program_code, updates)
    except ValueError as e:
        return make_response({"status": "error", "error": str(e)}, 400)
    except Exception:
        return make_response({"status": "error", "error": "update_failed"}, 500)

    if not success:
        return make_response({"status": "error", "error": "not_found_or_no_changes"}, 404)

    return make_response({"status": "success", "data": {"program_code": program_code}})


@bp.delete("/<program_code>")
@jwt_required()
def delete_program_route(program_code: str):
    try:
        success = delete_program(program_code)
    except Exception:
        return make_response({"status": "error", "error": "delete_failed"}, 500)

    if not success:
        return make_response({"status": "error", "error": "not_found"}, 404)

    return make_response({"status": "success", "data": {"program_code": program_code}})
