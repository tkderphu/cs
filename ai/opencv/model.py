import os
import cv2
import mediapipe as mp
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# ==============================
# 1. Hàm tính EAR và MAR
# ==============================
def eye_aspect_ratio(landmarks, eye_indices):
    p1, p2, p3, p4, p5, p6 = [landmarks[i] for i in eye_indices]
    # khoảng cách Euclid
    def euclid(a, b): return np.linalg.norm(np.array(a) - np.array(b))
    EAR = (euclid(p2, p6) + euclid(p3, p5)) / (2.0 * euclid(p1, p4))
    return EAR

def mouth_aspect_ratio(landmarks, mouth_indices):
    # chọn các điểm môi
    top = np.mean([landmarks[i] for i in mouth_indices["top"]], axis=0)
    bottom = np.mean([landmarks[i] for i in mouth_indices["bottom"]], axis=0)
    left = landmarks[mouth_indices["left"]]
    right = landmarks[mouth_indices["right"]]
    def euclid(a, b): return np.linalg.norm(np.array(a) - np.array(b))
    MAR = euclid(top, bottom) / euclid(left, right)
    return MAR

# ==============================
# 2. Vẽ confusion matrix
# ==============================
def plot_confusion_matrix(y_true, y_pred, labels, normalize=False,
                          title="Confusion Matrix", save_path=None):
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm = np.nan_to_num(cm)

    fig, ax = plt.subplots(figsize=(6,6))
    im = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax.set_title(title)
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)

    # annotate
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            value = cm[i, j]
            if normalize:
                text = f"{value:.2f}"
            else:
                row_sum = cm[i].sum()
                pct = (value / row_sum * 100) if row_sum > 0 else 0
                text = f"{value}\n({pct:.1f}%)"
            ax.text(j, i, text,
                    ha="center", va="center",
                    color="white" if value > thresh else "black")

    ax.set_ylabel('True label')
    ax.set_xlabel('Predicted label')
    fig.tight_layout()
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    if save_path:
        plt.savefig(save_path, dpi=150)
        print(f"Saved confusion matrix to {save_path}")

    plt.show()

# ==============================
# 3. Load dữ liệu + dự đoán
# ==============================
mp_face_mesh = mp.solutions.face_mesh

# index landmark trong Mediapipe
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
MOUTH = {
    "left": 78,
    "right": 308,
    "top": [13],
    "bottom": [14]
}

EAR_THRESH = 0.2
MAR_THRESH = 0.6

dataset_dir = "train"
true_labels = []
pred_labels = []

with mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1,
                           refine_landmarks=True, min_detection_confidence=0.5) as face_mesh:
    for label in os.listdir(dataset_dir):
        class_dir = os.path.join(dataset_dir, label)
        if not os.path.isdir(class_dir):
            continue
        for fname in os.listdir(class_dir):
            fpath = os.path.join(class_dir, fname)
            img = cv2.imread(fpath)
            if img is None:
                continue
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_mesh.process(rgb)

            if not results.multi_face_landmarks:
                continue

            face = results.multi_face_landmarks[0]
            h, w, _ = img.shape
            landmarks = [(int(p.x * w), int(p.y * h)) for p in face.landmark]

            EAR_left = eye_aspect_ratio(landmarks, LEFT_EYE)
            EAR_right = eye_aspect_ratio(landmarks, RIGHT_EYE)
            EAR = (EAR_left + EAR_right) / 2.0
            MAR = mouth_aspect_ratio(landmarks, MOUTH)

            # rule-based
            if EAR < EAR_THRESH or MAR > MAR_THRESH:
                pred = "buon_ngu"
            else:
                pred = "khong_buon_ngu"

            # gán nhãn ground truth
            if label in ["closed_eye", "yawn"]:
                true = "buon_ngu"
            else:
                true = "khong_buon_ngu"

            true_labels.append(true)
            pred_labels.append(pred)

# ==============================
# 4. Đánh giá
# ==============================
print(classification_report(true_labels, pred_labels, target_names=["khong_buon_ngu", "buon_ngu"]))

labels = ["khong_buon_ngu", "buon_ngu"]
plot_confusion_matrix(true_labels, pred_labels, labels=labels,
                      normalize=False, title="Confusion Matrix (count + %)",
                      save_path="cm_counts.png")
plot_confusion_matrix(true_labels, pred_labels, labels=labels,
                      normalize=True, title="Confusion Matrix (normalized)",
                      save_path="cm_norm.png")
