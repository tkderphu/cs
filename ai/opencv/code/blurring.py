import cv2 as cv
image_path = r"./img/dog.jpg"

image = cv.imread(image_path)

blurA = cv.blur(image, (5,5))
gauss = cv.GaussianBlur(image, (5,5),2)


cv.imshow("my image", blurA)
cv.imshow("my gau", gauss)
cv.waitKey(0)