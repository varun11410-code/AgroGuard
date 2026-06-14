import cv2
import numpy as np
import pywt
from typing import Union

class ImagePreprocessingError(Exception):
    """Exception raised when image preprocessing fails."""
    pass

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Applies the exact preprocessing pipeline used during training to a single BGR image.
    
    Preprocessing steps:
    1. Validate dimensions and format.
    2. Resize to 224x224.
    3. Apply CLAHE enhancement in LAB color space.
    4. Convert BGR to Grayscale.
    5. Apply 2D Haar Wavelet Transform (DWT) and extract the LL (low-low) approximation coefficients.
    6. Normalize the LL coefficients to the 0-255 range.
    7. Convert normalized grayscale LL approximation back to a 3-channel BGR image.
    8. Resize the 3-channel BGR image back to 224x224 using nearest-neighbor interpolation.
    
    Args:
        image: Input image as a NumPy array (BGR format, typically from cv2.imread or cv2.imdecode).
               Must have shape (H, W, 3).
               
    Returns:
        A preprocessed BGR image as a NumPy array of shape (224, 224, 3) and type np.uint8.
        
    Raises:
        ImagePreprocessingError: If the input image is invalid or preprocessing fails.
    """
    # 1. Validation
    if not isinstance(image, np.ndarray):
        raise ImagePreprocessingError(
            f"Input image must be a numpy.ndarray. Got: {type(image)}"
        )
    
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ImagePreprocessingError(
            f"Input image must have 3 dimensions and 3 channels (H, W, 3). Got shape: {image.shape}"
        )
        
    if image.shape[0] == 0 or image.shape[1] == 0:
        raise ImagePreprocessingError(
            f"Input image cannot have zero width or height. Got shape: {image.shape}"
        )

    try:
        # 2. Standardize Size (Resize to 224 x 224)
        # Using bilinear interpolation for the initial resize (OpenCV default and matches general cv2 resize behavior)
        img_resized = cv2.resize(image, (224, 224), interpolation=cv2.INTER_LINEAR)
        
        # 3. CLAHE Enhancement (LAB Space)
        lab = cv2.cvtColor(img_resized, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        enhanced = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)
        
        # 4. Convert enhanced image to grayscale
        gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
        
        # 5. Haar Wavelet Transform (Extract LL Approximation)
        coeffs2 = pywt.dwt2(gray, 'haar')
        LL, (LH, HL, HH) = coeffs2
        
        # 6. Normalize LL to 0-255 range
        # Note: If LL has no variance (min == max), cv2.normalize handles it, returning a zero array.
        LL_normalized = cv2.normalize(LL, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
        
        # 7. Convert the normalized grayscale output back to a 3-channel BGR image
        # This yields shape (112, 112, 3)
        bgr_112 = cv2.cvtColor(LL_normalized, cv2.COLOR_GRAY2BGR)
        
        # 8. Resize back to (224, 224, 3) using nearest-neighbor interpolation
        # This matches the Keras load_img(..., target_size=(224, 224)) default interpolation behavior.
        final_processed = cv2.resize(bgr_112, (224, 224), interpolation=cv2.INTER_NEAREST)
        
        return final_processed
        
    except Exception as e:
        raise ImagePreprocessingError(f"Failed to preprocess image: {str(e)}") from e
