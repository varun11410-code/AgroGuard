"""
AgroGuard Backend - RevokedToken Model

Defines the SQLAlchemy ORM model for storing revoked JWTs.
This enables logout functionality by persisting blacklisted tokens.
"""

from __future__ import annotations

import datetime
import uuid

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime

from app.database import db

class RevokedToken(db.Model):
    """
    ORM model representing the ``revoked_tokens`` table.
    
    Attributes:
        id:          UUID primary key.
        jti:         The unique identifier of the JWT (from the "jti" claim).
        created_at:  When the token was added to the database.
        expires_at:  When the token expires (so we can safely prune it).
    """

    __tablename__ = "revoked_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    jti: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        unique=True,
        index=True,
        doc="The JWT's unique identifier (jti claim).",
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.datetime.now(datetime.timezone.utc),
    )

    expires_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        doc="The absolute expiration time of the JWT, used for pruning.",
    )

    def __repr__(self) -> str:
        return f"<RevokedToken jti={self.jti!r}>"
