"""
AgroGuard Backend - Configuration Validator

Validates that all required environment variables are set before the
Flask application starts handling requests.

This is called by create_app() only in the production environment.
In development and testing, missing secrets fall back to safe placeholder
values so the server can start without external credentials.

Functions:
    validate_production_config: Raises RuntimeError if any required
                                production secret is absent.
"""

from flask import Flask


# Keys that MUST be set to non-default values in production.
# Each entry is (config_key, human_readable_label).
_REQUIRED_PRODUCTION_KEYS: list[tuple[str, str]] = [
    ("SECRET_KEY", "Flask session signing key (SECRET_KEY)"),
    ("JWT_SECRET_KEY", "JWT signing key (JWT_SECRET_KEY)"),
    ("SQLALCHEMY_DATABASE_URI", "PostgreSQL connection string (DATABASE_URL)"),
    ("GEMINI_API_KEY", "Google Gemini API key (GEMINI_API_KEY)"),
    ("CLOUDINARY_CLOUD_NAME", "Cloudinary cloud name (CLOUDINARY_CLOUD_NAME)"),
    ("CLOUDINARY_API_KEY", "Cloudinary API key (CLOUDINARY_API_KEY)"),
    ("CLOUDINARY_API_SECRET", "Cloudinary API secret (CLOUDINARY_API_SECRET)"),
]

# Config values that indicate a key is still using an insecure default.
_INSECURE_DEFAULTS: set[str] = {
    "change-me-in-production",
    "jwt-change-me-in-production",
    "sqlite:///agroguard_dev.db",
    "",
}


def validate_production_config(app: Flask) -> None:
    """
    Validate that all required production secrets are properly set.

    Checks both that a config key exists and that its value is not
    an insecure development placeholder.

    Args:
        app: The configured Flask application instance.

    Raises:
        RuntimeError: If any required production secret is missing
                      or still set to an insecure default value.

    Example:
        >>> validate_production_config(app)  # raises if secrets missing
    """
    missing: list[str] = []

    for config_key, label in _REQUIRED_PRODUCTION_KEYS:
        value = app.config.get(config_key)
        if not value or str(value) in _INSECURE_DEFAULTS:
            missing.append(f"  - {label}")

    if missing:
        missing_list = "\n".join(missing)
        raise RuntimeError(
            f"Production startup blocked — required config is missing or insecure:\n"
            f"{missing_list}\n\n"
            f"Set these values in your environment or .env file before deploying."
        )
