"""
AgroGuard Backend - Report Contract Schemas

Defines validation schemas for PDF report payloads.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, timezone

class ReportData(BaseModel):
    crop: str = Field(..., description="Name of the crop")
    disease: str = Field(..., description="Predicted disease name")
    confidence: float = Field(..., description="Confidence score from the ML model")
    selected_plan: Optional[str] = Field(None, description="The user's selected treatment plan (Budget, Standard, Premium)")
    image_path: Optional[str] = Field(None, description="Path or URL to the leaf image")
    
    # AI Enrichment fields (Phase 9)
    ai_summary: Optional[str] = Field(None, description="AI-generated summary of the diagnosis")
    treatment_recommendations: List[str] = Field(default_factory=list, description="AI-generated treatment recommendations")
    prevention_suggestions: List[str] = Field(default_factory=list, description="AI-generated prevention suggestions")
    
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of report generation")
