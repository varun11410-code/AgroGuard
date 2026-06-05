"""
AgroGuard Backend - Report Model

Defines the SQLAlchemy ORM model for the ``reports`` table in PostgreSQL
(Supabase).

Table: reports

Architecture reference: Architecture.md §6 — Database Design,
                        §10 — Report Generation Architecture
PRD reference:          PRD.md §7 F5 — PDF Report Generation

Report generation flow (Architecture.md §10):
    Result Page → Download Report → Generate PDF → Download

Storage strategy (Architecture.md §10):
    Store metadata only.  PDF is generated dynamically on each download.
    No permanent PDF file is stored (Cloudinary or otherwise).

Report contents captured here:
    * Scan reference   (via scan_id FK — links to crop, disease, confidence)
    * AI summary       (summary field — Gemini-generated text)
    * Report version   (report_version — tracks prompt/template changes)
    * Generation time  (generated_at — when the report was first created)

Design decisions:
    * ``scan_id`` is a **non-nullable** FK to ``scans.id``.  A report cannot
      exist without a parent scan — the scan holds the crop, disease, and
      confidence data that populate the PDF.

    * ``ondelete="CASCADE"`` on ``scan_id`` — if the scan record is deleted
      (e.g. after the 180-day retention window, PRD §10), the associated
      report metadata is also removed automatically.

    * **One-to-one relationship** with Scan (``uselist=False`` on the Scan
      side).  Each scan produces at most one report; subsequent downloads
      regenerate the PDF from the same metadata row rather than creating
      duplicate records.

    * ``generated_at`` is the Architecture.md-specified timestamp for this
      table (matching the column name exactly).  ``updated_at`` is added
      for consistency with all other models to track re-generation events
      (e.g. if the AI summary is refreshed for a new model version).

    * ``report_version`` (VARCHAR 10) defaults to ``"1.0"`` for V1.
      Incrementing this in the service layer lets administrators identify
      which prompt/template version produced a given report — important for
      reproducibility and debugging.

    * ``summary`` (TEXT) stores the raw Gemini AI response.  The PDF service
      layer renders this into the downloadable report at request time.

Usage:
    from app.models.report import Report

    report = Report(
        scan_id=scan.id,
        summary="AI-generated agricultural advisory...",
        report_version="1.0",
    )
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database import db

if TYPE_CHECKING:
    from app.models.scan import Scan


class Report(db.Model):
    """
    ORM model representing the ``reports`` table.

    Stores report metadata only — the PDF is generated dynamically on
    download (Architecture.md §10).

    Attributes:
        id:             UUID primary key, auto-generated on insert.
        scan_id:        FK → scans.id.  Non-nullable; cascades on scan deletion.
        report_version: Version string that identifies the prompt/template
                        used to generate the report (e.g. ``"1.0"``).
        summary:        Raw AI-generated text summary produced by Gemini.
                        Rendered into the PDF at download time.
        generated_at:   UTC timestamp of report creation, set once by the
                        database server.  Named per Architecture.md §6.
        updated_at:     UTC timestamp automatically refreshed on every UPDATE
                        (e.g. when the AI summary is regenerated).

    Relationships:
        scan:  Back-reference to the parent ``Scan`` instance.
    """

    __tablename__ = "reports"

    # ------------------------------------------------------------------
    # Primary Key
    # ------------------------------------------------------------------

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        doc="Unique report identifier (UUID v4, auto-generated).",
    )

    # ------------------------------------------------------------------
    # Foreign Key
    # ------------------------------------------------------------------

    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scans.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
        doc=(
            "FK to scans.id.  Non-nullable — every report is anchored to "
            "exactly one scan.  Unique constraint enforces the one-to-one "
            "relationship.  Cascades deletion when the parent scan is purged."
        ),
    )

    # ------------------------------------------------------------------
    # Report Content
    # ------------------------------------------------------------------

    report_version: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        default="1.0",
        doc=(
            "Version identifier for the report template and AI prompt set "
            "used at generation time (e.g. '1.0').  Increment when the prompt "
            "or PDF layout changes to aid reproducibility."
        ),
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        doc=(
            "AI-generated advisory text produced by Gemini.  "
            "Rendered into the downloadable PDF at request time.  "
            "NULL if generation failed or has not yet run."
        ),
    )

    # ------------------------------------------------------------------
    # Timestamps
    # ------------------------------------------------------------------

    generated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        doc=(
            "UTC timestamp of report creation, set once by the database server. "
            "Column name matches Architecture.md §6 specification."
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

    scan: Mapped["Scan"] = relationship(
        "Scan",
        back_populates="report",
        lazy="select",
        doc="The parent scan that this report was generated from.",
    )

    # ------------------------------------------------------------------
    # Representation
    # ------------------------------------------------------------------

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"<Report id={self.id} "
            f"scan_id={self.scan_id} "
            f"version={self.report_version!r}>"
        )
