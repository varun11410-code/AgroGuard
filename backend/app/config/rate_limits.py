"""
AgroGuard Backend - Rate Limits Configuration

Centralized configuration for API rate limits mapping endpoints to policies.
Policies are formatted as strings compatible with Flask-Limiter (e.g. "5 per minute").
"""

# The default limit if an endpoint is not explicitly configured
DEFAULT_RATE_LIMIT = "100 per minute"

# Mapping of endpoint names (Blueprint.function_name) to their rate limit policies
RATE_LIMIT_RULES = {
    # Critical Security Tier (Strict Limits)
    "auth.login": "5 per minute",
    "auth.register": "5 per hour",
    
    # High Compute / Cost Tier (Strict Limits)
    "scans.predict_scan": "50 per day",  # For auth users. Guest logic handled by hybrid identity.
    "chat.send_message": "20 per hour",
    "reports.generate_report": "10 per hour",
    
    # Standard API Tier (Moderate Limits)
    "auth.refresh": "10 per minute",
    "auth.me": "60 per minute",
    "auth.preferences": "20 per minute",
    "auth.logout": "10 per minute",
    
    "scans.get_scan_history": "60 per minute",
    "scans.delete_scan": "30 per minute",
    
    "reports.get_reports": "60 per minute",
    "reports.get_report": "60 per minute",
    "reports.delete_report": "30 per minute",
    
    "chat.get_session_history": "60 per minute",
    
    # Admin Tier
    "admin.get_stats": "100 per minute",
    "admin.get_logs": "100 per minute",
    "admin.get_analytics": "100 per minute",
    "admin.get_users": "100 per minute",
    "admin.get_scans": "100 per minute",
    "admin.get_reports": "100 per minute"
}

# Endpoints completely exempt from rate limiting
EXEMPT_ENDPOINTS = [
    "health.health_check",
    "static"
]
