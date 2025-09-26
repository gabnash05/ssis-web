from typing import Optional, Dict, Any
from ..database import execute_sql


def insert_user(email: str, password_hash: str, role: Optional[str]) -> bool:
    result = execute_sql(
        """
        INSERT INTO users (email, password_hash, role)
        VALUES (:email, :password_hash, COALESCE(:role, 'user'))
        """,
        {"email": email, "password_hash": password_hash, "role": role},
    )
    return result is not None


def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    result = execute_sql(
        """
        SELECT user_id, email, password_hash, role
        FROM users
        WHERE email = :email
        """,
        {"email": email},
    )
    return result.mappings().first() if result else None
