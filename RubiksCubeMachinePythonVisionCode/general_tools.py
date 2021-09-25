import cv2

def draw_text(img, text, font=cv2.FONT_HERSHEY_PLAIN, pos=(0, 0), font_scale=3, font_thickness=2, text_color=(255, 255, 255), text_color_bg=(0, 0, 0)):
    x, y = pos
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_w, text_h = text_size
    cv2.rectangle(img, (int(x-text_w/2), int(y-text_h/2)), (int(x + text_w/2), int(y + text_h/2)), text_color_bg, -1)
    cv2.putText(img, text, (int(x-text_w/2), int(y + text_h/2 + font_scale - 1)), font, font_scale, text_color, font_thickness)

    return text_size
