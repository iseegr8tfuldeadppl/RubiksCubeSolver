import cv2
import numpy as np
import pickle

colors_filename = "colors.pickle"
width = 1000
height = 30
bar_width = 15
font_size = 1.0
scheme_maxes = [180, 255, 255]
colors = []


try:
    with open(colors_filename, "rb") as f:
        colors = pickle.load(f)
except:
    from colors import colors as temp
    colors = temp


selected_color_index = -1
selected_range_index = -1
selected_min_or_max = None
previous_x = None
a_bar_is_held = False
selected_scheme = None
def bar_movement(event, x, y, flags, param):
    global selected_color_index, selected_range_index, selected_min_or_max, previous_x, a_bar_is_held, colors, selected_scheme

    if event==cv2.EVENT_LBUTTONDOWN:
        for scheme in range(0, 3):
            for color_index in range(0, len(contours[scheme])):
                for range_index in range(0, len(contours[scheme][color_index]["ranges"])):
                    max_result = cv2.pointPolygonTest(contours[scheme][color_index]["ranges"][range_index]["min"], (x,y), False) 
                    min_result = cv2.pointPolygonTest(contours[scheme][color_index]["ranges"][range_index]["max"], (x,y), False) 
                    if max_result>=0: # click is on the line of the contour or inside it
                        print("color", colors[color_index]["name"], "overlaps with mouse", "at scheme", scheme)
                        previous_x = x
                        selected_scheme = scheme
                        selected_color_index = color_index
                        selected_range_index = range_index
                        selected_min_or_max = "min"
                        a_bar_is_held = True
                        break
                    
                    if min_result>=0: # click is on the line of the contour or inside it
                        print("color", colors[color_index]["name"], "overlaps with mouse", "at scheme", scheme)
                        previous_x = x
                        selected_scheme = scheme
                        selected_color_index = color_index
                        selected_range_index = range_index
                        selected_min_or_max = "max"
                        a_bar_is_held = True
                        break
                if a_bar_is_held:
                    break
                    
    elif event==cv2.EVENT_MOUSEMOVE:
        if a_bar_is_held:
            previous_color_tuple = list(colors[selected_color_index]["ranges"][selected_range_index][selected_min_or_max])
            new_h_value = previous_color_tuple[selected_scheme] + (x - previous_x) * scheme_maxes[selected_scheme] / (width-bar_width)
            if new_h_value > scheme_maxes[selected_scheme]:
                new_h_value = scheme_maxes[selected_scheme]
            elif new_h_value < 0:
                new_h_value = 0
            previous_color_tuple[selected_scheme] = new_h_value
            colors[selected_color_index]["ranges"][selected_range_index][selected_min_or_max] = tuple(previous_color_tuple)
            previous_x = x

    elif event==cv2.EVENT_LBUTTONUP:
        a_bar_is_held = False

        with open(colors_filename, "wb") as f:
            pickle.dump(colors, f)

def draw_text(img, text, font=cv2.FONT_HERSHEY_PLAIN, pos=(0, 0), font_scale=3, font_thickness=2, text_color=(255, 255, 255), text_color_bg=(0, 0, 0)):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, (int(x-text_w/2), int(y-text_h/2)), (int(x + text_w/2), int(y + text_h/2)), text_color_bg, -1)
    cv2.putText(img, text, (int(x-text_w/2), int(y + text_h/2 + font_scale - 1)), font, font_scale, text_color, font_thickness)

    return text_size

while True:
    window = np.zeros((height*6*3, width, 3), dtype=np.uint8)
    contours = [[], [], []]
    for scheme in range(0, 3):
        color_index = -1

        for data in colors:
            color_index += 1
            for i in range(0, len(data["ranges"])):
                x = int( (width - bar_width) * data["ranges"][i]["min"][scheme] / scheme_maxes[scheme] )

                box_h = color_index*height + scheme*height*6
                min_contour = np.array([(x, box_h), (x+bar_width, box_h), (x + bar_width, box_h + height), (x, box_h+height)])

                window = cv2.rectangle(window, (x, box_h), (x + bar_width, box_h + height), data["representation"], -1)
                text_size = draw_text(window, "m", font_scale=font_size, pos=(x, box_h), text_color_bg=(0, 0, 0))
                draw_text(window, str(i+1), font_scale=font_size, pos=(x, text_size[1] + box_h), text_color_bg=(0, 0, 0))
                
                x = int( (width - bar_width) * data["ranges"][i]["max"][scheme] / scheme_maxes[scheme] )

                max_contour = np.array([(x, box_h), (x+bar_width, box_h), (x + bar_width, box_h + height), (x, box_h+height)])

                if len(contours[scheme]) < color_index+1:
                    contours[scheme].append({"ranges": [] })

                contours[scheme][color_index]["ranges"].append({"min": min_contour, "max": max_contour})

                window = cv2.rectangle(window, (x, box_h), (x + bar_width, box_h + height), data["representation"], -1)
                text_size = draw_text(window, "M", font_scale=font_size, pos=(x, box_h), text_color_bg=(0, 0, 0))
                draw_text(window, str(i+1), font_scale=font_size, pos=(x, text_size[1] + box_h), text_color_bg=(0, 0, 0))
        
    cv2.imshow("H Selection bar", window)
    cv2.setMouseCallback("H Selection bar", bar_movement)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
# Destroy all the windows
cv2.destroyAllWindows()