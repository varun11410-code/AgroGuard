"""
AgroGuard Backend - Models Package

Centralised import point for all SQLAlchemy ORM models.

Importing this package (or any module within it) ensures that every
model class is registered on ``db.metadata`` before Flask-Migrate
generates migrations.  The application factory (``create_app``) imports
this package inside ``_register_extensions`` so that Alembic can
auto-detect the full schema.

Exported models:
    User           — users table (Task 1.2)
"""

from app.models.user import User, UserRole, BudgetTier  # noqa: F401

__all__ = [
    "User",
    "UserRole",
    "BudgetTier",
]
