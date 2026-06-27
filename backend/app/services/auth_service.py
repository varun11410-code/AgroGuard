"""
AgroGuard Backend - Auth Service

Business logic for authentication.
"""
import bcrypt
import logging
from app.core.exceptions import (
    ConflictException,
    UnauthorizedException,
    NotFoundException,
    BadRequestException
)
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
            raise ConflictException("Email already exists", error_code="AUTH_EMAIL_EXISTS")

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

        from app.services.activity_log_service import ActivityLogService
        ActivityLogService.log_user_registered(user_id=created_user.id)

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
        Raises UnauthorizedException if credentials are invalid.
        """
        from flask import request
        user_agent = request.headers.get("User-Agent", "unknown") if request else "unknown"
        from app.services.activity_log_service import ActivityLogService

        user = UserRepository.get_by_email(email)
        if not user:
            ActivityLogService.log_user_login_failed(attempted_email=email, user_agent=user_agent)
            raise UnauthorizedException("Invalid email or password", error_code="AUTH_INVALID_CREDENTIALS")

        # Verify bcrypt password
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            ActivityLogService.log_user_login_failed(attempted_email=email, user_agent=user_agent)
            raise UnauthorizedException("Invalid email or password", error_code="AUTH_INVALID_CREDENTIALS")

        # Import JWT functions locally or at the top of the file
        from flask_jwt_extended import create_access_token, create_refresh_token

        identity = str(user.id)
        additional_claims = {"role": user.role.value}

        access_token = create_access_token(identity=identity, additional_claims=additional_claims)
        refresh_token = create_refresh_token(identity=identity, additional_claims=additional_claims)

        ActivityLogService.log_user_login_success(
            user_id=user.id,
            user_agent=user_agent
        )

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

    @staticmethod
    def get_current_user(user_id: str) -> dict:
        """
        Fetch the current authenticated user details.
        Raises ValueError if the user is not found in the database.
        """
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found", error_code="AUTH_USER_NOT_FOUND")

        return {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "language": user.language,
            "preferred_budget_tier": user.preferred_budget_tier.value,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }

    @staticmethod
    def update_preferences(user_id: str, language: str | None = None, preferred_budget_tier: str | None = None) -> dict:
        """
        Update user preferences.
        """
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise NotFoundException("User not found", error_code="AUTH_USER_NOT_FOUND")

        if language is not None:
            user.language = language

        if preferred_budget_tier is not None:
            from app.models.user import BudgetTier
            try:
                user.preferred_budget_tier = BudgetTier(preferred_budget_tier)
            except ValueError:
                raise BadRequestException("Invalid budget tier", error_code="AUTH_INVALID_BUDGET")

        UserRepository.update(user)

        return {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role.value,
            "language": user.language,
            "preferred_budget_tier": user.preferred_budget_tier.value,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }

    @staticmethod
    def logout_user(jti: str, expires_at: int) -> None:
        """
        Log out the user by revoking their refresh token.
        """
        import datetime
        from app.repositories.token_repository import TokenRepository
        
        # Convert the UNIX timestamp to a UTC datetime
        expiry_datetime = datetime.datetime.fromtimestamp(expires_at, datetime.timezone.utc)
        
        TokenRepository.add_revoked_token(jti=jti, expires_at=expiry_datetime)
        
        # We don't have the user_id readily available in the token payload directly in logout_user signature,
        # but we can try to extract it from get_jwt_identity() if needed. 
        # Alternatively, we can just log the JTI.
        from flask_jwt_extended import get_jwt_identity
        try:
            identity = get_jwt_identity()
        except Exception:
            pass
