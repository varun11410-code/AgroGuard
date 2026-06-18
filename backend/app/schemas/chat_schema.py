"""
AgroGuard Backend - Chat Schemas

Pydantic validation schemas for chat requests and responses.
"""
from typing import Optional
from pydantic import BaseModel, Field

class ChatRequestSchema(BaseModel):
    """Schema for incoming chat messages."""
    message: str = Field(..., min_length=1, description="The user's message")
    session_id: Optional[str] = Field(None, description="The UUID of the chat session, if it exists")
    scan_id: Optional[str] = Field(None, description="The UUID of the scan, if this is a Mode B session")
    selected_plan: Optional[str] = Field(None, description="The user's selected treatment plan, if applicable")
