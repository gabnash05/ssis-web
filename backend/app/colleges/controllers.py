from typing import Dict, Any, List
from ..database import execute_sql


def list_colleges(filters: str, params: Dict[str, Any], sort: str, order: str, limit: int, offset: int) -> List[Dict]:
    query = f"""
        SELECT college_code, college_name
        FROM colleges {filters}
        ORDER BY {sort} {order}
        LIMIT :limit OFFSET :offset
    """
    result = execute_sql(query, {**params, "limit": limit, "offset": offset})
    return result.mappings().all() if result else []


def count_colleges(filters: str, params: Dict[str, Any]) -> int:
    result = execute_sql(f"SELECT COUNT(*) FROM colleges {filters}", params)
    return int(result.scalar()) if result and result.scalar() is not None else 0


def create_college(data: Dict[str, Any]) -> None:
    if "college_code" not in data or "college_name" not in data:
        raise ValueError("missing_fields")
    result = execute_sql(
        """
        INSERT INTO colleges (college_code, college_name)
        VALUES (:college_code, :college_name)
        """,
        data,
    )
    if not result:
        raise RuntimeError("insert_failed")


def update_college(college_code: str, updates: Dict[str, Any]) -> bool:
    allowed = {"college_name"}
    set_items = []
    params = {"college_code": college_code}
    for k, v in updates.items():
        if k not in allowed:
            continue
        set_items.append(f"{k} = :{k}")
        params[k] = v
    if not set_items:
        return False
    result = execute_sql(f"UPDATE colleges SET {', '.join(set_items)} WHERE college_code = :college_code", params)
    return bool(result and result.rowcount > 0)


def delete_college(college_code: str) -> bool:
    result = execute_sql("DELETE FROM colleges WHERE college_code = :college_code", {"college_code": college_code})
    return bool(result and result.rowcount > 0)
