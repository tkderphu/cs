import cv2
import numpy as np

# Load original image
img = cv2.imread("./img/coins-table.jpg")

# Create a black mask with a white circle
mask = np.zeros(img.shape[:2], dtype="uint8")
cv2.circle(mask, (150, 150), 100, 255, -1)

# Apply mask
masked = cv2.bitwise_and(img, img, mask=mask)

cv2.imshow("Original", img)
cv2.imshow("Mask", mask)
cv2.imshow("Masked Image", masked)

cv2.waitKey(0)
cv2.destroyAllWindows() 
