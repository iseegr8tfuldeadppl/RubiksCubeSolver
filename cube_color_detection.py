import cv2
import sys
font = cv2.FONT_HERSHEY_COMPLEX
import time
from colors import colors
from colors import day_colors as colors
from drawerr import draw_cube
import numpy as np
from convert_pieces_to_kociemba import get_sol, correct_face

def rotate_image(image, angle):
  image_center = tuple(np.array(image.shape[1::-1]) / 2)
  rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
  result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
  return result

# time variables to add a delay between readings of cube faces initially only
delay = 1
previous_time = 0

# arrow variables for when instructing person to flip cube
arrow = 30
thiccness = 5
color = (0, 255, 0)
stroke_color = (0, 0, 255)
stroke_thiccness = 3
def draw_arrow(img, center, direction, reach):
    # deciding start/ending points
    # for straight line
    if direction=="up" or direction=="down":
        coef = 1 if direction=="up" else -1
        starting_point = (int(center[0]), int(center[1]+coef*reach))
        ending_point = (int(center[0]), int(center[1]-coef*reach))

        # arrows starting points
        arrow1_starting_point = (int(ending_point[0]-arrow), int(ending_point[1]+coef*arrow))
        arrow2_starting_point = (int(ending_point[0]+arrow), int(ending_point[1]+coef*arrow))

    if direction=="right" or direction=="left":
        coef = 1 if direction=="right" else -1
        starting_point = (int(center[0]-coef*reach), int(center[1]))
        ending_point = (int(center[0]+coef*reach), int(center[1]))

        # arrows starting points
        arrow1_starting_point = (int(ending_point[0]-coef*arrow), int(ending_point[1]-arrow))
        arrow2_starting_point = (int(ending_point[0]-coef*arrow), int(ending_point[1]+arrow))

    # stroke
    # straight line
    img = cv2.line(img, starting_point, ending_point, stroke_color, thiccness+stroke_thiccness)
    # wings
    img = cv2.line(img, arrow1_starting_point, ending_point, stroke_color, thiccness+stroke_thiccness)
    img = cv2.line(img, arrow2_starting_point, ending_point, stroke_color, thiccness+stroke_thiccness)

    # straight line
    img = cv2.line(img, starting_point, ending_point, color, thiccness)
    # wings
    img = cv2.line(img, arrow1_starting_point, ending_point, color, thiccness)
    img = cv2.line(img, arrow2_starting_point, ending_point, color, thiccness)

    return img


def draw_three_arrows(img, direction, center, half_piece_width, reach):
    side1_center = None
    side2_center = None
    if direction=="right" or direction=="left":
        side1_center = (center[0], center[1]-half_piece_width*2)
        side2_center = (center[0], center[1]+half_piece_width*2)
    elif direction=="up" or direction=="down":
        side1_center = (center[0]-half_piece_width*2, center[1])
        side2_center = (center[0]+half_piece_width*2, center[1])

    # center arrow
    img = draw_arrow(img, center, direction, reach)
    # side 1 arrow
    img = draw_arrow(img, side1_center, direction, reach)
    # side 2 arrow
    img = draw_arrow(img, side2_center, direction, reach)

    return img


def are_these_faces_oorientally_identical(face1, face2):
    return face1 == face2

def are_these_faces_identical(face1, face2):

    # check face upright
    if face1 == face2:
        return True

    # check face upside down
    upside_down_face = [face2[8], face2[7], face2[6],
                        face2[5], face2[4], face2[3],
                        face2[2], face2[1], face2[0]]

    if face1 == upside_down_face:
        return True

    # check face sleeping on its right
    sleeping_on_right_face = [face2[6], face2[3], face2[0],
                            face2[7], face2[4], face2[1],
                            face2[8], face2[5], face2[2]]

    if face1 == sleeping_on_right_face:
        return True

    # check face sleeping on its left
    sleeping_on_left_face = [face2[2], face2[5], face2[8],
                            face2[1], face2[4], face2[7],
                            face2[0], face2[3], face2[6]]

    if face1 == sleeping_on_left_face:
        return True

    return False


cv2.namedWindow('img_org')
cap = cv2.VideoCapture("http://192.168.1.57:8080/video")
#cap = cv2.VideoCapture(1)

img_org = None
img = None

def mouseRGB(event,x,y,flags,param):
    global img
    h = img[y,x,0]
    s = img[y,x,1]
    v = img[y,x,2]
    if event == cv2.EVENT_RBUTTONDOWN:
        print("hsv here", h, s, v)

cv2.setMouseCallback('img_org',mouseRGB)
previous_detection = {
    "colors of pieces": None,
    "centers": None,
    "entire cube state": [],
    "x half piece width": None,
    "y half piece width": None
}
previous_print = ""
recurrences = 0
confident_reccurance_count = 15

pieces = [
    ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
    ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
    ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
    ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
    ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
    ["white", "white", "white", "white", "white", "white", "white", "white", "white"]
]

# pieces = [
#     ["orange", "blue", "green", "yellow", "orange", "orange", "orange", "green", "orange"], #left
#     ["white", "red", "red", "yellow", "green", "orange", "blue", "yellow", "red"], #front
#     ["blue", "red", "green", "green", "red", "white", "blue", "red", "red"], #right
#     ["red", "blue", "yellow", "blue", "blue", "green", "yellow", "white", "yellow"], #back
#     ["white", "white", "orange", "green", "white", "orange", "white", "yellow", "blue"], # up # needs to be flipped
#     ["green", "orange", "green", "blue", "yellow", "white", "yellow", "red", "white"] # down # needs to be flipped
# ]

l = (15, 15)

while True:
    # Capture frame-by-frame
    ret, imgo = cap.read()
    imgo = rotate_image(imgo, -90)
    img_org = imgo.copy()

    #img_org = cv2.imread(sys.argv[1])
    img = cv2.cvtColor(img_org, cv2.COLOR_BGR2HSV)

    # detect contours of pieces
    samples = []
    for name, value in colors.items():
        for each_range in value["ranges"]:
            mask = cv2.inRange(img, each_range["min"], each_range["max"])

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

    # if we actually detected big enough colors
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

        # find centers of pieces to check which contours of colors occupy that center
        half_piece_width = abs(bottomright_corner["x"] - topleft_corner["x"]) / 6
        half_piece_height = abs(topleft_corner["y"] - bottomright_corner["y"]) / 6

        # if cube is way too small nahhhh, and if it's not square ish nahhhh
        ratio = half_piece_width/half_piece_height if half_piece_height != 0 else 0
        #print("ratio", ratio, "half_piece_width", half_piece_width, "half_piece_height", half_piece_height)
        minimum_distance_between_centers = 35
        if half_piece_width<minimum_distance_between_centers or half_piece_height<minimum_distance_between_centers or ratio > 1.2 or ratio < 0.8:
            # print an unpainted image since nothing promising was detected
            cv2.imshow('img_org',imgo)
        else:

            # calculate the proper position for centers
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

                    # does this center reside within this color's detected contour?
                    is_in_contour = cv2.pointPolygonTest(sample["contour"], (center["x"], center["y"]), True)
                    if is_in_contour>0:
                        center.update({"color": sample["color"]})

            # this will catch an error if the cube is diagonal way too much
            try:
                face_has_changed = False
                current_detection_colors = [center["color"] for center in centers]
                if current_detection_colors == previous_detection["colors of pieces"]:
                    recurrences += 1
                    if recurrences >= confident_reccurance_count:
                        # if cube colors have occured five times in a row then they're correct
                        colors_print = "centers " + str(current_detection_colors)
                        if previous_print != colors_print:
                            print(colors_print)
                            previous_print = colors_print
                            face_has_changed = True
                        recurrences = 0

                else:
                    recurrences = 0
                    previous_detection["centers"] = centers.copy()
                    previous_detection["colors of pieces"] = current_detection_colors.copy()
                    previous_detection["x half piece width"] = half_piece_width
                    previous_detection["y half piece width"] = half_piece_height


                if face_has_changed:

                    # check if face has alrdy been read
                    face_already_read = False
                    for face in previous_detection["entire cube state"]:
                        if are_these_faces_identical(face, previous_detection["colors of pieces"]):
                            face_already_read = True
                            break

                    # when registering faces, use a delay to give the user time to flip the cube without misreading the faces
                    # current_time = time.time()
                    # if current_time > previous_time + delay:
                    #     # save current time for next check
                    #     previous_time = current_time
                    #     # append current face if all gucci
                    if not face_already_read:
                        previous_detection["entire cube state"].append(previous_detection["colors of pieces"])

                    # print the proposed solution to the current face
                    faces_registered = len(previous_detection["entire cube state"])
                    if faces_registered < 6:

                        if faces_registered <= 3:
                            # draw three arrows facing to the right
                            # first determine the reach
                            extra_arrow_overshoot = 0.5 * half_piece_width
                            reach = half_piece_width*2 + extra_arrow_overshoot

                            img_org = draw_three_arrows(img_org, "right", (centers[4]["x"], centers[4]["y"]), half_piece_width, reach)
                        if faces_registered == 4:
                            img_org = draw_three_arrows(img_org, "up", (centers[4]["x"], centers[4]["y"]), half_piece_width, reach)
                        if faces_registered == 5:
                            img_org = draw_three_arrows(img_org, "down", (centers[4]["x"], centers[4]["y"]), half_piece_width, reach)

                    else:
                        #print("faces_registered", len(previous_detection["entire cube state"]), "are", "\n\n\n\n", previous_detection["entire cube state"])
                        print("broo")
                        try:
                            # prepare dummy cube
                            previous_detection["entire cube state"][4] = correct_face(previous_detection["entire cube state"][4], clockwise=True).copy() #fix U
                            previous_detection["entire cube state"][5] = correct_face(previous_detection["entire cube state"][5], clockwise=False).copy() #fix D
                            print("done", get_sol(previous_detection["entire cube state"]))
                        except Exception as e:
                            print("err", e)
                        print("done")
                        break
            except Exception as e:
                pass
                #print("error", e)

            # display image as preview
            cv2.imshow('img_org',img_org)
    else:

        # draw dummy cube
        imgo = draw_cube(imgo, left=pieces[0], front=pieces[1], right=pieces[2], back=pieces[3], up=pieces[4], down=pieces[5], location=l)

        # if previous_print != "no cube detected":
        #     print("no cube detected")
        #     previous_print = "no cube detected"
        # print an unpainted image since nothing promising was detected
        cv2.imshow('img_org',imgo)


    # check  for exits
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
