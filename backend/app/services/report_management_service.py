"""
AgroGuard Backend - Report Management Service

Handles business logic for report persistence, ownership validation,
and historical reconstruction. It separates DB I/O from pure PDF compilation.
"""
import io
import logging
from typing import List

from app.models.report import Report
from app.repositories.report_repository import ReportRepository
from app.repositories.scan_repository import ScanRepository
from app.schemas.report_contract import ReportData
from app.services.report_service import generate_report
from app.utils.image_helper import fetch_image_to_buffer

logger = logging.getLogger(__name__)

class ReportManagementService:
    @staticmethod
    def save_report_metadata(scan_id: str, user_id: str, summary: str) -> None:
        """
        Securely saves report metadata.
        Verifies that the scan exists and is owned by the user before creating the report.
        Silently handles duplicates via the repository.
        """
        # Verify scan exists and belongs to the user
        scan = ScanRepository.get_by_id(scan_id)
        if not scan:
            logger.warning(f"Attempt to save report for non-existent scan: {scan_id}")
            return
            
        if str(scan.user_id) != user_id:
            logger.warning(f"Ownership violation: User {user_id} attempted to save report for scan {scan_id}")
            return

        # Check if report already exists to avoid redundant DB calls if known
        existing_report = ReportRepository.get_by_scan_id(scan_id)
        if existing_report:
            return

        report = Report(
            scan_id=scan.id,
            summary=summary,
            report_version="1.0"
        )
        ReportRepository.create(report)

    @staticmethod
    def get_user_history(user_id: str) -> List[dict]:
        """
        Retrieves the user's report history, serialized for the frontend.
        Intentionally omits the heavy 'summary' field to optimize payload size.
        """
        reports = ReportRepository.get_all_by_user(user_id=user_id)
        
        result = []
        for report in reports:
            result.append({
                "id": str(report.id),
                "scan_id": str(report.scan_id),
                "report_version": report.report_version,
                "generated_at": report.generated_at.isoformat() if report.generated_at else None,
                "scan": {
                    "crop_name": report.scan.crop.name if report.scan.crop else "Unknown",
                    "predicted_disease": report.scan.predicted_disease,
                    "confidence_score": report.scan.confidence_score
                }
            })
            
        return result

    @staticmethod
    def reconstruct_report(report_id: str, user_id: str) -> io.BytesIO:
        """
        Securely reconstructs a historical report strictly from DB metadata.
        Verifies ownership before generating.
        """
        report = ReportRepository.get_by_id(report_id)
        if not report:
            raise ValueError("Report not found")
            
        if str(report.scan.user_id) != user_id:
            logger.warning(f"Ownership violation: User {user_id} attempted to download report {report_id}")
            raise ValueError("Access denied")

        image_stream = None
        if report.scan.image_url:
            try:
                image_stream = fetch_image_to_buffer(report.scan.image_url)
            except Exception as e:
                logger.warning(f"Failed to fetch image for historical report {report_id}: {e}")

        # Map DB models into the strict Pydantic contract
        data = ReportData(
            scan_id=str(report.scan_id),
            crop=report.scan.crop.name if report.scan.crop else "Unknown Crop",
            disease=report.scan.predicted_disease,
            confidence=float(report.scan.confidence_score),
            ai_summary=report.summary,
            image_stream=image_stream
        )
        
        # Call the pure compilation service
        return generate_report(data)
