"""
AgroGuard Backend - Report Contract Schemas

Defines validation schemas for PDF report payloads.
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Any
from datetime import datetime, timezone
from app.utils.validators import sanitize_string, validate_uuid4

class ReportData(BaseModel):
    scan_id: Optional[str] = Field(None, description="The ID of the parent scan")
    crop: str = Field(..., min_length=1, max_length=100, description="Name of the crop")
    disease: str = Field(..., min_length=1, max_length=100, description="Predicted disease name")
    confidence: float = Field(..., description="Confidence score from the ML model")
    selected_plan: Optional[str] = Field(None, max_length=100, description="The user's selected treatment plan (Budget, Standard, Premium)")
    image_stream: Optional[Any] = Field(None, description="Path string or BytesIO stream to the leaf image")
    
    # AI Enrichment fields
    ai_summary: Optional[str] = Field(None, max_length=10000, description="AI-generated summary of the diagnosis")
    risk_level: Optional[str] = Field(None, max_length=50, description="AI-assessed risk level")
    treatment_plans: Optional[List[dict]] = Field(None, description="Tiered JSON containing Budget, Standard, and Premium plans")
    
    # Legacy fields (Phase 9)
    treatment_recommendations: List[str] = Field(default_factory=list, description="Legacy AI-generated treatment recommendations")
    prevention_suggestions: List[str] = Field(default_factory=list, description="Legacy AI-generated prevention suggestions")
    
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of report generation")

    @field_validator("scan_id", mode="before")
    @classmethod
    def validate_uuid(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return validate_uuid4(v)
        return v

    @field_validator("crop", "disease", "selected_plan", "risk_level", mode="before")
    @classmethod
    def apply_sanitization(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return sanitize_string(v)
        return v
