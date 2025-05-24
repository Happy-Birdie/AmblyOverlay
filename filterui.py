#filterui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QComboBox, QApplication
from PyQt5.QtCore import QTimer
import sys
import global_var
import pygetwindow as gw
import win32gui
import win32con

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
        r8.selected_window = text

    def get_window_list(self):
        current_windows = [title for title in gw.getAllTitles() if title.strip()]
        current_windows = [title for title in current_windows
                       if title != self.windowTitle() and self. is_maximizable(title)]
        if current_windows != self.previous_windows and self.windowTitle() not in current_windows:
            self.combo_box.blockSignals(True)
            current_text = self.combo_box.currentText()
            self.combo_box.clear()
            self.combo_box.addItems(current_windows)
            if current_text in current_windows:
                self.combo_box.setCurrentText(current_text)
            self.combo_box.blockSignals(False)
            self.previous_windows = current_windows

    def is_maximizable(self, title):
        try:
            hwnds = gw.getWindowsWithTitle(title)
            if not hwnds:
                return False
            hwnd = hwnds[0]._hWnd
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
            has_maximize = bool(style & win32con.WS_MAXIMIZEBOX)
            is_visible = win32gui.IsWindowVisible(hwnd)
            return has_maximize and is_visible
        except Exception:
            return False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FilterUI()
    window.show()
    sys.exit(app.exec_())
