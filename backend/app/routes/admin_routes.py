"""
AgroGuard Backend - Admin Routes

Defines endpoints for the Admin Dashboard.
"""
from flask import Blueprint
from app.controllers.admin_controller import AdminController
from app.decorators.auth_decorators import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@admin_bp.get("/stats")
@admin_required()
def get_stats():
    """
    Get aggregate dashboard statistics.
    Requires ADMIN role.
    """
    return AdminController.get_stats()

@admin_bp.get("/logs")
@admin_required()
def get_logs():
    """
    Get paginated activity logs.
    Requires ADMIN role.
    """
    return AdminController.get_logs()
