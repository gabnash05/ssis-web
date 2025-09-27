from typing import Dict, Any, List
from ..db.database import execute_sql


from typing import List, Dict, Any
from sqlalchemy import text
from ..db.database import execute_sql


def fetch_colleges(
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
        if search_by:  # search specific column
            filters = f"WHERE {search_by} ILIKE :q"
        else:  # search across all allowed fields
            filters = "WHERE college_code ILIKE :q OR college_name ILIKE :q"
        params["q"] = f"%{search_term}%"

    query = f"""
            SELECT college_code, college_name
            FROM colleges
            {filters}
            ORDER BY {sort_by} {sort_order}
            LIMIT :limit OFFSET :offset
            """

    result = execute_sql(query, params)
    if result:
        return [dict(row) for row in result.mappings().all()]
    return []


def fetch_college_count(search_by: str, search_term: str) -> int:
    params: Dict[str, Any] = {}
    filters = ""

    if search_term:
        if search_by:  # search specific column
            filters = f"WHERE {search_by} ILIKE :q"
        else:  # search across all allowed fields
            filters = "WHERE college_code ILIKE :q OR college_name ILIKE :q"
        params["q"] = f"%{search_term}%"

    query = f"SELECT COUNT(*) FROM colleges {filters}"
    result = execute_sql(query, params)

    if not result:
        return 0

    value = result.scalar()
    return int(value) if value is not None else 0



def insert_college(college_code: str, college_name: str) -> bool:
    result = execute_sql(
        """
        INSERT INTO colleges (college_code, college_name)
        VALUES (:college_code, :college_name)
        """,
        {"college_code": college_code, "college_name": college_name},
    )
    return bool(result)


def update_college_record(college_code: str, updates: Dict[str, Any]) -> bool:
    allowed = {"college_code", "college_name"}
    set_items = []
    params = {"orig_college_code": college_code}  # keep original key

    for k, v in updates.items():
        if k not in allowed:
            continue
        set_items.append(f"{k} = :{k}")
        params[k] = v

    if not set_items:
        return False

    result = execute_sql(
        f"UPDATE colleges SET {', '.join(set_items)} WHERE college_code = :orig_college_code",
        params,
    )
    return bool(result and result.rowcount > 0)


def delete_college_record(college_code: str) -> bool:
    result = execute_sql(
        "DELETE FROM colleges WHERE college_code = :college_code",
        {"college_code": college_code},
    )
    return bool(result and result.rowcount > 0)
