import cv2
import numpy as np
import colorsys
font = cv2.FONT_HERSHEY_COMPLEX

def nothing(x):
    pass
cap = cv2.VideoCapture(1)

cv2.namedWindow('image')
cv2.createTrackbar('low','image',0,1000,nothing)
cv2.createTrackbar('high','image',0,1000,nothing)
cv2.setTrackbarPos('low','image', 60)
cv2.setTrackbarPos('high','image', 200)

img_org = None
# set this smallest var to [0, 0, 0] when checking for the highest hsv values for a certain color, and then just run the code and keep clicking allaround that color
# also change akbar and asghar > and < inside mouseRGB
highest = True
extreme = [0, 0, 0]
if not highest:
    extreme = [1000, 1000, 1000]

def mouseRGB(event,x,y,flags,param):
    global img_org
    global extreme
    if event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition
        h = img_org[y,x,0]
        s = img_org[y,x,1]
        v = img_org[y,x,2]

        if highest:
            extreme[0] = h if h > extreme[0] else extreme[0]
            extreme[1] = s if s > extreme[1] else extreme[1]
            extreme[2] = v if v > extreme[2] else extreme[2]
        else:
            extreme[0] = h if h < extreme[0] else extreme[0]
            extreme[1] = s if s < extreme[1] else extreme[1]
            extreme[2] = v if v < extreme[2] else extreme[2]

        print("clicked", h, s, v)
        print("current extreme", extreme)

cv2.setMouseCallback('image',mouseRGB)

method = cv2.TM_SQDIFF_NORMED
while True:
    low = cv2.getTrackbarPos('low','image')
    high = cv2.getTrackbarPos('high','image')

    # Capture frame-by-frame
    ret, img = cap.read()
    img_org = img.copy()
    img_org = cv2.cvtColor(img_org, cv2.COLOR_BGR2HSV)

    cv2.imshow('image',img_org)
    cv2.imshow('img',img)

    # check  for exits
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
