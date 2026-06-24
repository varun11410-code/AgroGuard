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
                    "activity_type": log.activity_type if isinstance(log.activity_type, str) else log.activity_type.value,
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

    @staticmethod
    def get_analytics():
        try:
            payload = AdminService.get_analytics_payload()
            return jsonify({"success": True, "data": payload}), 200
        except Exception as e:
            logger.error(f"Failed to fetch analytics: {str(e)}")
            return jsonify({"success": False, "message": "Failed to fetch analytics"}), 500

    @staticmethod
    def get_users():
        try:
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 20, type=int)
            users, total = AdminService.get_users(page, min(limit, 100))
            
            data = [{
                "id": str(u.id),
                "name": u.name,
                "email": u.email,
                "role": u.role.value if hasattr(u.role, 'value') else str(u.role),
                "created_at": u.created_at.isoformat()
            } for u in users]
            
            return jsonify({
                "success": True,
                "data": {
                    "users": data,
                    "pagination": {
                        "page": page, "limit": limit, "total": total,
                        "total_pages": (total + limit - 1) // limit if limit > 0 else 1
                    }
                }
            }), 200
        except Exception as e:
            logger.error(f"Failed to fetch users: {str(e)}")
            return jsonify({"success": False, "message": "Failed to fetch users"}), 500

    @staticmethod
    def get_scans():
        try:
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 20, type=int)
            scans, total = AdminService.get_scans(page, min(limit, 100))
            
            data = [{
                "id": str(s.id),
                "user_email": s.user.email if s.user else "Guest",
                "crop": s.crop.name if s.crop else "Unknown",
                "disease": s.predicted_disease,
                "confidence": s.confidence_score,
                "created_at": s.created_at.isoformat()
            } for s in scans]
            
            return jsonify({
                "success": True,
                "data": {
                    "scans": data,
                    "pagination": {
                        "page": page, "limit": limit, "total": total,
                        "total_pages": (total + limit - 1) // limit if limit > 0 else 1
                    }
                }
            }), 200
        except Exception as e:
            logger.error(f"Failed to fetch scans: {str(e)}")
            return jsonify({"success": False, "message": "Failed to fetch scans"}), 500

    @staticmethod
    def get_reports():
        try:
            page = request.args.get("page", 1, type=int)
            limit = request.args.get("limit", 20, type=int)
            reports, total = AdminService.get_reports(page, min(limit, 100))
            
            data = [{
                "id": str(r.id),
                "scan_id": str(r.scan_id),
                "generated_at": r.generated_at.isoformat(),
                "user_email": r.scan.user.email if r.scan and r.scan.user else "Guest"
            } for r in reports]
            
            return jsonify({
                "success": True,
                "data": {
                    "reports": data,
                    "pagination": {
                        "page": page, "limit": limit, "total": total,
                        "total_pages": (total + limit - 1) // limit if limit > 0 else 1
                    }
                }
            }), 200
        except Exception as e:
            logger.error(f"Failed to fetch reports: {str(e)}")
            return jsonify({"success": False, "message": "Failed to fetch reports"}), 500
