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

# Color spaces
