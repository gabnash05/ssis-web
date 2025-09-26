from typing import Dict, Any, List
from ..database import execute_sql


def list_programs(filters: str, params: Dict[str, Any], sort: str, order: str, limit: int, offset: int) -> List[Dict]:
    query = f"""
        SELECT program_code, program_name, college_code
        FROM programs {filters}
        ORDER BY {sort} {order}
        LIMIT :limit OFFSET :offset
    """
    result = execute_sql(query, {**params, "limit": limit, "offset": offset})
    return result.mappings().all() if result else []


def count_programs(filters: str, params: Dict[str, Any]) -> int:
    result = execute_sql(f"SELECT COUNT(*) FROM programs {filters}", params)
    return int(result.scalar()) if result and result.scalar() is not None else 0


def create_program(data: Dict[str, Any]) -> None:
    if "program_code" not in data or "program_name" not in data or "college_code" not in data:
        raise ValueError("missing_fields")
    college = execute_sql("SELECT 1 FROM colleges WHERE college_code = :c", {"c": data["college_code"]})
    if not college or college.scalar() is None:
        raise ValueError("unknown_college")
    result = execute_sql(
        """
        INSERT INTO programs (program_code, program_name, college_code)
        VALUES (:program_code, :program_name, :college_code)
        """,
        data,
    )
    if not result:
        raise RuntimeError("insert_failed")


def update_program(program_code: str, updates: Dict[str, Any]) -> bool:
    allowed = {"program_name", "college_code"}
    set_items = []
    params = {"program_code": program_code}
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

    result = execute_sql(f"UPDATE programs SET {', '.join(set_items)} WHERE program_code = :program_code", params)
    return bool(result and result.rowcount > 0)


def delete_program(program_code: str) -> bool:
    result = execute_sql("DELETE FROM programs WHERE program_code = :program_code", {"program_code": program_code})
    return bool(result and result.rowcount > 0)
