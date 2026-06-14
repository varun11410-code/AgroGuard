import os
import numpy as np
import tensorflow as tf
import joblib
from tensorflow.keras.applications import ResNet101, DenseNet201
from tensorflow.keras.applications.resnet import preprocess_input as res_pre
from tensorflow.keras.applications.densenet import preprocess_input as den_pre
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

# Disable TF logs for a clean terminal
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 

# 1. SETUP DIRECTORIES
ASSET_DIR = "Frontend_Assets/Plots"
DATA_SAVE_DIR = "Frontend_Assets/Data"
DATA_DIR = "Advanced_Processed_Dataset" # Ensure this matches your dataset folder name
os.makedirs(ASSET_DIR, exist_ok=True)
os.makedirs(DATA_SAVE_DIR, exist_ok=True)

print("📦 Initializing AI Models (ResNet101 & DenseNet201)...")
resnet_base = ResNet101(weights='imagenet', include_top=False, pooling='avg', input_shape=(224, 224, 3))
densenet_base = DenseNet201(weights='imagenet', include_top=False, pooling='avg', input_shape=(224, 224, 3))

def extract_all_features(img_path):
    img = load_img(img_path, target_size=(224, 224))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # Individual Extraction
    feat_res = resnet_base.predict(res_pre(x.copy()), verbose=0).flatten()
    feat_den = densenet_base.predict(den_pre(x.copy()), verbose=0).flatten()

    # The Fusion (Concatenation)
    fused_vector = np.concatenate([feat_res, feat_den])
    return feat_res, feat_den, fused_vector

# --- DATA PREPARATION ---
features_res, features_den, features_fused, labels = [], [], [], []
class_names = sorted(os.listdir(DATA_DIR))
print(f"🚀 Extracting Features from {len(class_names)} classes...")

# Limit images per class for faster processing/stability during demo
LIMIT_PER_CLASS = 50 

for label_idx, class_name in enumerate(class_names):
    class_path = os.path.join(DATA_DIR, class_name)
    if not os.path.isdir(class_path): continue
        
    files = [f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))][:LIMIT_PER_CLASS]
    
    for f in tqdm(files, desc=f"Scanning {class_name}"):
        path = os.path.join(class_path, f)
        try:
            f_res, f_den, f_fused = extract_all_features(path)
            features_res.append(f_res)
            features_den.append(f_den)
            features_fused.append(f_fused)
            labels.append(label_idx)
        except Exception as e:
            print(f"\n⚠️ Error processing {f}: {e}")

# --- PCA PROCESSING FUNCTION ---
def process_pca(feature_list):
    feat_np = StandardScaler().fit_transform(np.array(feature_list))
    pca = PCA(n_components=2)
    components = pca.fit_transform(feat_np)
    return components

print("⚙️ Computing PCA for visualization...")
comp_res = process_pca(features_res)
comp_den = process_pca(features_den)
comp_fused = process_pca(features_fused)

# --- INDIVIDUAL PLOTTING & SAVING (THE FIX) ---
titles = ["ResNet101 Features", "DenseNet201 Features", "Hybrid Fused Space (AgroGuard)"]
comps = [comp_res, comp_den, comp_fused]
filenames = ["phase2_resnet_only.png", "phase2_densenet_only.png", "phase2_fusion_impact.png"]

for i in range(3):
    plt.figure(figsize=(10, 7))
    for class_idx, name in enumerate(class_names):
        idx = np.where(np.array(labels) == class_idx)
        plt.scatter(comps[i][idx, 0], comps[i][idx, 1], label=name, alpha=0.6, edgecolors='w', s=40)
    
    plt.title(f"{titles[i]} Visualization (PCA)", fontsize=14, fontweight='bold')
    plt.xlabel("PC 1")
    plt.ylabel("PC 2")
    plt.grid(True, linestyle='--', alpha=0.3)
    
    # Save each plot to the asset directory
    save_path = os.path.join(ASSET_DIR, filenames[i])
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"💾 Saved Asset: {filenames[i]}")
    plt.close() # Important to free memory

# --- CRITICAL: SAVE DATA FOR PHASE 3 ---
# We scale the fused features one last time before saving for the SVM/Entropy Phase
print("💾 Saving fused features for Phase 3...")
scaler = StandardScaler()

X_fused_scaled = scaler.fit_transform(
    np.array(features_fused)
)

joblib.dump(
    scaler,
    os.path.join(DATA_SAVE_DIR, "scaler.pkl")
)
np.save(os.path.join(DATA_SAVE_DIR, "features.npy"), X_fused_scaled)
np.save(os.path.join(DATA_SAVE_DIR, "labels.npy"), np.array(labels))

print(f"\n✅ SUCCESS: Phase 2 Pipeline Complete.")
print(f"Total Features Extracted: {X_fused_scaled.shape[1]}")
print(f"Data saved in: {DATA_SAVE_DIR}")