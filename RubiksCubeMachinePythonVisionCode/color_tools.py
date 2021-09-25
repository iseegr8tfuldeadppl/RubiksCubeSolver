
import colorsys


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
