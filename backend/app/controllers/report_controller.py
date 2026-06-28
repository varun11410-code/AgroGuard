"""
AgroGuard Backend - Report Controller

Handles request-response lifecycle for report generation endpoints.
"""
import io
import base64
import logging
from flask import request
from app.core.exceptions import AgroGuardBaseException, jsonify, send_file
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import get_jwt_identity

from app.schemas.report_contract import ReportData
from app.services.report_service import generate_report
from app.services.report_management_service import ReportManagementService
from app.utils.image_helper import fetch_image_to_buffer

logger = logging.getLogger(__name__)

class ReportController:
    @staticmethod
    def generate():
        """
        Handle POST /api/reports/generate
        """
        try:
            # 1. Parse JSON payload
            data = request.get_json() or {}

            # 2. Validate using Pydantic
            validated_data = ReportData(**data)

            # 3. Handle optional image fetching
            if validated_data.image_stream and isinstance(validated_data.image_stream, str):
                if validated_data.image_stream.startswith('http'):
                    # Fetch external image (e.g., from Cloudinary)
                    stream = fetch_image_to_buffer(validated_data.image_stream)
                    validated_data.image_stream = stream
                elif validated_data.image_stream.startswith('data:image/'):
                    # Decode base64 data URI
                    try:
                        header, base64_data = validated_data.image_stream.split(',', 1)
                        image_bytes = base64.b64decode(base64_data)
                        validated_data.image_stream = io.BytesIO(image_bytes)
                    except Exception as e:
                        logger.warning(f"Failed to decode base64 image stream: {e}")
                        validated_data.image_stream = None

            # 4. Generate the PDF buffer
            pdf_buffer = generate_report(validated_data)

            # 5. Save metadata if authenticated and scan_id is provided
            user_id = get_jwt_identity()
            if user_id and validated_data.scan_id and validated_data.ai_summary:
                try:
                    ReportManagementService.save_report_metadata(
                        scan_id=validated_data.scan_id,
                        user_id=user_id,
                        summary=validated_data.ai_summary
                    )
                except Exception as e:
                    logger.error(f"Failed to save report metadata silently: {e}")

            # 6. Construct safe filename
            crop = validated_data.crop.replace(" ", "_")
            disease = validated_data.disease.replace(" ", "_")
            filename = f"AgroGuard_{crop}_{disease}.pdf"

            from app.services.activity_log_service import ActivityLogService
            import uuid
            uid_obj = None
            if user_id:
                try: uid_obj = uuid.UUID(user_id)
                except ValueError: pass
            
            ActivityLogService.log_report_downloaded(
                user_id=uid_obj,
                report_version="1.0",
                scan_id=uuid.UUID(validated_data.scan_id) if validated_data.scan_id else None
            )

            # 7. Stream file to client
            return send_file(
                pdf_buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=filename
            )

        except ValueError as e:
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400

        except (HTTPException, AgroGuardBaseException) as e:
            # Re-raise standard Flask HTTP exceptions
            raise e

        except Exception as e:
            # Log the traceback and return 500
            logger.exception("Unexpected error in report generation endpoint:")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred during report generation"
            }), 500

    @staticmethod
    def get_history():
        """
        Handle GET /api/reports
        """
        try:
            user_id = get_jwt_identity()
            reports = ReportManagementService.get_user_history(user_id)
            return jsonify({
                "success": True,
                "data": reports
            }), 200
        except Exception as e:
            logger.exception("Error fetching report history:")
            return jsonify({"success": False, "message": "Failed to fetch report history"}), 500

    @staticmethod
    def download_historical(report_id: str):
        """
        Handle GET /api/reports/<report_id>/download
        """
        try:
            user_id = get_jwt_identity()
            pdf_buffer = ReportManagementService.reconstruct_report(report_id, user_id)
            
            # Note: We use a generic filename here as crop/disease are inside the buffer's domain, 
            # or we could fetch it from the DB again. A simple generic one suffices.
            filename = f"AgroGuard_Historical_Report_{report_id[:8]}.pdf"
            
            from app.services.activity_log_service import ActivityLogService
            import uuid
            uid_obj = None
            if user_id:
                try: uid_obj = uuid.UUID(user_id)
                except ValueError: pass

            ActivityLogService.log_report_downloaded(
                user_id=uid_obj,
                report_version="1.0",
                report_id=uuid.UUID(report_id)
            )

            return send_file(
                pdf_buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=filename
            )
        except Exception as e:
            logger.exception("Error downloading historical report:")
            return jsonify({"success": False, "message": "Failed to download historical report"}), 500
