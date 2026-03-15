from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import bcrypt

from src.saas_db import create_user, get_user_by_email


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False


def signup_user(email: str, password: str) -> Tuple[Optional[Dict[str, Any]], str]:
    if not email.strip() or not password.strip():
        return None, "Email and password are required."
    if len(password) < 8:
        return None, "Password must be at least 8 characters."

    existing = get_user_by_email(email)
    if existing:
        return None, "An account with this email already exists."

    created = create_user(email=email, password_hash=hash_password(password))
    return created, "Account created successfully."


def login_user(email: str, password: str) -> Tuple[Optional[Dict[str, Any]], str]:
    user = get_user_by_email(email)
    if not user:
        return None, "Invalid email or password."

    if not verify_password(password, user.get("password_hash", "")):
        return None, "Invalid email or password."

    return user, "Login successful."
