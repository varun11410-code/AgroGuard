"""
AgroGuard Backend - Report Routes

Maps URLs to ReportController methods.
"""
from flask import Blueprint
from app.controllers.report_controller import ReportController

report_bp = Blueprint("reports", __name__)

@report_bp.post("/reports/generate")
def generate_report():
    """
    Exposes report generation pipeline via POST /api/reports/generate
    """
    return ReportController.generate()
