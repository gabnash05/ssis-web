from flask import Blueprint, request
from typing import Dict, Any
from ..utils.route_utils import make_response
from .services import (
    search_colleges,
    count_colleges,
    create_college,
    update_college,
    delete_college,
)

bp = Blueprint("colleges", __name__)


@bp.get("/")
def list_colleges():
    try:
        try:
            page = max(int(request.args.get("page", 1)), 1)
            page_size = max(min(int(request.args.get("page_size", 50)), 100), 1)
        except ValueError:
            return make_response({"status": "error", "error": "invalid_pagination"}, 400)
    
        sort_by = request.args.get("sort_by", "college_id")
        sort_order = request.args.get("sort_order", "ASC").upper()
        search_term = request.args.get("search_term", "")
        search_by = request.args.get("search_by", "")

        results, total_count = search_colleges(
            sort_by=sort_by,
            sort_order=sort_order,
            search_term=search_term,
            search_by=search_by,
            page=page,
            page_size=page_size,
        )

        payload = {
            "status": "success",
            "data": results,
            "pagination": {
                "total_count": total_count,
                "current_page": page,
                "page_size": page_size,
                "total_pages": (total_count + page_size - 1) // page_size,
            },
        }
        return make_response(payload, 200)

    except Exception as e:
        return make_response({"status": "error", "error": str(e)}, 500)


@bp.post("/")
def create_college_route():
    data: Dict[str, Any] = request.get_json(force=True) or {}
    try:
        create_college(data)
        return make_response(
            {"status": "success", "data": {"college_code": data["college_code"]}}, 201
        )
    except ValueError as e:
        return make_response({"status": "error", "error": str(e)}, 400)
    except Exception:
        return make_response({"status": "error", "error": "create_failed"}, 500)


@bp.put("/<college_code>")
def update_college_route(college_code: str):
    updates = request.get_json(force=True) or {}
    try:
        success = update_college(college_code, updates)
        if not success:
            return make_response(
                {"status": "error", "error": "not_found_or_no_changes"}, 404
            )
        return make_response(
            {"status": "success", "data": {"college_code": college_code}}, 200
        )
    except ValueError as e:
        return make_response({"status": "error", "error": str(e)}, 400)
    except Exception:
        return make_response({"status": "error", "error": "update_failed"}, 500)


@bp.delete("/<college_code>")
def delete_college_route(college_code: str):
    try:
        success = delete_college(college_code)
        if not success:
            return make_response(
                {"status": "error", "error": "not_found_or_referenced"}, 404
            )
        return make_response(
            {"status": "success", "data": {"college_code": college_code}}, 200
        )
    except Exception:
        return make_response({"status": "error", "error": "delete_failed"}, 500)
