"""
AgroGuard Backend - Report Repository

Handles database operations for Report records.
"""
from typing import List, Optional
import logging
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from app.database import db
from app.models.report import Report
from app.models.scan import Scan

logger = logging.getLogger(__name__)

class ReportRepository:
    @staticmethod
    def create(report: Report) -> Optional[Report]:
        """
        Creates a new Report record.
        Returns None if a report already exists for the given scan_id
        (catching the IntegrityError silently).
        """
        try:
            db.session.add(report)
            db.session.commit()
            return report
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Duplicate report creation attempted for scan_id: {report.scan_id}")
            return None
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating report: {e}", exc_info=True)
            raise e

    @staticmethod
    def get_by_id(report_id: str) -> Optional[Report]:
        """
        Retrieves a report by its UUID, eager loading the parent Scan.
        """
        return (
            db.session.execute(
                db.select(Report)
                .where(Report.id == report_id)
                .options(joinedload(Report.scan))
            ).scalar_one_or_none()
        )

    @staticmethod
    def get_by_scan_id(scan_id: str) -> Optional[Report]:
        """
        Retrieves a report by its parent scan_id.
        """
        return db.session.execute(
            db.select(Report).where(Report.scan_id == scan_id)
        ).scalar_one_or_none()

    @staticmethod
    def get_all_by_user(user_id: str) -> List[Report]:
        """
        Retrieves all reports owned by a specific user (via Scan.user_id),
        ordered by generation date descending.
        """
        return list(
            db.session.execute(
                db.select(Report)
                .join(Scan, Report.scan_id == Scan.id)
                .where(Scan.user_id == user_id)
                .options(joinedload(Report.scan))
                .order_by(Report.generated_at.desc())
            ).scalars().all()
        )

    @staticmethod
    def get_paginated_reports(page: int = 1, per_page: int = 50) -> tuple[list[Report], int]:
        """Fetch paginated reports, ordered by newest first."""
        query = db.select(Report).options(joinedload(Report.scan)).order_by(Report.generated_at.desc())
        total_count = db.session.scalar(db.select(db.func.count()).select_from(Report)) or 0
        offset = (page - 1) * per_page
        reports = list(db.session.execute(query.limit(per_page).offset(offset)).scalars().all())
        return reports, total_count
