import os
import cv2
import numpy as np
from typing import List
from datetime import datetime
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.ensemble import RandomForestClassifier
from models import Sample, TrainedModel, TrainingSample
import joblib


# --- Helper: Extract features from cropped images ---
def extract_features(samples: List["Sample"], target_size=(32, 32), base_path="./images"):
    """
    Extracts flattened pixel features from cropped eye regions.
    """
    X, y = [], []
    for s in samples:
        image_path = os.path.join(base_path, os.path.basename(s.image_file_path))

        if not os.path.exists(image_path):
            print(f"Warning: File not found {image_path}")
            continue

        img = cv2.imread(image_path)
        if img is None:
            print(f"Error reading image: {image_path}")
            continue

        h, w, _ = img.shape
        x_min, y_min, x_max, y_max = max(0, s.x_min), max(0, s.y_min), min(w, s.x_max), min(h, s.y_max)

        if x_max <= x_min or y_max <= y_min:
            print(f"Invalid crop box for sample {s.id}")
            continue

        crop = img[y_min:y_max, x_min:x_max]
        if crop.size == 0:
            print(f"Empty crop for sample {s.id}")
            continue

        # Resize and normalize
        crop_resized = cv2.resize(crop, target_size)
        arr = crop_resized.flatten() / 255.0

        X.append(arr)
        y.append(0 if s.label.lower() in ['closed', '0'] else 1)

    if not X:
        raise ValueError("No valid cropped images found for training/testing.")

    return np.array(X), np.array(y)


# --- Random Forest Model Training ---
def train(trainSamples: List["Sample"], testSamples: List["Sample"]) -> "TrainedModel":
    print("Starting Random Forest training with cropped images...")

    # --- Extract features ---
    X_train, y_train = extract_features(trainSamples)
    X_test, y_test = extract_features(testSamples)

    # --- Train model ---
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # --- Evaluate ---
    y_pred = clf.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)

    # --- Save model ---
    os.makedirs("artifacts", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_path = f"artifacts/random_forest_eye_crop_{timestamp}.pkl"
    joblib.dump(clf, artifact_path)

    print("\nRandom Forest training complete (with cropping).")
    print(f"   Accuracy : {acc:.3f}")
    print(f"   Precision: {prec:.3f}")
    print(f"   Recall   : {rec:.3f}")
    print(f"   F1 Score : {f1:.3f}")
    print(f"   Model saved to: {artifact_path}")

    return TrainedModel(
        id=-1,
        name="Random Forest",
        artifact_path=artifact_path,
        accuracy=acc,
        f1=f1,
        precision=prec,
        recall=rec,
        training_samples=[TrainingSample(sample=s) for s in trainSamples]
    )
