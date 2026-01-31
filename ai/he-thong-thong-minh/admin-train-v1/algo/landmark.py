import cv2
import mediapipe as mp
import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
from models import Sample, TrainedModel
from typing import Optional, List

# Initialize Mediapipe Face Mesh once
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

# Eye landmark indices (from Mediapipe's 468-point mesh)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [263, 387, 385, 362, 380, 373]


def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def eye_aspect_ratio(eye_points, landmarks, w, h):
    """Compute the Eye Aspect Ratio (EAR) from the Mediapipe landmarks."""
    points = [(int(landmarks[i].x * w), int(landmarks[i].y * h)) for i in eye_points]
    A = euclidean_distance(points[1], points[5])
    B = euclidean_distance(points[2], points[4])
    C = euclidean_distance(points[0], points[3])
    return (A + B) / (2.0 * C)


def predict_eye_state(sample: 'Sample', ear_thresh=0.25) -> Optional[str]:
    """
    Predict if eyes are open or closed using Mediapipe FaceMesh on the full image.
    """
    path = "./images/" + sample.image_file_path
    img = cv2.imread(path)

    if img is None:
        print(f"Cannot read image: {path}")
        return None

    # Convert to RGB (Mediapipe expects RGB images)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if not result.multi_face_landmarks:
        print(f"No landmarks detected for sample {sample.id}")
        return None

    landmarks = result.multi_face_landmarks[0].landmark
    h, w, _ = img.shape

    left_ear = eye_aspect_ratio(LEFT_EYE, landmarks, w, h)
    right_ear = eye_aspect_ratio(RIGHT_EYE, landmarks, w, h)
    avg_ear = (left_ear + right_ear) / 2.0

    # Classify based on EAR threshold
    return "open" if avg_ear > ear_thresh else "closed"


def train(samples: List[Sample]) -> Optional[TrainedModel]:
    """
    Evaluate Mediapipe landmark-based detection across dataset samples.
    """
    true_labels, pred_labels = [], []

    for sample in samples:
        pred = predict_eye_state(sample)
        if pred:
            true_labels.append(sample.label.lower())
            pred_labels.append(pred.lower())
        else:
            print(f"Skipped sample {sample.id}")

    if not true_labels:
        print("No valid samples detected.")
        return None

    labels = ["closed", "open"]
    acc = accuracy_score(true_labels, pred_labels)
    prec = precision_score(true_labels, pred_labels, labels=labels, pos_label="open", average='binary', zero_division=0)
    rec = recall_score(true_labels, pred_labels, labels=labels, pos_label="open", average='binary', zero_division=0)
    f1 = f1_score(true_labels, pred_labels, labels=labels, pos_label="open", average='binary', zero_division=0)

    print("Evaluation Results:")
    print(f"Accuracy : {acc:.3f}")
    print(f"Precision: {prec:.3f}")
    print(f"Recall   : {rec:.3f}")
    print(f"F1-score : {f1:.3f}")
    print("\nDetailed report:")
    print(classification_report(true_labels, pred_labels))

    return TrainedModel(
        name="Landmark",
        artifact_path=None,
        accuracy=acc,
        f1=f1,
        precision=prec,
        recall=rec,
        training_samples=None
    )
