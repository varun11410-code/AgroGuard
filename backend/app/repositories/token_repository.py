"""
AgroGuard Backend - Token Repository

Handles database operations for the RevokedToken model.
"""
import datetime
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models.revoked_token import RevokedToken

class TokenRepository:
    @staticmethod
    def add_revoked_token(jti: str, expires_at: datetime.datetime) -> None:
        """
        Add a token to the revoked tokens blocklist.
        Ignores if the token is already present (idempotent logout).
        """
        try:
            token = RevokedToken(jti=jti, expires_at=expires_at)
            db.session.add(token)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            # Token already blacklisted, this is fine for idempotent logout.

    @staticmethod
    def is_jti_blacklisted(jti: str) -> bool:
        """
        Check if a given JTI exists in the revoked tokens blocklist.
        """
        token = db.session.execute(
            db.select(RevokedToken).where(RevokedToken.jti == jti)
        ).scalar_one_or_none()
        return token is not None
