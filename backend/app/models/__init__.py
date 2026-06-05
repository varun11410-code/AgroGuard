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
    Crop           — crops table (Task 1.3)
    Scan           — scans table (Task 1.4)
    Report         — reports table (Task 1.5)
"""

from app.models.user import User, UserRole, BudgetTier  # noqa: F401
from app.models.crop import Crop                        # noqa: F401
from app.models.scan import Scan                        # noqa: F401
from app.models.report import Report                    # noqa: F401

__all__ = [
    # Task 1.2
    "User",
    "UserRole",
    "BudgetTier",
    # Task 1.3
    "Crop",
    # Task 1.4
    "Scan",
    # Task 1.5
    "Report",
]
