from typing import Dict, Any, List, Tuple
from .repository import (
    fetch_programs,
    fetch_program_count,
    insert_program,
    update_program_record,
    delete_program_record,
)
from ..db.database import execute_sql

ALLOWED_SORT = {"program_code", "program_name", "college_code"}
ALLOWED_SEARCH = {"program_code", "program_name", "college_code"}


def search_programs(
    sort_by: str,
    sort_order: str,
    search_term: str,
    search_by: str,
    page: int,
    page_size: int,
) -> Tuple[List[Dict[str, Any]], int]:
    if sort_by not in ALLOWED_SORT:
        sort_by = "program_code"

    if sort_order not in {"ASC", "DESC"}:
        sort_order = "ASC"

    if search_by and search_by not in ALLOWED_SEARCH:
        search_by = "program_code"

    offset = (page - 1) * page_size

    results = fetch_programs(
        search_by=search_by,
        search_term=search_term,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=page_size,
        offset=offset,
    )
    total_count = fetch_program_count(search_by=search_by, search_term=search_term)

    return results, total_count


def create_program(data: Dict[str, Any]) -> None:
    if "program_code" not in data or "program_name" not in data or "college_code" not in data:
        raise ValueError("missing_fields")

    college = execute_sql("SELECT 1 FROM colleges WHERE college_code = :c", {"c": data["college_code"]})
    if not college or college.scalar() is None:
        raise ValueError("unknown_college")

    if not insert_program(data["program_code"], data["program_name"], data["college_code"]):
        raise RuntimeError("insert_failed")


def update_program(program_code: str, updates: Dict[str, Any]) -> bool:
    return update_program_record(program_code, updates)


def delete_program(program_code: str) -> bool:
    return delete_program_record(program_code)
