"""
AgroGuard Backend - Admin Controller

Handles requests for admin dashboard endpoints.
"""
from flask import jsonify, request
from app.services.admin_service import AdminService
import logging

logger = logging.getLogger(__name__)

class AdminController:
    @staticmethod
    def get_stats():
        """
        Returns aggregate statistics for the dashboard.
        """
        try:
            stats = AdminService.get_dashboard_stats()
            return jsonify({
                "success": True,
                "data": stats
            }), 200
        except Exception as e:
            logger.error(f"Failed to fetch admin stats: {str(e)}")
            return jsonify({
                "success": False,
                "message": "Failed to fetch statistics"
            }), 500

    @staticmethod
    def get_logs():
        """
        Returns paginated activity logs.
        """
        try:
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 20, type=int)
            
            # Enforce maximum limit to prevent abuse
            if limit > 100:
                limit = 100
                
            logs, total = AdminService.get_activity_logs(page, limit)
            
            # Serialize logs
            serialized_logs = []
            for log in logs:
                serialized_logs.append({
                    "id": str(log.id),
                    "user_id": str(log.user_id) if log.user_id else None,
                    "user_email": log.user.email if log.user else "Guest",
                    "activity_type": log.activity_type.value,
                    "details": log.details,
                    "timestamp": log.timestamp.isoformat()
                })
                
            return jsonify({
                "success": True,
                "data": {
                    "logs": serialized_logs,
                    "pagination": {
                        "page": page,
                        "limit": limit,
                        "total": total,
                        "total_pages": (total + limit - 1) // limit if limit > 0 else 1
                    }
                }
            }), 200
        except Exception as e:
            logger.error(f"Failed to fetch activity logs: {str(e)}")
            return jsonify({
                "success": False,
                "message": "Failed to fetch activity logs"
            }), 500
