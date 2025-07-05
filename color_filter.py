import cv2
import numpy as np
from global_vars import CUSTOM_RED, CUSTOM_CYAN

def apply_filter(image): #image = frame (BGR format)
    blue, green, red = cv2.split(image)

    #cyan channel = combine green and blue channels
    #can average or add them, here averages and clip to max 255
    cyan = cv2.addWeighted(green, 0.5, blue, 0.5, 0)

    #merge red channel with cyan (green+blue) channels
    #output is (blue_out, green_out, red_out)
    #blue_out = cyan, green_out = cyan, red_out = red
    red_cyan_image = cv2.merge((cyan, cyan, red)) #BGR format

    #no need for float conversion and back if the desired output is just this merged image --> cheaper & faster
    return red_cyan_image # Direct return of uint8 BGR image
