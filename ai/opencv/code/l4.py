import cv2 as cv

video_path = r"C:\Users\FPT\Videos\Screen Recordings\test.mp4"
image_path = r"D:\WorkSpaceD\project\cs\uml-diagram\img\i5.webp"


img = cv.imread(image_path)
# cv.imshow("My image", img)

cropped = img[50:500, 100:400]

cv.imshow("Cropped image", cropped)

cv.waitKey(0)