"""
AgroGuard Backend - ActivityLog Model

Defines the SQLAlchemy ORM model for the ``activity_logs`` table in
PostgreSQL (Supabase).

Table: activity_logs

Architecture reference: Architecture.md §6 — Database Design,
                        §13 — Logging Strategy
PRD reference:          PRD.md §7 F10 — Admin Dashboard

Design decisions:
    * ``user_id`` is a **nullable** FK to ``users.id``.
      This allows logging actions performed by guest users (e.g. guest leaf image
      uploads, report downloads) as well as authenticated users.
      Furthermore, ``ondelete="SET NULL"`` ensures that deleting a user account
      does not delete their audit trail, preserving logs for compliance and analytics.

    * ``activity_type`` uses a Python ``ActivityType`` enum stored as ``VARCHAR(30)``.
      This follows the pattern of storing enums as strings (like MessageRole in ChatMessage)
      to avoid Postgres native type migration headaches.
      The activity type maps exactly to the event types specified in Architecture.md §13.

    * ``metadata`` uses SQLAlchemy's ``JSON`` type. This matches the Architecture.md spec,
      allowing the storage of variable, action-specific JSON contexts (e.g. scan_id, ip_address,
      or error details) without requiring a rigid column structure.

    * ``timestamp`` is non-nullable with a server default of ``now()``. This matches the
      Architecture.md-specified timestamp column name. Since log entries are immutable
      chronological entries, we do not require an ``updated_at`` column.

Usage:
    from app.models.activity_log import ActivityLog, ActivityType

    log = ActivityLog(
        user_id=user.id,
        activity_type=ActivityType.LOGIN,
        details={"ip_address": "192.168.1.1"}
    )
"""

from __future__ import annotations

import enum
import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, JSON, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database import db

if TYPE_CHECKING:
    from app.models.user import User


# ---------------------------------------------------------------------------
# Enum Definition
# ---------------------------------------------------------------------------

class ActivityType(str, enum.Enum):
    """
    Log event types as defined in Architecture.md §13.
    """

    USER_REGISTERED = "USER_REGISTERED"
    USER_LOGIN_SUCCESS = "USER_LOGIN_SUCCESS"
    USER_LOGIN_FAILED = "USER_LOGIN_FAILED"
    SCAN_COMPLETED = "SCAN_COMPLETED"
    REPORT_DOWNLOADED = "REPORT_DOWNLOADED"
    AI_INTERACTION = "AI_INTERACTION"
    SYSTEM_ERROR = "SYSTEM_ERROR"


# ---------------------------------------------------------------------------
# ActivityLog Model
# ---------------------------------------------------------------------------

class ActivityLog(db.Model):
    """
    ORM model representing the ``activity_logs`` table.

    Stores immutable audit trail records for both guest and authenticated user
    interactions with the system.

    Attributes:
        id:            UUID primary key, auto-generated on insert.
        user_id:       FK → users.id. Nullable to allow logging guest users.
                       SET NULL on user deletion to preserve audit history.
        activity_type: The type of log event (LOGIN, REGISTER, etc.).
        details:       JSON field containing additional event details (stored as 'metadata' in DB).
        timestamp:     UTC creation timestamp, set by database.

    Relationships:
        user: The associated user, or None if the action was guest-triggered.
    """

    __tablename__ = "activity_logs"

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Unique activity log identifier (UUID v4, auto-generated).",
    )

    # ------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc=(
            "FK to users.id. Nullable — allows logging guest user actions "
            "(e.g., guest scan uploads and report downloads). ON DELETE SET NULL "
            "retains audit logs even if the user deletes their account."
        ),
    )

    # ------------------------------------------------------------------
    # Log Attributes
    # ------------------------------------------------------------------

    activity_type: Mapped[ActivityType] = mapped_column(
        String(30),
        nullable=False,
        doc=(
            "The event type (e.g., LOGIN, UPLOAD). Stored as VARCHAR(30); "
            "validated against ActivityType enum at the application layer."
        ),
    )

    details: Mapped[dict | None] = mapped_column(
        "metadata",
        JSON,
        nullable=True,
        doc=(
            "Action-specific structured context (e.g., IP address, system details). "
            "Mapped to the 'metadata' DB column to avoid SQLAlchemy namespace conflicts."
        ),
    )

    # ------------------------------------------------------------------
    # Timestamp
    # ------------------------------------------------------------------

    timestamp: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
        doc="UTC timestamp of log creation, set once by the database server.",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    user: Mapped[User | None] = relationship(
        "User",
        back_populates="activity_logs",
        lazy="select",
        doc="The user associated with this log event, or None for guest actions.",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        activity_str = self.activity_type if isinstance(self.activity_type, str) else self.activity_type.value
        return (
            f"<ActivityLog id={self.id} "
            f"user_id={self.user_id} "
            f"activity_type={activity_str}>"
        )
