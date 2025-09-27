from typing import Dict, Any, List, Optional
from sqlalchemy import text
from ..db.database import execute_sql


def fetch_students(
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
            filters = (
                "WHERE id_number ILIKE :q OR first_name ILIKE :q "
                "OR last_name ILIKE :q OR program_code ILIKE :q"
            )
        params["q"] = f"%{search_term}%"

    query = f"""
        SELECT id_number, first_name, last_name, year_level, gender, program_code
        FROM students
        {filters}
        ORDER BY {sort_by} {sort_order}
        LIMIT :limit OFFSET :offset
        """
    result = execute_sql(query, params)
    if result:
        return [dict(row) for row in result.mappings().all()]
    return []


def fetch_student_count(search_by: str, search_term: str) -> int:
    params: Dict[str, Any] = {}
    filters = ""

    if search_term:
        if search_by:
            filters = f"WHERE {search_by} ILIKE :q"
        else:
            filters = (
                "WHERE id_number ILIKE :q OR first_name ILIKE :q "
                "OR last_name ILIKE :q OR program_code ILIKE :q"
            )
        params["q"] = f"%{search_term}%"

    query = f"SELECT COUNT(*) FROM students {filters}"
    result = execute_sql(query, params)

    if not result:
        return 0

    value = result.scalar() 
    return int(value) if value is not None else 0


def insert_student(data: Dict[str, Any]) -> bool:
    result = execute_sql(
        """
        INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code)
        VALUES (:id_number, :first_name, :last_name, :year_level, :gender, :program_code)
        """,
        data,
    )
    return bool(result)


def fetch_student(id_number: str) -> Optional[Dict[str, Any]]:
    result = execute_sql(
        """
        SELECT id_number, first_name, last_name, year_level, gender, program_code
        FROM students
        WHERE id_number = :id_number
        """,
        {"id_number": id_number},
    )
    return result.mappings().first() if result else None


def update_student_record(id_number: str, updates: Dict[str, Any]) -> bool:
    allowed = {"id_number", "first_name", "last_name", "year_level", "gender", "program_code"}
    set_items = []
    params = {"orig_id_number": id_number}

    for k, v in updates.items():
        if k not in allowed:
            continue
        set_items.append(f"{k} = :{k}")
        params[k] = v

    if not set_items:
        return False

    result = execute_sql(
        f"UPDATE students SET {', '.join(set_items)} WHERE id_number = :orig_id_number",
        params
    )
    return bool(result and result.rowcount > 0)


def delete_student_record(id_number: str) -> bool:
    result = execute_sql("DELETE FROM students WHERE id_number = :id_number", {"id_number": id_number})
    return bool(result and result.rowcount > 0)
