import os
import numpy as np
from datetime import datetime
from typing import List
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.utils import to_categorical
from sklearn.metrics import f1_score, precision_score, recall_score
import cv2
from models import Sample, TrainedModel, TrainingSample


# --- Helper: Load and preprocess cropped eye images ---
def load_image_data(samples: List["Sample"], target_size=(64, 64), base_path="./images"):
    X, y = [], []
    for s in samples:
        image_path = os.path.join(base_path, os.path.basename(s.image_file_path))

        if not os.path.exists(image_path):
            print(f"Warning: File not found {image_path}")
            continue

        # Load full image
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error reading image: {image_path}")
            continue

        # Validate crop coordinates
        h, w, _ = img.shape
        x_min, y_min, x_max, y_max = max(0, s.x_min), max(0, s.y_min), min(w, s.x_max), min(h, s.y_max)

        if x_max <= x_min or y_max <= y_min:
            print(f"Invalid crop box for sample {s.id}")
            continue

        # Crop the eye region
        crop = img[y_min:y_max, x_min:x_max]
        if crop.size == 0:
            print(f"Empty crop for sample {s.id}")
            continue

        # Resize and normalize
        crop_resized = cv2.resize(crop, target_size)
        arr = img_to_array(crop_resized) / 255.0

        X.append(arr)
        y.append(0 if s.label.lower() in ['closed', '0'] else 1)  # closed=0, open=1

    if not X:
        raise ValueError("No valid cropped images found for training/testing.")

    return np.array(X), np.array(y)


# --- CNN Model Training ---
def train(trainSamples: List["Sample"], testSamples: List["Sample"]) -> "TrainedModel":
    """
    Trains a CNN model on cropped eye regions for open/closed classification.
    """
    print("Starting CNN model training with cropped images...")

    # --- Load and preprocess data ---
    X_train, y_train = load_image_data(trainSamples)
    X_test, y_test = load_image_data(testSamples)

    # --- Convert labels to one-hot encoding ---
    y_train_cat = to_categorical(y_train, num_classes=2)
    y_test_cat = to_categorical(y_test, num_classes=2)

    # --- Define CNN architecture ---
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dropout(0.4),
        layers.Dense(2, activation='softmax')
    ])

    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # --- Train the model ---
    model.fit(
        X_train, y_train_cat,
        epochs=10,
        batch_size=8,
        verbose=1,
        validation_split=0.1
    )

    # --- Evaluate ---
    loss, acc = model.evaluate(X_test, y_test_cat, verbose=0)
    y_pred = np.argmax(model.predict(X_test), axis=1)

    f1 = f1_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)

    # --- Save model ---
    os.makedirs("artifacts", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    artifact_path = f"artifacts/cnn_eye_crop_{timestamp}.h5"
    model.save(artifact_path)

    print("\nCNN training complete (with cropping).")
    print(f"   Accuracy : {acc:.3f}")
    print(f"   Precision: {prec:.3f}")
    print(f"   Recall   : {rec:.3f}")
    print(f"   F1 Score : {f1:.3f}")
    print(f"   Model saved to: {artifact_path}")

    return TrainedModel(
        id=-1,
        name="CNN",
        artifact_path=artifact_path,
        accuracy=acc,
        f1=f1,
        precision=prec,
        recall=rec,
        training_samples=[TrainingSample(sample=s) for s in trainSamples]
    )
