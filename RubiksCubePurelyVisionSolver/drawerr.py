import cv2
from colors import colors

dummy_cube_piece_size = 20
w = dummy_cube_piece_size
h = dummy_cube_piece_size
face_h = h*3
face_w = w*3

def draw_face(img, pieces, l):
    cv2.rectangle(img, (l[0], l[1]), (l[0]+face_h, l[1]+face_w), (0, 0, 0), 2)

    # draw first layer
    cv2.rectangle(img, (l[0], l[1]), (l[0]+w, l[1]+h), colors[pieces[0]]["representation"], -1)
    cv2.rectangle(img, (l[0], l[1]), (l[0]+w, l[1]+h), (0, 0, 0), 1)
    cv2.rectangle(img, (l[0]+w, l[1]), (l[0]+w*2, l[1]+h), colors[pieces[1]]["representation"], -1)
    cv2.rectangle(img, (l[0]+w, l[1]), (l[0]+w*2, l[1]+h), (0, 0, 0), 1)
    cv2.rectangle(img, (l[0]+w*2, l[1]), (l[0]+face_w, l[1]+h), colors[pieces[2]]["representation"], -1)
    cv2.rectangle(img, (l[0]+w*2, l[1]), (l[0]+face_w, l[1]+h), (0, 0, 0), 1)

    # draw second layer
    cv2.rectangle(img, (l[0], l[1]+h), (l[0]+w, l[1]+h*2), colors[pieces[3]]["representation"], -1)
    cv2.rectangle(img, (l[0], l[1]+h), (l[0]+w, l[1]+h*2), (0, 0, 0), 1)
    cv2.rectangle(img, (l[0]+w, l[1]+h), (l[0]+w*2, l[1]+h*2), colors[pieces[4]]["representation"], -1)
    cv2.rectangle(img, (l[0]+w, l[1]+h), (l[0]+w*2, l[1]+h*2), (0, 0, 0), 1)
    cv2.rectangle(img, (l[0]+w*2, l[1]+h), (l[0]+face_w, l[1]+h*2), colors[pieces[5]]["representation"], -1)
    cv2.rectangle(img, (l[0]+w*2, l[1]+h), (l[0]+face_w, l[1]+h*2), (0, 0, 0), 1)

    # draw third layer
    cv2.rectangle(img, (l[0], l[1]+h*2), (l[0]+w, l[1]+face_h), colors[pieces[6]]["representation"], -1)
    cv2.rectangle(img, (l[0], l[1]+h*2), (l[0]+w, l[1]+face_h), (0, 0, 0), 1)
    cv2.rectangle(img, (l[0]+w, l[1]+h*2), (l[0]+w*2, l[1]+face_h), colors[pieces[7]]["representation"], -1)
    cv2.rectangle(img, (l[0]+w, l[1]+h*2), (l[0]+w*2, l[1]+face_h), (0, 0, 0), 1)
    cv2.rectangle(img, (l[0]+w*2, l[1]+h*2), (l[0]+face_w, l[1]+face_h), colors[pieces[8]]["representation"], -1)
    cv2.rectangle(img, (l[0]+w*2, l[1]+h*2), (l[0]+face_w, l[1]+face_h), (0, 0, 0), 1)

    return img

air = 3
def draw_cube(img, left=None, front=None, right=None, back=None, up=None, down=None, location=None):
    img = draw_face(img, left, (location[0], location[1]+face_h+air))
    img = draw_face(img, front, (location[0]+face_w+air, location[1]+face_h+air))
    img = draw_face(img, right, (location[0]+face_w*2+air*2, location[1]+face_h+air))
    img = draw_face(img, back, (location[0]+face_w*3+air*3, location[1]+face_h+air))

    img = draw_face(img, up, (location[0]+face_w+air, location[1]))
    img = draw_face(img, down, (location[0]+face_w+air, location[1]+face_h*2+air*2))

    return img
# draw_cube(left=pieces, front=pieces, right=pieces, back=pieces, up=pieces, down=pieces, location=l)
# cv2.imshow('img',img)
# while True:
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
#
# cv2.destroyAllWindows()
