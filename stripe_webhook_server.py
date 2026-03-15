from __future__ import annotations

import os
from typing import Any, Dict, Optional

import stripe
from fastapi import FastAPI, Header, HTTPException, Request

from src.saas_billing import apply_active_subscription, apply_inactive_subscription
from src.saas_db import get_user_by_stripe_customer, get_user_by_stripe_subscription, update_user

app = FastAPI(title="Resume Screening AI Stripe Webhook")

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
STRIPE_PRICE_PRO = os.getenv("STRIPE_PRICE_PRO", "")
STRIPE_PRICE_AGENCY = os.getenv("STRIPE_PRICE_AGENCY", "")

if not STRIPE_SECRET_KEY:
    raise RuntimeError("Missing STRIPE_SECRET_KEY")

stripe.api_key = STRIPE_SECRET_KEY


def _plan_from_price_id(price_id: str) -> str:
    if price_id == STRIPE_PRICE_AGENCY:
        return "agency"
    return "pro"


def _subscription_details(subscription_id: str) -> Optional[Dict[str, Any]]:
    if not subscription_id:
        return None
    subscription = stripe.Subscription.retrieve(subscription_id)
    items = subscription.get("items", {}).get("data", [])
    first_item = items[0] if items else None
    price_id = first_item.get("price", {}).get("id") if first_item else None
    return {
        "plan": _plan_from_price_id(price_id) if price_id else "pro",
        "current_period_end": subscription.get("current_period_end"),
        "customer_id": subscription.get("customer"),
    }


@app.post("/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(default="", alias="Stripe-Signature")):
    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=stripe_signature, secret=STRIPE_WEBHOOK_SECRET)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {exc}") from exc

    event_type = event.get("type", "")
    data_object = event.get("data", {}).get("object", {})

    if event_type == "checkout.session.completed":
        user_id = data_object.get("client_reference_id") or data_object.get("metadata", {}).get("user_id")
        plan = data_object.get("metadata", {}).get("plan", "pro")
        customer_id = data_object.get("customer")
        subscription_id = data_object.get("subscription")

        details = _subscription_details(subscription_id) if subscription_id else None
        period_end = details.get("current_period_end") if details else None
        inferred_plan = details.get("plan") if details else plan

        if user_id:
            apply_active_subscription(
                user_id=user_id,
                plan=inferred_plan,
                subscription_id=subscription_id,
                customer_id=customer_id,
                current_period_end_epoch=period_end,
            )

    elif event_type == "invoice.payment_succeeded":
        subscription_id = data_object.get("subscription")
        details = _subscription_details(subscription_id) if subscription_id else None
        if details:
            user = get_user_by_stripe_subscription(subscription_id)
            if user:
                apply_active_subscription(
                    user_id=user["user_id"],
                    plan=details["plan"],
                    subscription_id=subscription_id,
                    customer_id=details["customer_id"],
                    current_period_end_epoch=details["current_period_end"],
                )

    elif event_type in {"invoice.payment_failed", "customer.subscription.deleted"}:
        subscription_id = data_object.get("subscription") or data_object.get("id")
        customer_id = data_object.get("customer")

        user = None
        if subscription_id:
            user = get_user_by_stripe_subscription(subscription_id)
        if not user and customer_id:
            user = get_user_by_stripe_customer(customer_id)

        if user:
            apply_inactive_subscription(user["user_id"])

    return {"received": True, "event": event_type}
