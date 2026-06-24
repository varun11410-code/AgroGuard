"""
AgroGuard Backend - Activity Log Repository

Handles database operations for the ActivityLog model.
"""
from typing import List, Tuple
from sqlalchemy.orm import joinedload
from app.database import db
from app.models.activity_log import ActivityLog

class ActivityLogRepository:
    @staticmethod
    def create(log: ActivityLog) -> ActivityLog:
        """
        Insert a new activity log into the database.
        Raises an exception if an integrity constraint is violated.
        """
        try:
            db.session.add(log)
            db.session.commit()
            return log
        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_paginated_logs(page: int = 1, per_page: int = 50) -> Tuple[List[ActivityLog], int]:
        """
        Fetch paginated activity logs, ordered by newest first.
        Uses joinedload on user to prevent N+1 queries.
        Returns a tuple of (logs, total_count).
        """
        query = (
            db.select(ActivityLog)
            .options(joinedload(ActivityLog.user))
            .order_by(ActivityLog.timestamp.desc())
        )
        
        # We use SQLAlchemy's pagination strategy. For raw execute, we do limit/offset.
        total_count = db.session.scalar(
            db.select(db.func.count()).select_from(ActivityLog)
        ) or 0
        
        offset = (page - 1) * per_page
        query = query.limit(per_page).offset(offset)
        
        logs = list(db.session.execute(query).scalars().all())
        return logs, total_count

    @staticmethod
    def count_active_users_by_date_range(start_date, end_date) -> int:
        """Count distinct active users within a specific date range."""
        return db.session.scalar(
            db.select(db.func.count(db.distinct(ActivityLog.user_id)))
            .where(ActivityLog.timestamp >= start_date, ActivityLog.timestamp <= end_date, ActivityLog.user_id.isnot(None))
        ) or 0
