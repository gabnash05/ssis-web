from typing import Dict, Any, List, Tuple, Optional
from .repository import (
    fetch_students,
    fetch_student_count,
    insert_student,
    fetch_student,
    update_student_record,
    delete_student_record,
)
from ..utils.validation_utils import _valid_id_number
from ..db.database import execute_sql


ALLOWED_GENDERS = {"MALE", "FEMALE", "OTHER"}
ALLOWED_SORT = {"id_number", "first_name", "last_name", "year_level", "gender", "program_code"}
ALLOWED_SEARCH = {"id_number", "first_name", "last_name", "year_level", "gender", "program_code"}


def search_students(
    sort_by: str,
    sort_order: str,
    search_term: str,
    search_by: str,
    page: int,
    page_size: int,
) -> Tuple[List[Dict[str, Any]], int]:
    if sort_by not in ALLOWED_SORT:
        sort_by = "id_number"
    if sort_order not in {"ASC", "DESC"}:
        sort_order = "ASC"
    if search_by and search_by not in ALLOWED_SEARCH:
        search_by = "id_number"

    offset = (page - 1) * page_size

    results = fetch_students(
        search_by=search_by,
        search_term=search_term,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=page_size,
        offset=offset,
    )
    total_count = fetch_student_count(search_by=search_by, search_term=search_term)
    return results, total_count


def create_student(data: Dict[str, Any]) -> None:
    if "id_number" not in data or not _valid_id_number(data["id_number"]):
        raise ValueError("invalid_id_number")
    if "first_name" not in data or not isinstance(data["first_name"], str):
        raise ValueError("invalid_first_name")
    if "last_name" not in data or not isinstance(data["last_name"], str):
        raise ValueError("invalid_last_name")
    if "year_level" not in data or not isinstance(data["year_level"], int):
        raise ValueError("invalid_year_level")
    if "gender" not in data or data["gender"] not in ALLOWED_GENDERS:
        raise ValueError("invalid_gender")
    if "program_code" not in data or not isinstance(data["program_code"], str):
        raise ValueError("invalid_program_code")

    prog = execute_sql("SELECT 1 FROM programs WHERE program_code = :p", {"p": data["program_code"]})
    if not prog or prog.scalar() is None:
        raise ValueError("unknown_program")

    if not insert_student(data):
        raise RuntimeError("insert_failed")


def get_student(id_number: str) -> Optional[Dict[str, Any]]:
    if not _valid_id_number(id_number):
        return None
    return fetch_student(id_number)


def update_student(id_number: str, updates: Dict[str, Any]) -> bool:
    return update_student_record(id_number, updates)


def delete_student(id_number: str) -> bool:
    return delete_student_record(id_number)
