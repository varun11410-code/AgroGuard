"""
AgroGuard Backend - Rate Limit Middleware

Thin orchestration layer that coordinates the Policy Resolver and Rate Limit Manager.
Injects standard rate limiting headers into the HTTP response.
"""
from flask import request, g, jsonify
import logging
from app.services.rate_limit_policy_resolver import RateLimitPolicyResolver
from app.services.rate_limit_manager import rate_limiter

logger = logging.getLogger(__name__)

def register_rate_limit_middleware(app):
    
    @app.before_request
    def check_rate_limit():
        # Do not rate limit OPTIONS requests
        if request.method == "OPTIONS":
            return

        endpoint = request.endpoint
        
        # 1. Resolve Policy
        if RateLimitPolicyResolver.is_exempt(endpoint):
            return
            
        policy_str = RateLimitPolicyResolver.get_policy(endpoint)
        
        # 2. Check Engine
        result = rate_limiter.check_limit(endpoint, policy_str)
        
        # Store headers to be injected in after_request
        g.rate_limit_headers = result.get("headers", {})
        
        # 3. Handle Rejection
        if not result.get("allowed"):
            logger.warning(
                f"[RATE LIMIT EXCEEDED] "
                f"Method: {request.method} | "
                f"Identity: {result.get('identity')} | "
                f"Endpoint: {endpoint} | "
                f"Rule: {policy_str}"
            )
            
            response = jsonify({
                "success": False,
                "message": "Too many requests. Please try again later."
            })
            response.status_code = 429
            
            # Attach headers to early rejection response
            for key, value in g.rate_limit_headers.items():
                response.headers[key] = value
                
            return response

    @app.after_request
    def inject_rate_limit_headers(response):
        """
        Injects the X-RateLimit headers computed during before_request.
        """
        if hasattr(g, 'rate_limit_headers'):
            for key, value in g.rate_limit_headers.items():
                response.headers[key] = value
        return response
