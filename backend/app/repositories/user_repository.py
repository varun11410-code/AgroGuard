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
