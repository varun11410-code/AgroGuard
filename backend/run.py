"""
AgroGuard Backend - Entry Point

Loads environment variables from .env and starts the Flask development server.

Usage:
    python run.py
"""

import os
from dotenv import load_dotenv

# Load .env before importing create_app so all os.getenv() calls
# inside config classes receive the correct values.
load_dotenv()

from app import create_app  # noqa: E402

app = create_app(os.getenv("FLASK_ENV", "development"))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5001)),
        debug=app.config.get("DEBUG", False),
        use_reloader=False,  # Reloader causes blueprint registration issues on Windows
    )
