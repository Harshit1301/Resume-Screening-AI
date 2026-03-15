from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

import streamlit as st
from supabase import Client, create_client

from src.saas_config import load_config


@st.cache_resource
def get_supabase_client() -> Client:
    cfg = load_config()
    if not cfg.supabase_url or not cfg.supabase_key:
        raise RuntimeError("Supabase environment variables are missing.")
    return create_client(cfg.supabase_url, cfg.supabase_key)


def _normalize_email(email: str) -> str:
    return email.strip().lower()


def get_user_by_email(email: str) -> Optional[Dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("app_users").select("*").eq("email", _normalize_email(email)).limit(1).execute()
    records = response.data or []
    return records[0] if records else None


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("app_users").select("*").eq("user_id", user_id).limit(1).execute()
    records = response.data or []
    return records[0] if records else None


def create_user(email: str, password_hash: str) -> Dict[str, Any]:
    client = get_supabase_client()
    payload = {
        "user_id": str(uuid4()),
        "email": _normalize_email(email),
        "password_hash": password_hash,
        "subscription_plan": "free",
        "subscription_status": "active",
        "stripe_customer_id": None,
        "stripe_subscription_id": None,
        "subscription_expiry": None,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "usage_count": 0,
    }
    response = client.table("app_users").insert(payload).execute()
    created = response.data or []
    if not created:
        raise RuntimeError("Could not create user account.")
    return created[0]


def update_user(user_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    client = get_supabase_client()
    response = client.table("app_users").update(updates).eq("user_id", user_id).execute()
    updated = response.data or []
    if not updated:
        raise RuntimeError("User update failed.")
    return updated[0]


def increment_usage_count(user_id: str) -> Dict[str, Any]:
    user = get_user_by_id(user_id)
    if not user:
        raise RuntimeError("User not found for usage increment.")
    current = int(user.get("usage_count") or 0)
    return update_user(user_id, {"usage_count": current + 1})


def list_users() -> List[Dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("app_users").select("*").order("created_at", desc=True).execute()
    return response.data or []


def set_user_subscription_status(user_id: str, status: str) -> Dict[str, Any]:
    return update_user(user_id, {"subscription_status": status})


def deactivate_if_expired(user: Dict[str, Any]) -> Dict[str, Any]:
    expiry = user.get("subscription_expiry")
    if not expiry:
        return user

    try:
        expires_at = datetime.fromisoformat(str(expiry).replace("Z", "+00:00"))
    except ValueError:
        return user

    if datetime.now(timezone.utc) > expires_at and user.get("subscription_plan") != "free":
        return update_user(user["user_id"], {"subscription_status": "inactive"})
    return user


def get_user_by_stripe_customer(customer_id: str) -> Optional[Dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("app_users").select("*").eq("stripe_customer_id", customer_id).limit(1).execute()
    records = response.data or []
    return records[0] if records else None


def get_user_by_stripe_subscription(subscription_id: str) -> Optional[Dict[str, Any]]:
    client = get_supabase_client()
    response = client.table("app_users").select("*").eq("stripe_subscription_id", subscription_id).limit(1).execute()
    records = response.data or []
    return records[0] if records else None
