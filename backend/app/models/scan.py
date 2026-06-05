"""
AgroGuard Backend - Scan Model

Defines the SQLAlchemy ORM model for the ``scans`` table in PostgreSQL
(Supabase).

Table: scans

Architecture reference: Architecture.md §6 — Database Design,
                        §8 — Disease Detection Architecture,
                        §11 — Image Retention Policy
PRD reference:          PRD.md §7 F1 — Disease Detection,
                        §7 F4 — Treatment Recommendations,
                        §7 F7 — User History,
                        §7 F9 — Guest Access,
                        §10 — Data Retention Policy

Design decisions:
    * ``user_id`` is a **nullable** FK to ``users.id``.  A NULL value means
      the scan belongs to a guest user (PRD §7 F9).  Guest scans are
      transient — the image is deleted after analysis and no history is
      retained (PRD §10).  Making the FK nullable avoids a separate
      guest-scan table and keeps the query surface minimal.

    * ``crop_id`` is a **non-nullable** FK to ``crops.id``.  A crop must
      always be selected before an image can be uploaded (PRD §7 F2).

    * ``selected_plan`` reuses the ``BudgetTier`` enum (BUDGET / STANDARD /
      PREMIUM) already defined in ``user.py``.  Sharing one enum avoids
      divergence between the user preference and the scan plan fields.
      It is nullable because the user selects a plan after viewing results,
      not at scan creation time.

    * ``predicted_disease`` is nullable — set to NULL on scan creation and
      populated after the ML inference completes (§8 Disease Detection Flow).

    * ``confidence_score`` uses SQLAlchemy ``Float`` (Postgres DOUBLE PRECISION).
      Stored as a value in [0.0, 1.0]; display formatting (e.g. "89%") is
      handled in the presentation layer.

    * ``expires_at`` is nullable.  For authenticated users it is set to
      ``created_at + 180 days`` by the service layer at write time (PRD §10).
      For guest scans it remains NULL because no record is retained beyond
      the request lifecycle.

    * ``updated_at`` is added for consistency with other tables and to
      support future admin operations on scan records.

    * Cascade behaviour: ``ondelete="SET NULL"`` on ``user_id`` so that
      deleting a user account does not cascade-delete their historical scans
      (useful for admin audit purposes).  ``ondelete="RESTRICT"`` on
      ``crop_id`` prevents accidental crop removal while scans reference it.

Usage:
    from app.models.scan import Scan

    scan = Scan(
        user_id=user.id,
        crop_id=crop.id,
        image_url="https://res.cloudinary.com/...",
    )
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database import db
from app.models.user import BudgetTier

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.crop import Crop
    from app.models.report import Report


class Scan(db.Model):
    """
    ORM model representing the ``scans`` table.

    Attributes:
        id:                UUID primary key, auto-generated on insert.
        user_id:           FK → users.id.  NULL for guest scans.
        crop_id:           FK → crops.id.  Always required.
        image_url:         Cloudinary URL of the uploaded leaf image.
        predicted_disease: ML inference result (e.g. ``"Early Blight"``).
                           NULL until inference completes.
        confidence_score:  Model confidence in [0.0, 1.0].  NULL until
                           inference completes.
        selected_plan:     Treatment tier chosen by the user after viewing
                           results.  NULL until the user selects a plan.
        created_at:        UTC timestamp of scan creation.
        expires_at:        UTC timestamp after which the scan record may be
                           purged.  180 days from creation for authenticated
                           users; NULL for guest scans.
        updated_at:        UTC timestamp automatically refreshed on every UPDATE.

    Relationships:
        user:  Back-reference to the owning ``User`` instance (or None for guests).
        crop:  Back-reference to the associated ``Crop`` instance.
    """

    __tablename__ = "scans"

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Unique scan identifier (UUID v4, auto-generated).",
    )

    # ------------------------------------------------------------------
    # Foreign Keys
    # ------------------------------------------------------------------

    user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        doc=(
            "FK to users.id.  NULL indicates a guest scan — no account is "
            "associated and no history is retained (PRD §7 F9, §10)."
        ),
    )

    crop_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("crops.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        doc="FK to crops.id.  Crop selection is required before scanning (PRD §7 F2).",
    )

    # ------------------------------------------------------------------
    # Detection Results
    # ------------------------------------------------------------------

    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc="Cloudinary URL of the uploaded leaf image.",
    )

    predicted_disease: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
        doc=(
            "Disease label returned by the ML model "
            "(e.g. 'Healthy', 'Early Blight', 'Late Blight').  "
            "NULL until inference completes."
        ),
    )

    confidence_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
        doc=(
            "Model confidence score in the range [0.0, 1.0].  "
            "NULL until inference completes."
        ),
    )

    # ------------------------------------------------------------------
    # User Selection
    # ------------------------------------------------------------------

    selected_plan: Mapped[BudgetTier | None] = mapped_column(
        String(10),
        nullable=True,
        doc=(
            "Treatment plan tier selected by the user after viewing results "
            "(BUDGET / STANDARD / PREMIUM).  NULL until the user chooses a plan.  "
            "Stored as a plain VARCHAR that the application validates against BudgetTier."
        ),
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc="UTC timestamp of scan creation, set once by the database server.",
    )

    expires_at: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        doc=(
            "UTC expiry timestamp for this scan record.  "
            "Set to created_at + 180 days for authenticated users; "
            "NULL for guest scans (PRD §10)."
        ),
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

    user: Mapped["User | None"] = relationship(
        "User",
        back_populates="scans",
        lazy="select",
    )

    crop: Mapped["Crop"] = relationship(
        "Crop",
        back_populates="scans",
        lazy="select",
    )

    report: Mapped[Optional["Report"]] = relationship(
        "Report",
        back_populates="scan",
        uselist=False,
        lazy="select",
        cascade="all, delete-orphan",
        doc="The generated report for this scan, if one exists (one-to-one).",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Scan id={self.id} "
            f"crop_id={self.crop_id} "
            f"disease={self.predicted_disease!r} "
            f"confidence={self.confidence_score}>"
        )
