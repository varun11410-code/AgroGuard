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
