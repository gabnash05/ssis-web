from typing import Optional, Dict, Any
from ..database import execute_sql


def create_user(username: str, password_hash: str, role: Optional[str] = None) -> bool:
    result = execute_sql(
        """
        INSERT INTO users (username, password_hash, role)
        VALUES (:username, :password_hash, COALESCE(:role, 'admin'))
        """,
        {"username": username, "password_hash": password_hash, "role": role},
    )
    return result is not None


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    result = execute_sql(
        """
        SELECT user_id, username, password_hash, role
        FROM users
        WHERE username = :username
        """,
        {"username": username},
    )
    return result.mappings().first() if result else None
