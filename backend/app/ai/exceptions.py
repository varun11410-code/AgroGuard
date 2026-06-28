"""
AgroGuard Backend - AI Exceptions

Defines the standard exception hierarchy for the AI infrastructure.
These exceptions abstract away provider-specific errors (like GoogleAPIError)
so that the service layer only handles domain-level AI failures.
"""
from app.core.exceptions import AIProviderError

class AIProviderConfigurationError(AIProviderError):
    """Raised when the AI factory fails to resolve a provider due to missing config or invalid name."""
    pass

class AIProviderTimeout(AIProviderError):
    """Raised when the AI provider network request times out."""
    pass

class AIProviderRateLimit(AIProviderError):
    """Raised when the AI provider rate limit is exceeded."""
    pass

class AIProviderInvalidResponse(AIProviderError):
    """Raised when the AI provider returns a malformed response that violates the expected contract."""
    pass
