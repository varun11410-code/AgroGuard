import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional
import joblib
import numpy as np

# Configure logging
logger = logging.getLogger(__name__)

class ModelLoaderError(Exception):
    """Base exception raised when model loading or initialization fails."""
    pass

class ModelLoader:
    """
    Singleton service to load and cache machine learning models and artifacts.
    This service initializes TensorFlow models and loads scikit-learn models,
    scaler, indices, and class mappings once during application startup.
    """
    
    _initialized: bool = False
    
    # Class-level cached resources
    _svm_model: Optional[Any] = None
    _scaler: Optional[Any] = None
    _top_indices: Optional[np.ndarray] = None
    _class_mapping: Optional[Dict[str, Any]] = None
    _resnet_base: Optional[Any] = None
    _densenet_base: Optional[Any] = None

    @classmethod
    def load_all(cls) -> None:
        """
        Loads all required ML models and artifacts into memory.
        Fails fast and raises ModelLoaderError if any resource cannot be loaded.
        """
        if cls._initialized:
            logger.info("ML models and artifacts are already loaded and cached.")
            return

        logger.info("Initializing ML Model Loader Service...")
        
        # Define base artifacts path relative to this file
        artifacts_dir = Path(__file__).parent / "artifacts"
        
        # 1. Load class mapping (class_mapping.json)
        class_mapping_path = artifacts_dir / "class_mapping.json"
        cls._class_mapping = cls._load_class_mapping(class_mapping_path)
        
        # 2. Load feature selection indices (top_indices.npy)
        top_indices_path = artifacts_dir / "top_indices.npy"
        cls._top_indices = cls._load_top_indices(top_indices_path)
        
        # 3. Load StandardScaler (scaler.pkl)
        scaler_path = artifacts_dir / "scaler.pkl"
        cls._scaler = cls._load_pickle_file(scaler_path, "StandardScaler")
        
        # 4. Load SVM model (hybrid_svm_model.pkl)
        svm_path = artifacts_dir / "hybrid_svm_model.pkl"
        cls._svm_model = cls._load_pickle_file(svm_path, "SVM Model")
        
        # 5. Initialize ResNet101
        cls._resnet_base = cls._initialize_resnet101()
        
        # 6. Initialize DenseNet201
        cls._densenet_base = cls._initialize_densenet201()
        
        cls._initialized = True
        logger.info("✅ All ML models and artifacts successfully loaded and cached.")

    @classmethod
    def get_svm_model(cls) -> Any:
        cls._ensure_initialized()
        return cls._svm_model

    @classmethod
    def get_scaler(cls) -> Any:
        cls._ensure_initialized()
        return cls._scaler

    @classmethod
    def get_top_indices(cls) -> np.ndarray:
        cls._ensure_initialized()
        return cls._top_indices

    @classmethod
    def get_class_mapping(cls) -> Dict[str, Any]:
        cls._ensure_initialized()
        return cls._class_mapping

    @classmethod
    def get_resnet_base(cls) -> Any:
        cls._ensure_initialized()
        return cls._resnet_base

    @classmethod
    def get_densenet_base(cls) -> Any:
        cls._ensure_initialized()
        return cls._densenet_base

    @classmethod
    def is_initialized(cls) -> bool:
        return cls._initialized

    @classmethod
    def clear_cache(cls) -> None:
        """Clears all cached models and artifacts (primarily for testing)."""
        cls._svm_model = None
        cls._scaler = None
        cls._top_indices = None
        cls._class_mapping = None
        cls._resnet_base = None
        cls._densenet_base = None
        cls._initialized = False
        logger.info("ML Model Loader cache cleared.")

    @classmethod
    def _ensure_initialized(cls) -> None:
        if not cls._initialized:
            cls.load_all()

    @classmethod
    def _load_class_mapping(cls, path: Path) -> Dict[str, Any]:
        if not path.exists():
            raise ModelLoaderError(f"Required class mapping file not found at: {path}")
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            raise ModelLoaderError(f"Failed to parse class mapping JSON from {path}: {e}") from e

    @classmethod
    def _load_top_indices(cls, path: Path) -> np.ndarray:
        if not path.exists():
            raise ModelLoaderError(f"Required top indices file not found at: {path}")
        try:
            return np.load(path)
        except Exception as e:
            raise ModelLoaderError(f"Failed to load numpy array from {path}: {e}") from e

    @classmethod
    def _load_pickle_file(cls, path: Path, name: str) -> Any:
        if not path.exists():
            raise ModelLoaderError(f"Required {name} file not found at: {path}")
        try:
            return joblib.load(path)
        except Exception as e:
            raise ModelLoaderError(f"Failed to deserialize {name} from {path}: {e}") from e

    @classmethod
    def _initialize_resnet101(cls) -> Any:
        logger.info("Initializing ResNet101 Feature Extractor base model...")
        try:
            # Import tensorflow internally to avoid loading it globally unless required
            import tensorflow as tf
            from tensorflow.keras.applications import ResNet101
            
            # Disable TF logs for a cleaner terminal
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            
            # Support custom local weights paths for restricted/air-gapped environments
            local_weights_path = os.getenv("RESNET101_WEIGHTS_PATH")
            if local_weights_path:
                weights_file = Path(local_weights_path)
                if not weights_file.exists():
                    raise ModelLoaderError(f"Local ResNet101 weights file not found at: {local_weights_path}")
                logger.info(f"Loading ResNet101 weights locally from: {local_weights_path}")
                model = ResNet101(
                    weights=None,
                    include_top=False,
                    pooling='avg',
                    input_shape=(224, 224, 3)
                )
                model.load_weights(str(weights_file))
            else:
                # Standard Imagenet download / cache check
                logger.info("Initializing ResNet101 from ImageNet pre-trained weights (may trigger download).")
                model = ResNet101(
                    weights='imagenet',
                    include_top=False,
                    pooling='avg',
                    input_shape=(224, 224, 3)
                )
            return model
        except Exception as e:
            raise ModelLoaderError(f"Failed to initialize ResNet101 model: {e}") from e

    @classmethod
    def _initialize_densenet201(cls) -> Any:
        logger.info("Initializing DenseNet201 Feature Extractor base model...")
        try:
            import tensorflow as tf
            from tensorflow.keras.applications import DenseNet201
            
            # Disable TF logs for a cleaner terminal
            os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
            
            # Support custom local weights paths for restricted/air-gapped environments
            local_weights_path = os.getenv("DENSENET201_WEIGHTS_PATH")
            if local_weights_path:
                weights_file = Path(local_weights_path)
                if not weights_file.exists():
                    raise ModelLoaderError(f"Local DenseNet201 weights file not found at: {local_weights_path}")
                logger.info(f"Loading DenseNet201 weights locally from: {local_weights_path}")
                model = DenseNet201(
                    weights=None,
                    include_top=False,
                    pooling='avg',
                    input_shape=(224, 224, 3)
                )
                model.load_weights(str(weights_file))
            else:
                # Standard Imagenet download / cache check
                logger.info("Initializing DenseNet201 from ImageNet pre-trained weights (may trigger download).")
                model = DenseNet201(
                    weights='imagenet',
                    include_top=False,
                    pooling='avg',
                    input_shape=(224, 224, 3)
                )
            return model
        except Exception as e:
            raise ModelLoaderError(f"Failed to initialize DenseNet201 model: {e}") from e
