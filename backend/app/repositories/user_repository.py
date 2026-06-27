"""
AgroGuard Backend - User Repository

Handles database operations for the User model.
"""
from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models.user import User
from app.core.exceptions import DatabaseError

class UserRepository:
    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Fetch a user by email address."""
        return db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()

    @staticmethod
    def get_by_id(user_id: str) -> Optional[User]:
        """Fetch a user by ID."""
        import uuid
        try:
            uid = uuid.UUID(user_id)
            return db.session.execute(db.select(User).where(User.id == uid)).scalar_one_or_none()
        except ValueError:
            return None

    @staticmethod
    def create(user: User) -> User:
        """
        Insert a new user into the database.
        Raises ValueError if an integrity constraint (e.g. duplicate email) is violated.
        """
        try:
            db.session.add(user)
            db.session.commit()
            return user
        except IntegrityError as e:
            db.session.rollback()
            raise DatabaseError("Database integrity error during user creation", error_code="DB_INTEGRITY_ERROR") from e

    @staticmethod
    def update(user: User) -> User:
        """Commit changes to an existing user."""
        try:
            db.session.commit()
            return user
        except Exception as e:
            db.session.rollback()
            raise DatabaseError("Failed to update user", error_code="DB_UPDATE_ERROR") from e

    @staticmethod
    def get_total_count() -> int:
        """
        Get the total number of registered users.
        """
        return db.session.scalar(db.select(db.func.count()).select_from(User)) or 0

    @staticmethod
    def get_paginated_users(page: int = 1, per_page: int = 50) -> tuple[list[User], int]:
        """Fetch paginated users, ordered by newest first."""
        query = db.select(User).order_by(User.created_at.desc())
        total_count = db.session.scalar(db.select(db.func.count()).select_from(User)) or 0
        offset = (page - 1) * per_page
        users = list(db.session.execute(query.limit(per_page).offset(offset)).scalars().all())
        return users, total_count

    @staticmethod
    def count_by_date_range(start_date, end_date) -> int:
        """Count users created within a specific date range."""
        return db.session.scalar(
            db.select(db.func.count(User.id))
            .where(User.created_at >= start_date, User.created_at <= end_date)
        ) or 0
