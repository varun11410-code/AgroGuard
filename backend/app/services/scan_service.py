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

class ScanService:
    @staticmethod
    def save_scan(user_id: str, crop_name: str, disease: str, confidence: float) -> Scan:
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

        # Create scan with 180-day expiry
        expires_at = datetime.now(timezone.utc) + timedelta(days=180)
        
        scan = Scan(
            user_id=uid,
            crop_id=crop.id,
            image_url=None, # Deferred to Phase 12
            predicted_disease=disease,
            confidence_score=confidence,
            expires_at=expires_at
        )

        return ScanRepository.create(scan)

    @staticmethod
    def get_user_history(user_id: str) -> List[Scan]:
        """
        Retrieves the paginated scan history for a user.
        Returns a list of scans securely isolated to the authenticated user.
        """
        return ScanRepository.get_user_scans(user_id)
