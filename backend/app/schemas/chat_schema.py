"""
AgroGuard Backend - Chat Schemas

Pydantic validation schemas for chat requests and responses.
"""
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from app.utils.validators import sanitize_string, validate_uuid4

class ChatRequestSchema(BaseModel):
    """Schema for incoming chat messages."""
    message: str = Field(..., min_length=1, max_length=2000, description="The user's message")
    session_id: Optional[str] = Field(None, description="The UUID of the chat session, if it exists")
    scan_id: Optional[str] = Field(None, description="The UUID of the scan, if this is a Mode B session")
    selected_plan: Optional[str] = Field(None, max_length=100, description="The user's selected treatment plan, if applicable")

    @field_validator("session_id", "scan_id", mode="before")
    @classmethod
    def validate_uuids(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return validate_uuid4(v)
        return v

    @field_validator("selected_plan", mode="before")
    @classmethod
    def apply_sanitization(cls, v: Optional[str]) -> Optional[str]:
        if v:
            return sanitize_string(v)
        return v
