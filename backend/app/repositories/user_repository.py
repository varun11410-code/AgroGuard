"""
AgroGuard Backend - User Repository

Handles database operations for the User model.
"""
from typing import Optional
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models.user import User

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
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Email already exists")

    @staticmethod
    def update(user: User) -> User:
        """Commit changes to an existing user."""
        try:
            db.session.commit()
            return user
        except Exception:
            db.session.rollback()
            raise
