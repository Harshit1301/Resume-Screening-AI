from __future__ import annotations

import io
import os
import re
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple

import altair as alt
import pandas as pd
import streamlit as st

from src.jd_templates import (
    QUICK_INSERT_BLOCKS,
    generate_job_description_template,
    get_job_categories,
    get_role_skills,
    get_roles,
    get_subcategories,
    get_total_roles,
)
from src.pdf_utils import parse_resume
from src.ranking import ResumeRanker
from src.saas_auth import login_user, signup_user
from src.saas_billing import PLAN_CONFIG, create_billing_portal_session, create_checkout_session, get_resume_limit
from src.saas_config import has_required_saas_env
from src.saas_db import deactivate_if_expired, get_user_by_id, increment_usage_count, list_users, set_user_subscription_status
from src.text_utils import extract_job_keywords, matched_keywords

st.set_page_config(page_title="Resume Screening AI", layout="wide")


def inject_custom_css() -> None:
    """Apply modern SaaS-style theming and component styling."""
    st.markdown(
        """
        <style>
        :root {
            --bg: #0f172a;
            --panel: #111827;
            --muted: #94a3b8;
            --text: #e2e8f0;
            --accent: #6366f1;
            --accent2: #22d3ee;
            --ok: #22c55e;
            --warn: #f59e0b;
            --bad: #ef4444;
        }

        .stApp {
            background: radial-gradient(circle at top right, #1e293b 0%, #0f172a 45%, #0b1220 100%);
            color: var(--text);
        }

        .app-brand {
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }

        .subtle {
            color: var(--muted);
            font-size: 0.9rem;
        }

        .section-card {
            border: 1px solid rgba(148, 163, 184, 0.18);
            border-radius: 16px;
            padding: 0.9rem 1rem;
            background: linear-gradient(180deg, rgba(17,24,39,0.95), rgba(17,24,39,0.75));
            box-shadow: 0 8px 22px rgba(2,6,23,0.35);
            margin-bottom: 0.9rem;
        }

        .metric-pill {
            border-radius: 999px;
            padding: 0.2rem 0.65rem;
            display: inline-block;
            font-size: 0.78rem;
            border: 1px solid rgba(148, 163, 184, 0.35);
            color: #cbd5e1;
            margin-right: 0.45rem;
            margin-bottom: 0.35rem;
        }

        .score-pill {
            padding: 0.2rem 0.55rem;
            border-radius: 10px;
            font-weight: 600;
            display: inline-block;
        }

        .stButton > button {
            border: none !important;
            border-radius: 12px !important;
            background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            box-shadow: 0 6px 18px rgba(56, 189, 248, 0.25);
            transition: all 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 20px rgba(99, 102, 241, 0.35);
        }

        .candidate-row {
            border: 1px solid rgba(148, 163, 184, 0.15);
            border-radius: 12px;
            padding: 0.55rem 0.65rem;
            margin-bottom: 0.45rem;
            background: rgba(15, 23, 42, 0.7);
        }

        .score-good { background: rgba(34,197,94,0.20); color: #86efac; }
        .score-mid { background: rgba(245,158,11,0.22); color: #fde68a; }
        .score-low { background: rgba(239,68,68,0.20); color: #fecaca; }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def load_ranker() -> ResumeRanker:
    """Load the embedding model once and reuse across reruns."""
    return ResumeRanker(model_name="sentence-transformers/all-MiniLM-L6-v2")


def init_state() -> None:
    """Initialize session state containers used across reruns."""
    st.session_state.setdefault("uploaded_resume_store", {})
    st.session_state.setdefault("processing_status", "Idle")
    st.session_state.setdefault("job_description", "")
    categories = get_job_categories()
    default_category = categories[0]
    default_subcategory = get_subcategories(default_category)[0]
    default_role = get_roles(default_category, default_subcategory)[0]
    st.session_state.setdefault("selected_category", default_category)
    st.session_state.setdefault("selected_subcategory", default_subcategory)
    st.session_state.setdefault("selected_job_role", default_role)
    st.session_state.setdefault("active_preview_key", "")
    st.session_state.setdefault("analysis_outputs", None)
    st.session_state.setdefault("current_user", None)
    st.session_state.setdefault("admin_unlocked", False)


def to_csv_bytes(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def to_excel_bytes(df: pd.DataFrame) -> bytes:
    """Serialize DataFrame to an in-memory Excel workbook."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Candidate Rankings")
    return output.getvalue()


def estimate_experience_years(text: str) -> int:
    """Estimate years of experience using simple regex-based heuristics."""
    normalized = text.lower()
    matches = re.findall(r"(\d{1,2})\s*\+?\s*(?:years|yrs)", normalized)
    if not matches:
        return 0
    return min(max(int(value) for value in matches), 40)


def score_bucket(score_pct: float) -> str:
    if score_pct >= 90:
        return "score-good"
    if score_pct >= 70:
        return "score-mid"
    return "score-low"


def merge_uploaded_files(incoming_files: List[io.BytesIO]) -> None:
    """Merge uploaded files into persistent in-session storage with deduping."""
    if not incoming_files:
        return

    store = st.session_state.uploaded_resume_store
    progress = st.progress(0, text="Syncing uploaded resumes...")
    total = max(len(incoming_files), 1)

    for idx, file_obj in enumerate(incoming_files, start=1):
        file_key = f"{file_obj.name}::{file_obj.size}"
        if file_key not in store:
            store[file_key] = {
                "resume_name": file_obj.name,
                "resume_bytes": file_obj.getvalue(),
                "resume_size_kb": round(file_obj.size / 1024, 2),
            }
        progress.progress(idx / total, text=f"Synced {idx}/{total} files")

    progress.empty()


def run_analysis(job_description: str, stored_resumes: Dict[str, Dict[str, object]]) -> Dict[str, object]:
    """Process resumes, rank candidates, and return outputs for rendering."""
    ranker = load_ranker()

    parsed_resumes = []
    resume_texts = []
    skipped_files: List[str] = []

    job_keywords = extract_job_keywords(job_description, top_k=15)

    progress = st.progress(0, text="Step 1/4: Extracting resume text")
    step_placeholder = st.empty()
    step_placeholder.markdown("**Step 1:** Extracting resume text")
    total = max(len(stored_resumes), 1)

    with tempfile.TemporaryDirectory(prefix="resume_screening_") as temp_dir:
        temp_path = Path(temp_dir)

        for idx, (resume_key, payload) in enumerate(stored_resumes.items(), start=1):
            progress.progress((idx / total) * 0.45, text=f"Step 1/4: Processed {idx}/{total} resumes")
            try:
                safe_name = Path(payload["resume_name"]).name
                file_path = temp_path / safe_name
                file_path.write_bytes(payload["resume_bytes"])

                file_bytes = file_path.read_bytes()
                candidate_name, resume_text = parse_resume(file_bytes, safe_name)

                if not resume_text:
                    skipped_files.append(safe_name)
                    continue

                parsed_resumes.append(
                    {
                        "candidate_name": candidate_name,
                        "resume_name": safe_name,
                        "resume_key": resume_key,
                        "resume_text": resume_text,
                        "resume_bytes": file_bytes,
                    }
                )
                resume_texts.append(resume_text)
            except Exception:
                skipped_files.append(str(payload["resume_name"]))
                continue

    if not resume_texts:
        raise ValueError("No valid text could be extracted from the uploaded PDFs.")

    step_placeholder.markdown("**Step 2:** Generating embeddings")
    progress.progress(0.55, text="Step 2/4: Encoding job description and resumes")
    similarities = ranker.rank(job_description, resume_texts)

    step_placeholder.markdown("**Step 3:** Calculating similarity and candidate insights")
    progress.progress(0.75, text="Step 3/4: Building candidate insights")

    rows = []
    for item, score in zip(parsed_resumes, similarities):
        keyword_hits = matched_keywords(item["resume_text"], job_keywords)
        missing_keywords = [kw for kw in job_keywords if kw not in keyword_hits][:8]
        score_pct = max(0.0, min(float(score) * 100, 100.0))
        rows.append(
            {
                "Candidate Name": item["candidate_name"],
                "Resume Filename": item["resume_name"],
                "Similarity Score": round(float(score), 4),
                "Match Score (%)": round(score_pct, 2),
                "Matching Skills": ", ".join(keyword_hits),
                "Missing Skills": ", ".join(missing_keywords),
                "Resume Length (words)": len(item["resume_text"].split()),
                "Estimated Experience (Years)": estimate_experience_years(item["resume_text"]),
                "_resume_key": item["resume_key"],
                "_resume_bytes": item["resume_bytes"],
                "_resume_text": item["resume_text"],
            }
        )

    df = pd.DataFrame(rows)
    step_placeholder.markdown("**Step 4:** Ranking candidates")
    progress.progress(0.93, text="Step 4/4: Sorting and preparing dashboard")

    df = df.sort_values(by="Similarity Score", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))

    top5 = df.head(5).copy()
    top10 = df.head(10).copy()

    progress.progress(1.0, text="Analysis complete")
    step_placeholder.markdown("**Done:** Candidate ranking complete")

    return {
        "ranked_df": df,
        "top5_df": top5,
        "top10_df": top10,
        "job_keywords": job_keywords,
        "skipped_files": skipped_files,
    }


def render_sidebar() -> Tuple[int, int]:
    """Render sidebar controls and app status."""
    with st.sidebar:
        st.markdown("<div class='app-brand'>🧠 Resume Screening AI</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtle'>AI-powered candidate ranking dashboard</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("**Model Info**")
        st.caption("Embedding model: all-MiniLM-L6-v2")
        st.caption("Vector similarity: cosine")
        st.caption(f"Role library: {get_total_roles()} roles")

        st.markdown("**Settings**")
        shortlist_size = st.slider("Shortlist Size", min_value=5, max_value=20, value=10, step=1)
        preview_chars = st.slider("Resume Preview Length", min_value=180, max_value=600, value=320, step=20)

        st.markdown("**Pipeline Status**")
        st.info(st.session_state.processing_status)
        st.metric("Stored Resumes", len(st.session_state.uploaded_resume_store))

        st.markdown("---")
        st.caption("Built with Streamlit + SentenceTransformers")

        user = st.session_state.get("current_user")
        if user:
            st.markdown("---")
            st.markdown("**Account**")
            st.caption(user.get("email", ""))
            st.caption(f"Plan: {str(user.get('subscription_plan', 'free')).upper()}")
            st.caption(f"Status: {str(user.get('subscription_status', 'inactive')).upper()}")
            if st.button("Logout", use_container_width=True):
                st.session_state.current_user = None
                st.session_state.analysis_outputs = None
                st.rerun()

            with st.expander("Admin Mode"):
                admin_input = st.text_input("Admin Password", type="password", key="admin_pass_input")
                if st.button("Unlock Admin"):
                    if admin_input and admin_input == os.getenv("ADMIN_PASSWORD", ""):
                        st.session_state.admin_unlocked = True
                    else:
                        st.error("Invalid admin password")

    return shortlist_size, preview_chars


def render_admin_controls() -> None:
    if not st.session_state.get("admin_unlocked"):
        return

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Admin Controls")
    users = list_users()
    if not users:
        st.caption("No users found.")
        st.markdown("</div>", unsafe_allow_html=True)
        return

    users_df = pd.DataFrame(users)
    safe_cols = [
        "user_id",
        "email",
        "subscription_plan",
        "subscription_status",
        "stripe_customer_id",
        "subscription_expiry",
        "created_at",
        "usage_count",
    ]
    display_cols = [col for col in safe_cols if col in users_df.columns]
    st.dataframe(users_df[display_cols], use_container_width=True, hide_index=True)

    selected_email = st.selectbox("Deactivate user", options=users_df["email"].tolist(), key="admin_deactivate_email")
    if st.button("Deactivate Selected User"):
        selected_record = users_df[users_df["email"] == selected_email].iloc[0].to_dict()
        set_user_subscription_status(selected_record["user_id"], "inactive")
        st.success("User deactivated.")
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _safe_current_user() -> Dict[str, object] | None:
    user = st.session_state.get("current_user")
    if not user:
        return None
    fresh_user = get_user_by_id(user["user_id"])
    if not fresh_user:
        st.session_state.current_user = None
        return None
    fresh_user = deactivate_if_expired(fresh_user)
    st.session_state.current_user = fresh_user
    return fresh_user


def render_authentication_view() -> bool:
    """Render signup/login workflow and return True when authenticated."""
    st.title("Resume Screening AI")
    st.caption("Sign in to access your subscription and candidate screening workspace.")

    if not has_required_saas_env():
        st.error("SaaS environment variables are not configured. Add Supabase and Stripe secrets first.")
        return False

    if _safe_current_user():
        return True

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)

        if submit:
            user, message = login_user(email, password)
            if user:
                st.session_state.current_user = user
                st.success(message)
                st.rerun()
            else:
                st.error(message)

    with signup_tab:
        with st.form("signup_form"):
            email = st.text_input("Work Email")
            password = st.text_input("Create Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")
            submit = st.form_submit_button("Create Account", use_container_width=True)

        if submit:
            if password != confirm:
                st.error("Passwords do not match.")
            else:
                user, message = signup_user(email, password)
                if user:
                    st.session_state.current_user = user
                    st.success(message)
                    st.rerun()
                else:
                    st.error(message)

    return False


def render_account_dashboard(user: Dict[str, object]) -> None:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Account Dashboard")

    plan = str(user.get("subscription_plan", "free"))
    status = str(user.get("subscription_status", "inactive"))
    expiry = str(user.get("subscription_expiry") or "N/A")
    usage_count = int(user.get("usage_count") or 0)
    limit = get_resume_limit(plan)
    remaining = "Unlimited" if limit is None else str(limit)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("User", str(user.get("email", "")))
    c2.metric("Plan", plan.upper())
    c3.metric("Status", status.upper())
    c4.metric("Next Billing", expiry)
    c5.metric("Remaining Usage", remaining)
    st.caption(f"Total analyses run: {usage_count}")

    st.markdown("**Plans**")
    plan_cols = st.columns(3)
    ordered = ["free", "pro", "agency"]
    for idx, plan_name in enumerate(ordered):
        with plan_cols[idx]:
            cfg = PLAN_CONFIG[plan_name]
            st.markdown(f"**{cfg['label']}**")
            st.caption(f"Resume limit: {'Unlimited' if cfg['resume_limit'] is None else cfg['resume_limit']}")
            st.caption(" • ".join(cfg["features"]))

    app_base_url = os.getenv("APP_BASE_URL", "http://localhost:8501")
    success_url = f"{app_base_url}?payment=success"
    cancel_url = f"{app_base_url}?payment=cancel"

    action_cols = st.columns([1, 1, 1])
    with action_cols[0]:
        if st.button("Activate Free Plan", use_container_width=True):
            from src.saas_db import update_user

            updated = update_user(user["user_id"], {"subscription_plan": "free", "subscription_status": "active"})
            st.session_state.current_user = updated
            st.success("Free plan activated.")
            st.rerun()
    with action_cols[1]:
        if st.button("Upgrade to Pro", use_container_width=True):
            checkout_url = create_checkout_session(user, "pro", success_url=success_url, cancel_url=cancel_url)
            st.link_button("Open Stripe Checkout (Pro)", url=checkout_url, use_container_width=True)
    with action_cols[2]:
        if st.button("Upgrade to Agency", use_container_width=True):
            checkout_url = create_checkout_session(user, "agency", success_url=success_url, cancel_url=cancel_url)
            st.link_button("Open Stripe Checkout (Agency)", url=checkout_url, use_container_width=True)

    portal_url = create_billing_portal_session(user, return_url=app_base_url)
    if portal_url:
        st.link_button("Manage Subscription", url=portal_url, use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


def has_active_access(user: Dict[str, object]) -> bool:
    return str(user.get("subscription_status", "inactive")) == "active"


def render_job_description_assistant() -> str:
    """Render JD generator + editable job description section."""
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Job Description Assistant")

    categories = get_job_categories()

    st.markdown("**Step 1 — Select Job Category (Industry)**")
    selected_category = st.selectbox(
        "Select Industry",
        options=categories,
        key="selected_category",
    )

    subcategories = get_subcategories(selected_category)
    if st.session_state.selected_subcategory not in subcategories:
        st.session_state.selected_subcategory = subcategories[0]

    st.markdown("**Step 2 — Select Subcategory (Specialization)**")
    selected_subcategory = st.selectbox(
        "Select Specialization",
        options=subcategories,
        key="selected_subcategory",
    )

    roles = get_roles(selected_category, selected_subcategory)
    if st.session_state.selected_job_role not in roles:
        st.session_state.selected_job_role = roles[0]

    st.markdown("**Step 3 — Select Job Role**")
    selected_role = st.selectbox(
        "Select Job Role",
        options=roles,
        key="selected_job_role",
    )

    role_skills = get_role_skills(selected_category, selected_subcategory, selected_role)
    skill_pills = "".join([f"<span class='metric-pill'>{skill}</span>" for skill in role_skills])
    st.caption("Auto Skill Suggestions")
    st.markdown(skill_pills, unsafe_allow_html=True)

    st.markdown("**Step 4 — Auto-generate Job Description**")
    col_generate, col_clear = st.columns([1, 1])
    with col_generate:
        if st.button("Generate Role Template", use_container_width=True):
            st.session_state.job_description = generate_job_description_template(
                category=selected_category,
                subcategory=selected_subcategory,
                role=selected_role,
            )
    with col_clear:
        if st.button("Clear Description", use_container_width=True):
            st.session_state.job_description = ""

    st.caption("Quick Insert Templates")
    block_columns = st.columns(len(QUICK_INSERT_BLOCKS))
    for idx, (block_name, block_content) in enumerate(QUICK_INSERT_BLOCKS.items()):
        with block_columns[idx]:
            if st.button(f"Insert {block_name}", key=f"insert_block_{block_name}"):
                existing = st.session_state.job_description.strip()
                separator = "\n\n" if existing else ""
                st.session_state.job_description = f"{existing}{separator}{block_content}"

    st.markdown("**Step 5 — Edit Description Before Analysis**")
    job_description = st.text_area(
        "Job Description",
        value=st.session_state.job_description,
        placeholder="Write or generate a job description...",
        height=320,
    )
    st.session_state.job_description = job_description

    jd_keywords = extract_job_keywords(job_description, top_k=12) if job_description.strip() else []
    st.caption("Extracted JD Keywords")
    if jd_keywords:
        keyword_pills = "".join([f"<span class='metric-pill'>{keyword}</span>" for keyword in jd_keywords])
        st.markdown(keyword_pills, unsafe_allow_html=True)
    else:
        st.caption("Keywords will appear as you write or generate a description.")

    st.markdown("</div>", unsafe_allow_html=True)
    return job_description


def render_upload_area() -> None:
    """Render improved uploader UI with counter, preview list, and remove actions."""
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Resume Upload")

    incoming_files = st.file_uploader(
        "Upload PDF resumes",
        type=["pdf"],
        accept_multiple_files=True,
        key="resume_uploader",
        help="Batch upload resumes (recommended up to 200 files).",
    )

    if incoming_files:
        merge_uploaded_files(incoming_files)

    total = len(st.session_state.uploaded_resume_store)
    st.markdown(f"**Uploaded Resumes ({total})**")

    if total == 0:
        st.caption("No resumes uploaded yet.")
    else:
        for resume_key, payload in list(st.session_state.uploaded_resume_store.items()):
            row_cols = st.columns([6, 1])
            with row_cols[0]:
                st.markdown(f"• {payload['resume_name']} ({payload['resume_size_kb']} KB)")
            with row_cols[1]:
                if st.button("Remove", key=f"remove_{resume_key}"):
                    st.session_state.uploaded_resume_store.pop(resume_key, None)
                    st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_top_candidate_cards(top_df: pd.DataFrame) -> None:
    """Render top candidates as visual cards with scores and actions."""
    st.subheader("Top Candidates")
    if top_df.empty:
        st.caption("No candidates to display.")
        return

    card_columns = st.columns(min(len(top_df), 5))
    for idx, (_, row) in enumerate(top_df.iterrows()):
        with card_columns[idx]:
            css_class = score_bucket(float(row["Match Score (%)"]))
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            st.markdown(f"**#{int(row['Rank'])} — {row['Candidate Name']}**")
            st.caption(row["Resume Filename"])
            st.markdown(
                f"<span class='score-pill {css_class}'>{row['Match Score (%)']}% Match</span>",
                unsafe_allow_html=True,
            )
            st.progress(float(row["Match Score (%)"]) / 100.0)
            st.caption(f"Matching: {row['Matching Skills'] or '—'}")

            if st.button("View", key=f"top_view_{row['_resume_key']}"):
                st.session_state.active_preview_key = row["_resume_key"]
            st.download_button(
                label="Download",
                data=row["_resume_bytes"],
                file_name=row["Resume Filename"],
                mime="application/pdf",
                key=f"top_download_{row['_resume_key']}",
            )
            st.markdown("</div>", unsafe_allow_html=True)


def render_score_visualizations(df: pd.DataFrame) -> None:
    """Render histogram and top-candidate bar chart for score distribution."""
    st.subheader("Score Analytics")
    if df.empty:
        st.caption("No scores available for visualization.")
        return

    col_hist, col_bar = st.columns(2)

    with col_hist:
        histogram = (
            alt.Chart(df)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Match Score (%):Q", bin=alt.Bin(maxbins=12), title="Match Score (%)"),
                y=alt.Y("count():Q", title="Candidates"),
                color=alt.value("#38bdf8"),
                tooltip=[alt.Tooltip("count():Q", title="Candidates")],
            )
            .properties(height=260, title="Score Distribution")
        )
        st.altair_chart(histogram, use_container_width=True)

    with col_bar:
        top10 = df.head(10).copy()
        bar_chart = (
            alt.Chart(top10)
            .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
            .encode(
                x=alt.X("Match Score (%):Q", title="Match Score (%)"),
                y=alt.Y("Candidate Name:N", sort="-x", title="Candidate"),
                color=alt.value("#818cf8"),
                tooltip=["Candidate Name", "Resume Filename", "Match Score (%)"],
            )
            .properties(height=260, title="Top 10 Candidates")
        )
        st.altair_chart(bar_chart, use_container_width=True)


def render_candidate_table(df: pd.DataFrame) -> pd.DataFrame:
    """Render searchable, filterable, sortable candidate table with actions."""
    st.subheader("Interactive Candidate Table")
    if df.empty:
        st.caption("No candidates to display.")
        return df

    control_cols = st.columns([2, 1, 1, 1])
    with control_cols[0]:
        search_query = st.text_input("Search candidate/resume/skills", value="")
    with control_cols[1]:
        min_score = st.slider("Min Score", 0, 100, 0)
    with control_cols[2]:
        sort_by = st.selectbox(
            "Sort By",
            options=["Rank", "Match Score (%)", "Candidate Name", "Resume Length (words)", "Estimated Experience (Years)"],
            index=1,
        )
    with control_cols[3]:
        descending = st.checkbox("Descending", value=True)

    filtered = df.copy()
    if search_query.strip():
        query = search_query.lower()
        mask = (
            filtered["Candidate Name"].str.lower().str.contains(query)
            | filtered["Resume Filename"].str.lower().str.contains(query)
            | filtered["Matching Skills"].str.lower().str.contains(query)
        )
        filtered = filtered[mask]

    filtered = filtered[filtered["Match Score (%)"] >= min_score]
    filtered = filtered.sort_values(by=sort_by, ascending=not descending).reset_index(drop=True)

    display_cols = [
        "Rank",
        "Candidate Name",
        "Resume Filename",
        "Match Score (%)",
        "Matching Skills",
        "Missing Skills",
        "Resume Length (words)",
        "Estimated Experience (Years)",
    ]
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)

    st.markdown("**View Resume**")
    for _, row in filtered.iterrows():
        score_css = score_bucket(float(row["Match Score (%)"]))
        st.markdown("<div class='candidate-row'>", unsafe_allow_html=True)
        row_cols = st.columns([0.6, 1.3, 1.4, 0.8, 0.9, 1])
        row_cols[0].markdown(f"**#{int(row['Rank'])}**")
        row_cols[1].markdown(row["Candidate Name"])
        row_cols[2].caption(row["Resume Filename"])
        row_cols[3].markdown(
            f"<span class='score-pill {score_css}'>{row['Match Score (%)']}%</span>",
            unsafe_allow_html=True,
        )
        if row_cols[4].button("View", key=f"view_{row['_resume_key']}"):
            st.session_state.active_preview_key = row["_resume_key"]
        row_cols[5].download_button(
            "Download",
            data=row["_resume_bytes"],
            file_name=row["Resume Filename"],
            mime="application/pdf",
            key=f"download_{row['_resume_key']}",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    return filtered


def render_resume_preview(df: pd.DataFrame, preview_chars: int) -> None:
    """Show a text preview for the selected resume."""
    preview_key = st.session_state.active_preview_key
    if not preview_key:
        return

    row = df[df["_resume_key"] == preview_key]
    if row.empty:
        return

    record = row.iloc[0]
    st.subheader("Resume Preview")
    st.caption(f"{record['Candidate Name']} • {record['Resume Filename']}")
    snippet = str(record["_resume_text"])[:preview_chars]
    st.text_area("Extracted Resume Text", value=snippet, height=220)


def render_keywords(job_keywords: List[str]) -> None:
    """Render extracted job keywords as UI pills."""
    st.subheader("Extracted Job Keywords")
    if not job_keywords:
        st.caption("No keywords extracted from job description.")
        return

    pills = "".join([f"<span class='metric-pill'>{keyword}</span>" for keyword in job_keywords])
    st.markdown(pills, unsafe_allow_html=True)


def render_exports(df: pd.DataFrame) -> None:
    """Render CSV and Excel export actions for recruiter workflows."""
    st.subheader("Export Results")
    export_df = df[["Rank", "Resume Filename", "Match Score (%)"]].copy()

    col_csv, col_excel = st.columns(2)
    with col_csv:
        st.download_button(
            label="Export CSV",
            data=to_csv_bytes(export_df),
            file_name="ranked_candidates.csv",
            mime="text/csv",
        )
    with col_excel:
        st.download_button(
            label="Export Excel",
            data=to_excel_bytes(export_df),
            file_name="ranked_candidates.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


def main() -> None:
    init_state()
    inject_custom_css()

    if not render_authentication_view():
        return

    user = _safe_current_user()
    if not user:
        return

    shortlist_size, preview_chars = render_sidebar()

    render_admin_controls()
    render_account_dashboard(user)

    if not has_active_access(user):
        st.warning("Your subscription is inactive. Please complete payment to unlock screening access.")
        return

    st.title("Resume Screening AI")
    st.caption("A modern AI recruiting workspace to screen and rank resumes against any job description.")

    job_description = render_job_description_assistant()
    render_upload_area()

    analyze = st.button("Analyze Candidates", type="primary", use_container_width=True)

    if analyze:
        if not job_description.strip():
            st.error("Please enter a job description.")
            return
        if not st.session_state.uploaded_resume_store:
            st.error("Please upload at least one resume PDF.")
            return
        if len(st.session_state.uploaded_resume_store) > 200:
            st.warning("More than 200 resumes uploaded. For best performance, process in batches of up to 200.")

        plan = str(user.get("subscription_plan", "free"))
        limit = get_resume_limit(plan)
        resume_count = len(st.session_state.uploaded_resume_store)
        if limit is not None and resume_count > limit:
            st.error("You have exceeded your plan limit. Upgrade your plan to continue.")
            return

        st.session_state.processing_status = "Running analysis"
        try:
            with st.spinner("Analyzing resumes. This can take a moment for large batches..."):
                outputs = run_analysis(job_description, st.session_state.uploaded_resume_store)
                st.session_state.analysis_outputs = outputs
                updated_user = increment_usage_count(user["user_id"])
                st.session_state.current_user = updated_user
        except ValueError as error:
            st.session_state.processing_status = "Analysis failed"
            st.error(str(error))
            return

        st.session_state.processing_status = "Completed"

    outputs = st.session_state.analysis_outputs
    if outputs:
        ranked_df: pd.DataFrame = outputs["ranked_df"]
        top5_df: pd.DataFrame = outputs["top5_df"]
        top10_df: pd.DataFrame = outputs["top10_df"].head(shortlist_size)
        job_keywords: List[str] = outputs["job_keywords"]
        skipped_files: List[str] = outputs["skipped_files"]

        st.success(f"Analysis complete. Ranked {len(ranked_df)} candidates.")
        if skipped_files:
            st.warning(f"Skipped {len(skipped_files)} file(s) with no extractable text or invalid PDF format.")

        render_top_candidate_cards(top5_df)
        if str(user.get("subscription_plan", "free")) != "free":
            render_score_visualizations(ranked_df)
        else:
            st.info("Upgrade to Pro to unlock full analytics visualizations.")
        filtered_df = render_candidate_table(ranked_df)
        if str(user.get("subscription_plan", "free")) != "free":
            render_resume_preview(filtered_df, preview_chars=preview_chars)
        render_keywords(job_keywords)
        if str(user.get("subscription_plan", "free")) == "free":
            st.info("CSV/Excel exports are available on Pro and Agency plans.")
        else:
            render_exports(top10_df)


if __name__ == "__main__":
    main()
