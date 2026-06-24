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

    @staticmethod
    def get_users(page: int, per_page: int):
        return UserRepository.get_paginated_users(page, per_page)

    @staticmethod
    def get_scans(page: int, per_page: int):
        return ScanRepository.get_paginated_scans(page, per_page)

    @staticmethod
    def get_reports(page: int, per_page: int):
        from app.repositories.report_repository import ReportRepository
        return ReportRepository.get_paginated_reports(page, per_page)

    @staticmethod
    def get_analytics_payload() -> Dict[str, Any]:
        from datetime import datetime, timedelta, timezone
        
        now = datetime.now(timezone.utc)
        thirty_days_ago = now - timedelta(days=30)
        sixty_days_ago = now - timedelta(days=60)
        yesterday = now - timedelta(days=1)
        two_days_ago = now - timedelta(days=2)

        def calc_growth(cur, prev):
            if prev == 0:
                return 100 if cur > 0 else 0
            return round(((cur - prev) / prev) * 100, 1)

        cur_users = UserRepository.count_by_date_range(thirty_days_ago, now)
        prev_users = UserRepository.count_by_date_range(sixty_days_ago, thirty_days_ago)
        
        cur_scans = ScanRepository.count_by_date_range(thirty_days_ago, now)
        prev_scans = ScanRepository.count_by_date_range(sixty_days_ago, thirty_days_ago)

        active_today = ActivityLogRepository.count_active_users_by_date_range(yesterday, now)
        active_yesterday = ActivityLogRepository.count_active_users_by_date_range(two_days_ago, yesterday)

        sparkline_users = []
        sparkline_scans = []
        scans_overview = []
        
        for i in range(6, -1, -1):
            day_start = now - timedelta(days=i+1)
            day_end = now - timedelta(days=i)
            day_name = day_start.strftime("%b %d")
            
            u_cnt = UserRepository.count_by_date_range(day_start, day_end)
            s_cnt = ScanRepository.count_by_date_range(day_start, day_end)
            
            sparkline_users.append(u_cnt)
            sparkline_scans.append(s_cnt)
            scans_overview.append({"name": day_name, "scans": s_cnt})

        return {
            "user_growth": {
                "current": cur_users,
                "previous": prev_users,
                "percentage": calc_growth(cur_users, prev_users),
                "sparkline": sparkline_users
            },
            "scan_growth": {
                "current": cur_scans,
                "previous": prev_scans,
                "percentage": calc_growth(cur_scans, prev_scans),
                "sparkline": sparkline_scans
            },
            "scans_overview": scans_overview,
            "active_today": {
                "count": active_today,
                "previous": active_yesterday
            }
        }
