import cv2 as cv
import numpy as np

from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtCore import Signal, Slot, Qt, QThread
from PySide6 import QtCore, QtGui

class VideoThread(QThread):
    pixmap_signal = Signal(np.ndarray)
    
    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv.VideoCapture(0)
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                self.pixmap_signal.emit(frame)
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Theia")
        self.showMaximized()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Video Input
        self.disp_w, self.disp_h = 640, 480
        self.frame = QLabel()
        self.frame.resize(self.disp_w, self.disp_h)

        # Scan Button
        self.button_widget = QWidget()
        self.button_widget_layout = QVBoxLayout(self.button_widget)
        self.button_widget_layout.setAlignment(QtCore.Qt.AlignHCenter)

        self.button = QPushButton("Scan")

        self.button_widget_layout.addWidget(self.button)

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.button_widget)

        self.thread = VideoThread()
        self.thread.pixmap_signal.connect(self.update_image)
        self.thread.start()

    def close(self, event):
        self.thread.stop()
        event.accept()

    @Slot(np.ndarray)
    def update_image(self, frame):
        qt_frame = self.convert_frame(frame)
        self.frame.setPixmap(qt_frame)

    def convert_frame(self, frame):
        rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        height, width, ch = rgb_image.shape
        bytes = width * ch
        qt_fmt = QtGui.QImage(rgb_image, width, height, bytes, QtGui.QImage.Format.Format_RGB888)
        scaled = qt_fmt.scaled(self.disp_w, self.disp_h, QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(scaled)