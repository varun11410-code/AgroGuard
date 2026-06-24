"""
AgroGuard Backend - Scan Repository

Handles database operations for the Scan model.
"""
from typing import List
from sqlalchemy.orm import joinedload
from app.database import db
from app.models.scan import Scan

class ScanRepository:
    @staticmethod
    def create(scan: Scan) -> Scan:
        """
        Insert a new scan into the database.
        Raises an exception if an integrity constraint is violated.
        """
        try:
            db.session.add(scan)
            db.session.commit()
            return scan
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_user_scans(user_id: str) -> List[Scan]:
        """
        Fetch all scans for a given user, ordered by creation date descending.
        Uses joinedload on crop to prevent N+1 queries.
        """
        import uuid
        try:
            uid = uuid.UUID(user_id)
            query = (
                db.select(Scan)
                .where(Scan.user_id == uid)
                .options(joinedload(Scan.crop))
                .order_by(Scan.created_at.desc())
            )
            return list(db.session.execute(query).scalars().all())
        except ValueError:
            return []

    @staticmethod
    def get_by_id(scan_id: str) -> Scan | None:
        """
        Fetch a single scan by its UUID.
        """
        import uuid
        try:
            uid = uuid.UUID(scan_id)
            return db.session.execute(db.select(Scan).where(Scan.id == uid)).scalar_one_or_none()
        except ValueError:
            return None

    @staticmethod
    def delete(scan: Scan) -> None:
        """
        Deletes a scan record.
        """
        try:
            db.session.delete(scan)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_total_count() -> int:
        """
        Get the total number of scans.
        """
        return db.session.scalar(db.select(db.func.count()).select_from(Scan)) or 0

    @staticmethod
    def get_top_diseases(limit: int = 3) -> list:
        """
        Get the top predicted diseases.
        Excludes None, empty strings, and 'Unsupported'.
        """
        query = (
            db.select(Scan.predicted_disease, db.func.count(Scan.id).label("count"))
            .where(
                Scan.predicted_disease.isnot(None),
                Scan.predicted_disease != "",
                Scan.predicted_disease != "Unsupported"
            )
            .group_by(Scan.predicted_disease)
            .order_by(db.func.count(Scan.id).desc())
            .limit(limit)
        )
        results = db.session.execute(query).all()
        return [{"disease": row[0], "count": row[1]} for row in results]

    @staticmethod
    def get_paginated_scans(page: int = 1, per_page: int = 50) -> tuple[list[Scan], int]:
        """Fetch paginated scans, ordered by newest first."""
        query = db.select(Scan).options(joinedload(Scan.crop)).order_by(Scan.created_at.desc())
        total_count = db.session.scalar(db.select(db.func.count()).select_from(Scan)) or 0
        offset = (page - 1) * per_page
        scans = list(db.session.execute(query.limit(per_page).offset(offset)).scalars().all())
        return scans, total_count

    @staticmethod
    def count_by_date_range(start_date, end_date) -> int:
        """Count scans created within a specific date range."""
        return db.session.scalar(
            db.select(db.func.count(Scan.id))
            .where(Scan.created_at >= start_date, Scan.created_at <= end_date)
        ) or 0
