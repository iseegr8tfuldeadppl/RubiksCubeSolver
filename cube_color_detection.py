import cv2
import sys
font = cv2.FONT_HERSHEY_COMPLEX

cv2.namedWindow('img_org')
cap = cv2.VideoCapture(1)

img_org = None
img = None

colors = {
    "red":{
        "representation": (255, 0, 0),
        "ranges": [{"low":(0, 180, 150), "high": (3, 255, 255)}, {"low":(165, 65, 70), "high": (185, 255, 255)}]
    },
    "blue":{
        "representation": (0, 0, 255),
        "ranges": [{"low":(70, 85, 80), "high": (120, 255, 255)}] # other suggestion {"low":(110, 150, 50), "high": (120, 255, 255)}
    },
    "green":{
        "representation": (0, 255, 0),
        "ranges": [{"low":(44, 120, 72), "high": (80, 255, 255)}]
    },
    "yellow":{
        "representation": (255, 255, 0),
        "ranges": [{"low":(25, 150, 160), "high": (40, 255, 255)}]
    },
    "white":{
        "representation": (255, 255, 255),
        "ranges": [{"low":(0, 0, 140), "high": (90, 106, 249)}]
    },
    "orange":{
        "representation": (255, 165, 0),
        "ranges": [{"low":(5, 80, 170), "high": (21, 255, 255)}]
    }
}
# color = "blue"
# previous_low = colors[color]["ranges"][0]["low"]
# previous_high = colors[color]["ranges"][0]["high"]

def mouseRGB(event,x,y,flags,param):
    global img
    global colors
    global previous_low
    global previous_high
    h = img[y,x,0]
    s = img[y,x,1]
    v = img[y,x,2]
    if event == cv2.EVENT_RBUTTONDOWN:
        print("hsv here", h, s, v)
    elif event == cv2.EVENT_LBUTTONDOWN: #checks mouse left button down condition

        low = list(colors[color]["ranges"][0]["low"])
        high = list(colors[color]["ranges"][0]["high"])
        if h < low[0]:
            low[0] = h
        if s < low[1]:
            low[1] = s
        if v < low[2]:
            low[2] = v

        if h > high[0]:
            high[0] = h
        if s > high[1]:
            high[1] = s
        if v > high[2]:
            high[2] = v

        colors[color]["ranges"][0]["low"] = tuple(low)
        colors[color]["ranges"][0]["high"] = tuple(high)

        #print("color", color, "lowest", colors[color]["ranges"][0]["low"], "highest", colors[color]["ranges"][0]["high"])

cv2.setMouseCallback('img_org',mouseRGB)

while True:
    # Capture frame-by-frame
    ret, img_org = cap.read()
    #img_org = cv2.imread(sys.argv[1])
    img = cv2.cvtColor(img_org, cv2.COLOR_BGR2HSV)

    # detect contours of pieces
    samples = []
    for name, value in colors.items():
        for each_range in value["ranges"]:
            mask = cv2.inRange(img, each_range["low"], each_range["high"])

            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            # close = cv2.morphologyEx(target, cv2.MORPH_CLOSE, kernel, iterations=1)

            # target = cv2.cvtColor(target, cv2.COLOR_HSV2RGB)
            # gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)

            cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                area = cv2.contourArea(c)
                x,y,w,h = cv2.boundingRect(c)
                # if area>1000 and area<3000:
                #     approx = cv2.approxPolyDP(c, 0.01* cv2.arcLength(c, True), True)
                #     print("area", area, "approx", len(approx))
                if area>3000:
                    # print("approx", len(approx), "area", area)
                    # cv2.rectangle(img_org, (x, y), (x + w, y + h), (255,255,255), 2)
                    cv2.drawContours(img_org, [c], -1, (0, 0, 0), 2)
                    cv2.putText(img_org, name, (x+20, y+20), font, 0.75, (255, 255, 255))

                    samples.append({
                        "area": area,
                        "width": w,
                        "height": h,
                        "x": x,
                        "y": y,
                        "color": name,
                        "contour": c
                    })

    if len(samples)>0:
        # find top left corner of cube face
        topleft_piece = samples[0].copy()
        for sample in samples:
            if sample["x"] < topleft_piece["x"]:
                topleft_piece = sample.copy()
        for sample in samples:
            y_difference = sample["y"] - topleft_piece["y"]
            x_difference = sample["x"] - topleft_piece["x"]
            if y_difference<0:
                x_difference = abs(x_difference)
                ratio = abs(y_difference)/x_difference if x_difference!=0 else 1.0
                if x_difference==0 or (0<ratio and ratio>1.5):
                    topleft_piece = sample.copy()

        # find bottom right corner of cube face
        bottomright_piece = samples[0].copy()
        for sample in samples:
            if sample["x"]+sample["width"] > bottomright_piece["x"]+bottomright_piece["width"]:
                bottomright_piece = sample.copy()
        for sample in samples:
            y_difference = sample["y"]+sample["height"] - (bottomright_piece["y"]+bottomright_piece["height"])
            x_difference = sample["x"]+sample["width"] - (bottomright_piece["x"]+bottomright_piece["width"])
            if y_difference>0:
                x_difference = abs(x_difference)
                ratio = abs(y_difference)/x_difference if x_difference!=0 else 1.0
                if x_difference==0 or (0<ratio and ratio>1.5):
                    bottomright_piece = sample.copy()

        topleft_corner = {"x":topleft_piece["x"], "y":topleft_piece["y"]}
        bottomright_corner = {"x":bottomright_piece["x"]+bottomright_piece["width"], "y": bottomright_piece["y"]+bottomright_piece["height"]}

        # find centers of pieces to check colors at them
        half_piece_width = abs(bottomright_corner["x"] - topleft_corner["x"]) / 6
        half_piece_height = abs(topleft_corner["y"] - bottomright_corner["y"]) / 6

        centers = []
        for y in range(1, 7, 2):
            for x in range(1, 7, 2):
                centers.append({
                    "x": int(topleft_corner["x"]+x*half_piece_width),
                    "y": int(topleft_corner["y"]+y*half_piece_height)
                })

        # determine the color for each center
        for center in centers:
            cv2.rectangle(img_org, (center["x"], center["y"]), (center["x"]+5, center["y"]+5), (255,255,255), 2)
            for sample in samples:
                is_in_contour = cv2.pointPolygonTest(sample["contour"], (center["x"], center["y"]), True)
                if is_in_contour>0:
                    center.update({"color": sample["color"]})

        # this will crash if the cube is rotated way too much
        try:
            print("centers", [center["color"] for center in centers])
        except:
            print("please don't hold the cube diagonally")
    # else:
        # print("no cube detected")

    # display image as preview
    cv2.imshow('img_org',img_org)

    # check  for exits
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
