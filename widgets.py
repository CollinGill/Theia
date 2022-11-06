import cv2 as cv
import numpy as np
import math
import pyaudio
import collections
import audioop
import time
import wave
import os
import subprocess

from PySide6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QGraphicsDropShadowEffect
from PySide6.QtCore import Signal, Slot, QThread 
from PySide6 import QtCore, QtGui

import visionAPI
import translationAPI
import transcriptionAPI

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
        self.disp_w, self.disp_h = 1.5 * 640, 1.5 * 480
        self.frame = QLabel()
        self.frame.resize(self.disp_w, self.disp_h)
        self.frame.setStyleSheet("border: 10px solid black; border-radius: 10%;")

        # Output Widget
        self.output_label = QLabel()
        self.output_label.setWordWrap(True)
        self.output_label.setStyleSheet("QLabel{font-size: 24pt;}")
        self.output_label.setText("")

        self.output_label_widget = QWidget()
        self.output_label_widget_layout = QVBoxLayout(self.output_label_widget)
        self.output_label_widget_layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.output_label_widget_layout.addWidget(self.output_label)

        # Top Widget
        self.top = QWidget()
        self.top_layout = QHBoxLayout(self.top)
        self.top_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.top_layout.addWidget(self.frame)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.output_label)
        self.top_layout.addStretch()

        # Buttons
        self.button_stylesheet = "QPushButton{font-size: 24pt; border: 5px outset black; border-radius: 10%; padding: 5px;}"
        self.buttons = []

        self.quit_button = QPushButton("Quit")
        self.quit_button.setStyleSheet(self.button_stylesheet)
        self.quit_button.clicked.connect(self.abort)
        self.buttons.append(self.quit_button)

        self.scan_button = QPushButton("Currency Conversion")
        self.scan_button.setStyleSheet(self.button_stylesheet)
        self.scan_button.clicked.connect(self.get_exchange)
        self.buttons.append(self.scan_button)

        self.text_button = QPushButton("Text Translation")
        self.text_button.setStyleSheet(self.button_stylesheet)
        self.text_button.clicked.connect(self.get_translation)
        self.buttons.append(self.text_button)

        self.speech_button = QPushButton("Speech Transcription")
        self.speech_button.setStyleSheet(self.button_stylesheet)
        self.speech_button.clicked.connect(self.get_transcription)
        self.buttons.append(self.speech_button)

        self.button_widget = QWidget()
        self.button_widget_layout = QHBoxLayout(self.button_widget)
        self.button_widget_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.button_widget_layout.setSpacing(10)

        for button in self.buttons:
            self.button_widget_layout.addWidget(button)

        # Bottom Widget
        self.bottom = QWidget()
        self.bottom_layout = QHBoxLayout(self.bottom)
        self.bottom_layout.setAlignment(QtCore.Qt.AlignLeft)
        self.bottom_layout.addWidget(self.button_widget)

        # Adding all the widgets to the layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.top)
        self.layout.addWidget(self.bottom)

        # video feed thread
        self.thread = VideoThread()
        self.thread.pixmap_signal.connect(self.update_image)
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()

    def abort(self):
        self.thread.stop()
        exit()

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

    def get_exchange(self):
        cv.imwrite("output/currency.jpg", self.img)

        original, usd = visionAPI.get_output()

        output_txt = ""
        if usd == 'ERROR':
            output_txt = "Sorry, can't read text"

        else:
            output_txt = f'{original} = {usd}'

        self.output_label.setText(output_txt)

    def get_translation(self):
        cv.imwrite("output/translation.jpg", self.img)

        _, text = translationAPI.get_output()

        self.output_label.setText(text)

    def get_transcription(self):
        filename = "output/output.wav"
        chunk = 1024
        format = pyaudio.paInt16
        channels = 1
        rate = 44100
        seconds = 5

        p = pyaudio.PyAudio()

        print('RECORDING')

        stream = p.open(format=format, 
                        channels=channels, 
                        rate=rate, 
                        input=True, 
                        # output=True, 
                        frames_per_buffer=chunk)

        frames = []



        for i in range(0, int(rate / chunk * seconds)):
        # while 
            data = stream.read(chunk)
            frames.append(data)


        stream.stop_stream()
        stream.close()
        p.terminate()

        print('finished recording')

        wf = wave.open(filename, "wb")
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        os.system(f"flac {filename} -o {filename[:-4] + '.flac'} && rm {filename}")