import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif
from tqdm import tqdm

# --- 1. LOAD DATA ---
DATA_PATH = "Frontend_Assets/Data"
ASSET_DIR = "Frontend_Assets/Plots"
os.makedirs(ASSET_DIR, exist_ok=True)

print("📂 Loading Fused Features from Phase 2...")
X = np.load(os.path.join(DATA_PATH, "features.npy"))
y = np.load(os.path.join(DATA_PATH, "labels.npy"))

# --- 2. ENTROPY CALCULATION (Mutual Information) ---
print(f"🧠 Calculating Shannon Entropy for {X.shape[1]} features...")
# This ranks features by how much 'Information' they provide about the disease
importances = mutual_info_classif(X, y)
indices = np.argsort(importances)[::-1] # Sort: Highest Information Gain first

TOP_K_MODEL = 500 # Number of features for the actual ML model
TOP_K_PLOT = 20   # Number of features for the bar chart

# Create the optimized dataset (Top 500)
X_optimized = X[:, indices[:TOP_K_MODEL]]

# --- 3. VISUALIZATION ---
plt.figure(figsize=(12, 6))
plt.bar(range(TOP_K_PLOT), importances[indices[:TOP_K_PLOT]], color='teal', alpha=0.8)
plt.xticks(range(TOP_K_PLOT), [f"F_{i}" for i in indices[:TOP_K_PLOT]], rotation=45)
plt.title("Phase 3: Top 20 High-Entropy Features (Information Gain)", fontsize=14, fontweight='bold')
plt.ylabel("Entropy Score (Mutual Information)")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(os.path.join(ASSET_DIR, "phase3_entropy_bar.png"), dpi=300)

# --- 4. SAVE DATA FOR THE APP ---
# Save the optimized features for the Phase 4 training script
np.save(os.path.join(DATA_PATH, "features_optimized.npy"), X_optimized)

# CRITICAL: Save the specific indices so app.py knows which features to extract in real-time
np.save(os.path.join(DATA_PATH, "top_indices.npy"), indices[:TOP_K_MODEL])

print(f"\n📉 Feature Reduction: {X.shape[1]} -> {X_optimized.shape[1]}")
print(f"✅ SAVED: top_indices.npy (Essential for real-time inference)")
plt.show()