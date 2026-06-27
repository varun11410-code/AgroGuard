"""
AgroGuard Backend - Activity Log Service
"""
import logging
from typing import Optional, Any, Dict
import uuid

from app.models.activity_log import ActivityLog, ActivityType
from app.repositories.activity_log_repository import ActivityLogRepository

logger = logging.getLogger(__name__)

class ActivityLogService:
    @staticmethod
    def log_activity(
        activity_type: ActivityType,
        user_id: Optional[uuid.UUID] = None,
        metadata: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[str] = None
    ) -> None:
        """
        Log an activity synchronously with failure isolation.
        """
        if metadata is None:
            metadata = {}
            
        if correlation_id:
            metadata["correlation_id"] = correlation_id

        try:
            log = ActivityLog(
                user_id=user_id,
                activity_type=activity_type,
                details=metadata
            )
            ActivityLogRepository.create(log)
        except Exception:
            # We swallow the error and log it to standard error stream
            # to ensure logging never interrupts the primary business operation.
            logger.exception("Failed to write activity log for %s", activity_type.value)

    # Helper methods for strictly typed metadata creation
    @staticmethod
    def log_user_registered(user_id: uuid.UUID, correlation_id: Optional[str] = None) -> None:
        ActivityLogService.log_activity(ActivityType.USER_REGISTERED, user_id=user_id, correlation_id=correlation_id)

    @staticmethod
    def log_user_login_success(user_id: uuid.UUID, user_agent: str, correlation_id: Optional[str] = None) -> None:
        metadata = {"user_agent": user_agent}
        ActivityLogService.log_activity(ActivityType.USER_LOGIN_SUCCESS, user_id=user_id, metadata=metadata, correlation_id=correlation_id)

    @staticmethod
    def log_user_login_failed(attempted_email: str, user_agent: str, correlation_id: Optional[str] = None) -> None:
        metadata = {"attempted_email": attempted_email, "user_agent": user_agent}
        ActivityLogService.log_activity(ActivityType.USER_LOGIN_FAILED, metadata=metadata, correlation_id=correlation_id)

    @staticmethod
    def log_scan_completed(user_id: Optional[uuid.UUID], crop: str, disease: str, confidence_score: float, scan_id: uuid.UUID, correlation_id: Optional[str] = None) -> None:
        metadata = {
            "crop": crop,
            "disease": disease,
            "confidence_score": confidence_score,
            "scan_id": str(scan_id)
        }
        ActivityLogService.log_activity(ActivityType.SCAN_COMPLETED, user_id=user_id, metadata=metadata, correlation_id=correlation_id)

    @staticmethod
    def log_report_downloaded(user_id: Optional[uuid.UUID], report_version: str, scan_id: Optional[uuid.UUID] = None, report_id: Optional[uuid.UUID] = None, correlation_id: Optional[str] = None) -> None:
        metadata = {
            "report_version": report_version
        }
        if scan_id:
            metadata["scan_id"] = str(scan_id)
        if report_id:
            metadata["report_id"] = str(report_id)
        ActivityLogService.log_activity(ActivityType.REPORT_DOWNLOADED, user_id=user_id, metadata=metadata, correlation_id=correlation_id)

    @staticmethod
    def log_ai_interaction(user_id: Optional[uuid.UUID], provider: str, interaction_type: str, session_id: Optional[uuid.UUID] = None, scan_id: Optional[uuid.UUID] = None, correlation_id: Optional[str] = None) -> None:
        metadata = {
            "provider": provider,
            "interaction_type": interaction_type
        }
        if session_id:
            metadata["session_id"] = str(session_id)
        if scan_id:
            metadata["scan_id"] = str(scan_id)
        ActivityLogService.log_activity(ActivityType.AI_INTERACTION, user_id=user_id, metadata=metadata, correlation_id=correlation_id)

    @staticmethod
    def log_system_error(error_category: str, endpoint: str, request_method: str, user_id: Optional[uuid.UUID] = None, correlation_id: Optional[str] = None) -> None:
        metadata = {
            "error_category": error_category,
            "endpoint": endpoint,
            "request_method": request_method
        }
        ActivityLogService.log_activity(ActivityType.SYSTEM_ERROR, user_id=user_id, metadata=metadata, correlation_id=correlation_id)
