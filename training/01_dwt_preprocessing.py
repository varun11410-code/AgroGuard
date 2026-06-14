import cv2
import numpy as np
import pywt
import os
from tqdm import tqdm # Run 'pip install tqdm' for a progress bar

def process_image(image_path):
    # 1. Read & Standardize Size
    img = cv2.imread(image_path)
    if img is None: return None
    img = cv2.resize(img, (224, 224)) # Standardizing to AI input size now
    
    # 2. CLAHE Enhancement (LAB Space)
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced = cv2.cvtColor(cv2.merge((cl, a, b)), cv2.COLOR_LAB2BGR)
    
    # 3. Wavelet Transform (Extracting the LL 'Clean' Approximation)
    gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
    coeffs2 = pywt.dwt2(gray, 'haar')
    LL, (LH, HL, HH) = coeffs2
    
    # Normalize LL to 0-255 so it can be saved as a standard image
    LL_normalized = cv2.normalize(LL, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    final_processed = cv2.cvtColor(LL_normalized, cv2.COLOR_GRAY2BGR)
    return final_processed
    

# --- CONFIGURATION ---
INPUT_DIR = "Raw_Dataset"  # Point to your folder with subfolders
OUTPUT_DIR = "Advanced_Processed_Dataset"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print(f"🚀 Starting Batch Processing from {INPUT_DIR} to {OUTPUT_DIR}...")

for root, dirs, files in os.walk(INPUT_DIR):
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            # Create subfolder structure in Output
            rel_path = os.path.relpath(root, INPUT_DIR)
            save_path = os.path.join(OUTPUT_DIR, rel_path)
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            
            # Process and Save
            input_file = os.path.join(root, filename)
            processed_img = process_image(input_file)
            
            if processed_img is not None:
                cv2.imwrite(os.path.join(save_path, filename), processed_img)

print(f"✅ Success! Your 'Research-Ready' dataset is at: {OUTPUT_DIR}")