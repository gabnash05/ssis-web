from typing import Dict, Any, List
from sqlalchemy import text
from ..database import execute_sql


def fetch_programs(
    search_by: str,
    search_term: str,
    sort_by: str,
    sort_order: str,
    limit: int,
    offset: int,
) -> List[Dict[str, Any]]:
    params: Dict[str, Any] = {"limit": limit, "offset": offset}
    filters = ""

    if search_term:
        if search_by:
            filters = f"WHERE {search_by} ILIKE :q"
        else:
            filters = "WHERE program_code ILIKE :q OR program_name ILIKE :q OR college_code ILIKE :q"
        params["q"] = f"%{search_term}%"

    query = text(
        f"""
        SELECT program_code, program_name, college_code
        FROM programs
        {filters}
        ORDER BY {sort_by} {sort_order}
        LIMIT :limit OFFSET :offset
        """
    )
    result = execute_sql(query, params)
    return result.mappings().all() if result else []


def fetch_program_count(search_by: str, search_term: str) -> int:
    params: Dict[str, Any] = {}
    filters = ""

    if search_term:
        if search_by:
            filters = f"WHERE {search_by} ILIKE :q"
        else:
            filters = "WHERE program_code ILIKE :q OR program_name ILIKE :q OR college_code ILIKE :q"
        params["q"] = f"%{search_term}%"

    query = text(f"SELECT COUNT(*) FROM programs {filters}")
    result = execute_sql(query, params)
    return int(result.scalar()) if result and result.scalar() is not None else 0


def insert_program(program_code: str, program_name: str, college_code: str) -> bool:
    result = execute_sql(
        """
        INSERT INTO programs (program_code, program_name, college_code)
        VALUES (:program_code, :program_name, :college_code)
        """,
        {"program_code": program_code, "program_name": program_name, "college_code": college_code},
    )
    return bool(result)


def update_program_record(program_code: str, updates: Dict[str, Any]) -> bool:
    allowed = {"program_code", "program_name", "college_code"}
    set_items = []
    params = {"orig_program_code": program_code} 

    for k, v in updates.items():
        if k not in allowed:
            continue
        if k == "college_code":
            college = execute_sql("SELECT 1 FROM colleges WHERE college_code = :c", {"c": v})
            if not college or college.scalar() is None:
                raise ValueError("unknown_college")
        set_items.append(f"{k} = :{k}")
        params[k] = v

    if not set_items:
        return False

    result = execute_sql(
        f"UPDATE programs SET {', '.join(set_items)} WHERE program_code = :orig_program_code",
        params
    )
    return bool(result and result.rowcount > 0)


def delete_program_record(program_code: str) -> bool:
    result = execute_sql("DELETE FROM programs WHERE program_code = :program_code", {"program_code": program_code})
    return bool(result and result.rowcount > 0)
