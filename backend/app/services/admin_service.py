"""
AgroGuard Backend - Admin Service

Handles business logic for the Admin Dashboard.
"""
from typing import Dict, Any, List, Tuple
from app.repositories.user_repository import UserRepository
from app.repositories.scan_repository import ScanRepository
from app.repositories.activity_log_repository import ActivityLogRepository
from app.models.activity_log import ActivityLog

class AdminService:
    @staticmethod
    def get_dashboard_stats() -> Dict[str, Any]:
        """
        Aggregates statistics for the admin dashboard.
        """
        total_users = UserRepository.get_total_count()
        total_scans = ScanRepository.get_total_count()
        top_diseases = ScanRepository.get_top_diseases(limit=3)
        
        return {
            "total_users": total_users,
            "total_scans": total_scans,
            "top_diseases": top_diseases
        }

    @staticmethod
    def get_activity_logs(page: int, per_page: int) -> Tuple[List[ActivityLog], int]:
        """
        Retrieves paginated activity logs.
        """
        return ActivityLogRepository.get_paginated_logs(page, per_page)
