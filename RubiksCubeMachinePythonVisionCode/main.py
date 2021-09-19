# import the opencv library
# pip install --user webcolors

import cv2
import pickle
import numpy as np
import time
import colorsys
import webcolors
from sklearn.cluster import KMeans
from collections import Counter
from threading import Thread

drawing = False # true if mouse is pressed
sets_of_points = []
flying_point = None
filename = "contours.pickle"
hsvs = []
'''
print("How to use:")
print("")
print("")
print("Left Click to start creating a contour\ndraw the points where ever you want")
print("  and then to close the contour Right Click and the code will automatically start")
print("  displaying its predicted color + its index in the contours array")
print("")
print("")
print("Right click on a contour to Enable or Disable reporting of the dominant colors inside it")
print("  that is being displayed inside the color ranges window (disignated by half height white boxes")
print("  drawn always on the red color bar)")
print("  (disabled contours are colored green and enabled contours are colored black)")
print("")
print("")
print("Right click away from all contours to start a reordering process where you can Left Click all of the")
print("  contours sequentially to put them in the order you want inside the contours array in order to code")
print("  relative to the array's indexes, once you have selected all of the contours right click again away from")
print("  any contour and the new order will be applied")
print("  (selected contours will be colored green during selection)")
print("")
print("")
print("The color range selection GUI is split vertically onto three parts, H and S and V and each line")
print("  contains the value for each of the six colors")
print("  each color has two knobs that you can drag left and right to adjust the limits (except for red ")
print("  it has four knobs in order to adjust two ranges because that seems to work better")
print("")
print("")
print("Everything is saved inside pickle files in the project directory")
'''


def reinit_color_occurencies():
    global color_occurencies_in_contours
    color_occurencies_in_contours = [ [0, 0, 0, 0, 0, 0] for i in range(0, len(sets_of_points))]

color_occurencies_in_contours = []
try:
    with open(filename, "rb") as f:
        sets_of_points = pickle.load(f)
        reinit_color_occurencies()
except:
    pass
colors_filename = "colors.pickle"
width = 1000
height = 30
bar_width = 15
font_size = 1.0
scheme_maxes = [180, 255, 255]
colors = []
contours = [[], [], []]


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
                        previous_x = x
                        selected_scheme = scheme
                        selected_color_index = color_index
                        selected_range_index = range_index
                        selected_min_or_max = "min"
                        a_bar_is_held = True
                        break
                    
                    if min_result>=0: # click is on the line of the contour or inside it
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

def treat_color_range_selector_gui():
    global contours, hsvs, exit
    while True:
        window = np.zeros((height*6*3, width, 3), dtype=np.uint8)
        contours = [[], [], []]
        for scheme in range(0, 3):
            color_index = -1

            # draw the actual detected colors here for reference
            for hsv in hsvs:
                x = int( (width - bar_width) * hsv[0] / 180 )
                window = cv2.rectangle(window, (x, int(height/2)), (x + bar_width, height), (255, 255, 255), -1)
                x = int( (width - bar_width) * hsv[1] / 255 )
                window = cv2.rectangle(window, (x, height*6+int(height/2)), (x + bar_width, height*6 + height), (255, 255, 255), -1)
                x = int( (width - bar_width) * hsv[2] / 255 )
                window = cv2.rectangle(window, (x, 2*height*6+int(height/2)), (x + bar_width, 2*height*6 + height), (255, 255, 255), -1)
                #hsvs.remove(hsv)

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
        
        # if we pressed exit stop
        if cv2.waitKey(1) & 0xFF == ord('q') or exit:
            exit = True
            return



def draw_text(img, text,
          font=cv2.FONT_HERSHEY_PLAIN,
          pos=(0, 0),
          font_scale=3,
          font_thickness=2,
          text_color=(255, 255, 255),
          text_color_bg=(0, 0, 0)
          ):

    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, (int(x-text_w/2), int(y-text_h/2)), (int(x + text_w/2), int(y + text_h/2)), text_color_bg, -1)
    cv2.putText(img, text, (int(x-text_w/2), int(y + text_h/2 + font_scale - 1)), font, font_scale, text_color, font_thickness)

    return text_size

def get_dominant_color(image, k=4, image_processing_size = None):
    """
    takes an image as input
    returns the dominant color of the image as a list
    
    dominant color is found by running k means on the 
    pixels & returning the centroid of the largest cluster

    processing time is sped up by working with a smaller image; 
    this resizing can be done with the image_processing_size param 
    which takes a tuple of image dims as input

    get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
    [56.2423442, 34.0834233, 70.1234123]
    """
    #resize image if new dims provided
    if image_processing_size is not None:
        image = cv2.resize(image, image_processing_size, 
                            interpolation = cv2.INTER_AREA)
    
    #reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    #cluster and assign labels to the pixels 
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(image)

    #count labels to find most popular
    label_counts = Counter(labels)

    #subset out most popular centroid
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    return clt.cluster_centers_ 


reordering = False
new_contours_order = []



# mouse callback function
def line_drawing(event, x, y, flags, param):
    global drawing, flying_point, sets_of_points, hsvs, reordering, new_contours_order

    if event==cv2.EVENT_LBUTTONDOWN:

        if reordering:
            for contour in sets_of_points:
                result = cv2.pointPolygonTest(contour["points"], (x,y), False) 
                if result>=0: # click is on the line of the contour or inside it
                    
                    its_in_new_contours_order = False
                    for z in range(0, len(new_contours_order)):
                        if str(new_contours_order[z]) == str(contour):
                            its_in_new_contours_order = True
                            break
                    if not its_in_new_contours_order:
                        new_contours_order.append(contour)
            return

        if not drawing:
            # if we're creating a new contour create one
            sets_of_points.append({"enabled":False, "points": []})
            drawing = True
        
        # add point to contour
        sets_of_points[len(sets_of_points)-1]["points"].append((x, y))

    elif event==cv2.EVENT_MBUTTONDOWN:
        if drawing: # cancel currently being drawn contour
            drawing = False
            sets_of_points.pop()
        else:
            # confirm if we're trying to delete a contour
            for contour in sets_of_points:
                result = cv2.pointPolygonTest(contour["points"], (x,y), False) 
                if result>=0: # click is on the line of the contour or inside it
                    for z in range(0, len(sets_of_points)):
                        if str(sets_of_points[z]) == str(contour):
                            sets_of_points.pop(z)
                            break

        with open(filename, "wb") as f:
            pickle.dump(sets_of_points, f)
            reinit_color_occurencies()

    elif event==cv2.EVENT_RBUTTONDOWN:
        if drawing: # if right click happened during drawing that means we need to close the contour
            drawing = False

            # if the contour does not have more than two points reject it
            if len(sets_of_points[len(sets_of_points)-1]["points"])<=2:
                sets_of_points.pop()
            else: # else accept it as a new contour
                sets_of_points[len(sets_of_points)-1]["enabled"] = True
                sets_of_points[len(sets_of_points)-1]["points"] = np.array(sets_of_points[len(sets_of_points)-1]["points"])
                x,y,w,h = cv2.boundingRect(sets_of_points[len(sets_of_points)-1]["points"])
                sets_of_points[len(sets_of_points)-1].update({"size_and_location": [x,y,w,h]})

        else: # if we are not drawing then check if we're trying to disable a contour by checking if we clicked one
            clicked_a_contour = False
            for contour in sets_of_points:
                result = cv2.pointPolygonTest(contour["points"], (x,y), False) 
                if result>=0: # click is on the line of the contour or inside it
                    contour["enabled"] = not contour["enabled"]
                    clicked_a_contour = True

                    # if we just disabled a contour we'll reset the colors in the colors gui since it appears we're about to move onto another color
                    if not contour["enabled"]:
                        hsvs = []

            if not clicked_a_contour:
                if not reordering:
                    print("Reordering of contours initiated")
                    # else if we didn't right click any contour then we're attempting to recorder contours
                    reordering = True
                    new_contours_order = []
                else:
                    print("Reordering of contours finished")
                    reordering = False
                    # start reordering contours IFFFF we selected any at all
                    if len(new_contours_order) == len(sets_of_points):
                        sets_of_points = new_contours_order.copy()
                        new_contours_order = []
                        with open(filename, "wb") as f:
                            pickle.dump(sets_of_points, f)
                            reinit_color_occurencies()
                    else:
                        print("You have not yet selected every contour")

        with open(filename, "wb") as f:
            pickle.dump(sets_of_points, f)
            reinit_color_occurencies()

    elif event==cv2.EVENT_MOUSEMOVE:
        if drawing==True:
            flying_point = (x, y)

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
    return actual_name, closest_name



def convert_hsv_to_rgb(hsv):
    #get rgb percentage: range (0-1, 0-1, 0-1 )
    hue_percentage= hsv[0] / float(180)
    saturation_percentage= hsv[1]/ float(255)
    value_percentage= hsv[2]/ float(255)
    
    #get hsv percentage: range (0-1, 0-1, 0-1)
    color_rgb_percentage=colorsys.hsv_to_rgb(hue_percentage, saturation_percentage, value_percentage) 
    
    #get normal hsv: range (0-360, 0-255, 0-255)
    color_r=round(255*color_rgb_percentage[0])
    color_g=round(255*color_rgb_percentage[1])
    color_b=round(255*color_rgb_percentage[2])
    color_rgb=(color_r, color_g, color_b)
    return color_rgb

def convert_rgb_to_hsv(rgb):
    #get rgb percentage: range (0-1, 0-1, 0-1 )
    red_percentage= rgb[0] / float(255)
    green_percentage= rgb[1]/ float(255)
    blue_percentage= rgb[2]/ float(255)

    
    #get hsv percentage: range (0-1, 0-1, 0-1)
    color_hsv_percentage=colorsys.rgb_to_hsv(red_percentage, green_percentage, blue_percentage) 
    
    #get normal hsv: range (0-360, 0-255, 0-255)
    color_h=round(180*color_hsv_percentage[0])
    color_s=round(255*color_hsv_percentage[1])
    color_v=round(255*color_hsv_percentage[2])
    color_hsv=(color_h, color_s, color_h)
    return color_hsv

def drawPoints(frame):
    for j in range(0, len(sets_of_points)):

        for i in range(0, len(sets_of_points[j]["points"])):
            if i+1==len(sets_of_points[j]["points"]):
                if j == len(sets_of_points)-1:
                    if drawing:
                        end_of_line = flying_point
                    else:
                        end_of_line = sets_of_points[j]["points"][0]
                else:
                    end_of_line = sets_of_points[j]["points"][0]
            else:
                end_of_line = sets_of_points[j]["points"][i+1]

            color_to_use = (0, 0, 0) if sets_of_points[j]["enabled"] else (0, 0, 255)
            its_in_new_contours_order = False
            for z in range(0, len(new_contours_order)):
                if str(new_contours_order[z]) == str(sets_of_points[j]):
                    its_in_new_contours_order = True
                    break
            color_to_use = (0, 255, 0) if its_in_new_contours_order else color_to_use
            frame = cv2.line(frame, sets_of_points[j]["points"][i], end_of_line, color=color_to_use, thickness=3)
    return frame

cube = {
    "F": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "B": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "L": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "R": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "U": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "D": [-1, -1, -1, -1, -1, -1, -1, -1, -1]
}
ready_contours = []
def treat_contour(contour, i):
    global color_occurencies_in_contours, ready_contours

    # create a mask of the contour to blackout any colors surounding it
    mask = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.uint8)
    cv2.fillPoly(mask, pts =[contour["points"]], color=(255,255,255))
    res = cv2.bitwise_and(frame, frame, mask = mask)

    # crop the image down to the contour only to prevent too much calculation and less black in the image
    x,y,w,h = contour["size_and_location"]
    ROI = res[y:y+h, x:x+w]

    # Display the resulting frame
    #a = np.ones((50, 50, 3), dtype=np.uint8)
    max_colors = 4
    start = time.time()
    cds = get_dominant_color(ROI, k=max_colors, image_processing_size=(25, 25)) # (25, 25) worked
    #print("done within", (time.time()-start), "seconds")

    #colorsss = np.zeros((200, 50*max_colors, 3), dtype=np.uint8)
    color_occurencies = [0, 0, 0, 0, 0, 0] # all six colors
    max_colors_used = 2
    for j in range(0, max_colors_used):
        rgb = tuple(cds[j])

        predicted_color = get_colour_name(rgb)
        if predicted_color=="black":
            max_colors_used += 1
            if max_colors_used > max_colors:
                max_colors_used = max_colors
            continue

        hsv = convert_rgb_to_hsv(rgb)
        if contour["enabled"]: # only show colors of enabled contours inside the colors gui
            hsvs.append(hsv)

        # Dominant colors display, ranked left to right
        for data in colors:
            for each_range in data["ranges"]:
                if hsv[0] >= each_range["min"][0] and hsv[1] >= each_range["min"][1] and hsv[2] >= each_range["min"][2] \
                    and hsv[0] <= each_range["max"][0] and hsv[1] <= each_range["max"][1] and hsv[2] <= each_range["max"][2]:
                    if data["name"] == "yellow":
                        color_occurencies[0] += 1
                    elif data["name"] == "blue":
                        color_occurencies[1] += 1
                    elif data["name"] == "green":
                        color_occurencies[2] += 1
                    elif data["name"] == "orange":
                        color_occurencies[3] += 1
                    elif data["name"] == "red":
                        color_occurencies[4] += 1
                    elif data["name"] == "white":
                        color_occurencies[5] += 1
                
        #colorsss = cv2.rectangle(colorsss, (i*50, 0), ((i+1)*50, 200), tuple(cds[i]), -1)

    # write the name of the most occurent color in this contour
    most_occurences = max(color_occurencies)
    if most_occurences>0: # if one of the colors showed up at least
        most_occurent_color = color_occurencies.index(most_occurences)

        # add this occurency to the array now
        color_occurencies_in_contours[i][most_occurent_color] += 1


    ready_contours.append(i)

step = 0
coloz = ["Yellow", "Blue", "Green", "Orange", "Red", "White"]
def treat_predictions(predictions):
    global step, cube

    if step<0:
        return

    print("predictions", [coloz[i] for i in predictions])

    if step==0:
        print("Read first face")
        print("Predictions", len(predictions), predictions)
        
        if len(predictions) == 27:
            for i in range(0, 9):
                cube["U"][i] = predictions[i]
            for i in range(9, 18):
                cube["B"][i-9] = predictions[i]
            for i in range(18, 27):
                cube["L"][i-18] = predictions[i]

        step += 1
    elif step==1:
        print("Read second face")
        step += 1
    elif step==2:
        print("Read third face")
        step += 1
    elif step==3:
        step = -1
        print("Finished reading faces")

how_many_captures_should_we_take_to_average = 1
frame = None
def treat_footage():
    global vid, hsvs, exit, frame, ready_contours
    called = False
    recordings = 0
    texts_to_draw = []
    predictions = [-1 for i in range(0, len(sets_of_points))]
    start_time2 = time.time()
    start_time = time.time()
    ready_contours = []
    while True:
        finished_a_reading = False
        
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
        #frame = cv2.imread("yes.png")

        if time.time() - start_time2 > 12:

            # if color occurencies array wasn't updated yet then update it
            if len(color_occurencies_in_contours) < len(sets_of_points):
                reinit_color_occurencies()

            if not called:
                called = True
                for i in range(0, len(sets_of_points)):
                    
                    # ignore any currently being made contour
                    if i == len(sets_of_points) - 1:
                        if drawing:
                            continue # skip the rest because it's not a complete contour

                    Thread(target = treat_contour, args=[sets_of_points[i], i]).start()
                    #treat_contour(sets_of_points[i], i)

            # if all contours have been checked then update the recordings
            if len(ready_contours)==len(sets_of_points):
                ready_contours = []
                recordings += 1
                called = False
                
            # once we've made the amount of repetitions we want we'll display shit
            if recordings >= how_many_captures_should_we_take_to_average:
                finished_a_reading = True
                recordings = 0
                texts_to_draw = []
                temp_color_occurencies_in_contours = color_occurencies_in_contours.copy() # to avoid the next iteration modifying it
                for i in range(0, len(temp_color_occurencies_in_contours)):
                    most_occurent_color_text = None
                    most_occurent_color_val = max(temp_color_occurencies_in_contours[i])
                    if most_occurent_color_val>0:
                        most_occurent_color_index = temp_color_occurencies_in_contours[i].index(most_occurent_color_val)
                        if most_occurent_color_index==0:
                            most_occurent_color_text = "Yellow"
                        elif most_occurent_color_index==1:
                            most_occurent_color_text = "Blue"
                        elif most_occurent_color_index==2:
                            most_occurent_color_text = "Green"
                        elif most_occurent_color_index==3:
                            most_occurent_color_text = "Orange"
                        elif most_occurent_color_index==4:
                            most_occurent_color_text = "Red"
                        elif most_occurent_color_index==5:
                            most_occurent_color_text = "White"

                        x,y,w,h = sets_of_points[i]["size_and_location"]
                        texts_to_draw.append({
                            "text": str(i+1) + " " + most_occurent_color_text,
                            "pos": (x+w/2, y+h/2)
                        })
                    predictions[i] = most_occurent_color_index if most_occurent_color_val>0 else -1

                # display how much time it took
                now = time.time()
                #print("recognition of", how_many_captures_should_we_take_to_average, "iteration" + ("s" if how_many_captures_should_we_take_to_average>1 else ""), "took", (now - start_time), "seconds")
                start_time = now

                #cv2.imshow('colors', colorsss)

            frame = drawPoints(frame)
            
            # just write the time in top left corner to see if we didn't freeze
            draw_text(frame, str(int(time.time())), font_scale=2, pos=(15, 15), text_color_bg=(0, 0, 0))

            # color segmentation texts for each contour along with their order number
            for text in texts_to_draw:
                draw_text(frame, text["text"], font_scale=1, pos=text["pos"], text_color_bg=(0, 0, 0))

        cv2.imshow('frame', frame)
        cv2.setMouseCallback('frame', line_drawing)

        # if we pressed exit stop
        if cv2.waitKey(1) & 0xFF == ord('q') or exit:
            exit = True
            return

            
        # do whatever we want with our predictions stored inside
        if finished_a_reading:
            treat_predictions(predictions)

vid = None
exit = False
def main():
    global vid, exit
    # define a video capture object
    vid = cv2.VideoCapture(0)

    Thread(target = treat_color_range_selector_gui).start()
    treat_footage()
    
    # After the loop release the cap object
    #vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()