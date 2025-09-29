from typing import Optional, Dict, Any
from werkzeug.security import generate_password_hash, check_password_hash
from .repository import insert_user, find_user_by_email, find_user_by_username


def create_user(username: str, email: str, password: str, role: Optional[str] = None) -> Optional[int]:
    password_hash = generate_password_hash(password)
    return insert_user(username, email, password_hash, role)


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    user = find_user_by_email(email)
    if user and check_password_hash(user["password_hash"], password):
        return {
            "user_id": user["user_id"], 
            "username": user["username"],
            "email": user["email"], 
            "role": user["role"]
        }
    return None