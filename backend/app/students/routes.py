from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from typing import Dict, Any
from ..utils.route_utils import make_response
from .services import (
    search_students,
    get_student,
    get_students_by_program,
    get_all_students,
    create_student,
    update_student,
    delete_student
)

bp = Blueprint("students", __name__)


@bp.get("/")
@jwt_required()
def list_students_route():
    try: 
        try:
            page = max(int(request.args.get("page", 1)), 1)
            page_size = max(min(int(request.args.get("page_size", 50)), 100), 1)
        except ValueError:
            return make_response({
                "status": "error", 
                "message": "Invalid pagination parameters",
                "error_code": "INVALID_PAGINATION"
            }, 400)

        sort_by = request.args.get("sort_by", "id_number")
        sort_order = request.args.get("order", "ASC").upper()
        search_term = request.args.get("q", "")
        search_by = request.args.get("search_by", "")

        result = search_students(
            sort_by=sort_by,
            sort_order=sort_order,
            search_term=search_term,
            search_by=search_by,
            page=page,
            page_size=page_size,
        )

        if result["success"]:
            return make_response({
                "status": "success",
                "message": result["message"],
                "data": result["data"],
                "meta": {
                    "page": result["page"], 
                    "per_page": result["page_size"], 
                    "total": result["total_count"]
                },
            }, 200)
        else:
            return make_response({
                "status": "error",
                "message": result["message"],
                "error_code": result["error_code"]
            }, 500)
    
    except Exception as e:
        return make_response({
            "status": "error", 
            "message": f"Unexpected error occurred: {str(e)}",
            "error_code": "UNEXPECTED_ERROR"
        }, 500)


@bp.post("/")
@jwt_required()
def create_student_route():
    data: Dict[str, Any] = request.get_json(force=True) or {}
    try:
        result = create_student(data)
        
        if result["success"]:
            return make_response({
                "status": "success",
                "message": result["message"],
                "data": result["data"]
            }, 201)
        else:
            status_code = 400
            if result["error_code"] == "STUDENT_ID_EXISTS":
                status_code = 409  # Conflict
            elif result["error_code"] == "PROGRAM_NOT_FOUND":
                status_code = 400
            elif result["error_code"] == "DATABASE_ERROR":
                status_code = 500
            
            return make_response({
                "status": "error",
                "message": result["message"],
                "error_code": result["error_code"],
                "details": result.get("details", {})
            }, status_code)
            
    except Exception as e:
        return make_response({
            "status": "error", 
            "message": f"Unexpected error occurred: {str(e)}",
            "error_code": "UNEXPECTED_ERROR"
        }, 500)


@bp.get("/<id_number>")
@jwt_required()
def get_student_route(id_number: str):
    try:
        result = get_student(id_number)
        
        if result["success"]:
            return make_response({
                "status": "success",
                "message": result["message"],
                "data": result["data"]
            }, 200)
        else:
            status_code = 400
            if result["error_code"] == "STUDENT_NOT_FOUND":
                status_code = 404
            
            return make_response({
                "status": "error",
                "message": result["message"],
                "error_code": result["error_code"]
            }, status_code)
            
    except Exception as e:
        return make_response({
            "status": "error", 
            "message": f"Unexpected error occurred: {str(e)}",
            "error_code": "UNEXPECTED_ERROR"
        }, 500)


@bp.put("/<id_number>")
@jwt_required()
def update_student_route(id_number: str):
    updates = request.get_json(force=True) or {}
    try:
        result = update_student(id_number, updates)
        
        if result["success"]:
            return make_response({
                "status": "success",
                "message": result["message"],
                "data": result["data"]
            }, 200)
        else:
            status_code = 400
            if result["error_code"] == "STUDENT_NOT_FOUND":
                status_code = 404
            elif result["error_code"] == "STUDENT_ID_EXISTS":
                status_code = 409  # Conflict
            elif result["error_code"] == "PROGRAM_NOT_FOUND":
                status_code = 400
            elif result["error_code"] == "DATABASE_ERROR":
                status_code = 500
            
            return make_response({
                "status": "error",
                "message": result["message"],
                "error_code": result["error_code"],
                "details": result.get("details", {})
            }, status_code)
            
    except Exception as e:
        return make_response({
            "status": "error", 
            "message": f"Unexpected error occurred: {str(e)}",
            "error_code": "UNEXPECTED_ERROR"
        }, 500)


@bp.delete("/<id_number>")
@jwt_required()
def delete_student_route(id_number: str):
    try:
        result = delete_student(id_number)
        
        if result["success"]:
            return make_response({
                "status": "success",
                "message": result["message"]
            }, 200)
        else:
            status_code = 400
            if result["error_code"] == "STUDENT_NOT_FOUND":
                status_code = 404
            elif result["error_code"] == "DATABASE_ERROR":
                status_code = 500
            
            return make_response({
                "status": "error",
                "message": result["message"],
                "error_code": result["error_code"],
                "details": result.get("details", {})
            }, status_code)
            
    except Exception as e:
        return make_response({
            "status": "error", 
            "message": f"Unexpected error occurred: {str(e)}",
            "error_code": "UNEXPECTED_ERROR"
        }, 500)
