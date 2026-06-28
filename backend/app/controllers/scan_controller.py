import logging
import cv2
import numpy as np
from flask import request
from flask import jsonify
from app.core.exceptions import AgroGuardBaseException
from flask_jwt_extended import get_jwt_identity

from app.ml import preprocess_image, predict_disease, ImagePreprocessingError, PredictionError
from app.services.scan_service import ScanService
from app.services.ai_enrichment_service import AIEnrichmentService
from app.utils.risk_calculator import calculate_risk

# Configure logger
logger = logging.getLogger(__name__)

class ScanController:
    @staticmethod
    def predict():
        """
        Handle POST /api/scans
        """
        try:
            from app.schemas.scan_schema import ScanPredictionFormSchema
            form_data = ScanPredictionFormSchema(**request.form.to_dict())
            crop_name = form_data.crop

            from app.utils.upload_validators import validate_extension, validate_mimetype, validate_magic_number, validate_dimensions

            # 1. Validate uploaded image field exists
            if "image" not in request.files:
                logger.warning("Prediction request rejected: Missing image field in files payload.")
                return jsonify({"success": False, "message": "Missing image field"}), 400

            file = request.files["image"]

            # 2. UX & Advisory Checks (Extension and MIME)
            if file.filename == "":
                logger.warning("Prediction request rejected: Uploaded file filename is empty.")
                return jsonify({"success": False, "message": "Empty upload"}), 400
                
            if not validate_extension(file.filename):
                logger.warning(f"Prediction request rejected: Invalid extension '{file.filename}'")
                return jsonify({"success": False, "message": "Unsupported or invalid image file"}), 400
                
            if not validate_mimetype(file.mimetype):
                logger.warning(f"Prediction request rejected: Invalid mimetype '{file.mimetype}'")
                return jsonify({"success": False, "message": "Unsupported or invalid image file"}), 400

            # 3. Authoritative Check (Magic Number) via Chunked Reading
            header = file.read(16)
            detected_format = validate_magic_number(header)
            if not detected_format:
                logger.warning("Prediction request rejected: Invalid magic number signature")
                return jsonify({"success": False, "message": "Unsupported or invalid image file"}), 400
                
            # Seek back to beginning before reading full payload
            file.seek(0)

            # 4. Read full payload and decode via OpenCV
            try:
                image_bytes = file.read()
                np_arr = np.frombuffer(image_bytes, np.uint8)
                # IMREAD_COLOR normalizes RGBA/Grayscale to 3-channel BGR safely
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            except Exception as e:
                logger.warning(f"Prediction request rejected: Failed to read/decode file bytes: {str(e)}")
                return jsonify({"success": False, "message": "Unsupported or invalid image file"}), 400

            # 5. Structural Validation (Decode Success & Dimensions)
            if img is None or img.shape[0] == 0 or img.shape[1] == 0:
                logger.warning("Prediction request rejected: OpenCV image decoding returned None.")
                return jsonify({"success": False, "message": "Unsupported or invalid image file"}), 400
                
            height, width = img.shape[:2]
            if not validate_dimensions(width, height):
                logger.warning(f"Prediction request rejected: Dimensions {width}x{height} exceed total pixel limit")
                return jsonify({"success": False, "message": "Image dimensions exceed limits"}), 400

            # 6. Sanitize by Re-encoding into the Original Validated Format (Defense-in-depth)
            try:
                # Map detected magic number format to cv2 encode ext
                ext_map = {"jpeg": ".jpg", "png": ".png"}
                encode_ext = ext_map.get(detected_format, ".jpg")
                
                success, encoded_img = cv2.imencode(encode_ext, img)
                if not success:
                    raise Exception("cv2.imencode failed")
                sanitized_bytes = encoded_img.tobytes()
            except Exception as e:
                logger.warning(f"Prediction request rejected: Failed to re-encode image: {str(e)}")
                return jsonify({"success": False, "message": "Failed to process image"}), 500

            # Use sanitized bytes for persistence
            image_bytes = sanitized_bytes

            # 5. Run preprocessing
            try:
                preprocessed = preprocess_image(img)
            except ImagePreprocessingError as e:
                logger.warning(f"Image preprocessing failed for request: {str(e)}")
                return jsonify({
                    "success": False,
                    "message": str(e)
                }), 422

            # 6. Run prediction
            try:
                prediction = predict_disease(preprocessed)
            except PredictionError as e:
                logger.warning(f"Disease prediction failed for request: {str(e)}")
                return jsonify({
                    "success": False,
                    "message": str(e)
                }), 422

            # 6.5 Calculate Risk
            risk_level = calculate_risk(
                disease=prediction["disease"],
                confidence=prediction["confidence"],
                is_supported=prediction.get("is_supported", True)
            )
            prediction["risk_level"] = risk_level

            # 6.6 Run AI Enrichment
            if prediction.get("is_supported", True):
                try:
                    enrichment_data = AIEnrichmentService.enrich_prediction(
                        crop=crop_name,
                        disease=prediction["disease"],
                        confidence=prediction["confidence"]
                    )
                    prediction.update(enrichment_data)
                except Exception as e:
                    logger.error(f"Enrichment service failed to return data: {e}")

            # 7. Persist scan for authenticated users
            user_id = get_jwt_identity()
            if user_id:
                try:
                    created_scan = ScanService.save_scan(
                        user_id=user_id,
                        crop_name=crop_name,
                        disease=prediction["disease"],
                        confidence=prediction["confidence"],
                        image_bytes=image_bytes,
                        ai_summary=prediction.get("ai_summary"),
                        treatment_plans=prediction.get("treatment_plans"),
                        risk_level=prediction.get("risk_level")
                    )
                    prediction["scan_id"] = str(created_scan.id)
                    if created_scan.image_url:
                        prediction["image_url"] = created_scan.image_url
                except Exception as e:
                    logger.error(f"Failed to persist scan: {str(e)}")
                    # Proceed to return success even if persistence fails

            # 8. Return structured success JSON response
            return jsonify({
                "success": True,
                "data": prediction
            }), 200

        except Exception as e:
            logger.exception("Unexpected error occurred in scan prediction endpoint")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500

    @staticmethod
    def get_history():
        """
        Handle GET /api/scans
        """
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({"success": False, "message": "Unauthorized"}), 401
                
            scans = ScanService.get_user_history(user_id)
            
            # Serialize
            data = []
            for scan in scans:
                data.append({
                    "id": str(scan.id),
                    "crop_name": scan.crop.name,
                    "image_url": scan.image_url,
                    "predicted_disease": scan.predicted_disease,
                    "confidence_score": scan.confidence_score,
                    "ai_summary": scan.ai_summary,
                    "treatment_plans": scan.treatment_plans,
                    "risk_level": scan.risk_level,
                    "created_at": scan.created_at.isoformat()
                })
                
            return jsonify({
                "success": True,
                "data": data
            }), 200
            
        except Exception as e:
            logger.exception("Unexpected error occurred in get history endpoint")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500

    @staticmethod
    def delete(scan_id: str):
        """
        Handle DELETE /api/scans/<scan_id>
        """
        try:
            user_id = get_jwt_identity()
            ScanService.delete_scan(scan_id, user_id)
            return jsonify({
                "success": True,
                "message": "Scan deleted successfully"
            }), 200
        except ValueError as e:
            if str(e) == "Scan not found":
                return jsonify({"success": False, "message": str(e)}), 404
            elif str(e) == "Access denied":
                return jsonify({"success": False, "message": str(e)}), 403
            return jsonify({"success": False, "message": str(e)}), 400
        except Exception as e:
            logger.exception("Unexpected error occurred in delete scan endpoint")
            return jsonify({
                "success": False,
                "message": "An unexpected server error occurred"
            }), 500
