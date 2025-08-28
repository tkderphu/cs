
import cv2 as cv
import numpy as np
video_path = r"C:\Users\FPT\Videos\Screen Recordings\test.mp4"
image_path = r"D:\WorkSpaceD\project\cs\uml-diagram\img\i5.webp"


#Create blank image (wid * hei) and has three color dtype range value from 0 - 255
blank = np.zeros((500, 500, 3), dtype='uint8')

cv.line(blank, (0, 0), (255, 255), (255,150,150), thickness=1, lineType=cv.LINE_4)
# cv.imshow("My image", blank)
cv.putText(blank, "Hello world", (255, 255), cv.FONT_ITALIC,1.2, (255,255,255),thickness=2, lineType=cv.LINE_AA)
cv.imshow("Puttext",blank)
cv.rectangle(blank, (50, 50), (300, 300), (0,0,255), thickness=3)
# cv.imshow("Retangle",blank)

cv.circle(blank, (450,450), 50, (0,255,0), thickness=5)
# cv.imshow("Circle", blank)
cv.waitKey(0)

