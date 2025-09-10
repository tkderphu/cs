import cv2 as cv
image_path = r"./img/dog.jpg"

image = cv.imread(image_path)

gray_image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
_, thresh = cv.threshold(gray_image, 127, 255, cv.THRESH_BINARY)
contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(image, contours, -1, (0,255,0), 2)

edges = cv.Canny(image, 100, 200)

cv.imshow("test", edges)
conto, _= cv.findContours(edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

OUTPUT = image.copy()
cv.drawContours(OUTPUT, conto, -1, (0,255,0), 2)

cv.imshow("Contours from edges", OUTPUT)

cv.imshow("my image", image)
cv.imshow("another image", thresh)
cv.waitKey(0)