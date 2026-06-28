"""
AgroGuard Backend - Scan Service

Handles business logic for scan operations, ensuring data integrity before persistence.
"""
from datetime import datetime, timedelta, timezone
from typing import List
import uuid
from sqlalchemy import func

from app.database import db
from app.models.scan import Scan
from app.models.crop import Crop
from app.repositories.scan_repository import ScanRepository
from app.storage import storage
from app.core.exceptions import (
    BadRequestException,
    NotFoundException,
    ForbiddenException
)
from app.storage.exceptions import StorageError
import logging

logger = logging.getLogger(__name__)

class ScanService:
    @staticmethod
    def save_scan(user_id: str, crop_name: str, disease: str, confidence: float, image_bytes: bytes = None, ai_summary: str = None, treatment_plans: dict = None, risk_level: str = None) -> Scan:
        """
        Creates and persists a scan for an authenticated user.
        Raises ValueError if crop_name does not match any valid crop.
        """
        if not crop_name:
            raise BadRequestException("Crop name is required", error_code="SCAN_MISSING_CROP")
            
        crop = db.session.execute(
            db.select(Crop).where(func.lower(Crop.name) == crop_name.lower())
        ).scalar_one_or_none()

        if not crop:
            raise BadRequestException("Invalid crop type specified", error_code="SCAN_INVALID_CROP")

        try:
            uid = uuid.UUID(user_id)
        except ValueError:
            raise BadRequestException("Invalid user ID", error_code="SCAN_INVALID_USER_ID")

        scan_id = uuid.uuid4()
        image_url = None
        if image_bytes:
            try:
                # Uploading first. Will bubble StorageUploadError up if failed.
                result = storage.upload_file(image_bytes, f"scans/{scan_id}")
                image_url = result.url
            except Exception as e:
                logger.error(f"Storage upload failed for scan {scan_id}: {str(e)}")
                raise

        # Create scan with 180-day expiry
        expires_at = datetime.now(timezone.utc) + timedelta(days=180)
        
        scan = Scan(
            id=scan_id,
            user_id=uid,
            crop_id=crop.id,
            image_url=image_url,
            predicted_disease=disease,
            confidence_score=confidence,
            ai_summary=ai_summary,
            treatment_plans=treatment_plans,
            risk_level=risk_level,
            expires_at=expires_at
        )

        try:
            created_scan = ScanRepository.create(scan)
            logger.info(f"Scan {scan_id} persisted successfully.")
        except Exception as db_error:
            logger.error(f"Failed to persist scan {scan_id}: {str(db_error)}")
            if image_bytes:
                try:
                    storage.delete_file(f"scans/{scan_id}")
                except StorageError as cleanup_error:
                    logger.error(f"Failed to cleanup orphaned image {scan_id}: {cleanup_error}")
            raise db_error

        # Log the activity
        from app.services.activity_log_service import ActivityLogService
        ActivityLogService.log_scan_completed(
            user_id=uid,
            crop=crop_name,
            disease=disease,
            confidence_score=confidence,
            scan_id=created_scan.id
        )

        return created_scan

    @staticmethod
    def get_user_history(user_id: str) -> List[Scan]:
        """
        Retrieves the paginated scan history for a user.
        Returns a list of scans securely isolated to the authenticated user.
        """
        return ScanRepository.get_user_scans(user_id)

    @staticmethod
    def _execute_scan_deletion(scan: Scan) -> None:
        """
        Executes the 'Storage First' deletion sequence.
        Shared by manual user deletion and automated cleanup tasks.
        """
        # Delete storage asset first to prevent unrecoverable orphaned files.
        # Broken DB records can be recovered by Task 12.5 cleanup.
        if scan.image_url:
            storage.delete_file(f"scans/{scan.id}")
            
        ScanRepository.delete(scan)

    @staticmethod
    def delete_scan(scan_id: str, user_id: str) -> None:
        """
        Deletes a scan securely after verifying ownership.
        Raises ValueError if scan is not found or access is denied.
        """
        scan = ScanRepository.get_by_id(scan_id)
        if not scan:
            raise NotFoundException("Scan not found", error_code="SCAN_NOT_FOUND")
            
        if str(scan.user_id) != user_id:
            raise ForbiddenException("Access denied", error_code="SCAN_ACCESS_DENIED")
            
        ScanService._execute_scan_deletion(scan)

    @staticmethod
    def cleanup_expired_scans(batch_size: int = 100) -> dict:
        """
        Orchestrates the deletion of all expired scans.
        Processes in batches until no expired scans remain.
        Returns a summary dictionary with counts.
        """
        summary = {"found": 0, "deleted": 0, "failed": 0}
        
        while True:
            scans = ScanRepository.get_expired_scans(limit=batch_size)
            if not scans:
                break
                
            summary["found"] += len(scans)
            
            for scan in scans:
                try:
                    ScanService._execute_scan_deletion(scan)
                    summary["deleted"] += 1
                except Exception as e:
                    logger.error(f"Failed to cleanup expired scan {scan.id}: {e}")
                    summary["failed"] += 1
                    
            # If a batch entirely fails (e.g. database down), avoid infinite loop
            if summary["failed"] >= summary["found"]:
                logger.error("Cleanup job aborting due to 100% failure rate in batch.")
                break
                
        return summary
