"""
AgroGuard Backend - Database Module

Provides shared SQLAlchemy and Flask-Migrate extension instances.

These instances are created without being bound to a specific Flask app.
Binding happens inside create_app() via the init_app() pattern, which
allows the application factory to work correctly.

Exports:
    db:      SQLAlchemy instance — use for model definitions and queries.
    migrate: Flask-Migrate instance — use for database migrations.

Usage:
    from app.database import db
    class MyModel(db.Model): ...
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Shared extension instances (not yet bound to a Flask app)
db: SQLAlchemy = SQLAlchemy()
migrate: Migrate = Migrate()
