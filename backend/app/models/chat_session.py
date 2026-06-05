"""
AgroGuard Backend - ChatSession Model

Defines the SQLAlchemy ORM model for the ``chat_sessions`` table in
PostgreSQL (Supabase).

Table: chat_sessions

Architecture reference: Architecture.md §6 — Database Design,
                        §9 — AI Architecture
PRD reference:          PRD.md §7 F3 — AI Agricultural Assistant,
                        §7 F9 — Guest Access

AI Assistant modes (Architecture.md §9):

    Mode A — General Agriculture Assistant
        Available to authenticated users before any diagnosis.
        ``scan_id`` is NULL — no prediction context is required.

    Mode B — Diagnosis-Aware Assistant
        Activated after disease detection.
        ``scan_id`` is set — the assistant receives crop, disease,
        confidence, and selected plan as context.

Design decisions:
    * ``user_id`` is a **non-nullable** FK to ``users.id``.
      PRD §7 F9 explicitly states: "Guests may NOT: Use AI Assistant."
      Only authenticated users can open chat sessions, so NULL is never
      a valid value here.

    * ``scan_id`` is a **nullable** FK to ``scans.id``.
      Mode A sessions start before any scan exists; the field is
      populated only when the session is diagnosis-aware (Mode B).
      ``ondelete="SET NULL"`` preserves the session row when the linked
      scan is purged after its 180-day retention window (PRD §10),
      degrading the session context gracefully instead of cascade-deleting
      conversation history.

    * ``ondelete="CASCADE"`` on ``user_id`` — a chat session has no value
      without its owner; deleting the user account removes all their sessions
      (and, via ChatMessage cascade, all their messages).

    * ``expires_at`` is nullable to match the Architecture.md schema.
      The service layer sets this at session creation time based on
      application policy (e.g. 24-hour TTL).  NULL means no explicit
      expiry is set.

    * ``updated_at`` is added for operational consistency even though it is
      not in the Architecture.md spec.  Task 1.7 (ChatMessage) will update
      sessions; having this column lets the API expose "last activity" easily.

Usage:
    from app.models.chat_session import ChatSession

    # Mode A — general assistant
    session = ChatSession(user_id=user.id)

    # Mode B — diagnosis-aware assistant
    session = ChatSession(user_id=user.id, scan_id=scan.id)
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database import db

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.scan import Scan
    from app.models.chat_message import ChatMessage


class ChatSession(db.Model):
    """
    ORM model representing the ``chat_sessions`` table.

    Each row represents one conversation between an authenticated user
    and the AI agricultural assistant.

    Attributes:
        id:         UUID primary key, auto-generated on insert.
        user_id:    FK → users.id.  Non-nullable — only authenticated users
                    may open chat sessions (PRD §7 F9).
        scan_id:    FK → scans.id.  NULL for Mode A (general) sessions;
                    set for Mode B (diagnosis-aware) sessions.
        created_at: UTC timestamp of session creation, set by the database.
        expires_at: UTC expiry timestamp set by the service layer.
                    NULL means no explicit expiry is enforced.
        updated_at: UTC timestamp refreshed on every modification.

    Relationships:
        user:     The authenticated owner of this session.
        scan:     The linked scan for Mode B sessions (or None for Mode A).
        messages: All chat messages belonging to this session (added in 1.7).
    """

    __tablename__ = "chat_sessions"

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Unique session identifier (UUID v4, auto-generated).",
    )

    # ------------------------------------------------------------------
    # Foreign Keys
    # ------------------------------------------------------------------

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        doc=(
            "FK to users.id.  Non-nullable — chat sessions require an "
            "authenticated user (PRD §7 F9).  Cascades deletion when "
            "the user account is removed."
        ),
    )

    scan_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scans.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc=(
            "FK to scans.id.  NULL for Mode A (general assistant) sessions. "
            "Set for Mode B (diagnosis-aware) sessions.  SET NULL on scan "
            "deletion preserves conversation history after retention expiry."
        ),
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="UTC timestamp of session creation, set once by the database server.",
    )

    expires_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc=(
            "UTC timestamp after which this session should be considered "
            "expired.  Set by the service layer at creation time.  "
            "NULL means no explicit expiry policy is applied."
        ),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        doc="UTC timestamp automatically refreshed on every row modification.",
    )

    # ------------------------------------------------------------------
    # Relationships
    # ------------------------------------------------------------------

    user: Mapped["User"] = relationship(
        "User",
        back_populates="chat_sessions",
        lazy="select",
        doc="The authenticated user who owns this chat session.",
    )

    scan: Mapped["Scan | None"] = relationship(
        "Scan",
        back_populates="chat_sessions",
        lazy="select",
        doc="The linked scan for Mode B sessions; None for Mode A sessions.",
    )

    messages: Mapped[List["ChatMessage"]] = relationship(
        "ChatMessage",
        back_populates="session",
        lazy="select",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
        doc="All messages exchanged in this session, ordered by creation time.",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<ChatSession id={self.id} "
            f"user_id={self.user_id} "
            f"scan_id={self.scan_id}>"
        )
