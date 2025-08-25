# resize image video, rescaling


import cv2 as cv
video_path = r"C:\Users\FPT\Videos\Screen Recordings\test.mp4"
image_path = r"D:\WorkSpaceD\project\cs\uml-diagram\img\i5.webp"

# img = cv.imread(image_path)
# cv.imshow('My image', img)


def changeRes(width, height):
    # live video
    capture.set(3, width)
    capture.set(4, height)


def rescaleFrame(frame, scale=0.75):

    # live video, image, video

    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)

    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)



capture = cv.VideoCapture(
    video_path
)

while True:
    isTrue, frame = capture.read()

    frame_resized = rescaleFrame(frame, 0.5)

    cv.imshow('Video resized', frame_resized)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break
capture.release()
cv.destroyAllWindows()