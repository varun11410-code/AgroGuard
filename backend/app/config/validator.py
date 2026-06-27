"""
AgroGuard Backend - Configuration Validator

Validates that all required environment variables are set before the
Flask application starts handling requests in production.

Ensures that:
1. Debug mode is disabled.
2. Required static secrets are set.
3. The configured AI_PROVIDER is supported and its specific key is present.
4. Secrets do not contain insecure placeholder strings.
"""

from flask import Flask

# Base keys that MUST be set to non-default values in production.
_REQUIRED_PRODUCTION_KEYS: list[tuple[str, str]] = [
    ("SECRET_KEY", "Flask session signing key (SECRET_KEY)"),
    ("JWT_SECRET_KEY", "JWT signing key (JWT_SECRET_KEY)"),
    ("SQLALCHEMY_DATABASE_URI", "PostgreSQL connection string (DATABASE_URL)"),
    ("CLOUDINARY_CLOUD_NAME", "Cloudinary cloud name (CLOUDINARY_CLOUD_NAME)"),
    ("CLOUDINARY_API_KEY", "Cloudinary API key (CLOUDINARY_API_KEY)"),
    ("CLOUDINARY_API_SECRET", "Cloudinary API secret (CLOUDINARY_API_SECRET)"),
]

# AI Provider requirements mapping
AI_PROVIDER_REQUIREMENTS: dict[str, list[tuple[str, str]]] = {
    "groq": [("GROQ_API_KEY", "Groq API key (GROQ_API_KEY)")],
    "gemini": [("GEMINI_API_KEY", "Google Gemini API key (GEMINI_API_KEY)")],
}

# Substrings that indicate a key is still using an insecure placeholder.
# Uses substring matching to catch variations like "jwt-changeme" or "my-secret-key"
_INSECURE_SUBSTRINGS: list[str] = [
    "changeme",
    "secret",
    "password",
    "dev",
    "test",
    "default",
    "your-secret-key"
]

# Specific exact values that are also insecure (like empty string or default sqlite path)
_INSECURE_EXACT: set[str] = {
    "",
    "sqlite:///agroguard_dev.db"
}

def _is_insecure(value: str) -> bool:
    """Returns True if the value matches any insecure heuristic."""
    val_str = str(value).lower().strip()
    
    if val_str in _INSECURE_EXACT:
        return True
        
    for substring in _INSECURE_SUBSTRINGS:
        if substring in val_str:
            return True
            
    return False

def validate_production_config(app: Flask) -> None:
    """
    Validate that all required production secrets are properly set.
    """
    missing: list[str] = []

    # 1. Enforce DEBUG = False
    if app.config.get("DEBUG") is True:
        missing.append("  - DEBUG mode must be disabled in production")

    # 2. Build full required keys list
    required_keys = list(_REQUIRED_PRODUCTION_KEYS)
    
    provider = app.config.get("AI_PROVIDER", "").lower()
    
    if not provider:
        missing.append("  - AI_PROVIDER is missing")
    elif provider not in AI_PROVIDER_REQUIREMENTS:
        missing.append(f"  - AI_PROVIDER '{provider}' is not supported")
    else:
        required_keys.extend(AI_PROVIDER_REQUIREMENTS[provider])

    # 3. Check all required keys
    for config_key, label in required_keys:
        value = app.config.get(config_key)
        if not value or _is_insecure(value):
            missing.append(f"  - {label}")

    if missing:
        missing_list = "\n".join(missing)
        raise RuntimeError(
            f"Production startup blocked — required config is missing or insecure:\n"
            f"{missing_list}\n\n"
            f"Set these values securely in your environment before deploying."
        )
