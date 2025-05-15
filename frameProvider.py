from PyQt5.QtCore import QThread, pyqtSignal
import cv2

class FrameProvider(QThread):
    frame_ready = pyqtSignal(object)

    def run(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                self.frame_ready.emit(frame)
