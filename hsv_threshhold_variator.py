import numpy as np
import cv2
def nothing(x):
    pass

img = cv2.imread("1.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


cv2.namedWindow('image')
cv2.createTrackbar('H','image',0,180,nothing)
cv2.createTrackbar('S','image',0,255,nothing)
cv2.createTrackbar('V','image',0,255,nothing)

h, s, v = (0, 0, 0)
def updateBars(bars):
    h, s, v = bars
    cv2.setTrackbarPos('H','image', h)
    cv2.setTrackbarPos('S','image', s)
    cv2.setTrackbarPos('V','image', v)

# orange
orange = (7, 173, 255)
# range wide=10, wide2=50, wide3=50

# blue
blue = (99, 209, 205)
# range wide=10, wide2=50, wide3=50

# yellow
yellow = (35, 156, 222)
# range wide=10, wide2=50, wide3=50

# green
green = (61, 178, 206)
green = (61, 144, 206)
# range wide=10, wide2=50, wide3=50

# white
white = (17, 0, 203)
white = (96, 0, 203)
# range wide=10, wide2=50, wide3=50

# red
red = (173, 125, 228)
# range wide=10, wide2=50, wide3=50

updateBars(white)
wide = 10
wide2 = 50
wide3 = 30
while True:
    mask = cv2.inRange(img, (h-wide, s-wide2, v-wide3), (h+wide, s+wide2, v+wide3))
    target = cv2.bitwise_and(img,img, mask=mask)

    cv2.imshow('image',target)
    h = cv2.getTrackbarPos('H','image')
    s = cv2.getTrackbarPos('S','image')
    v = cv2.getTrackbarPos('V','image')

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

print("hsv", h, s, v)
cv2.destroyAllWindows()
