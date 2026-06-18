"""
AgroGuard Backend - Application Exceptions

Defines custom exceptions for the application.
"""

class AgroGuardBaseException(Exception):
    """Base exception for all custom AgroGuard exceptions."""
    pass

class ReportGenerationError(AgroGuardBaseException):
    """Raised when PDF report generation fails fundamentally."""
    pass

class AIProviderError(AgroGuardBaseException):
    """Raised when the AI provider fails to generate text or returns invalid data."""
    pass
