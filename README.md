# Resume Screening AI

A modern, recruiter-friendly AI screening dashboard built with Python + Streamlit and fully open-source tooling.

## Features

- Email/password authentication with bcrypt hashing
- Supabase-backed user database and subscription metadata
- Stripe Checkout integration for Pro and Agency upgrades
- Stripe Billing Portal integration for self-service subscription management
- Automated webhook-driven payment verification and access activation/revocation
- Plan-based access controls and usage limits
- Admin controls (hidden mode via environment variable password)
- SaaS-style dashboard layout with sidebar, cards, analytics, and interactive ranking workspace
- Multi-PDF upload with file counter, preview list, and remove option
- Job Description Assistant with editable role templates for common job types
- Structured Job Assistant with Industry → Specialization → Job Role selection
- Text extraction using `PyPDF2`
- Embeddings using `SentenceTransformers` + Hugging Face model `all-MiniLM-L6-v2`
- Cosine similarity scoring with `scikit-learn`
- Top-candidate cards with color-coded score bands and progress indicators
- Full ranking table with search, filtering, sorting, and resume view/download actions
- Candidate insights: matching skills, missing skills, resume length, estimated experience
- Score analytics: histogram + top-candidate bar chart
- CSV and Excel export
- Temporary local file storage during processing (auto-cleanup)
- Invalid/empty-PDF skip handling with user warning

## Tech Stack

- Python
- Streamlit
- SentenceTransformers
- Hugging Face model: `sentence-transformers/all-MiniLM-L6-v2`
- PyPDF2
- Scikit-learn
- Pandas

## Project Structure

```text
resume-screening-ai/
├── app.py
├── stripe_webhook_server.py
├── supabase_schema.sql
├── run.ps1
├── requirements.txt
├── README.md
└── src/
    ├── __init__.py
  ├── jd_templates.py
    ├── pdf_utils.py
    ├── ranking.py
  ├── saas_auth.py
  ├── saas_billing.py
  ├── saas_config.py
  ├── saas_db.py
    └── text_utils.py
```

## How It Works

1. Recruiter selects Industry → Specialization → Job Role and auto-generates a structured job description.
2. Recruiter optionally inserts quick template blocks and edits the job description.
3. The app extracts text from each PDF.
4. The system encodes job description + resumes with `all-MiniLM-L6-v2`.
5. Cosine similarity is calculated between the JD embedding and each resume embedding.
6. Candidates are ranked with recruiter-focused insights and visual analytics.
## Job Taxonomy System

The Job Description Assistant now uses a 3-level structure:

- **Industry (Category)**
- **Specialization (Subcategory)**
- **Job Role**

The taxonomy and role templates live in [src/jd_templates.py](src/jd_templates.py).

- `JOB_CATALOG`: hierarchical category → subcategory → role mapping
- `ROLE_TEMPLATE_DATA`: structured role templates (30+ role-specific templates)
- `SUBCATEGORY_SKILLS`: skill suggestions attached to each specialization
- `QUICK_INSERT_BLOCKS`: one-click section blocks for fast JD editing

## How to Expand Categories Easily

1. Add a new category/subcategory/role list entry in `JOB_CATALOG`.
2. Add default skill tags for the subcategory in `SUBCATEGORY_SKILLS`.
3. (Optional) Add a richer role-specific template in `ROLE_TEMPLATE_DATA`.
4. Restart the app — dropdowns update automatically from the data structure.

## Local Installation

### 1) Clone and enter project

```bash
git clone <your-repo-url>
cd resume-screening-ai
```

### 2) Create virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Mac/Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 3.1) Configure environment variables

Set the following secrets locally (or in Streamlit Cloud Secrets):

- `SUPABASE_URL`
- `SUPABASE_KEY` (use service role key for backend updates)
- `STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET`
- `STRIPE_PRICE_PRO`
- `STRIPE_PRICE_AGENCY`
- `APP_BASE_URL` (example: `https://your-app.streamlit.app`)
- `ADMIN_PASSWORD`

On local PowerShell:

```powershell
$env:SUPABASE_URL="https://<project>.supabase.co"
$env:SUPABASE_KEY="<service_role_key>"
$env:STRIPE_SECRET_KEY="<stripe_secret_key>"
$env:STRIPE_WEBHOOK_SECRET="<webhook_secret>"
$env:STRIPE_PRICE_PRO="price_xxx"
$env:STRIPE_PRICE_AGENCY="price_xxx"
$env:APP_BASE_URL="http://localhost:8501"
$env:ADMIN_PASSWORD="change-this"
```

### 4) Run app

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal.

## Supabase Setup

1. Create a Supabase project.
2. Open SQL Editor and run [supabase_schema.sql](supabase_schema.sql).
3. Copy project URL and service role key into environment variables.

### User table fields

- `user_id`
- `email`
- `password_hash`
- `subscription_plan`
- `subscription_status`
- `stripe_customer_id`
- `stripe_subscription_id`
- `subscription_expiry`
- `created_at`
- `usage_count`

## Stripe Setup

1. Create two recurring Stripe Prices:
  - Pro monthly (`STRIPE_PRICE_PRO`)
  - Agency monthly (`STRIPE_PRICE_AGENCY`)
2. Set API secret in `STRIPE_SECRET_KEY`.
3. Configure webhook endpoint to your webhook server URL:
  - `checkout.session.completed`
  - `invoice.payment_succeeded`
  - `invoice.payment_failed`
  - `customer.subscription.deleted`
4. Save webhook signing secret in `STRIPE_WEBHOOK_SECRET`.

## Webhook Verification Logic

Webhook handler file: [stripe_webhook_server.py](stripe_webhook_server.py)

- Verifies Stripe event signature.
- Updates Supabase user subscription status automatically.
- Activates access on successful payment.
- Revokes access on payment failure/cancellation.

Run webhook server locally:

```bash
uvicorn stripe_webhook_server:app --host 0.0.0.0 --port 8000
```

For local Stripe webhook testing:

```bash
stripe listen --forward-to localhost:8000/stripe/webhook
```

## Access Control and Usage Limits

- Users must log in before accessing screening features.
- `subscription_status` must be `active`.
- Subscription expiry is automatically checked and inactive users are blocked.
- Plan limits enforced before analysis:
  - Free: max 10 resumes
  - Pro: max 200 resumes
  - Agency: unlimited

## Streamlit Cloud Deployment

1. Push repository to GitHub.
2. Deploy [app.py](app.py) on Streamlit Cloud.
3. Add all required secrets in Streamlit Cloud → App Settings → Secrets.
4. Set `APP_BASE_URL` to your Streamlit Cloud app URL.
5. Deploy webhook server separately (Render/Railway/Fly/Cloud Run) and register that URL in Stripe webhook settings.
6. Verify end-to-end flow:
  - Signup/login
  - Upgrade via Stripe Checkout
  - Webhook updates subscription in Supabase
  - Access automatically unlocks in Streamlit app

### Windows one-command launcher (PowerShell)

```powershell
.\run.ps1
```

Install deps and run in one command:

```powershell
.\run.ps1 -Install
```

Run on a custom port:

```powershell
.\run.ps1 -Port 8502
```

## Free Deployment Options

### Option A: Streamlit Community Cloud (Recommended)

1. Push this project to GitHub.
2. Go to Streamlit Community Cloud.
3. Create new app from your repo.
4. Set entrypoint to `app.py`.
5. Deploy.

### Option B: Hugging Face Spaces

1. Create a new Space (SDK: Streamlit).
2. Upload project files.
3. Ensure `requirements.txt` is included.
4. Set `app.py` as the main app.
5. Launch the Space.

## Performance Notes for 200 Resumes

- Embeddings are generated in batches for faster throughput.
- Model loading is cached using `st.cache_resource`.
- Uploaded files are written to a temporary directory during analysis and removed automatically.
- Candidate insights use lightweight heuristics to preserve speed and memory.
- Use concise PDFs and avoid scanned/image-only PDFs when possible (OCR is not included).

## Business Readiness Notes

- This MVP is suitable for startup/agency pilots.
- For production sales, consider:
  - Authentication & user management
  - Persistent storage (S3/Blob + DB)
  - Background processing queue
  - Audit logs and model monitoring
  - GDPR/data-retention controls

## Future Enhancements

- OCR support for scanned resumes (Tesseract or PaddleOCR)
- LLM-based section scoring (experience, skills, education)
- Multi-job benchmark ranking
- Recruiter feedback loop for reranking

## SaaS Productization Suggestions

- Add user authentication and role-based access for recruiter teams
- Persist jobs/resumes/results in a managed database and object storage
- Introduce async background workers for larger resume batches
- Add billing (usage tiers), team workspaces, and audit logging
- Implement compliance controls for retention, deletion, and consent tracking
