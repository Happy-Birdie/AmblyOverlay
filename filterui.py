#filterui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QApplication
from PyQt5.QtCore import QTimer
import sys
import global_vars
import pygetwindow as gw
import win32gui
import win32con
from overlay import CaptureWindow

class FilterUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Color Blindness Filter Menu")
        self.setGeometry(100, 100, 300, 200)

        self.layout = QVBoxLayout()

        self.combo_box = QComboBox()
        self.combo_box.currentTextChanged.connect(self.on_window_selected)

        self.layout.addWidget(self.combo_box)
        self.setLayout(self.layout)

        self.previous_windows = []
        self.get_window_list()

        #QTimer refreshes every 2 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.get_window_list)
        self.timer.start(2000)  #2000 milliseconds == 2 seconds

    def on_window_selected(self, text):
        print(f"Selected window: {text}")
        global_vars.selected_window = text

        if global_vars.overlay_window:
            global_vars.overlay_window.close()  #remove old one

        hwnd = win32gui.FindWindow(None, text)
        if hwnd:
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(100, lambda: self.spawn_overlay(text))  #delay launch slightly so less huge lag

    def spawn_overlay(self, title):
        global_vars.overlay_window = CaptureWindow(title)
        global_vars.overlay_window.show()

    def is_valid(self, title):
        return any(title.strip().lower() == b.lower() for b in global_vars.WINDOW_INVALID) 

    def get_window_list(self):
        current_windows = [title for title in gw.getAllTitles() if title.strip()]
        current_windows = [title for title in current_windows
                if title != self.windowTitle() and not self.is_valid(title)]
        if current_windows != self.previous_windows and self.windowTitle() not in current_windows:
            self.combo_box.blockSignals(True)
            current_text = self.combo_box.currentText()
            self.combo_box.clear()
            self.combo_box.addItems(current_windows)
            if current_text in current_windows:
                self.combo_box.setCurrentText(current_text)
            self.combo_box.blockSignals(False)
            self.previous_windows = current_windows



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilterUI()
    window.show()
    sys.exit(app.exec_())
