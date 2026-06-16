import logging
import cv2
import numpy as np
from flask import request, jsonify

from app.ml import preprocess_image, predict_disease, ImagePreprocessingError, PredictionError

# Configure logger
logger = logging.getLogger(__name__)

class ScanController:
    @staticmethod
    def predict():
        """
        Handle POST /api/scans
        """
        try:
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

            # 7. Return structured success JSON response
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
