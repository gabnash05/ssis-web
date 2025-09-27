from typing import Optional, Dict, Any
from ..db.database import execute_sql


def insert_user(username: str, email: str, password_hash: str, role: Optional[str]) -> bool:
    result = execute_sql(
        """
        INSERT INTO users (username, email, password_hash, role)
        VALUES (:username, :email, :password_hash, COALESCE(:role, 'admin'))
        """,
        {"username": username, "email": email, "password_hash": password_hash, "role": role},
    )
    return result is not None


def find_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    result = execute_sql(
        """
        SELECT user_id, username, email, password_hash, role
        FROM users
        WHERE email = :email
        """,
        {"email": email},
    )
    return result.mappings().first() if result else None


def find_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    result = execute_sql(
        """
        SELECT user_id, username, email, password_hash, role
        FROM users
        WHERE username = :username
        """,
        {"username": username},
    )
    return result.mappings().first() if result else None