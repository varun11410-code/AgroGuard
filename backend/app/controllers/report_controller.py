"""
AgroGuard Backend - Report Controller

Handles request-response lifecycle for report generation endpoints.
"""
import logging
from flask import request, jsonify, send_file
from werkzeug.exceptions import HTTPException
from pydantic import ValidationError

from app.schemas.report_contract import ReportData
from app.services.report_service import generate_report
from app.utils.image_helper import fetch_image_to_buffer
import base64
import io

logger = logging.getLogger(__name__)

class ReportController:
    @staticmethod
    def generate():
        """
        Handle POST /api/reports/generate
        """
        try:
            # 1. Parse JSON payload
            data = request.get_json(silent=True)
            if not data or not isinstance(data, dict):
                return jsonify({"success": False, "message": "Missing or invalid JSON payload"}), 400

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

            # 5. Construct safe filename
            crop = validated_data.crop.replace(" ", "_")
            disease = validated_data.disease.replace(" ", "_")
            filename = f"AgroGuard_{crop}_{disease}.pdf"

            # 6. Stream file to client
            return send_file(
                pdf_buffer,
                mimetype="application/pdf",
                as_attachment=True,
                download_name=filename
            )

        except ValidationError as e:
            # Return 400 Validation errors
            formatted_errors = []
            for err in e.errors():
                loc = err.get("loc", ("unknown",))
                field = str(loc[-1]) if loc else "unknown"
                formatted_errors.append({"field": field, "message": err.get("msg")})
                
            return jsonify({
                "success": False,
                "errors": formatted_errors
            }), 400

        except ValueError as e:
            return jsonify({
                "success": False,
                "message": str(e)
            }), 400

        except HTTPException as e:
            # Re-raise standard Flask HTTP exceptions
            raise e

        except Exception as e:
            # Log the traceback and return 500
            logger.exception("Unexpected error in report generation endpoint:")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred during report generation"
            }), 500
