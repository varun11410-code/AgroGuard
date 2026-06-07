"""
AgroGuard Backend - Auth Decorators

Provides reusable decorators for Role-Based Access Control (RBAC).
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required():
    """
    Decorator that requires a valid JWT access token and ADMIN role.
    Rejects USER role with 403 Forbidden.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # Verify JWT exists and is valid
            verify_jwt_in_request()
            
            # Extract claims from the valid JWT
            claims = get_jwt()
            
            # Check the role claim
            if claims.get("role") != "ADMIN":
                return jsonify({
                    "success": False,
                    "message": "Admin access required"
                }), 403
                
            return fn(*args, **kwargs)
        return decorator
    return wrapper
