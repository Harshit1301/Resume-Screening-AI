from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

import stripe

from src.saas_config import load_config
from src.saas_db import update_user

PLAN_CONFIG: Dict[str, Dict[str, Any]] = {
    "free": {
        "label": "Free",
        "resume_limit": 10,
        "features": ["Core matching", "Top candidates", "Basic dashboard"],
    },
    "pro": {
        "label": "Pro",
        "resume_limit": 200,
        "features": ["Full dashboard", "CSV + Excel export", "All analytics"],
    },
    "agency": {
        "label": "Agency",
        "resume_limit": None,
        "features": ["Unlimited resumes", "Priority processing", "Advanced analytics"],
    },
}


def _init_stripe() -> None:
    cfg = load_config()
    if not cfg.stripe_secret_key:
        raise RuntimeError("Missing STRIPE_SECRET_KEY")
    stripe.api_key = cfg.stripe_secret_key


def get_resume_limit(plan: str) -> Optional[int]:
    config = PLAN_CONFIG.get(plan, PLAN_CONFIG["free"])
    return config["resume_limit"]


def ensure_stripe_customer(user: Dict[str, Any]) -> str:
    _init_stripe()
    customer_id = user.get("stripe_customer_id")
    if customer_id:
        return str(customer_id)

    customer = stripe.Customer.create(email=user["email"], metadata={"user_id": user["user_id"]})
    updated = update_user(user["user_id"], {"stripe_customer_id": customer["id"]})
    return str(updated["stripe_customer_id"])


def create_checkout_session(user: Dict[str, Any], target_plan: str, success_url: str, cancel_url: str) -> str:
    _init_stripe()
    cfg = load_config()
    price_map = {
        "pro": cfg.stripe_price_pro,
        "agency": cfg.stripe_price_agency,
    }
    price_id = price_map.get(target_plan)
    if not price_id:
        raise RuntimeError(f"Missing Stripe price id for plan: {target_plan}")

    customer_id = ensure_stripe_customer(user)
    session = stripe.checkout.Session.create(
        mode="subscription",
        customer=customer_id,
        line_items=[{"price": price_id, "quantity": 1}],
        success_url=success_url,
        cancel_url=cancel_url,
        client_reference_id=user["user_id"],
        metadata={"user_id": user["user_id"], "plan": target_plan},
        allow_promotion_codes=True,
    )
    return str(session.url)


def create_billing_portal_session(user: Dict[str, Any], return_url: str) -> Optional[str]:
    _init_stripe()
    customer_id = user.get("stripe_customer_id")
    if not customer_id:
        return None

    portal = stripe.billing_portal.Session.create(customer=customer_id, return_url=return_url)
    return str(portal.url)


def apply_active_subscription(
    user_id: str,
    plan: str,
    subscription_id: str,
    customer_id: str,
    current_period_end_epoch: Optional[int],
) -> Dict[str, Any]:
    expiry_iso = None
    if current_period_end_epoch:
        expiry_iso = datetime.fromtimestamp(current_period_end_epoch, tz=timezone.utc).isoformat()

    return update_user(
        user_id,
        {
            "subscription_plan": plan,
            "subscription_status": "active",
            "stripe_customer_id": customer_id,
            "stripe_subscription_id": subscription_id,
            "subscription_expiry": expiry_iso,
        },
    )


def apply_inactive_subscription(user_id: str) -> Dict[str, Any]:
    return update_user(user_id, {"subscription_status": "inactive"})
