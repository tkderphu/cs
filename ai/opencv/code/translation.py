


import cv2 as cv
import numpy as np

video_path = r"C:\Users\FPT\Videos\Screen Recordings\test.mp4"
image_path = r"D:\WorkSpaceD\project\cs\uml-diagram\img\i5.webp"


image = cv.imread(image_path)

def translate(img, x, y):
    matrix = np.float32([[1,0,x], [0,1,y]])
    demensions = img.shape[:2]

    return cv.warpAffine(img, matrix, demensions)


translated = translate(image, 20, 20)
cv.imshow("Origainal", image)
cv.imshow("Translated", translated)



cv.waitKey(0)