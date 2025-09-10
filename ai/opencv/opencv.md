# Install dependencies

```
pip install opencv-contrib-python
pip install caer
```

# Read image and video

# Resize and rescaling

# Draw shapes and putting text

# 5 essential function

1. Convert to gray

```
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
```

- Converts the 3-channel color image (BGR) into a single channel (grayscale) image.

- Why?

    - Many algorithms (edge detection, thresholding, contour detection) only need intensity values, not colors.

    - This reduces computation (1 channel instead of 3).

- Result: image values range 0–255 (black → white).

2. Blur

```
blur = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
```

3. Edge cascade

```
cany = cv.Canny(img, 125, 175)
```

4. Dilating the image

```
dilated = cv.dilate(canny, (3, 3), interations=1)
```

5. Eroding

```
eroded = cv.erode(dilated, (3, 3), interations=1)
```

6. Cropping

```
cropped = img[50:200, 100:300]  # rows(y): 50→200, cols(x): 100→300
```

- Crops a region of interest (ROI) by slicing the NumPy array.

- Why?

    - To work only on a smaller ROI instead of the whole image.

    - Useful when you know where the object lies.


# Image transformations

1. Resize(scaling)

```
resized = cv.resize(img, (400, 300))
```

- resize of images
- speed up processing
- zoom in, out to focus on details or view context

2. Translation

```
def translate(img, x, y):
    M = np.float32([[1, 0, x], [0, 1, y]])   # Translation matrix
    return cv.warpAffine(img, M, (img.shape[1], img.shape[0]))

# x > 0 => right, x < 0 => left
# y > 0 => down, y < 0 => up

shifted = translate(img, 100, 50)  # move right 100px, down 50px
```

- Data augmentation → teach models that objects can appear in different places.

- Extract regions of interest (ROI) by shifting.

- Align objects in preprocessing (e.g., move a detected face to the center).

3. Rotation

4. Flip(Mirror)

5. Affine transformation
6. Perspective transformation
7. Image pyramids(scaling repeatedly)

# Contour detection

Contour detection is a CV technique used to indentify and extract the boundaries(contours) of objects within an image

A contour is simply a curve or line that joins all continuous point(pixels) along the boundary of an object that share the same intensity or color

- Purpose
    - detect shapes and objects in an image
    - usefull for object recognition

- How works
    - usually applied on a binary image(black and white)
    - steps:
        - convert image => grayscale
        - apply thresholding or edge detection
        - use a contour-finding algorithm

- Thresholding
    - converts an image into binary(black&white)
    - every pixel is set to either
        - white if aobve a threshold
        - black(0) if below
    - this makes it easy to separate foreground objects from background
- Edge detection(canny)
    - finds edges in an image based on gradients
    - produces a binary image where white lines represent edges
    - usefull when object are not uniform in clor but still have clear boundaries

Sometimes you need to decide:

- Do you want the object filled (use thresholding)

- Or do you just want the outline (use edge detection)

# Color spaces

A color space is basically a way to represent colors numberiacally

1. RGB
2. BGR(opencv used it)
3. Grayscale
    - only intensity, no color
    - range 0 => 255
4. HSV(hue, saturation, value)
    - separates color(hue) from brightness(value)
    - components:
        - hue => the color type(0 - 179 in opebcv)
            - 0= red, 60=green, 120=blue
        - saturation => color intensity (0 = gray, 255 = pure color)
        - value => brightness(0=balck, 255=full brightness)
    - Useful for color detection & filtering (e.g., detect red objects regardless of lighting).
5. LAB
    - desinged to mimic human vision
    - components:
        - L => lightness
        - a => green <=> red
        - b => blue <=> yellow
6. YCrCb
    - used in video compssion(JPEG, MPEG)
    - components:
        - Y = luminance(brightness)
        - Cr, Cb = chrominance(color difference)

```
import cv2

img = cv2.imread("shapes.png")

# Convert to different color spaces
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv  = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lab  = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

cv2.imshow("Gray", gray)
cv2.imshow("HSV", hsv)
cv2.imshow("LAB", lab)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

- Summary:

    ```
    RGB/BGR → display images.

    Grayscale → intensity only (no color).

    HSV → good for color detection.

    LAB → good for image processing & correction.

    YCrCb → used in video encoding.
    ```


# Color channels

# blurring

# Bitwise operation

A bitwise operation works directly on the bits (0s and 1s) of numbers or image pixels.
In image processing (with OpenCV), bitwise operations are used to combine, mask, or modify images at the pixel level.

- result = cv2.bitwise_and(img1, img2)
    - Keeps a pixel only if it’s non-zero (white) in both images.
    - Useful for masking (extracting an object from background).
- result = cv2.bitwise_or(img1, img2)
    - Keeps a pixel if it’s non-zero in either image.
    - Useful for combining objects
- result = cv2.bitwise_xor(img1, img2)
    - Keeps a pixel only if it’s non-zero (white) in both images.
    - Useful for masking (extracting an object from background).
- result = cv2.bitwise_not(img)
    - Inverts bits: black ↔ white, colors flipped.
    - Useful for negative effects, or preparing masks.

```
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
cv2.imshow("AND", and_img)
cv2.imshow("OR", or_img)
cv2.imshow("XOR", xor_img)
cv2.imshow("NOT", not_img)

cv2.waitKey(0)
cv2.destroyAllWindows()
```