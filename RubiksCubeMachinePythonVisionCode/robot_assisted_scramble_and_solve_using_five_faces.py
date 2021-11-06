# 0orange 1red 2white 3yellow 4blue 5green
import cv2
import numpy as np
import keyboard
from serial_communicator import send_command

serial = None

cube = {
    "left": [0, 0, 0, 0, 0, 0, 0, 0, 0],
    "right": [1, 1, 1, 1, 1, 1, 1, 1, 1],
    "up": [2, 2, 2, 2, 2, 2, 2, 2, 2],
    "down": [3, 3, 3, 3, 3, 3, 3, 3, 3],
    "back": [4, 4, 4, 4, 4, 4, 4, 4, 4],
    "forth": [5, 5, 5, 5, 5, 5, 5, 5, 5]
}

def turn_face(cw_or_acw, face):
    global cube

    if cw_or_acw:
        cube[face] = [
            cube[face][6], 
            cube[face][3], 
            cube[face][0], 
            cube[face][7], 
            cube[face][4], 
            cube[face][1], 
            cube[face][8], 
            cube[face][5],
            cube[face][2]
        ]
    else:
        cube[face] = [
            cube[face][2], 
            cube[face][5], 
            cube[face][8], 
            cube[face][1], 
            cube[face][4], 
            cube[face][7], 
            cube[face][0], 
            cube[face][3], 
            cube[face][6]
        ]

def L(cw_or_acw):
    global cube

    # turn the face itself
    turn_face(cw_or_acw, "left")

    # turn surounding faces

    if cw_or_acw:
        temp_down = cube["down"].copy()
        
        cube["down"][0] = cube["forth"][0] 
        cube["down"][3] = cube["forth"][3]
        cube["down"][6] = cube["forth"][6]

        cube["forth"][0] = cube["up"][0]
        cube["forth"][3] = cube["up"][3]
        cube["forth"][6] = cube["up"][6]

        cube["up"][6] = cube["back"][2]
        cube["up"][3] = cube["back"][5]
        cube["up"][0] = cube["back"][8]

        cube["back"][8] = temp_down[0] 
        cube["back"][5] = temp_down[3]
        cube["back"][2] = temp_down[6]

    else:
        temp_back = cube["back"].copy()
        cube["back"][2] = cube["up"][6]
        cube["back"][5] = cube["up"][3]
        cube["back"][8] = cube["up"][0]
        
        cube["up"][0] = cube["forth"][0]
        cube["up"][3] = cube["forth"][3]
        cube["up"][6] = cube["forth"][6]
        
        cube["forth"][0] = cube["down"][0]
        cube["forth"][3] = cube["down"][3]
        cube["forth"][6] = cube["down"][6]
        
        cube["down"][0] = temp_back[8]
        cube["down"][3] = temp_back[5]
        cube["down"][6] = temp_back[2]
        

def R(cw_or_acw):
    global cube

    # turn the face itself
    turn_face(cw_or_acw, "right")

    # turn surounding faces

    if cw_or_acw:
        temp_down = cube["down"].copy()
        
        cube["down"][8] = cube["back"][0] 
        cube["down"][5] = cube["back"][3]
        cube["down"][2] = cube["back"][6]

        cube["back"][6] = cube["up"][2]
        cube["back"][3] = cube["up"][5]
        cube["back"][0] = cube["up"][8]

        cube["up"][2] = cube["forth"][2]
        cube["up"][5] = cube["forth"][5]
        cube["up"][8] = cube["forth"][8]

        cube["forth"][2] = temp_down[2] 
        cube["forth"][5] = temp_down[5]
        cube["forth"][8] = temp_down[8]

    else:
        temp_back = cube["back"].copy()
        cube["back"][6] = cube["down"][2]
        cube["back"][3] = cube["down"][5]
        cube["back"][0] = cube["down"][8]
        
        cube["down"][2] = cube["forth"][2]
        cube["down"][5] = cube["forth"][5]
        cube["down"][8] = cube["forth"][8]
        
        cube["forth"][2] = cube["up"][2]
        cube["forth"][5] = cube["up"][5]
        cube["forth"][8] = cube["up"][8]
        
        cube["up"][8] = temp_back[0]
        cube["up"][5] = temp_back[3]
        cube["up"][2] = temp_back[6]


def U(cw_or_acw):
    global cube

    # turn the face itself
    turn_face(cw_or_acw, "up")

    # turn surounding faces

    if cw_or_acw:
        temp_left = cube["left"].copy()
        
        cube["left"][0] = cube["forth"][0] 
        cube["left"][1] = cube["forth"][1]
        cube["left"][2] = cube["forth"][2]

        cube["forth"][0] = cube["right"][0]
        cube["forth"][1] = cube["right"][1]
        cube["forth"][2] = cube["right"][2]

        cube["right"][0] = cube["back"][0]
        cube["right"][1] = cube["back"][1]
        cube["right"][2] = cube["back"][2]

        cube["back"][0] = temp_left[0] 
        cube["back"][1] = temp_left[1]
        cube["back"][2] = temp_left[2]

    else:
        temp_left = cube["left"].copy()
        
        cube["left"][0] = cube["back"][0] 
        cube["left"][1] = cube["back"][1]
        cube["left"][2] = cube["back"][2]

        cube["back"][0] = cube["right"][0]
        cube["back"][1] = cube["right"][1]
        cube["back"][2] = cube["right"][2]

        cube["right"][0] = cube["forth"][0]
        cube["right"][1] = cube["forth"][1]
        cube["right"][2] = cube["forth"][2]

        cube["forth"][0] = temp_left[0] 
        cube["forth"][1] = temp_left[1]
        cube["forth"][2] = temp_left[2]


def D(cw_or_acw):
    global cube

    # turn the face itself
    turn_face(cw_or_acw, "down")

    # turn surounding faces

    if cw_or_acw:
        temp_left = cube["left"].copy()
        
        cube["left"][6] = cube["back"][6] 
        cube["left"][7] = cube["back"][7]
        cube["left"][8] = cube["back"][8]

        cube["back"][6] = cube["right"][6]
        cube["back"][7] = cube["right"][7]
        cube["back"][8] = cube["right"][8]

        cube["right"][6] = cube["forth"][6]
        cube["right"][7] = cube["forth"][7]
        cube["right"][8] = cube["forth"][8]

        cube["forth"][6] = temp_left[6] 
        cube["forth"][7] = temp_left[7]
        cube["forth"][8] = temp_left[8]

    else:
        temp_left = cube["left"].copy()
        
        cube["left"][6] = cube["forth"][6] 
        cube["left"][7] = cube["forth"][7]
        cube["left"][8] = cube["forth"][8]

        cube["forth"][6] = cube["right"][6]
        cube["forth"][7] = cube["right"][7]
        cube["forth"][8] = cube["right"][8]

        cube["right"][6] = cube["back"][6]
        cube["right"][7] = cube["back"][7]
        cube["right"][8] = cube["back"][8]

        cube["back"][6] = temp_left[6] 
        cube["back"][7] = temp_left[7]
        cube["back"][8] = temp_left[8]

def printo(cube):
    print(cube)
    print("")
    print([get_color_name(color) for color in cube["left"]])
    print([get_color_name(color) for color in cube["right"]])
    print([get_color_name(color) for color in cube["up"]])
    print([get_color_name(color) for color in cube["down"]])
    print([get_color_name(color) for color in cube["back"]])
    print([get_color_name(color) for color in cube["forth"]])

def B(cw_or_acw):
    global cube

    # turn the face itself
    turn_face(cw_or_acw, "back")

    # turn surounding faces

    if cw_or_acw:
        temp_left = cube["left"].copy()
        
        cube["left"][6] = cube["up"][0] 
        cube["left"][3] = cube["up"][1]
        cube["left"][0] = cube["up"][2]

        cube["up"][0] = cube["right"][2]
        cube["up"][1] = cube["right"][5]
        cube["up"][2] = cube["right"][8]

        cube["right"][2] = cube["down"][8]
        cube["right"][5] = cube["down"][7]
        cube["right"][8] = cube["down"][6]

        cube["down"][6] = temp_left[0] 
        cube["down"][7] = temp_left[3]
        cube["down"][8] = temp_left[6]

    else:
        temp_left = cube["left"].copy()
        
        cube["left"][0] = cube["down"][6] 
        cube["left"][3] = cube["down"][7]
        cube["left"][6] = cube["down"][8]

        cube["down"][6] = cube["right"][8]
        cube["down"][7] = cube["right"][5]
        cube["down"][8] = cube["right"][2]

        cube["right"][2] = cube["up"][0]
        cube["right"][5] = cube["up"][1]
        cube["right"][8] = cube["up"][2]

        cube["up"][0] = temp_left[6] 
        cube["up"][1] = temp_left[3]
        cube["up"][2] = temp_left[0]

def get_color(index):
    if index==0:
        return (0, 165, 255)
    if index==1:
        return (0, 0, 255)
    if index==2:
        return (255, 255, 255)
    if index==3:
        return (0, 255, 255)
    if index==4:
        return (255, 0, 0)
    if index==5:
        return (0, 255, 0)


lol =""
def get_color_name(index):
    if index==0:
        return "L"
    if index==1:
        return "R"
    if index==2:
        return "U"
    if index==3:
        return "D"
    if index==4:
        return "B"
    if index==5:
        return "F"

def solve():
    global serial
    global cube
    inputting = ""

    for piece in cube["up"]:
        inputting += get_color_name(piece)
    
    for piece in cube["right"]:
        inputting += get_color_name(piece)
    
    for piece in cube["forth"]:
        inputting += get_color_name(piece)
    
    for piece in cube["down"]:
        inputting += get_color_name(piece)
    
    for piece in cube["left"]:
        inputting += get_color_name(piece)
    
    for piece in cube["back"]:
        inputting += get_color_name(piece)

    #print(inputting)

    import kociemba
    print(inputting)
    solution = kociemba.solve(inputting)
    solution = solution.replace("F2", "RLD2U2R'L'B2RLD2U2R'L'")
    solution = solution.replace("F'", "RLU2D2R'L'B'RLU2D2R'L'")
    solution = solution.replace("F", "RLU2D2R'L'BRLU2D2R'L'")
    #print(solution)
    solution = solution.replace("R'", "r")
    solution = solution.replace("L'", "l")
    solution = solution.replace("U'", "u")
    solution = solution.replace("D'", "d")
    solution = solution.replace("B'", "b")
    
    solution = solution.replace("R2", "rr")
    solution = solution.replace("L2", "ll")
    solution = solution.replace("U2", "uu")
    solution = solution.replace("D2", "dd")
    solution = solution.replace("B2", "bb")
    solution = solution.replace(" ", "")

    print(len(solution))
    print(solution)

    sol = ""
    global lol
    for i in range(len(lol)-1, -1, -1):
        if lol[i]=="l":
            sol += "L"
        if lol[i]=="L":
            sol += "l"
        if lol[i]=="R":
            sol += "r"
        if lol[i]=="r":
            sol += "R"
        if lol[i]=="U":
            sol += "u"
        if lol[i]=="u":
            sol += "U"
        if lol[i]=="d":
            sol += "D"
        if lol[i]=="D":
            sol += "d"
        if lol[i]=="B":
            sol += "b"
        if lol[i]=="b":
            sol += "B"

    sol = sol.replace("uU", "")
    sol = sol.replace("Uu", "")
    sol = sol.replace("dD", "")
    sol = sol.replace("Dd", "")
    sol = sol.replace("Rr", "")
    sol = sol.replace("rR", "")
    sol = sol.replace("Ll", "")
    sol = sol.replace("lL", "")
    sol = sol.replace("Bb", "")
    sol = sol.replace("bB", "")
    sol = sol.replace("bbb", "b")
    sol = sol.replace("BBB", "B")
    sol = sol.replace("ddd", "d")
    sol = sol.replace("DDD", "D")
    sol = sol.replace("uuu", "u")
    sol = sol.replace("UUU", "U")
    sol = sol.replace("lll", "l")
    sol = sol.replace("LLL", "L")
    sol = sol.replace("rrr", "r")
    sol = sol.replace("RRR", "R")
    sol = "ULRrlu" + sol
    print(lol)
    print(sol)
    
    for move in sol:
        if move=="L":
            L(True)
        if move=="l":
            L(False)
        if move=="R":
            R(True)
        if move=="r":
            R(False)
        if move=="U":
            U(True)
        if move=="u":
            U(False)
        if move=="D":
            D(True)
        if move=="d":
            D(False)
        if move=="B":
            B(True)
        if move=="b":
            B(False)

    serial = send_command(serial, "MOVE " + sol)
    serial = send_command(serial, "MOTORS RESET")

Exit = False
moveer = None
def mover():
    global Exit
    global moveer
    global serial
    while not Exit:
        if keyboard.is_pressed('q') == True:
            Exit = True

        if moveer!=None:
            serial = send_command(serial, "MOVE " + moveer)
            moveer = None


serial = send_command(serial, "START")
serial = send_command(serial, "MOTORS RESET")
window = np.zeros(( 30*3*3, 30*4*3, 3), dtype=np.uint8)
e_pressed = False
d_pressed = False
r_pressed = False
f_pressed = False
s_pressed = False
t_pressed = False
g_pressed = False
y_pressed = False
h_pressed = False
u_pressed = False
j_pressed = False
i_pressed = False

from threading import Thread
#Thread(target=mover).start()
while not Exit:
    
    if keyboard.is_pressed('q') == True:
        Exit = True
    
    if keyboard.is_pressed('e') == True:
        if not e_pressed:
            moveer = "L"
            lol += "L"
            serial = send_command(serial, "MOVE L")
            L(True)
            printo(cube)
            
        e_pressed = True
    else:
        e_pressed = False

    if keyboard.is_pressed('d') == True:
        if not d_pressed:
            moveer = "l"
            lol += "l"
            serial = send_command(serial, "MOVE l")
            L(False)
            printo(cube)
            
        d_pressed = True
    else:
        d_pressed = False



    if keyboard.is_pressed('r') == True:
        if not r_pressed:
            moveer = "R"
            lol += "R"
            serial = send_command(serial, "MOVE R")
            R(True)
            printo(cube)
            
        r_pressed = True
    else:
        r_pressed = False

    if keyboard.is_pressed('f') == True:
        if not f_pressed:
            moveer = "r"
            lol += "r"
            serial = send_command(serial, "MOVE r")
            R(False)
            printo(cube)
            
        f_pressed = True
    else:
        f_pressed = False
        
    if keyboard.is_pressed('t') == True:
        if not t_pressed:
            moveer = "U"
            lol += "U"
            serial = send_command(serial, "MOVE U")
            U(True)
            printo(cube)

        t_pressed = True
    else:
        t_pressed = False

    if keyboard.is_pressed('g') == True:
        if not g_pressed:
            moveer = "u"
            lol += "u"
            serial = send_command(serial, "MOVE u")
            U(False)
            printo(cube)
            
        g_pressed = True
    else:
        g_pressed = False


        
    if keyboard.is_pressed('y') == True:
        if not y_pressed:
            moveer = "D"
            lol += "D"
            serial = send_command(serial, "MOVE D")
            D(True)
            printo(cube)
            
        y_pressed = True
    else:
        y_pressed = False

    if keyboard.is_pressed('h') == True:
        if not h_pressed:
            moveer = "d"
            lol += "d"
            serial = send_command(serial, "MOVE d")
            D(False)
            printo(cube)
            
        h_pressed = True
    else:
        h_pressed = False


        
    '''
    if keyboard.is_pressed('u') == True:
        if not u_pressed:
            moveer = "B"
            lol += "B"
            #serial = send_command(serial, "MOVE B")
            B(True)
            printo(cube)
            
        u_pressed = True
    else:
        u_pressed = False

    if keyboard.is_pressed('j') == True:
        if not j_pressed:
            moveer = "b"
            lol += "b"
            #serial = send_command(serial, "MOVE b")
            B(False)
            printo(cube)
            
        j_pressed = True
    else:
        j_pressed = False
    '''


    if keyboard.is_pressed('i') == True:
        if not i_pressed:
            #serial = send_command(serial, "MOVE " + lol)
            #B(False)
            printo(cube)
            
        i_pressed = True
    else:
        i_pressed = False

    if keyboard.is_pressed('s') == True:
        if not s_pressed:
            print(lol)
            solve()
            lol = ""
            s_pressed = True
    else:
        s_pressed = False


    x = 0
    y = 90
    window[y:y+30, x:x+30, :] = list(get_color(cube["down"][6]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["down"][7]))
    y += 30
    window[y:y+30, x:x+30, :]= list(get_color(cube["down"][8]))
    y = 90
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["down"][3]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["down"][4]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["down"][5]))
    y = 90
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["down"][0]))
    y += 30
    window[y:y+30, x:x+30, :]= list(get_color(cube["down"][1]))
    y += 30
    window[y:y+30, x:x+30, :]= list(get_color(cube["down"][2]))





    
    x += 30

    y = 0
    window[y:y+30, x:x+30, :] = list(get_color(cube["left"][8]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["left"][5]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["left"][2]))
    y = 0
    x += 30
    
    window[y:y+30, x:x+30, :]= list(get_color(cube["left"][7]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["left"][4]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["left"][1]))
    y = 0
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["left"][6]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["left"][3]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["left"][0]))




    x += 30 - 30 * 3
    y = 30*3
    window[y:y+30, x:x+30, :] = list(get_color(cube["forth"][6]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["forth"][7]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["forth"][8]))
    y = 30*3
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["forth"][3]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["forth"][4]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["forth"][5]))
    y = 30*3
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["forth"][0]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["forth"][1]))
    y += 30
    window[y:y+30, x:x+30, :]= list(get_color(cube["forth"][2]))

    

    x += 30 - 30 * 3
    y = 30*3 * 2
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][0]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][3]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][6]))
    y = 30*3 * 2
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][1]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][4]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][7]))
    y = 30*3 * 2
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][2]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][5]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["right"][8]))



    

    

    x += 30
    y = 30*3 * 1
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][6]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][7]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][8]))
    y = 30*3 * 1
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][3]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][4]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][5]))
    y = 30*3 * 1
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][0]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][1]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["up"][2]))



    

    

    x += 30
    y = 30*3 * 1
    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][2]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][1]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][0]))
    y = 30*3 * 1
    x += 30

    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][5]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][4]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][3]))
    y = 30*3 * 1
    x += 30
    
    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][8]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][7]))
    y += 30
    window[y:y+30, x:x+30, :] = list(get_color(cube["back"][6]))

    


    cv2.imshow("window", window)
    cv2.waitKey(1)