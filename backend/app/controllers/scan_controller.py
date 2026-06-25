import logging
import cv2
import numpy as np
from flask import request, jsonify
from flask_jwt_extended import get_jwt_identity

from app.ml import preprocess_image, predict_disease, ImagePreprocessingError, PredictionError
from app.services.scan_service import ScanService

# Configure logger
logger = logging.getLogger(__name__)

class ScanController:
    @staticmethod
    def predict():
        """
        Handle POST /api/scans
        """
        try:
            crop_name = request.form.get("crop")
            if not crop_name:
                logger.warning("Prediction request rejected: Missing crop parameter.")
                return jsonify({
                    "success": False,
                    "message": "Missing crop parameter"
                }), 400

            # 1. Validate uploaded image field exists
            if "image" not in request.files:
                logger.warning("Prediction request rejected: Missing image field in files payload.")
                return jsonify({
                    "success": False,
                    "message": "Missing image field"
                }), 400

            file = request.files["image"]

            # 2. Validate file is not empty
            if file.filename == "":
                logger.warning("Prediction request rejected: Uploaded file filename is empty.")
                return jsonify({
                    "success": False,
                    "message": "Empty upload"
                }), 400

            # 3. Read raw bytes and decode the image using OpenCV
            try:
                image_bytes = file.read()
                np_arr = np.frombuffer(image_bytes, np.uint8)
                img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            except Exception as e:
                logger.warning(f"Prediction request rejected: Failed to read file bytes: {str(e)}")
                return jsonify({
                    "success": False,
                    "message": "Invalid/corrupted image file"
                }), 400

            # 4. Validate that decoding succeeded
            if img is None or img.shape[0] == 0 or img.shape[1] == 0:
                logger.warning("Prediction request rejected: OpenCV image decoding returned None or empty array.")
                return jsonify({
                    "success": False,
                    "message": "Invalid/corrupted image file"
                }), 400

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

            # 7. Persist scan for authenticated users
            user_id = get_jwt_identity()
            if user_id:
                try:
                    ScanService.save_scan(
                        user_id=user_id,
                        crop_name=crop_name,
                        disease=prediction["disease"],
                        confidence=prediction["confidence"],
                        image_bytes=image_bytes
                    )
                except Exception as e:
                    logger.error(f"Failed to persist scan for user {user_id}: {str(e)}")
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
