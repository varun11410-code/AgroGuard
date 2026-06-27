"""
AgroGuard Backend - Core Exceptions

Defines the centralized exception hierarchy for the application.
All custom exceptions must inherit from AgroGuardBaseException.
Exception classes should remain lightweight and contain NO business logic.
"""

from typing import Optional

class AgroGuardBaseException(Exception):
    """
    Root exception for all custom AgroGuard exceptions.
    
    Attributes:
        message (str): A safe, user-facing error message.
        status_code (int): The HTTP status code to return to the client.
        error_code (str | None): An internal, machine-readable error code for observability and logging.
    """
    def __init__(
        self,
        message: str,
        status_code: int = 500,
        error_code: Optional[str] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


# -----------------------------------------------------------------------------
# Standardized HTTP Exceptions (Client Errors - 4xx)
# -----------------------------------------------------------------------------

class BadRequestException(AgroGuardBaseException):
    """Raised for 400 Bad Request client errors."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=400, error_code=error_code)


class UnauthorizedException(AgroGuardBaseException):
    """Raised for 401 Unauthorized errors (authentication failures)."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=401, error_code=error_code)


class ForbiddenException(AgroGuardBaseException):
    """Raised for 403 Forbidden errors (authorization failures)."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=403, error_code=error_code)


class NotFoundException(AgroGuardBaseException):
    """Raised for 404 Not Found errors."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=404, error_code=error_code)


class ConflictException(AgroGuardBaseException):
    """Raised for 409 Conflict errors (e.g., resource already exists)."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=409, error_code=error_code)


class RateLimitException(AgroGuardBaseException):
    """Raised for 429 Too Many Requests errors."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=429, error_code=error_code)


# -----------------------------------------------------------------------------
# Domain Exceptions (Operational Errors - 5xx)
# -----------------------------------------------------------------------------

class DatabaseError(AgroGuardBaseException):
    """Base exception for all database operations."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=500, error_code=error_code)


class StorageError(AgroGuardBaseException):
    """Base exception for all storage operations."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=500, error_code=error_code)


class StorageConnectionError(StorageError):
    """Raised when the storage provider cannot be reached or authentication fails."""
    pass


class StorageUploadError(StorageError):
    """Raised when an upload operation fails."""
    pass


class StorageDeleteError(StorageError):
    """Raised when a deletion operation fails."""
    pass


class AIProviderError(AgroGuardBaseException):
    """Raised when the AI provider fails to generate text or returns invalid data."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=500, error_code=error_code)


class ReportGenerationError(AgroGuardBaseException):
    """Raised when PDF report generation fails fundamentally."""
    def __init__(self, message: str, error_code: Optional[str] = None):
        super().__init__(message, status_code=500, error_code=error_code)
