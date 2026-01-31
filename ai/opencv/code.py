import os
import cv2
import mediapipe as mp
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score
import matplotlib.pyplot as plt

# ---------- Cấu hình ----------
DATA_DIR = "train"   # folder chứa 4 thư mục con: yawn, no_yawn, Open, Closed
EAR_THRESH = 0.25
MAR_THRESH = 0.6

# Mediapipe FaceMesh (ảnh tĩnh)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True, min_detection_confidence=0.5)

# Landmark indices (Mediapipe FaceMesh)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]
# for MAR we'll use inner top/bottom and left/right
MOUTH_TOP = 13
MOUTH_BOTTOM = 14
MOUTH_LEFT = 61
MOUTH_RIGHT = 291

# ---------- Hàm tính EAR / MAR ----------
def euclid(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def compute_EAR(landmarks, eye_idx):
    pts = [landmarks[i] for i in eye_idx]
    A = euclid(pts[1], pts[5])
    B = euclid(pts[2], pts[4])
    C = euclid(pts[0], pts[3])
    if C == 0: return 0.0
    return (A + B) / (2.0 * C)

def compute_MAR(landmarks):
    top = landmarks[MOUTH_TOP]
    bottom = landmarks[MOUTH_BOTTOM]
    left = landmarks[MOUTH_LEFT]
    right = landmarks[MOUTH_RIGHT]
    horiz = euclid(left, right)
    if horiz == 0: return 0.0
    vert = euclid(top, bottom)
    return vert / horiz

# ---------- Lists để lưu nhãn thực & dự đoán cho từng task ----------
true_eye = []
pred_eye = []
true_mouth = []
pred_mouth = []

count_images = 0
count_no_face = 0

# ---------- Duyệt ảnh trong thư mục ----------
for folder in os.listdir(DATA_DIR):
    folder_path = os.path.join(DATA_DIR, folder)
    if not os.path.isdir(folder_path):
        continue
    # chuẩn hóa tên folder để so sánh (không phân biệt hoa thường)
    lab = folder.strip()
    lab_low = lab.lower()

    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        # đọc ảnh
        img = cv2.imread(fpath)
        if img is None:
            continue
        count_images += 1
        h, w = img.shape[:2]
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        results = face_mesh.process(img_rgb)
        if not results.multi_face_landmarks:
            count_no_face += 1
            # bỏ qua ảnh không phát hiện mặt
            continue

        # lấy mặt đầu tiên
        face_lm = results.multi_face_landmarks[0]
        # toạ độ pixel
        landmarks = [(int(p.x * w), int(p.y * h)) for p in face_lm.landmark]

        # tính EAR & MAR
        ear_left = compute_EAR(landmarks, LEFT_EYE)
        ear_right = compute_EAR(landmarks, RIGHT_EYE)
        ear = (ear_left + ear_right) / 2.0
        mar = compute_MAR(landmarks)

        # Dự đoán cho mouth task (yawn / no_yawn)
        mouth_pred = "yawn" if mar > MAR_THRESH else "no_yawn"

        # Dự đoán cho eye task (Open / Closed)
        eye_pred = "Closed" if ear < EAR_THRESH else "Open"

        # Nếu folder là yawn / no_yawn --> đánh giá cho mouth task
        if lab_low in ("yawn", "yawm", "yawm"):   # hỗ trợ typo
            true_mouth.append("yawn")
            pred_mouth.append(mouth_pred)
        elif lab_low in ("no_yawn", "no_yawm", "no-yawn", "no_yawm"):  # hỗ trợ vài dạng
            true_mouth.append("no_yawn")
            pred_mouth.append(mouth_pred)
        # Nếu folder là Open / Closed --> đánh giá cho eye task
        elif lab_low in ("open", "open_eye", "openeye", "open_eye"):
            true_eye.append("Open")
            pred_eye.append(eye_pred)
        elif lab_low in ("closed", "closed_eye", "closedeye", "closed_eye"):
            true_eye.append("Closed")
            pred_eye.append(eye_pred)
        else:
            # Nếu folder tên khác (không nằm trong 4 nhãn), in cảnh báo và bỏ qua
            print(f"Warning: folder name '{folder}' không phải nhãn mong đợi; ảnh {fname} sẽ bỏ qua.")

# ---------- In thống kê nhanh ----------
print(f"\nTổng ảnh duyệt: {count_images}, ảnh không phát hiện mặt: {count_no_face}")
print(f"Số mẫu eye-task (Open/Closed): {len(true_eye)}")
print(f"Số mẫu mouth-task (yawn/no_yawn): {len(true_mouth)}\n")



# ---------- Đánh giá eye task ----------
if len(true_eye) > 0:
    print("=== EYE TASK (Open vs Closed) ===")
    print("Accuracy:", f"{accuracy_score(true_eye, pred_eye)*100:.2f}%")
    print(classification_report(true_eye, pred_eye, digits=3))
    labels_eye = ["Open", "Closed"]
    cm_eye = confusion_matrix(true_eye, pred_eye, labels=labels_eye)
    disp_e = ConfusionMatrixDisplay(confusion_matrix=cm_eye, display_labels=labels_eye)
    disp_e.plot(cmap="Greens", values_format="d")
    plt.title("Confusion Matrix - Eye (Open / Closed)")
    plt.show()
else:
    print("No eye samples to evaluate.")
