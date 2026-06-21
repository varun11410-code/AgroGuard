"""
AgroGuard Backend - Report Routes

Maps URLs to ReportController methods.
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.report_controller import ReportController

report_bp = Blueprint("reports", __name__)

@report_bp.post("/reports/generate")
@jwt_required(optional=True)
def generate_report():
    """
    Exposes report generation pipeline via POST /api/reports/generate.
    Allows guests, but persists metadata for authenticated users.
    """
    return ReportController.generate()

@report_bp.get("/reports")
@jwt_required()
def get_reports():
    """
    Retrieves the authenticated user's report history.
    """
    return ReportController.get_history()

@report_bp.get("/reports/<report_id>/download")
@jwt_required()
def download_historical_report(report_id):
    """
    Dynamically reconstructs and downloads a historical report.
    """
    return ReportController.download_historical(report_id)
