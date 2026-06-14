import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib 
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import (
    classification_report, confusion_matrix, accuracy_score, 
    recall_score, precision_score, f1_score
)

# --- 1. DIRECTORY CONFIGURATION ---
DATA_PATH = "Frontend_Assets/Data"
ASSET_DIR = "Frontend_Assets/Plots"
MODEL_DIR = "Frontend_Assets/Model" # Sub-folder for the brain
CLASS_NAMES_PATH = "Advanced_Processed_Dataset"

# Safety: Create all required folders before doing any math
os.makedirs(ASSET_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(DATA_PATH, exist_ok=True)

print("📂 Initializing Research Evaluation Pipeline...")

# --- 2. DATA LOADING ---
try:
    X = np.load(os.path.join(DATA_PATH, "features_optimized.npy"))
    y = np.load(os.path.join(DATA_PATH, "labels.npy"))
    
    # Get actual folder names for the Confusion Matrix labels
    class_names = sorted([d for d in os.listdir(CLASS_NAMES_PATH) 
                         if os.path.isdir(os.path.join(CLASS_NAMES_PATH, d))])
    
except Exception as e:
    print(f"❌ Initialization Error: {e}. Ensure Phase 1-3 are complete!")
    exit()

# --- 3. TRAIN/TEST SPLIT (80-20) ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# --- 4. TRAIN THE HYBRID CLASSIFIER ---
print(f"🧠 Training Research SVM (RBF Kernel) on {X_train.shape[1]} Entropy-Selected Features...")
model = SVC(kernel='rbf', probability=True, C=1.0)
model.fit(X_train, y_train)

# --- 5. MULTI-DIMENSIONAL EVALUATION ---
y_pred = model.predict(X_test)

def calculate_specificity(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    spec_list = []
    for i in range(len(cm)):
        tn = np.sum(cm) - (np.sum(cm[i, :]) + np.sum(cm[:, i]) - cm[i, i])
        fp = np.sum(cm[:, i]) - cm[i, i]
        spec_list.append(tn / (tn + fp) if (tn + fp) > 0 else 0)
    return np.mean(spec_list)

acc = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
spec = calculate_specificity(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=class_names, zero_division=0)

# --- 6. ASSET EXPORT (FOR THE WEBSITE & VIVA) ---
print("\n🏆 --- FINAL RESEARCH METRICS --- 🏆")
print(f"✅ Accuracy:    {acc*100:.2f}%")
print(f"✅ Specificity: {spec*100:.2f}%")
print(f"✅ F1-Score:    {f1*100:.2f}%")

# Save Summary Metrics
with open(os.path.join(ASSET_DIR, "phase4_summary_metrics.txt"), "w") as f:
    f.write(f"Accuracy: {acc*100:.2f}%\nPrecision: {prec*100:.2f}%\nRecall: {rec*100:.2f}%\nSpecificity: {spec*100:.2f}%\nF1-Score: {f1*100:.2f}%")

# Save Detailed Class Report (Professor's Favorite)
with open(os.path.join(ASSET_DIR, "phase4_detailed_report.txt"), "w") as f:
    f.write(report)

# --- 7. VISUALIZATION ---
plt.figure(figsize=(12, 9))
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names)

plt.title("Phase 4: Hybrid Model Confusion Matrix", fontsize=15, fontweight='bold')
plt.ylabel('Actual Crop Disease')
plt.xlabel('Predicted Crop Disease')
plt.xticks(rotation=45, ha='right')

plt.savefig(os.path.join(ASSET_DIR, "phase4_confusion_matrix.png"), dpi=300, bbox_inches='tight')

# --- 8. FINAL MODEL SAVE ---
joblib.dump(model, os.path.join(MODEL_DIR, "hybrid_svm_model.pkl"))

print(f"\n🚀 ALL PHASES COMPLETE! Check 'Frontend_Assets' for your website files.")
plt.show()