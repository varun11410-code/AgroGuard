"""
AgroGuard Backend - Scan Schemas

Defines validation schemas for scan endpoints, including form data.
"""
from pydantic import BaseModel, Field, field_validator
from app.utils.validators import sanitize_string

class ScanPredictionFormSchema(BaseModel):
    """
    Schema for validating the form data sent to POST /api/scans.
    Note: The file upload itself is validated explicitly in the controller 
    to prevent large payload body parsing issues, but the metadata is validated here.
    """
    crop: str = Field(..., min_length=1, max_length=100, description="Name of the crop")

    @field_validator("crop", mode="before")
    @classmethod
    def apply_sanitization(cls, v: str) -> str:
        return sanitize_string(v)
