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

``
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
```

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