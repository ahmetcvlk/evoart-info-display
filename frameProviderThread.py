from PyQt5.QtCore import QThread, pyqtSignal
import cv2


class FrameProviderThread(QThread):
    frame_ready = pyqtSignal(object)

    def __init__(self, camera_index):
        super().__init__()
        self.camera_index = camera_index
        self._running = True

    def run(self):
        self._running = True
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            return
        while self._running:
            ret, frame = cap.read()
            if ret:
                self.frame_ready.emit(frame.copy())
            else:
                break
        cap.release()
        del cap

    def stop(self):
        self._running = False
        self.wait()
