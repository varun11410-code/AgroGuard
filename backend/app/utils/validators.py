"""
AgroGuard Backend - Reusable Validators

Provides custom Pydantic validators and general validation utilities
used across various schemas to ensure DRY principles.
"""
from uuid import UUID

def validate_uuid4(v: str) -> str:
    """
    Reusable validator to ensure a string is a valid UUID4.
    """
    try:
        val = UUID(v, version=4)
        return str(val)
    except ValueError:
        raise ValueError("Invalid UUID format")

def sanitize_string(v: str) -> str:
    """
    Reusable validator to strip whitespace from strings.
    """
    if isinstance(v, str):
        return v.strip()
    return v
