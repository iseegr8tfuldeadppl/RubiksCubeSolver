import numpy as np
import cv2
from colors import colors, day_colors
def nothing(x):
    pass

img = cv2.imread("samples/1.jpg")

img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


cv2.namedWindow('image')
cv2.namedWindow('imge')
cv2.createTrackbar('min H','image',0,180,nothing)
cv2.createTrackbar('min S','image',0,255,nothing)
cv2.createTrackbar('min V','image',0,255,nothing)
cv2.createTrackbar('max H','imge',0,180,nothing)
cv2.createTrackbar('max S','imge',0,255,nothing)
cv2.createTrackbar('max V','imge',0,255,nothing)

h, s, v = (0, 0, 0)
def updateBars(low, high):
    h, s, v = low
    cv2.setTrackbarPos('min H','image', h)
    cv2.setTrackbarPos('min S','image', s)
    cv2.setTrackbarPos('min V','image', v)
    h, s, v = high
    cv2.setTrackbarPos('max H','imge', h)
    cv2.setTrackbarPos('max S','imge', s)
    cv2.setTrackbarPos('max V','imge', v)

color = day_colors["white"]["ranges"][0]
low = color["min"]
high = color["max"]

updateBars(low, high)

def mouseRGB(event,x,y,flags,param):
    global img
    global low, high
    h = img[y,x,0]
    s = img[y,x,1]
    v = img[y,x,2]
    h = int(h*180/255)
    s = int(s)
    v = int(v)
    if event == cv2.EVENT_LBUTTONDOWN:
        print("adding hsv here", h, s, v)

        new_min = list(low)
        if h<low[0]:
            new_min[0] = h
        if s<low[1]:
            new_min[1] = s
        if v<low[2]:
            new_min[2] = v

        low = tuple(new_min)

        new_max = list(high)
        if h>high[0]:
            new_max[0] = h
        if s>high[1]:
            new_max[1] = s
        if v>high[2]:
            new_max[2] = v

        high = tuple(new_max)

        updateBars(low, high)

import numpy as np

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

#cap = cv2.VideoCapture(1)
cap = cv2.VideoCapture("http://192.168.1.57:8080/video")
while True:
    ret, img = cap.read()
    img = rotate_image(img, -90)
    cv2.imshow('imge',img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(img, low, high)
    target = cv2.bitwise_and(img,img, mask=mask)

    cv2.imshow('image',mask)
    #cv2.imshow('img',img)
    cv2.setMouseCallback('imge',mouseRGB)
    low = (cv2.getTrackbarPos('min H','image'), cv2.getTrackbarPos('min S','image'), cv2.getTrackbarPos('min V','image'))
    high = (cv2.getTrackbarPos('max H','imge'), cv2.getTrackbarPos('max S','imge'), cv2.getTrackbarPos('max V','imge'))

    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

print("min:", low, ",max:", high)
cv2.destroyAllWindows()
