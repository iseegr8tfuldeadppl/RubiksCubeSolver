import kociemba

def correct_face(face, clockwise=True):
    # this will rotate a face clockwise without affecting the other faces
    if clockwise:
        new_face = [face[6], face[3], face[0], face[7], face[4], face[1], face[8], face[5], face[2]]
    else:
        new_face = [face[2], face[5], face[8], face[1], face[4], face[7], face[0], face[3], face[6]]
    return new_face

def get_sol(pieces):
    print("pieces", pieces)
    back = "blue"
    front = "green"
    left = "orange"
    right = "red"
    up = "white"
    down = "yellow"
    print("pieces", pieces)
    faces = [up, right, front, down, left, back]

    result = ""
    for side in faces:
        for face in pieces:
            if face[4]==side:

                # replace pieces of this face with their notation
                for i in range(0, len(face)):
                    if face[i] == back:
                        face[i] = "B"
                    elif face[i] == front:
                        face[i] = "F"
                    elif face[i] == left:
                        face[i] = "L"
                    elif face[i] == right:
                        face[i] = "R"
                    elif face[i] == up:
                        face[i] = "U"
                    elif face[i] == down:
                        face[i] = "D"

                # append them all into the result
                # put all these elements into a string
                result += ''.join(face)

    solution = kociemba.solve(result)
    return solution

def test():
    pieces = [['red', 'red', 'white', 'white', 'green', 'blue', 'white', 'green', 'yellow'], ['blue', 'red', 'yellow', 'orange', 'red', 'red', 'orange', 'blue', 'yellow'], ['blue', 'green', 'red', 'white', 'blue', 'red', 'green', 'blue', 'yellow'], ['blue', 'green', 'green', 'blue', 'orange', 'orange', 'blue', 'orange', 'orange'], ['red', 'yellow', 'orange', 'orange', 'white', 'green', 'white', 'yellow', 'white'], ['orange', 'yellow', 'green', 'white', 'yellow', 'white', 'red', 'yellow', 'green']]
    pieces[4] = correct_face(pieces[4], clockwise=True).copy() #fix U
    pieces[5] = correct_face(pieces[5], clockwise=False).copy() #fix D

    print(get_sol(pieces))
