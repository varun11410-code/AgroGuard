"""
AgroGuard Backend - Common Schemas

Defines generic, reusable schemas such as pagination models.
"""
from pydantic import BaseModel, Field
from typing import Optional

class PaginationQuerySchema(BaseModel):
    """
    Reusable schema for validating pagination query parameters.
    """
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)

class ChatSessionQuerySchema(BaseModel):
    """
    Schema for validating chat session query parameters.
    """
    scan_id: Optional[str] = Field(default=None)
