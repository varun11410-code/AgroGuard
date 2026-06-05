"""
AgroGuard Backend - Database Module

Provides shared SQLAlchemy and Flask-Migrate extension instances,
plus a health check utility for verifying the Supabase/PostgreSQL
connection at runtime.

Architecture:
    This module follows the application factory pattern.  The `db`
    and `migrate` instances are created here without being bound to
    any particular Flask app.  Binding happens later inside
    create_app() via the init_app() calls in app/__init__.py.

    ┌──────────────┐         ┌──────────────────────┐
    │  app/database│  ─────► │  Flask app (factory) │
    │  db / migrate│         │  db.init_app(app)    │
    └──────────────┘         └──────────────────────┘

Exports:
    db:             SQLAlchemy instance — import for model definitions
                    and query execution.
    migrate:        Flask-Migrate instance — drives Alembic migrations.
    check_db_health: Callable that verifies the live database connection.

Usage:
    # Model definition
    from app.database import db

    class MyModel(db.Model):
        id = db.Column(db.Integer, primary_key=True)

    # Health check (called inside an app context)
    from app.database import check_db_health

    with app.app_context():
        status = check_db_health()
        print(status)  # {"status": "ok", "database": "postgresql", ...}
"""

from __future__ import annotations

import time
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import text

# ---------------------------------------------------------------------------
# Shared extension instances
# ---------------------------------------------------------------------------
# Created here once; bound to the Flask app inside create_app() via init_app().

db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()


# ---------------------------------------------------------------------------
# Health check utility
# ---------------------------------------------------------------------------

def check_db_health() -> dict[str, Any]:
    """
    Verify the live database connection and return a status dictionary.

    Executes a lightweight ``SELECT 1`` query against the configured
    database.  Must be called from within an active Flask application
    context (i.e. after ``db.init_app(app)`` has been called and
    inside ``app.app_context()``).

    Returns:
        dict: A status payload with at least the following keys:

        .. code-block:: python

            {
                "status":        "ok" | "error",
                "database":      "postgresql" | "sqlite" | "unknown",
                "response_ms":   float,          # round-trip latency
                "error":         str | None,     # present only on failure
            }

    Example:
        >>> with app.app_context():
        ...     result = check_db_health()
        ...     assert result["status"] == "ok"
    """
    start = time.monotonic()

    try:
        # A trivial query that every supported backend understands.
        db.session.execute(text("SELECT 1"))

        elapsed_ms = round((time.monotonic() - start) * 1000, 2)

        # Determine the backend dialect for informational purposes.
        dialect = _get_dialect_name()

        return {
            "status": "ok",
            "database": dialect,
            "response_ms": elapsed_ms,
        }

    except Exception as exc:  # noqa: BLE001  (broad — intentional for health probes)
        elapsed_ms = round((time.monotonic() - start) * 1000, 2)
        return {
            "status": "error",
            "database": "unknown",
            "response_ms": elapsed_ms,
            "error": str(exc),
        }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _get_dialect_name() -> str:
    """
    Return a human-readable name for the active SQLAlchemy dialect.

    Returns:
        str: One of ``"postgresql"``, ``"sqlite"``, or ``"unknown"``.
    """
    try:
        dialect = db.engine.dialect.name  # type: ignore[union-attr]
        if dialect == "postgresql":
            return "postgresql"
        if dialect == "sqlite":
            return "sqlite"
        return dialect
    except Exception:  # noqa: BLE001
        return "unknown"
