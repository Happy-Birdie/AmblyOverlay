import threading
from windows_capture import WindowsCapture, Frame, InternalCaptureControl
import cv2

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
        frame.save_as_image("scrn.jpg") #save as img if you want
        img = cv2.imread("scrn.jpg")
        if img is not None:
            current_frame = img

    @capture.event
    def on_closed():
        print("Capture session closed")

    threading.Thread(target=capture.start, daemon=True).start()
    return capture
