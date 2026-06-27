"""
AgroGuard Backend - Rate Limit Manager

An internal abstraction layer encapsulating the rate limiting engine (limits/Flask-Limiter core).
This ensures the rest of the application never depends directly on third-party libraries.
"""
import time
from math import ceil
from typing import Dict, Any
from limits import parse, strategies, storage
from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
import logging

logger = logging.getLogger(__name__)

class RateLimitManager:
    def __init__(self, storage_uri: str = "memory://"):
        """
        Initializes the rate limiting engine.
        Defaults to in-memory storage. 
        For Redis, simply pass 'redis://localhost:6379' from config.
        """
        self.storage = storage.storage_from_string(storage_uri)
        # FixedWindow is generally preferred for simple reliable API limiting
        self.strategy = strategies.FixedWindowRateLimiter(self.storage)

    def get_identity(self) -> str:
        """
        Implements the hybrid identity strategy.
        Returns the User UUID if authenticated, otherwise the Client IP.
        """
        try:
            # Try to verify JWT to get user identity without enforcing it
            verify_jwt_in_request(optional=True)
            user_id = get_jwt_identity()
            if user_id:
                return f"user:{user_id}"
        except Exception:
            pass
            
        # Fallback to IP address (respecting proxies)
        ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        if ip:
            # X-Forwarded-For can contain multiple IPs, take the first client IP
            ip = ip.split(',')[0].strip()
        return f"ip:{ip}"

    def check_limit(self, endpoint: str, policy_str: str) -> Dict[str, Any]:
        """
        Evaluates the rate limit for the current request.
        Returns a dictionary containing hit status and headers.
        """
        identity = self.get_identity()
        key = f"{endpoint}:{identity}"
        
        try:
            limit_item = parse(policy_str)
            # Hit the limit token bucket
            is_allowed = self.strategy.hit(limit_item, key)
            
            # Fetch window statistics for headers
            stats = self.strategy.get_window_stats(limit_item, key)
            
            # Calculate Retry-After in seconds
            now = time.time()
            retry_after = max(0, ceil(stats.reset_time - now))
            
            headers = {
                "X-RateLimit-Limit": str(limit_item.amount),
                "X-RateLimit-Remaining": str(stats.remaining),
                "X-RateLimit-Reset": str(ceil(stats.reset_time)),
            }
            
            if not is_allowed:
                headers["Retry-After"] = str(retry_after)
                
            return {
                "allowed": is_allowed,
                "headers": headers,
                "identity": identity
            }
            
        except Exception as e:
            # Fail open if the rate limiter itself crashes (e.g. Redis disconnects)
            logger.error(f"Rate limiter engine failed: {str(e)}")
            return {
                "allowed": True,
                "headers": {},
                "identity": identity
            }

# Singleton instance using in-memory storage for now
# Future: Initialize with config URL e.g. RATE_LIMIT_STORAGE_URL
rate_limiter = RateLimitManager()
