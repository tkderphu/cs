
import cv2 as cv
import numpy as np
video_path = r"C:\Users\FPT\Videos\Screen Recordings\test.mp4"
image_path = r"D:\WorkSpaceD\project\cs\uml-diagram\img\i5.webp"


blank = np.zeros((500, 500, 3), dtype='uint8')

blank[:] = 0,255,0
cv.imshow('blank', blank)
img = cv.imread(image_path)
cv.imshow('My video', img)
cv.waitKey(0)

