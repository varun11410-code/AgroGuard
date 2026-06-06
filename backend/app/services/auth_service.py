"""
AgroGuard Backend - Auth Service

Business logic for authentication.
"""
import bcrypt
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserRole

class AuthService:
    @staticmethod
    def register_user(name: str, email: str, password: str) -> dict:
        """
        Register a new user.
        Raises ValueError if email is already taken.
        """
        # Pre-check if email exists
        existing_user = UserRepository.get_by_email(email)
        if existing_user:
            raise ValueError("Email already exists")

        # Hash password using bcrypt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

        new_user = User(
            name=name,
            email=email,
            password_hash=hashed_password,
            role=UserRole.USER
        )

        # Race conditions mitigation: create() handles IntegrityError and raises ValueError
        created_user = UserRepository.create(new_user)

        return {
            "id": str(created_user.id),
            "name": created_user.name,
            "email": created_user.email,
            "role": created_user.role.value
        }
