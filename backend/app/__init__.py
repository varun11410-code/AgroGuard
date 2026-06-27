"""
AgroGuard Backend - Application Factory

This module defines create_app(), the central factory function that
initialises Flask extensions, registers blueprints, and returns a
fully configured Flask application instance.

Using a factory function (instead of a module-level app object) allows:
  - Multiple configurations (dev / test / prod) from the same codebase.
  - Easier unit testing by calling create_app("testing") per test.
  - No circular-import issues between extensions and models.

Usage:
    from app import create_app
    app = create_app("development")
    app.run()
"""

import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import config_map
from app.config.validator import validate_production_config
from app.database import db, migrate


def create_app(env: str | None = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        env: Environment name — "development", "testing", or "production".
             Defaults to the FLASK_ENV environment variable, falling back
             to "development".

    Returns:
        A fully configured Flask application instance.
    """
    if env is None:
        env = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)

    # ------------------------------------------------------------------ #
    # Configuration                                                        #
    # ------------------------------------------------------------------ #
    app.config.from_object(config_map[env])

    # Validate required secrets are set before accepting requests.
    # Only enforced in production — dev/testing use safe fallback defaults.
    if env == "production":
        validate_production_config(app)

    # ------------------------------------------------------------------ #
    # Extensions                                                           #
    # ------------------------------------------------------------------ #
    _register_extensions(app)

    # ------------------------------------------------------------------ #
    # Middleware / Error Handlers                                          #
    # ------------------------------------------------------------------ #
    from app.middleware.error_handler import register_error_handlers
    register_error_handlers(app)

    # ------------------------------------------------------------------ #
    # Blueprints                                                           #
    # ------------------------------------------------------------------ #
    _register_blueprints(app)

    # ------------------------------------------------------------------ #
    # Commands                                                             #
    # ------------------------------------------------------------------ #
    _register_commands(app)

    # ------------------------------------------------------------------ #
    # ML Models Loading                                                  #
    # ------------------------------------------------------------------ #
    if not app.config.get("TESTING"):
        with app.app_context():
            from app.ml import ModelLoader
            ModelLoader.load_all()

    return app



def _register_extensions(app: Flask) -> None:
    """Initialise all Flask extensions with the application instance."""
    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    # Storage
    from app.storage import storage
    storage.init_app(app)

    # Import all models so Alembic/Flask-Migrate can auto-detect the full
    # schema when generating migrations.  Uses an alias to avoid shadowing
    # the `app` Flask-instance parameter with the `app` Python package.
    import app.models as _models  # noqa: F401, PLC0415

    # Authentication
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        """
        Callback to check if a JWT has been revoked.
        Uses the TokenRepository to verify against the database.
        """
        # Optimization: Only check the blocklist for refresh tokens.
        # This keeps standard API requests fast and stateless.
        if jwt_payload.get("type") == "access":
            return False
            
        from app.repositories.token_repository import TokenRepository
        jti = jwt_payload["jti"]
        return TokenRepository.is_jti_blacklisted(jti)

    # Cross-Origin Resource Sharing
    CORS(
        app,
        origins=app.config.get("CORS_ORIGINS", ["http://localhost:3000"]),
        supports_credentials=True,
    )



def _register_blueprints(app: Flask) -> None:
    """Register all route blueprints on the application."""
    from app.routes.health import health_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.scan_routes import scan_bp
    from app.routes.report_routes import report_bp
    from app.routes.chat_routes import chat_bp
    from app.routes.admin_routes import admin_bp

    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(scan_bp, url_prefix="/api")
    app.register_blueprint(report_bp, url_prefix="/api")
    app.register_blueprint(chat_bp, url_prefix="/api")
    app.register_blueprint(admin_bp)



def _register_commands(app: Flask) -> None:
    """Register all custom CLI commands on the application."""
    from app.commands import register_commands
    register_commands(app)
