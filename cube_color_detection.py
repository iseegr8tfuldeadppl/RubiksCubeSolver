import cv2
import sys
font = cv2.FONT_HERSHEY_COMPLEX

print("you must enter the picture path as an argument")
img_org = cv2.imread(sys.argv[1])
img = cv2.cvtColor(img_org, cv2.COLOR_BGR2HSV)

h_reach=10
s_reach=50
v_reach=50

colors = {
    "red":{
        "representation": (255, 0, 0),
        "low": (173-h_reach, 125-s_reach, 228-v_reach),
        "high": (173+h_reach, 125+s_reach, 228+v_reach)
    },
    "blue":{
        "representation": (0, 0, 255),
        "low": (99-h_reach, 209-s_reach, 205-v_reach),
        "high": (99+h_reach, 209+s_reach, 205+v_reach)
    },
    "green":{
        "representation": (0, 255, 0),
        "low": (61-h_reach, 144-s_reach, 206-v_reach),
        "high":  (61+h_reach, 178+s_reach, 206+v_reach)
    },
    "yellow":{
        "representation": (255, 255, 0),
        "low": (35-h_reach, 156-s_reach, 222-v_reach),
        "high": (35+h_reach, 156+s_reach, 222+v_reach)
    },
    "white":{
        "representation": (255, 255, 255),
        "low": (17-h_reach, 0-s_reach, 227-v_reach),
        "high": (88+h_reach, 0+s_reach, 227+v_reach)
    },
    "orange":{
        "representation": (255, 165, 0),
        "low": (7-h_reach, 173-s_reach, 255-v_reach),
        "high": (7+h_reach, 173+s_reach, 255+v_reach)
    }
}

# remove anything outside limits
for _, color in colors.items():
    low_high_lists = [list(color["low"]), list(color["high"])]

    for each in low_high_lists:
        if each[0]<0:
            each[0] = 0
        elif each[0]>180:
            each[0] = 180

        if each[1]<0:
            each[1] = 0
        elif each[1]>255:
            each[1] = 255

        if each[2]<0:
            each[2] = 0
        elif each[2]>255:
            each[2] = 255

        color["low"] = tuple(low_high_lists[0])
        color["high"] = tuple(low_high_lists[1])

samples = []
for name, value in colors.items():
    mask = cv2.inRange(img, value["low"], value["high"])

    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    # close = cv2.morphologyEx(target, cv2.MORPH_CLOSE, kernel, iterations=1)

    # target = cv2.cvtColor(target, cv2.COLOR_HSV2RGB)
    # gray = cv2.cvtColor(target, cv2.COLOR_RGB2GRAY)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    for c in cnts:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        if area>1000:
            # cv2.rectangle(img_org, (x, y), (x + w, y + h), (255,255,255), 2)
            cv2.drawContours(img_org, [c], -1, (0,255,0), 3)
            cv2.putText(img_org, name, (x, y+10), font, 0.45, (0, 0, 0))

            samples.append({
                "area": area,
                "width": w,
                "height": h,
                "x": x,
                "y": y,
                "color": name,
                "contour": c
            })


# find top left corner of cube face
topleft_piece = samples[0].copy()

for sample in samples:
    if sample["x"] < topleft_piece["x"]:
        topleft_piece = sample.copy()

for sample in samples:
    y_difference = sample["y"] - topleft_piece["y"]
    x_difference = sample["x"] - topleft_piece["x"]
    if y_difference<0:
        if x_difference==0 or y_difference==0 or abs(y_difference)/abs(x_difference)>1.5:
            topleft_piece = sample.copy()


# find bottom right corner of cube face
bottomright_piece = samples[0].copy()

for sample in samples:
    if sample["x"]+sample["width"] > bottomright_piece["x"]+bottomright_piece["width"]:
        bottomright_piece = sample.copy()

for sample in samples:
    y_difference = sample["y"]+sample["height"] - (bottomright_piece["y"]+bottomright_piece["height"])
    x_difference = sample["x"]+sample["width"] - (bottomright_piece["x"]+bottomright_piece["width"])
    if y_difference>0 and abs(y_difference)/abs(x_difference)>1.5:
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

cv2.imshow('img_org',img_org)
cv2.waitKey()
