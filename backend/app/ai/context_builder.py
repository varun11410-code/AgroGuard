"""
AgroGuard Backend - Context Builder

Safely extracts and formats disease context from the database layer for use 
by the Gemini AI layer.
"""
from typing import Dict, Any, Optional
from app.models.scan import Scan

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
            raise ValueError("Scan cannot be None.")
            
        if not scan.crop:
            raise ValueError("Scan is missing required crop association.")
            
        if scan.predicted_disease is None:
            raise ValueError("Prediction is pending or missing.")
            
        if scan.confidence_score is None or not (0.0 <= scan.confidence_score <= 1.0):
            raise ValueError("Confidence score out of bounds or missing.")
            
        return {
            "crop": scan.crop.name,
            "disease": scan.predicted_disease,
            "confidence": scan.confidence_score,
            "selected_plan": selected_plan
        }
