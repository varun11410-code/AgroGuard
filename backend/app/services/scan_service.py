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
from app.storage.exceptions import StorageError
import logging

logger = logging.getLogger(__name__)

class ScanService:
    @staticmethod
    def save_scan(user_id: str, crop_name: str, disease: str, confidence: float, image_bytes: bytes = None) -> Scan:
        """
        Creates and persists a scan for an authenticated user.
        Raises ValueError if crop_name does not match any valid crop.
        """
        if not crop_name:
            raise ValueError("Crop name is required")
            
        crop = db.session.execute(
            db.select(Crop).where(func.lower(Crop.name) == crop_name.lower())
        ).scalar_one_or_none()

        if not crop:
            raise ValueError("Invalid crop type specified")

        try:
            uid = uuid.UUID(user_id)
        except ValueError:
            raise ValueError("Invalid user ID")

        scan_id = uuid.uuid4()
        image_url = None
        if image_bytes:
            # Uploading first. Will bubble StorageUploadError up if failed.
            result = storage.upload_file(image_bytes, f"scans/{scan_id}")
            image_url = result.url

        # Create scan with 180-day expiry
        expires_at = datetime.now(timezone.utc) + timedelta(days=180)
        
        scan = Scan(
            id=scan_id,
            user_id=uid,
            crop_id=crop.id,
            image_url=image_url,
            predicted_disease=disease,
            confidence_score=confidence,
            expires_at=expires_at
        )

        try:
            created_scan = ScanRepository.create(scan)
        except Exception as db_error:
            if image_bytes:
                try:
                    storage.delete_file(f"scans/{scan_id}")
                except StorageError as cleanup_error:
                    logger.error(f"Failed to cleanup orphaned image {scan_id}: {cleanup_error}")
            raise db_error

        # Log the activity
        from app.services.auth_service import AuthService
        AuthService._safe_log_activity(
            user_id=user_id,
            activity_type="PREDICTION",
            details={
                "crop_name": crop_name,
                "disease": disease,
                "confidence": confidence,
                "scan_id": str(created_scan.id)
            }
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
            raise ValueError("Scan not found")
            
        if str(scan.user_id) != user_id:
            raise ValueError("Access denied")
            
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
