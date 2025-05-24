import sys
import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt
import window_capture

class CaptureWindow(QWidget):
    def __init__(self, window_title):
        super().__init__()
        self.setWindowTitle(f"Capturing: {window_title}")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool | Qt.WindowTransparentForInput)
        #self.showFullScreen()
        
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignTop | Qt.AlignLeft)  #align to top-left
        self.label.setScaledContents(False)  #prevents automatic scaling so that its the same size as the window

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  #mo margins (meaning white stuff around it)
        layout.setSpacing(0)
        layout.addWidget(self.label)

        self.capture = r5.start_capture(window_title)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_display)
        self.timer.start(33)

    def update_display(self):
        frame = r5.current_frame
        if frame is None:
            return
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.label.setPixmap(pixmap)
        self.label.resize(pixmap.size())  #resize QLabel to image
        self.resize(pixmap.size())        #resize main window to match

    def closeEvent(self, event):
        try:
            self.capture.stop()
        except Exception:
            pass
        super().closeEvent(event)

    '''
    def move_to_target_window(self, title):
        hwnd = win32gui.FindWindow(None, title)
        if hwnd:
            rect = win32gui.GetWindowRect(hwnd)
            x, y, x2, y2 = rect
            self.move(x, y)
            self.resize(x2 - x, y2 - y)
        else:
            print(f"Could not find window: {title}")
    '''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    title = "Microsoft Store"  #change as needed
    win = CaptureWindow(title)
    win.show()
    sys.exit(app.exec_())
