"""
AgroGuard Backend - Scan Routes

Maps URLs to ScanController methods.
"""
from flask import Blueprint
from app.controllers.scan_controller import ScanController

scan_bp = Blueprint("scans", __name__)

@scan_bp.post("/scans")
def predict_scan():
    """
    Exposes prediction pipeline via POST /api/scans
    """
    return ScanController.predict()
