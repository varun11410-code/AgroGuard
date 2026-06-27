"""
AgroGuard Backend - Rate Limit Policy Resolver

Isolates endpoint-to-policy resolution logic to keep middleware thin.
"""
from app.config.rate_limits import RATE_LIMIT_RULES, DEFAULT_RATE_LIMIT, EXEMPT_ENDPOINTS

class RateLimitPolicyResolver:
    @staticmethod
    def get_policy(endpoint: str) -> str:
        """
        Resolves the rate limit policy string for a given endpoint.
        Falls back to DEFAULT_RATE_LIMIT if not explicitly mapped.
        """
        if not endpoint:
            return DEFAULT_RATE_LIMIT
            
        return RATE_LIMIT_RULES.get(endpoint, DEFAULT_RATE_LIMIT)
        
    @staticmethod
    def is_exempt(endpoint: str) -> bool:
        """
        Checks if an endpoint is completely exempt from rate limiting.
        """
        if not endpoint:
            return True
            
        # Ignore static file routing and explicit health checks
        if endpoint in EXEMPT_ENDPOINTS or endpoint == "static":
            return True
            
        return False
