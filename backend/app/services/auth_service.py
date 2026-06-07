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

    @staticmethod
    def login_user(email: str, password: str) -> dict:
        """
        Authenticate a user and return JWT tokens.
        Raises ValueError if credentials are invalid.
        """
        user = UserRepository.get_by_email(email)
        if not user:
            raise ValueError("Invalid email or password")

        # Verify bcrypt password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise ValueError("Invalid email or password")

        # Import JWT functions locally or at the top of the file
        from flask_jwt_extended import create_access_token, create_refresh_token

        identity = str(user.id)
        additional_claims = {"role": user.role.value}

        access_token = create_access_token(identity=identity, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": identity,
                "name": user.name,
                "email": user.email,
                "role": user.role.value
            }
        }

    @staticmethod
    def refresh_access_token(identity: str, claims: dict) -> str:
        """
        Generate a new access token using existing identity and claims.
        """
        from flask_jwt_extended import create_access_token

        additional_claims = {}
        if "role" in claims:
            additional_claims["role"] = claims["role"]

        access_token = create_access_token(identity=identity, additional_claims=additional_claims)

        return access_token
