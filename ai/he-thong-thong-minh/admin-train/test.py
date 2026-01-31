import cv2
from rapidocr import RapidOCR

# Khởi tạo engine OCR
engine = RapidOCR()

# Đường dẫn ảnh
img_path = "D:\\WorkSpaceD\\project\\cs\\ai\\he-thong-thong-minh\\admin-train-v1\\images\\bill7.jpg"

# 1. Load và tiền xử lý ảnh
img = cv2.imread(img_path)

# Chuyển sang grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Áp dụng threshold để tăng độ tương phản
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Resize ảnh lớn hơn để OCR tốt hơn
height, width = thresh.shape
scale = 2  # scale lên 2x
resized = cv2.resize(thresh, (width*scale, height*scale), interpolation=cv2.INTER_LINEAR)

# Lưu tạm ảnh đã xử lý
preprocessed_path = "temp_preprocessed.jpg"
cv2.imwrite(preprocessed_path, resized)

# 2. Thực hiện OCR
result = engine(preprocessed_path)

# 3. Gom tất cả text thành một chuỗi, mỗi dòng cách nhau bằng \n
full_text = "\n".join(result.txts)

# 4. In ra màn hình
print("=== Nội dung OCR ===")
print(full_text)

# 5. Xuất ảnh có bounding box (tùy chọn)
result.vis("vis_result.jpg")
