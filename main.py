import ctypes
ctypes.windll.user32.SetProcessDPIAware()  # Fix zoomed-in window capture

import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
wincap = WindowCapture('Home - File Explorer') #Snipping Tool

loop_time = time()
while True:
    # get an updated image of the window
    screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
