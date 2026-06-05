"""
AgroGuard Backend - Health Routes

Provides liveness and readiness check endpoints for the API.

Endpoints:
    GET /api/health          — Basic liveness probe (no DB required)
    GET /api/health/db       — Database readiness probe (pings Supabase)

Responses:
    200 OK   — service / database is reachable
    503      — database is unreachable (db endpoint only)
"""

from flask import Blueprint, jsonify

from app.database import check_db_health

health_bp = Blueprint("health", __name__)


# ---------------------------------------------------------------------------
# GET /api/health
# ---------------------------------------------------------------------------

@health_bp.get("/health")
def health_check():
    """
    Liveness endpoint.

    Does not touch the database — always returns 200 if the process is alive.

    Returns:
        JSON: ``{"success": true, "message": "AgroGuard API is running", "version": "1.0"}``
    """
    return jsonify({
        "success": True,
        "message": "AgroGuard API is running",
        "version": "1.0",
    }), 200


# ---------------------------------------------------------------------------
# GET /api/health/db
# ---------------------------------------------------------------------------

@health_bp.get("/health/db")
def db_health_check():
    """
    Database readiness endpoint.

    Executes a lightweight SELECT 1 against the configured Supabase/PostgreSQL
    instance and returns connection latency.

    Returns:
        200 — database reachable:
            ``{"success": true, "database": {...}}``
        503 — database unreachable:
            ``{"success": false, "database": {...}}``
    """
    result = check_db_health()
    is_ok = result["status"] == "ok"

    return jsonify({
        "success": is_ok,
        "database": result,
    }), 200 if is_ok else 503
