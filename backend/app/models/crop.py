"""
AgroGuard Backend - Crop Model

Defines the SQLAlchemy ORM model for the ``crops`` table in PostgreSQL
(Supabase).

Table: crops

Architecture reference: Architecture.md §6 — Database Design
PRD reference:          PRD.md §5 — Supported Scope (V1), §7 F2 — Crop Selection

Supported crops in V1:
    * Tomato — Healthy, Early Blight, Late Blight
    * Potato — Late Blight

Design decisions:
    * UUID primary key — consistent with all other tables in the schema
      (Architecture.md §13 — Database Rules).
    * ``supported`` boolean flag — allows the table to hold a full crop
      catalogue while toggling active/inactive state without deleting rows.
      Future crops can be inserted as ``supported=False`` and enabled via a
      config change rather than a schema migration.
    * ``name`` carries a unique constraint so duplicate crop names cannot
      be seeded accidentally, and an index so look-ups by name are O(log n).
    * ``updated_at`` auto-refreshes on every UPDATE via ``onupdate=func.now()``
      so the seed script and admin operations never need to set it manually.

Usage:
    from app.models.crop import Crop

    tomato = Crop(name="Tomato", supported=True)
    potato = Crop(name="Potato", supported=True)
"""

from __future__ import annotations

import uuid

from sqlalchemy import Boolean, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import DateTime

from app.database import db


class Crop(db.Model):
    """
    ORM model representing the ``crops`` table.

    Attributes:
        id:         UUID primary key, auto-generated on insert.
        name:       Crop display name (e.g. ``"Tomato"``).  Unique and indexed.
        supported:  When ``True`` the crop is available for disease detection.
                    When ``False`` it is catalogued but not yet active.
        created_at: UTC timestamp of row creation, set once by the database.
        updated_at: UTC timestamp automatically refreshed on every UPDATE.
    """

    __tablename__ = "crops"

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Unique crop identifier (UUID v4, auto-generated).",
    )

    # ------------------------------------------------------------------
    # Identity Fields
    # ------------------------------------------------------------------

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
        index=True,
        doc="Crop display name (e.g. 'Tomato', 'Potato'). Must be unique.",
    )

    # ------------------------------------------------------------------
    # Status Flag
    # ------------------------------------------------------------------

    supported: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc=(
            "True if this crop is actively supported for disease detection. "
            "False marks it as catalogued but not yet available."
        ),
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="UTC timestamp of row creation, set once by the database server.",
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        doc="UTC timestamp automatically updated on every row modification.",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        return f"<Crop id={self.id} name={self.name!r} supported={self.supported}>"
