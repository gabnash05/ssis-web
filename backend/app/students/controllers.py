from typing import Dict, Any, List, Optional
import re
from ..database import execute_sql

ID_NUMBER_RE = re.compile(r"^\d{4}-\d{4}$")
ALLOWED_GENDERS = {"male", "female", "other"}


def _valid_id_number(id_number: str) -> bool:
    return bool(ID_NUMBER_RE.match(id_number))


def _valid_student_payload(data: Dict[str, Any]) -> Optional[str]:
    if "id_number" not in data or not _valid_id_number(data["id_number"]):
        return "invalid_id_number"
    if "first_name" not in data or not isinstance(data["first_name"], str):
        return "invalid_first_name"
    if "last_name" not in data or not isinstance(data["last_name"], str):
        return "invalid_last_name"
    if "year_level" not in data or not isinstance(data["year_level"], int):
        return "invalid_year_level"
    if "gender" not in data or data["gender"] not in ALLOWED_GENDERS:
        return "invalid_gender"
    if "program_code" not in data or not isinstance(data["program_code"], str):
        return "invalid_program_code"
    return None


def list_students(filters: str, params: Dict[str, Any], sort: str, order: str, limit: int, offset: int) -> List[Dict]:
    query = f"""
        SELECT id_number, first_name, last_name, year_level, gender, program_code
        FROM students {filters}
        ORDER BY {sort} {order}
        LIMIT :limit OFFSET :offset
    """
    result = execute_sql(query, {**params, "limit": limit, "offset": offset})
    return result.mappings().all() if result else []


def count_students(filters: str, params: Dict[str, Any]) -> int:
    result = execute_sql(f"SELECT COUNT(*) FROM students {filters}", params)
    return int(result.scalar()) if result and result.scalar() is not None else 0


def create_student(data: Dict[str, Any]) -> bool:
    validation_error = _valid_student_payload(data)
    if validation_error:
        raise ValueError(validation_error)

    # ensure program exists (basic referential check)
    prog = execute_sql("SELECT 1 FROM programs WHERE program_code = :p", {"p": data["program_code"]})
    if not prog or prog.scalar() is None:
        raise ValueError("unknown_program")

    result = execute_sql(
        """
        INSERT INTO students (id_number, first_name, last_name, year_level, gender, program_code)
        VALUES (:id_number, :first_name, :last_name, :year_level, :gender, :program_code)
        """,
        data,
    )
    return result is not None


def get_student(id_number: str) -> Optional[Dict[str, Any]]:
    if not _valid_id_number(id_number):
        return None
    result = execute_sql(
        """
        SELECT id_number, first_name, last_name, year_level, gender, program_code
        FROM students
        WHERE id_number = :id_number
        """,
        {"id_number": id_number},
    )
    return result.mappings().first() if result else None


def update_student(id_number: str, updates: Dict[str, Any]) -> bool:
    if not _valid_id_number(id_number):
        return False

    allowed = {"first_name", "last_name", "year_level", "gender", "program_code"}
    set_items = []
    params: Dict[str, Any] = {"id_number": id_number}
    for k, v in updates.items():
        if k not in allowed:
            continue
        # basic type checks
        if k in {"first_name", "last_name", "program_code"} and not isinstance(v, str):
            raise ValueError(f"invalid_{k}")
        if k == "year_level" and not isinstance(v, int):
            raise ValueError("invalid_year_level")
        if k == "gender" and v not in ALLOWED_GENDERS:
            raise ValueError("invalid_gender")
        set_items.append(f"{k} = :{k}")
        params[k] = v

    if not set_items:
        return False

    # If updating program_code, ensure it exists
    if "program_code" in params:
        prog = execute_sql("SELECT 1 FROM programs WHERE program_code = :p", {"p": params["program_code"]})
        if not prog or prog.scalar() is None:
            raise ValueError("unknown_program")

    result = execute_sql(f"UPDATE students SET {', '.join(set_items)} WHERE id_number = :id_number", params)
    return bool(result and result.rowcount > 0)


def delete_student(id_number: str) -> bool:
    if not _valid_id_number(id_number):
        return False
    result = execute_sql("DELETE FROM students WHERE id_number = :id_number", {"id_number": id_number})
    return bool(result and result.rowcount > 0)
