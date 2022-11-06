import cv2 as cv
import numpy as np

from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QFrame
from PySide6.QtCore import Signal, Slot, QThread 
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
        self.img = None
        super().__init__()
        self.setWindowTitle("Theia")
        self.showMaximized()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Video Input Widget
        self.disp_w, self.disp_h = 640, 480
        self.frame = QLabel()
        self.frame.resize(self.disp_w, self.disp_h)

        # Scan Button
        self.button = QPushButton("Scan")
        self.button.setStyleSheet("QPushButton{font-size: 18pt;}")
        self.button.clicked.connect(self.scan_image)

        self.button_widget = QWidget()
        self.button_widget_layout = QVBoxLayout(self.button_widget)
        self.button_widget_layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.button_widget_layout.addWidget(self.button)

        # Output Widget
        self.output_label = QLabel()
        self.output_label.setStyleSheet("QLabel{font-size: 18pt;}")
        self.output_label.setText("OUTPUT TEXT")

        self.output_label_widget = QWidget()
        self.output_label_widget_layout = QVBoxLayout(self.output_label_widget)
        self.output_label_widget_layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.output_label_widget_layout.addWidget(self.output_label)

        # Adding all the widgets to the layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.layout.addWidget(self.frame)
        self.layout.addWidget(self.button_widget)
        self.layout.addWidget(self.output_label_widget)

        # video feed thread
        self.thread = VideoThread()
        self.thread.pixmap_signal.connect(self.update_image)
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    @Slot(np.ndarray)
    def update_image(self, frame):
        self.img = frame
        qt_frame = self.convert_frame(frame)
        self.frame.setPixmap(qt_frame)

    def convert_frame(self, frame):
        rgb_image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        height, width, ch = rgb_image.shape
        bytes = width * ch
        qt_fmt = QtGui.QImage(rgb_image, width, height, bytes, QtGui.QImage.Format.Format_RGB888)
        scaled = qt_fmt.scaled(self.disp_w, self.disp_h, QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(scaled)

    def scan_image(self):
        cv.imwrite("output/currency.jpeg", self.img)

        '''
        original, usd = visionAPI.get_output()
        self.output_label.setText(f'{original} = {usd}')
        '''