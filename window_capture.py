# window_capture.py
import threading
from windows_capture import WindowsCapture, Frame, InternalCaptureControl
import cv2
import global_vars
import io
import numpy as np # Import numpy

current_frame = None

def start_capture(window_name: str):
    capture = WindowsCapture(
        cursor_capture=False,
        draw_border=False,
        window_name=window_name
    )

    @capture.event
    def on_frame_arrived(frame: Frame, capture_control: InternalCaptureControl):
        global current_frame
        # Save as BMP for potentially faster disk I/O (less compression overhead)
        frame.save_as_image("scrn.bmp") # Changed from scrn.jpg to scrn.bmp
        img = cv2.imread("scrn.bmp")
        if img is not None:
            current_frame = img

    @capture.event
    def on_closed():
        print("Capture session closed")

    threading.Thread(target=capture.start, daemon=True).start()
    return capture
