"""
AgroGuard Backend - Report Contract Schemas

Defines validation schemas for PDF report payloads.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime, timezone

class ReportData(BaseModel):
    scan_id: Optional[str] = Field(None, description="The ID of the parent scan")
    crop: str = Field(..., description="Name of the crop")
    disease: str = Field(..., description="Predicted disease name")
    confidence: float = Field(..., description="Confidence score from the ML model")
    selected_plan: Optional[str] = Field(None, description="The user's selected treatment plan (Budget, Standard, Premium)")
    image_stream: Optional[Any] = Field(None, description="Path string or BytesIO stream to the leaf image")
    
    # AI Enrichment fields
    ai_summary: Optional[str] = Field(None, description="AI-generated summary of the diagnosis")
    risk_level: Optional[str] = Field(None, description="AI-assessed risk level")
    treatment_plans: Optional[List[dict]] = Field(None, description="Tiered JSON containing Budget, Standard, and Premium plans")
    
    # Legacy fields (Phase 9)
    treatment_recommendations: List[str] = Field(default_factory=list, description="Legacy AI-generated treatment recommendations")
    prevention_suggestions: List[str] = Field(default_factory=list, description="Legacy AI-generated prevention suggestions")
    
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of report generation")
