
def F_turn(scramble, face):

    R_temp = [scramble["R"][0], scramble["R"][3], scramble["R"][6]]
    U_temp = [scramble["U"][6], scramble["U"][7], scramble["U"][8]]
    L_temp = [scramble["L"][2], scramble["L"][5], scramble["L"][8]]
    D_temp = [scramble["D"][0], scramble["D"][1], scramble["D"][2]]

    scramble["F"] = [
        scramble["F"][6], scramble["F"][3], scramble["F"][0],
        scramble["F"][7], scramble["F"][4], scramble["F"][1],
        scramble["F"][8], scramble["F"][5], scramble["F"][2]
    ]

    scramble["R"][0] = U_temp[0]
    scramble["R"][3] = U_temp[1]
    scramble["R"][6] = U_temp[2]

    scramble["U"][6] = L_temp[0]
    scramble["U"][7] = L_temp[1]
    scramble["U"][8] = L_temp[2]

    scramble["L"][2] = D_temp[0]
    scramble["L"][5] = D_temp[1]
    scramble["L"][8] = D_temp[2]

    scramble["R"][0] = R_temp[0]
    scramble["R"][3] = R_temp[1]
    scramble["R"][6] = R_temp[2]

    return scramble

scramble = {
            "F": ["green", "green", "green", "green", "green", "green", "green", "green", "green"],
            "R": ["red", "red", "red", "red", "red", "red", "red", "red", "red"],
            "L": ["orange", "orange", "orange", "orange", "orange", "orange", "orange", "orange", "orange"],
            "U": ["white", "white", "white", "white", "white", "white", "white", "white", "white"],
            "D": ["yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow", "yellow"],
            "B": ["blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue"]
        }

# always solving front side green, top side white for now

print(F_turn(scramble))
