from typing import Dict, Any, List, Tuple
from .repository import (
    fetch_colleges,
    fetch_college_count,
    insert_college,
    update_college_record,
    delete_college_record,
)

ALLOWED_SORT = {"college_code", "college_name"}
ALLOWED_SEARCH = {"college_code", "college_name"}


def search_colleges(
    sort_by: str,
    sort_order: str,
    search_term: str,
    search_by: str,
    page: int,
    page_size: int,
) -> Tuple[List[Dict[str, Any]], int]:
    if sort_by not in ALLOWED_SORT:
        sort_by = "college_code"
    if sort_order not in {"ASC", "DESC"}:
        sort_order = "ASC"
    if search_by and search_by not in ALLOWED_SEARCH:
        search_by = "college_code"

    offset = (page - 1) * page_size

    results = fetch_colleges(
        search_by=search_by,
        search_term=search_term,
        sort_by=sort_by,
        sort_order=sort_order,
        limit=page_size,
        offset=offset,
    )

    total_count = fetch_college_count(search_by=search_by, search_term=search_term)

    return results, total_count


def count_colleges(search_by: str, search_term: str) -> int:
    if search_by not in ALLOWED_SEARCH:
        search_by = "college_code"
    return fetch_college_count(search_by=search_by, search_term=search_term)


def create_college(data: Dict[str, Any]) -> None:
    if "college_code" not in data or "college_name" not in data:
        raise ValueError("missing_fields")
    inserted = insert_college(data["college_code"], data["college_name"])
    if not inserted:
        raise RuntimeError("insert_failed")


def update_college(college_code: str, updates: Dict[str, Any]) -> bool:
    return update_college_record(college_code, updates)


def delete_college(college_code: str) -> bool:
    return delete_college_record(college_code)
