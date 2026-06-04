"""
AgroGuard Backend - Health Route

Provides a simple liveness check endpoint for the API.

Endpoint:
    GET /api/health

Response:
    200 OK  — {"success": true, "message": "AgroGuard API is running", "version": "1.0"}
"""

from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("/health")
def health_check():
    """
    Liveness endpoint.

    Returns:
        JSON response confirming the API is running.
    """
    return jsonify({
        "success": True,
        "message": "AgroGuard API is running",
        "version": "1.0",
    }), 200
