# import the opencv library
import cv2
import pickle
import numpy as np
import time
import webcolors
from sklearn.cluster import KMeans
from collections import Counter
from threading import Thread
from serial_communicator import send_command
from color_tools import *
from important_constants import *
from general_tools import draw_text
import keyboard


drawing = False # true if mouse is pressed
sets_of_points = []
flying_point = None

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

contours = [[], [], []]

reordering = False
ready_contours = []
new_contours_order = []
step = 0
frame2 = None
frame = None
how_many_captures_should_we_take_to_average = 1

serial = None

cube = {
    "F": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "B": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "L": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "R": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "U": [-1, -1, -1, -1, -1, -1, -1, -1, -1],
    "D": [-1, -1, -1, -1, -1, -1, -1, -1, -1]
}


Exit = False
selected_scheme = None
previous_x = None
selected_min_or_max = None
selected_color_index = -1
selected_range_index = -1
a_bar_is_held = False
colors = []


colors_filename = "colors.pickle"

try:
    with open(colors_filename, "rb") as f:
        colors = pickle.load(f)
except:
    from colors import colors as temp
    colors = temp
scheme_maxes = [180, 255, 255]
hsvs = []

def treat_color_range_selector_gui():
    global contours, hsvs, Exit
    while not Exit:
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
        cv2.waitKey(1)
        if keyboard.is_pressed('q') == True:
            Exit = True

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

# mouse callback function
def line_drawing(event, x, y, flags, param):
    global drawing, flying_point, sets_of_points, hsvs, reordering, new_contours_order, called

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
                called = False
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

        hsv = convert_rgb_to_hsv(rgb)
        if contour["enabled"]: # only show colors of enabled contours inside the colors gui
            hsvs.append(hsv)

        # Dominant colors display, ranked left to right
            h_occurencies = 0
            s_occurencies = 0
            v_occurencies = 0
        for data in colors:
            index = -1
            h_occurencies = 0
            s_occurencies = 0
            v_occurencies = 0
            for each_range in data["ranges"]:
                index += 1
                if hsv[0] >= each_range["min"][0] and hsv[0] <= each_range["max"][0]:
                    h_occurencies += 1
                if hsv[1] >= each_range["min"][1] and hsv[1] <= each_range["max"][1]:
                    s_occurencies += 1
                if hsv[2] >= each_range["min"][2] and hsv[2] <= each_range["max"][2]:
                    v_occurencies += 1

            if h_occurencies>0 or s_occurencies>0 or v_occurencies>0:
                maxer = max([h_occurencies*5, s_occurencies*1, v_occurencies*1])
                if data["name"] == "yellow":
                    color_occurencies[0] += maxer
                elif data["name"] == "blue":
                    color_occurencies[1] += maxer
                elif data["name"] == "green":
                    color_occurencies[2] += maxer
                elif data["name"] == "orange":
                    color_occurencies[3] += maxer
                elif data["name"] == "red":
                    color_occurencies[4] += maxer
                elif data["name"] == "white":
                    color_occurencies[5] += maxer
                
        #colorsss = cv2.rectangle(colorsss, (i*50, 0), ((i+1)*50, 200), tuple(cds[i]), -1)

    # write the name of the most occurent color in this contour
    most_occurences = max(color_occurencies)
    if most_occurences>0: # if one of the colors showed up at least
        most_occurent_color = color_occurencies.index(most_occurences)

        # add this occurency to the array now
        if len(color_occurencies_in_contours) > i:
            color_occurencies_in_contours[i][most_occurent_color] += 1


    ready_contours.append(i)

def treat_predictions(previous_predictions, contours_to_treat, desired_contours_count=27):
    global step, cube, serial

    debugging = False
    if debugging:
        step = 9000
        desired_contours_count = 27

    #print("len", len(previous_predictions), desired_contours_count)
    #print("len(previous_predictions", len(previous_predictions), "desired_contours_count", desired_contours_count)
    #print("predictions", [coloz[i] for i in previous_predictions])
    contours_count = 0
    for piece in contours_to_treat:
        if len(previous_predictions) > piece:
            if previous_predictions[piece]!=-1:
                contours_count += 1

    full_reading = desired_contours_count == contours_count

    if step<0:
        return []

    if step==0: # this is to pass the first ever command before agknowledging the face
        step = 1
        print("contours_to_treat", contours_to_treat)
        print("previous_predictions", previous_predictions)
        #serial = send_command(serial, "MOTORS RESET")
        contours_to_treat = [i for i in range(0, 27)]
        return contours_to_treat
    elif step==1:
        if full_reading:
            print("contours_to_treat", contours_to_treat)
            print("previous_predictions", previous_predictions)
            step += 1
            print("predictions", [coloz[i] for i in previous_predictions])
            '''
            for i in range(0, 9):
                cube["U"][i] = previous_predictions[i]
            for i in range(9, 18):
                cube["B"][i-9] = previous_predictions[i]
            for i in range(18, 27):
                cube["L"][i-18] = previous_predictions[i]
            '''
            #serial = send_command(serial, "MOVE L")
            #serial = send_command(serial, "MOTORS RESET")
            contours_to_treat = [11, 14, 17]
            return contours_to_treat
    elif step==2:
        if full_reading:
            print("contours_to_treat", contours_to_treat)
            print("previous_predictions", previous_predictions)
            '''
            for i in range(0, 9):
                cube["U"][i] = previous_predictions[i]
            for i in range(9, 18):
                cube["B"][i-9] = previous_predictions[i]
            for i in range(18, 27):
                cube["L"][i-18] = previous_predictions[i]
            '''
            #serial = send_command(serial, "MOVE lb")
            #serial = send_command(serial, "MOTORS RESET")
            step += 1
            contours_to_treat = [18, 21, 24]
            return contours_to_treat
    elif step==3:
        if full_reading:
            print("contours_to_treat", contours_to_treat)
            print("previous_predictions", previous_predictions)
            '''
            for i in range(0, 9):
                cube["U"][i] = previous_predictions[i]
            for i in range(9, 18):
                cube["B"][i-9] = previous_predictions[i]
            for i in range(18, 27):
                cube["L"][i-18] = previous_predictions[i]
            '''
            #serial = send_command(serial, "MOVE B")
            #serial = send_command(serial, "MOTORS RESET")
            step += 1
            return contours_to_treat

    contours_to_treat = [i for i in range(0, desired_contours_count)]
    return contours_to_treat

called = False
def treat_footage():
    global hsvs, ready_contours, frame, Exit, called

    treat_color_range_selector_gui_thread = Thread(target = treat_color_range_selector_gui)
    #treat_color_range_selector_gui_thread.setDaemon(True)
    treat_color_range_selector_gui_thread.start()

    debug_motor_testors_thread = Thread(target = debug_motor_testors)
    debug_motor_testors_thread

    vid = cv2.VideoCapture(2)
    recordings = 0
    texts_to_draw = []
    start_time2 = time.time()
    start_time = time.time()
    ready_contours = []
    finished_a_reading = False
    contours_to_treat = []
    desired_contours_count = len(contours_to_treat)
    yes = False # debugging variable
    while not Exit:
        predictions = [-1 for i in range(0, len(sets_of_points))]
        # Capture the video frame
        ret, frame = vid.read()

        if time.time() - start_time2 > start_delay:

            # if color occurencies array wasn't updated yet then update it
            if len(color_occurencies_in_contours) < len(sets_of_points):
                reinit_color_occurencies()

            if not called:
                ready_contours = []
                called = True
                for i in range(0, len(sets_of_points)):
                    
                    # ignore any currently being made contour
                    if i == len(sets_of_points) - 1:
                        if drawing:
                            continue # skip it because it's not a complete contour

                    if i in contours_to_treat:
                        Thread(target = treat_contour, args=[sets_of_points[i], i]).start()
                        #treat_contour(sets_of_points[i], i)
                    else:
                        ready_contours.append(i)

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
                    if not i in contours_to_treat:
                        continue

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
                            "text": str(i) + " " + most_occurent_color_text,
                            "pos": (x+w/2, y+h/2)
                        })
                        predictions[i] = most_occurent_color_index
                    else:
                        predictions[i] = -1

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

        # if we pressed Exit stop
        cv2.waitKey(1)
        if keyboard.is_pressed('q') == True:
            Exit = True
            
        # do whatever we want with our predictions stored inside
        if finished_a_reading:
            finished_a_reading = False
            #contours_to_treat = treat_predictions(predictions, contours_to_treat, desired_contours_count=desired_contours_count)

            printer = ""
            for i in predictions:
                if i!=-1:
                    printer += coloz[i] + " "
            print("predictions", printer)
            #print("predictions", [coloz[i] for i in predictions])
            
            contours_to_treat = [11, 14, 17]
            contours_to_treat = [18, 21, 24]

            contours_to_treat = [i for i in range(0, 27)]
            desired_contours_count = len(contours_to_treat)

def debug_motor_testors():
    # debugging purely
    global serial, Exit
    
    while not Exit:
        if keyboard.is_pressed('l') == True:
            serial = send_command(serial, "MOVE r")
            serial = send_command(serial, "MOTORS RESET")
        if keyboard.is_pressed('r') == True:
            serial = send_command(serial, "MOVE R")
            serial = send_command(serial, "MOTORS RESET")
        if keyboard.is_pressed('q') == True:
            Exit = True
    '''
    time.sleep(1)
    '''

def treat_footage2():
    global frame2, Exit
    vid2 = cv2.VideoCapture(0)
    while not Exit:
        ret, frame2 = vid2.read()

        cv2.imshow('frame2', frame2)

        # if we pressed exit stop
        cv2.waitKey(1)
        if keyboard.is_pressed('q') == True:
            Exit = True


def main():
    global serial
    serial = send_command(serial, "START")


    treat_footage()
    #treat_footage_thread = Thread(target = treat_footage)
    #treat_footage_thread.start()

    #treat_footage2_thread = Thread(target = treat_footage2)
    #treat_footage2_thread.start()

if __name__ == '__main__':
    main()