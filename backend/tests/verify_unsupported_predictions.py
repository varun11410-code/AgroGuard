import os
import sys
import numpy as np
from unittest.mock import MagicMock, patch

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.ml.model_loader import ModelLoader
from app.ml.predictor import predict_disease, PredictionError

def run_tests():
    print("Starting verification tests...")

    # Mock the return values of ModelLoader to avoid loading heavy weights/tensorflow
    mock_resnet = MagicMock()
    mock_densenet = MagicMock()
    
    mock_resnet.predict.return_value = np.zeros((1, 2048))
    mock_densenet.predict.return_value = np.zeros((1, 1920))

    mock_scaler = MagicMock()
    mock_scaler.transform.return_value = np.zeros((1, 3968))

    mock_top_indices = np.arange(500)

    mock_svm = MagicMock()

    # Define standard class mapping matching class_mapping.json
    mock_class_mapping = {
        "0": {"crop": "Potato", "disease": "Early Blight", "label": "Potato___Early_blight"},
        "1": {"crop": "Potato", "disease": "Late Blight", "label": "Potato___Late_blight"},
        "2": {"crop": "Potato", "disease": "Healthy", "label": "Potato___healthy"},
        "3": {"crop": "Tomato", "disease": "Early Blight", "label": "Tomato___Early_blight"},
        "4": {"crop": "Tomato", "disease": "Late Blight", "label": "Tomato___Late_blight"},
        "5": {"crop": "Tomato", "disease": "Healthy", "label": "Tomato___healthy"},
    }

    # Patch the getters
    with patch.object(ModelLoader, 'is_initialized', return_value=True), \
         patch.object(ModelLoader, 'get_resnet_base', return_value=mock_resnet), \
         patch.object(ModelLoader, 'get_densenet_base', return_value=mock_densenet), \
         patch.object(ModelLoader, 'get_scaler', return_value=mock_scaler), \
         patch.object(ModelLoader, 'get_top_indices', return_value=mock_top_indices), \
         patch.object(ModelLoader, 'get_svm_model', return_value=mock_svm), \
         patch.object(ModelLoader, 'get_class_mapping', return_value=mock_class_mapping):

        # Prepare a dummy BGR input image (224x224x3)
        dummy_image = np.zeros((224, 224, 3), dtype=np.uint8)

        # ---------------------------------------------
        # Test 1: Low Confidence Prediction (< 0.50)
        # ---------------------------------------------
        print("\n--- Running Test 1: Low Confidence Prediction ---")
        mock_svm.predict.return_value = np.array([1]) # Predicted index = 1
        probs = np.zeros(6)
        probs[1] = 0.45
        mock_svm.predict_proba.return_value = np.array([probs])

        res = predict_disease(dummy_image)
        print("Result:", res)
        assert res["is_supported"] is False, "Expected is_supported to be False"
        assert res["prediction_index"] is None, "Expected prediction_index to be None"
        assert res["crop"] == "Unknown", "Expected crop to be 'Unknown'"
        assert res["disease"] == "Unsupported", "Expected disease to be 'Unsupported'"
        assert res["label"] is None, "Expected label to be None"
        assert res["confidence"] == 0.45, "Expected confidence to be 0.45"
        print("[PASSED] Test 1: Low confidence prediction handled successfully.")

        # ---------------------------------------------
        # Test 2: Normal Prediction (>= 0.50)
        # ---------------------------------------------
        print("\n--- Running Test 2: Normal Prediction ---")
        mock_svm.predict.return_value = np.array([1])
        probs = np.zeros(6)
        probs[1] = 0.88
        mock_svm.predict_proba.return_value = np.array([probs])

        res = predict_disease(dummy_image)
        print("Result:", res)
        assert res["is_supported"] is True, "Expected is_supported to be True"
        assert res["prediction_index"] == 1, "Expected prediction_index to be 1"
        assert res["crop"] == "Potato", "Expected crop to be 'Potato'"
        assert res["disease"] == "Late Blight", "Expected disease to be 'Late Blight'"
        assert res["label"] == "Potato___Late_blight", "Expected label to be 'Potato___Late_blight'"
        assert res["confidence"] == 0.88, "Expected confidence to be 0.88"
        print("[PASSED] Test 2: Normal prediction handled successfully.")

        # ---------------------------------------------
        # Test 3: Missing Class Mapping
        # ---------------------------------------------
        print("\n--- Running Test 3: Missing Class Mapping ---")
        mock_svm.predict.return_value = np.array([99]) # Out of bounds index
        probs = np.zeros(100)
        probs[99] = 0.95
        mock_svm.predict_proba.return_value = np.array([probs])

        try:
            predict_disease(dummy_image)
            assert False, "Expected PredictionError to be raised for missing index 99"
        except PredictionError as e:
            print("Caught expected exception:", str(e))
            assert str(e) == "No class mapping found for prediction index 99", f"Unexpected error message: {str(e)}"
            print("[PASSED] Test 3: Missing class mapping raises correct PredictionError.")

    print("\nAll verification tests completed successfully!")

if __name__ == "__main__":
    run_tests()
