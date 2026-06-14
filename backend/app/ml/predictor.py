import logging
import numpy as np
from typing import Dict, Any

from app.ml.model_loader import ModelLoader

# Configure logging
logger = logging.getLogger(__name__)

class PredictionError(Exception):
    """Exception raised when disease prediction pipeline fails."""
    pass

def predict_disease(image: np.ndarray) -> Dict[str, Any]:
    """
    Orchestrates the hybrid disease prediction pipeline for a single preprocessed image.
    
    The pipeline steps include:
    1. Input validation (dimensions must be 224x224x3).
    2. Batching the image to (1, 224, 224, 3) and converting to float32.
    3. ResNet101 and DenseNet201 feature extraction (applying respective Keras preprocessors).
    4. Concatenation of feature vectors (ResNet first, then DenseNet).
    5. StandardScaler transformation of the fused vector.
    6. Defensive dimensional validation and top index feature selection.
    7. SVM prediction and class probability/confidence score extraction.
    8. Mapping the prediction index to class metadata using class_mapping.json.
    
    Args:
        image: A preprocessed BGR image array of shape (224, 224, 3) and type np.uint8.
        
    Returns:
        A dictionary containing the structured prediction results:
        {
            "prediction_index": int,
            "crop": str,
            "disease": str,
            "label": str,
            "confidence": float
        }
        
    Raises:
        PredictionError: If pipeline execution fails or dimensions are invalid.
    """
    # 1. Input validation
    if not isinstance(image, np.ndarray):
        raise PredictionError(f"Input image must be a numpy.ndarray. Got: {type(image)}")
        
    if image.shape != (224, 224, 3):
        raise PredictionError(f"Input image must have dimensions (224, 224, 3). Got shape: {image.shape}")

    try:
        # Import Keras preprocessors internally to avoid namespace clutter or early loading issues
        from tensorflow.keras.applications.resnet import preprocess_input as res_pre
        from tensorflow.keras.applications.densenet import preprocess_input as den_pre

        # Ensure ModelLoader is initialized
        if not ModelLoader.is_initialized():
            logger.info("Initializing ModelLoader during inference request...")
            ModelLoader.load_all()

        # Retrieve cached ML resources
        resnet_model = ModelLoader.get_resnet_base()
        densenet_model = ModelLoader.get_densenet_base()
        scaler = ModelLoader.get_scaler()
        top_indices = ModelLoader.get_top_indices()
        svm_model = ModelLoader.get_svm_model()
        class_mapping = ModelLoader.get_class_mapping()

        # 2. Batch the image and cast to float32
        x = np.expand_dims(image.astype(np.float32), axis=0)

        # 3. Extract features using cached models (applying Keras preprocessing)
        logger.debug("Extracting ResNet101 features...")
        feat_res = resnet_model.predict(
            res_pre(x.copy()),
            verbose=0
        ).flatten()

        logger.debug("Extracting DenseNet201 features...")
        feat_den = densenet_model.predict(
            den_pre(x.copy()),
            verbose=0
        ).flatten()

        # 4. Concatenate both feature vectors (ResNet -> DenseNet)
        fused_vector = np.concatenate([feat_res, feat_den])

        # Reshape to a 2D sample array (1, n_features) for scikit-learn
        fused_vector_reshaped = fused_vector.reshape(1, -1)

        # 5. Transform using the cached StandardScaler
        scaled_vector = scaler.transform(fused_vector_reshaped)

        # 8. Defensive validation before feature selection
        if scaled_vector.shape[1] <= np.max(top_indices):
            raise PredictionError("Feature vector dimensions do not match training artifacts.")

        # 6. Apply top_indices feature selection
        selected_features = scaled_vector[:, top_indices]

        # 7. SVM prediction and class probability/confidence extraction
        pred_idx = int(svm_model.predict(selected_features)[0])
        probs = svm_model.predict_proba(selected_features)[0]
        confidence = float(probs[pred_idx])

        # 9. Map prediction using class_mapping.json
        str_pred_idx = str(pred_idx)
        if str_pred_idx not in class_mapping:
            raise PredictionError(f"Prediction index '{str_pred_idx}' not found in class mapping.")
            
        class_info = class_mapping[str_pred_idx]

        logger.info(f"Successful prediction: Index={pred_idx}, Crop={class_info['crop']}, Disease={class_info['disease']}, Confidence={confidence:.4f}")

        return {
            "prediction_index": pred_idx,
            "crop": class_info["crop"],
            "disease": class_info["disease"],
            "label": class_info["label"],
            "confidence": confidence
        }

    except PredictionError:
        raise
    except Exception as e:
        logger.exception("Error occurred in the prediction pipeline")
        raise PredictionError(f"Prediction pipeline failed: {str(e)}") from e
