"""
AgroGuard Backend - Scan Routes

Maps URLs to ScanController methods.
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.scan_controller import ScanController

scan_bp = Blueprint("scans", __name__)

@scan_bp.post("/scans")
@jwt_required(optional=True)
def predict_scan():
    """
    Exposes prediction pipeline via POST /api/scans
    """
    return ScanController.predict()

@scan_bp.get("/scans")
@jwt_required()
def get_scan_history():
    """
    Retrieves the authenticated user's scan history.
    """
    return ScanController.get_history()
