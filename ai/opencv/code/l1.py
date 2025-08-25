
import cv2 as cv
video_path = r"C:\Users\FPT\Videos\Screen Recordings\test.mp4"
image_path = r"D:\WorkSpaceD\project\cs\uml-diagram\img\i5.webp"

# img = cv.imread(image_path)

# cv.imshow('My video', img)

#reading video

capture = cv.VideoCapture(
    video_path
)

while True:
    isTrue, frame = capture.read()
    cv.imshow('Video', frame)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()