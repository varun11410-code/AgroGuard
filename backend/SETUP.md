# AgroGuard Backend — Developer Setup Guide

## Prerequisites

- Python 3.11+ installed
- `py` launcher available on Windows (`py --version`)

---

## 1. Create Virtual Environment

```bash
# From the backend/ directory
py -m venv venv
```

This creates `backend/venv/` — it is **gitignored** and must never be committed.

---

## 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

Your prompt will show `(venv)` when active.

---

## 3. Install Dependencies

```bash
# Production dependencies
pip install -r requirements.txt

# Development + testing dependencies
pip install -r requirements-dev.txt
```

---

## 4. Configure Environment Variables

```bash
# Copy the template
cp .env.example .env
```

Then open `.env` and fill in your values:

| Variable | Required | Description |
|---|---|---|
| `FLASK_ENV` | Yes | `development` \| `testing` \| `production` |
| `FLASK_DEBUG` | Dev only | `1` to enable debugger |
| `PORT` | No | Dev server port (default: `5001`) |
| `SECRET_KEY` | Yes (prod) | Random string for session signing |
| `DATABASE_URL` | Yes (prod) | PostgreSQL connection string — blank = SQLite fallback |
| `JWT_SECRET_KEY` | Yes (prod) | Random string for JWT signing |
| `GEMINI_API_KEY` | Yes | Google Gemini API key |
| `CLOUDINARY_CLOUD_NAME` | Yes | Cloudinary cloud name |
| `CLOUDINARY_API_KEY` | Yes | Cloudinary API key |
| `CLOUDINARY_API_SECRET` | Yes | Cloudinary API secret |

**Generate secret keys:**
```bash
py -c "import secrets; print(secrets.token_hex(32))"
```

---

## 5. Run the Development Server

```bash
py run.py
```

Expected output:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5001
```

---

## 6. Verify

```bash
curl http://127.0.0.1:5001/api/health
# Expected: {"message": "AgroGuard API is running", "success": true, "version": "1.0"}
```

---

## Environment Loading Strategy

```
run.py
  │
  ├── load_dotenv()          ← loads backend/.env into os.environ
  │
  ├── create_app(FLASK_ENV)  ← selects config class
  │
  └── Config class
        ├── os.getenv("DATABASE_URL") or "sqlite:///..."   ← safe empty-string fallback
        ├── os.getenv("JWT_SECRET_KEY") or "dev-default"
        └── os.getenv("SECRET_KEY") or "dev-default"
```

**Why `or` instead of `os.getenv("KEY", "default")`:**
`python-dotenv` sets a variable to `""` (empty string) when a key is present in `.env` but has no value. `os.getenv("KEY", "default")` returns `""` in that case, not the default. Using `os.getenv("KEY") or "default"` treats both `None` and `""` as missing.

---

## Dependency Groups

### `requirements.txt` — Production

| Package | Purpose |
|---|---|
| `flask` | Web framework |
| `flask-sqlalchemy` | ORM integration |
| `flask-migrate` | Database migrations (Alembic) |
| `flask-jwt-extended` | JWT authentication |
| `flask-cors` | Cross-origin resource sharing |
| `python-dotenv` | Load `.env` file |
| `pydantic` | Request/response validation |
| `bcrypt` | Password hashing |
| `psycopg2-binary` | PostgreSQL driver |
| `reportlab` | PDF generation |
| `google-generativeai` | Gemini AI API client |
| `cloudinary` | Image storage SDK |

### `requirements-dev.txt` — Development Only

| Package | Purpose |
|---|---|
| `pytest` | Test runner |
| `pytest-flask` | Flask test utilities |
| `pytest-cov` | Coverage reporting |
| `flake8` | Linting |
| `black` | Code formatting |
| `isort` | Import sorting |
