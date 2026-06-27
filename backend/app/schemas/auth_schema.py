"""
AgroGuard Backend - Auth Schemas

Defines validation schemas for authentication endpoints.
"""
import re
from typing import Literal, Optional
from pydantic import BaseModel, Field, field_validator
from app.utils.validators import sanitize_string

class RegisterRequestSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: str = Field(..., min_length=5, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)

    @field_validator("name", mode="before")
    @classmethod
    def apply_sanitization(cls, v: str) -> str:
        return sanitize_string(v)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Strip whitespace and lowercase the email."""
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("Invalid email format")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        return v

class LoginRequestSchema(BaseModel):
    email: str = Field(...)
    password: str = Field(...)

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        """Strip whitespace and lowercase the email."""
        if isinstance(v, str):
            return v.strip().lower()
        return v

    @field_validator("email")
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", v):
            raise ValueError("Invalid email format")
        return v

class UpdatePreferencesSchema(BaseModel):
    language: Optional[Literal["en", "hi"]] = Field(default=None)
    preferred_budget_tier: Optional[Literal["BUDGET", "STANDARD", "PREMIUM"]] = Field(default=None)
