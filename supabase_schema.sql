create table if not exists public.app_users (
  user_id text primary key,
  email text unique not null,
  password_hash text not null,
  subscription_plan text not null default 'free',
  subscription_status text not null default 'active',
  stripe_customer_id text,
  stripe_subscription_id text,
  subscription_expiry timestamptz,
  created_at timestamptz not null default now(),
  usage_count integer not null default 0
);

create index if not exists idx_app_users_email on public.app_users(email);
create index if not exists idx_app_users_subscription on public.app_users(subscription_status, subscription_plan);

alter table public.app_users enable row level security;

create policy if not exists "service_role_full_access"
on public.app_users
for all
to service_role
using (true)
with check (true);
