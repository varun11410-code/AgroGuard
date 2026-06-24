"""
AgroGuard Backend - User Model

Defines the SQLAlchemy ORM model for the ``users`` table in PostgreSQL
(Supabase).

Table: users

Architecture reference: Architecture.md §6 — Database Design
PRD reference:          PRD.md §7 F6 — User Authentication, F8 — User Preferences

Design decisions:
    * UUID primary key — avoids sequential ID enumeration attacks and
      matches the Architecture.md schema specification.
    * Native PostgreSQL UUID type (``sqlalchemy.dialects.postgresql.UUID``)
      so the column is stored as a true 16-byte uuid, not a VARCHAR.
    * Python Enum classes (``UserRole``, ``BudgetTier``) paired with
      SQLAlchemy's ``Enum`` type give compile-time type safety and a
      DB-enforced constraint (PostgreSQL CHECK or native ENUM).
    * ``password_hash`` stores only the bcrypt digest — never the raw
      password (AI_AGENT_RULES.md §16).
    * ``last_login_at`` is nullable; it is set to NULL until the user's
      first successful login.
    * ``updated_at`` is set server-side and auto-refreshes on every UPDATE
      via ``onupdate=func.now()``, keeping the column accurate without any
      application-layer boilerplate.

Usage:
    from app.models.user import User, UserRole, BudgetTier

    user = User(
        name="Varun",
        email="varun@example.com",
        password_hash=hashed_pw,
        role=UserRole.USER,
    )
"""

from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, Enum, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database import db

if TYPE_CHECKING:
    from app.models.scan import Scan
    from app.models.chat_session import ChatSession
    from app.models.activity_log import ActivityLog


# ---------------------------------------------------------------------------
# Enum Definitions
# ---------------------------------------------------------------------------

class UserRole(str, enum.Enum):
    """
    Role assigned to a registered user.

    Attributes:
        USER:  Standard user — can scan, view history, download reports,
               and use the AI assistant.
        ADMIN: Platform administrator — has access to analytics, activity
               logs, and user statistics.
    """

    USER = "USER"
    ADMIN = "ADMIN"


class BudgetTier(str, enum.Enum):
    """
    User's preferred treatment recommendation budget tier.

    Attributes:
        BUDGET:   Low-cost treatment approach.
        STANDARD: Balanced treatment approach.
        PREMIUM:  Comprehensive treatment approach.
    """

    BUDGET = "BUDGET"
    STANDARD = "STANDARD"
    PREMIUM = "PREMIUM"


# ---------------------------------------------------------------------------
# User Model
# ---------------------------------------------------------------------------

class User(db.Model):
    """
    ORM model representing the ``users`` table.

    Attributes:
        id:                   UUID primary key, auto-generated on insert.
        name:                 Display name (max 120 chars).
        email:                Unique, indexed login identifier (max 255 chars).
        password_hash:        bcrypt digest of the user's password (never plaintext).
        role:                 UserRole enum — USER or ADMIN.
        language:             Preferred display language (e.g. ``"en"``, ``"hi"``).
        preferred_budget_tier: Default treatment plan tier.
        is_active:            Soft-disable flag; False blocks login.
        created_at:           Row creation timestamp (set by database server).
        last_login_at:        Timestamp of most recent successful login; NULL
                              until first login.
        updated_at:           Automatically refreshed on every UPDATE.
    """

    __tablename__ = "users"

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Unique user identifier (UUID v4, auto-generated).",
    )

    # ------------------------------------------------------------------
    # Identity Fields
    # ------------------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
        doc="User's display name.",
    )

    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
        doc="User's email address — must be unique across all accounts.",
    )

    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="bcrypt hash of the user's password. Never store plaintext.",
    )

    # ------------------------------------------------------------------
    # Role & Preferences
    # ------------------------------------------------------------------

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role", create_type=True),
        nullable=False,
        default=UserRole.USER,
        doc="Access role. Defaults to USER on registration.",
    )

    language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="en",
        doc="ISO 639-1 language code for the user's preferred UI language.",
    )

    preferred_budget_tier: Mapped[BudgetTier] = mapped_column(
        Enum(BudgetTier, name="budget_tier", create_type=True),
        nullable=False,
        default=BudgetTier.STANDARD,
        doc="Default treatment recommendation tier selected by the user.",
    )

    # ------------------------------------------------------------------
    # Status Flag
    # ------------------------------------------------------------------

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="When False the account is disabled and login is blocked.",
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
        doc="UTC timestamp of account creation, set once by the database.",
    )

    last_login_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        doc="UTC timestamp of the user's most recent successful login.",
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        doc="UTC timestamp automatically updated on every row modification.",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    scans: Mapped[List["Scan"]] = relationship(
        "Scan",
        back_populates="user",
        lazy="select",
        cascade="all, delete-orphan",
        doc="All scans belonging to this user.",
    )

    chat_sessions: Mapped[List["ChatSession"]] = relationship(
        "ChatSession",
        back_populates="user",
        lazy="select",
        cascade="all, delete-orphan",
        doc="All chat sessions opened by this user.",
    )

    activity_logs: Mapped[List["ActivityLog"]] = relationship(
        "ActivityLog",
        back_populates="user",
        lazy="select",
        doc="All activity logs associated with this user.",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        return f"<User id={self.id} email={self.email!r} role={self.role.value}>"
