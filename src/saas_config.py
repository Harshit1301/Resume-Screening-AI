from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class SaaSConfig:
    supabase_url: str
    supabase_key: str
    stripe_secret_key: str
    stripe_webhook_secret: str
    stripe_price_pro: str
    stripe_price_agency: str
    app_base_url: str
    admin_password: str


def load_config() -> SaaSConfig:
    return SaaSConfig(
        supabase_url=os.getenv("SUPABASE_URL", ""),
        supabase_key=os.getenv("SUPABASE_KEY", ""),
        stripe_secret_key=os.getenv("STRIPE_SECRET_KEY", ""),
        stripe_webhook_secret=os.getenv("STRIPE_WEBHOOK_SECRET", ""),
        stripe_price_pro=os.getenv("STRIPE_PRICE_PRO", ""),
        stripe_price_agency=os.getenv("STRIPE_PRICE_AGENCY", ""),
        app_base_url=os.getenv("APP_BASE_URL", "http://localhost:8501"),
        admin_password=os.getenv("ADMIN_PASSWORD", ""),
    )


def has_required_saas_env(config: Optional[SaaSConfig] = None) -> bool:
    cfg = config or load_config()
    return bool(cfg.supabase_url and cfg.supabase_key and cfg.stripe_secret_key)
