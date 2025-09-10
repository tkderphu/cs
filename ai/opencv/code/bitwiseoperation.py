import cv2
import numpy as np

# Create a black image
img1 = np.zeros((300, 300), dtype="uint8")
img2 = np.zeros((300, 300), dtype="uint8")

# Draw a white rectangle & circle
cv2.rectangle(img1, (50, 50), (250, 250), 255, -1)
cv2.circle(img2, (150, 150), 100, 255, -1)

# Bitwise operations
and_img = cv2.bitwise_and(img1, img2)
or_img  = cv2.bitwise_or(img1, img2)
xor_img = cv2.bitwise_xor(img1, img2)
not_img = cv2.bitwise_not(img1)

# Show results
cv2.imshow("Rectangle", img1)
cv2.imshow("Circle", img2)
# cv2.imshow("AND", and_img)
# cv2.imshow("OR", or_img)
# cv2.imshow("XOR", xor_img)
cv2.imshow("NOT", not_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
