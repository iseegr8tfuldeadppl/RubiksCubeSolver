import cv2

cap = cv2.VideoCapture(1)


reach = 150
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
        starting_point = (center[0], center[1]+coef*reach)
        ending_point = (center[0], center[1]-coef*reach)

        # arrows starting points
        arrow1_starting_point = (ending_point[0]-arrow, ending_point[1]+coef*arrow)
        arrow2_starting_point = (ending_point[0]+arrow, ending_point[1]+coef*arrow)

    if direction=="right" or direction=="left":
        coef = 1 if direction=="right" else -1
        starting_point = (center[0]-coef*reach, center[1])
        ending_point = (center[0]+coef*reach, center[1])

        # arrows starting points
        arrow1_starting_point = (ending_point[0]-coef*arrow, ending_point[1]-arrow)
        arrow2_starting_point = (ending_point[0]-coef*arrow, ending_point[1]+arrow)

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

coords = (320, 240)
while True:
    # Capture frame-by-frame
    ret, img = cap.read()

    img = draw_arrow(img, coords, "down", reach)

    cv2.imshow('img',img)

    # check  for exits
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
