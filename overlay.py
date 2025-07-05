# ... (rest of your imports)
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import win32gui
import window_capture
import global_vars
import color_filter

class CaptureWindow(QWidget):
    def __init__(self, window_title):
        super().__init__()
        self.window_title = window_title
        global_vars.overlay_window = self  #track current overlay

        self.setWindowTitle(f"Capturing: {window_title}")
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool |
            Qt.WindowTransparentForInput
        )

        self.label = QLabel(self)
        self.label.setScaledContents(True)

        self.capture = window_capture.start_capture(window_title)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(16)  # Changed from 33 to 16 for ~60 FPS

        self.tracker = QTimer(self)
        self.tracker.timeout.connect(self.sync_with_target)
        self.tracker.start(500) # Changed from 33 to 500 (0.5 seconds), less frequent sync is fine

    def sync_with_target(self):
        hwnd = win32gui.FindWindow(None, self.window_title)
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            x, y, x2, y2 = rect
            width, height = x2 - x, y2 - y
            self.setGeometry(x, y, width, height)
            self.label.setGeometry(0, 0, width, height)
        else:
            print(f"[INFO] {self.window_title} not found. Closing overlay.")
            self.close()

    def update_display(self):
        frame = window_capture.current_frame
        if frame is None:
            return

        frame = color_filter.apply_filter(frame)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        try:
            if self.capture: #ensure capture object exists before stopping
                self.capture.stop()
        except Exception as e:
            print(f"Error stopping capture: {e}")
        super().closeEvent(event)
