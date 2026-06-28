"""
AgroGuard Backend - Context Builder

Safely extracts and formats disease context from the database layer for use 
by the Gemini AI layer.
"""
from typing import Dict, Any, Optional
from app.models.scan import Scan
from app.core.exceptions import BadRequestException
import json

class ContextBuilder:
    @staticmethod
    def build_disease_context(scan: Scan, selected_plan: Optional[str] = None) -> Dict[str, Any]:
        """
        Safely extracts and whitelists context data from a Scan.
        
        Args:
            scan: The authorized Scan database model instance.
            selected_plan: The transient user-selected treatment tier.
            
        Returns:
            dict: Structured dictionary containing only whitelisted context fields.
            
        Raises:
            ValueError: If the scan is invalid, missing crops, pending, or has out-of-bounds confidence.
        """
        if not scan:
            raise BadRequestException("Scan cannot be None.", error_code="CONTEXT_SCAN_NONE")
            
        if not scan.crop:
            raise BadRequestException("Scan is missing required crop association.", error_code="CONTEXT_MISSING_CROP")
            
        if scan.predicted_disease is None:
            raise BadRequestException("Prediction is pending or missing.", error_code="CONTEXT_MISSING_PREDICTION")
            
        if scan.confidence_score is None or not (0.0 <= scan.confidence_score <= 1.0):
            raise BadRequestException("Confidence score out of bounds or missing.", error_code="CONTEXT_INVALID_CONFIDENCE")
            
        return {
            "crop": scan.crop.name,
            "disease": scan.predicted_disease,
            "confidence": scan.confidence_score,
            "selected_plan": selected_plan
        }
